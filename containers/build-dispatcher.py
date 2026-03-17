#!/usr/bin/env python3
"""
build-dispatcher.py

Reads the dependency JSON produced by docker-build-order_ad.py and dispatches
container builds to GitHub Actions build slots in topological (dependency) order.

Architecture:
  - One worker thread per build slot (up to 8).
  - A shared Queue feeds WorkItems (image + attempt number) to idle workers.
  - When a build succeeds its dependents are unlocked into the queue.
  - When a build exhausts all retries the image is failed and every downstream
    dependent is cascade-skipped so nothing waits forever.

Features:
  - 3 build attempts per image (1 initial + 2 retries).
  - Cascade failure: failed image → all dependents recursively skipped.
  - --skip / filter list: images excluded before the run starts.
  - Failed/skipped report written to --out-failed at the end.
"""

import json
import argparse
import os
import sys
import time
import threading
import queue
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

import requests


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GITHUB_API = "https://api.github.com"
MAX_ATTEMPTS = 3  # total attempts per image (1 initial + 2 retries)
POLL_INTERVAL = 60  # seconds between workflow-status polls
DISPATCH_SETTLE = 8  # seconds to wait after dispatch before searching for run ID
RUN_SEARCH_TRIES = 15  # how many 5-second polls to find the dispatched run ID


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------


@dataclass
class WorkItem:
    """A single unit of work: an image name and how many times we've tried."""

    image: str
    attempt: int = 1


# ---------------------------------------------------------------------------
# GitHub Actions build slot
# ---------------------------------------------------------------------------


class GitHubBuildSlot:
    """
    Represents one GitHub Actions build-slot workflow.

    Responsible for:
      1. Triggering a workflow_dispatch event.
      2. Locating the resulting run ID (GitHub does NOT return it on dispatch).
      3. Polling until the run reaches a terminal state.
    """

    def __init__(
        self,
        slot_number: int,
        token: str,
        owner: str,
        repo: str,
        ref: str,
    ) -> None:
        self.slot_number = slot_number
        self.owner = owner
        self.repo = repo
        self.ref = ref
        self.workflow_file = f"container-build-slot-{slot_number}.yml"
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def build(self, container_name: str) -> bool:
        """Dispatch the workflow and wait for it to finish. Returns True on success."""
        run_id = self._dispatch(container_name)
        if run_id is None:
            return False
        self._log(f"Waiting for run {run_id}  ({container_name}) …")
        return self._wait_for_run(run_id)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _log(self, msg: str) -> None:
        print(f"[slot-{self.slot_number}] {msg}", flush=True)

    def _dispatch(self, container_name: str) -> Optional[str]:
        """Trigger workflow_dispatch and return the run ID, or None on error."""
        triggered_at = datetime.now(timezone.utc).timestamp()
        url = f"{GITHUB_API}/repos/{self.owner}/{self.repo}" f"/actions/workflows/{self.workflow_file}/dispatches"
        payload = {
            "ref": self.ref,
            "inputs": {
                "container_name": container_name,
                "ref": self.ref,
            },
        }
        resp = requests.post(url, json=payload, headers=self._headers)
        if resp.status_code != 204:
            self._log(f"Dispatch failed for '{container_name}': " f"HTTP {resp.status_code} — {resp.text}")
            return None

        self._log(f"Dispatched '{container_name}', waiting for run ID …")

        # GitHub doesn't return the run ID; give the API a moment to register it.
        time.sleep(DISPATCH_SETTLE)
        return self._find_run_id(triggered_at)

    def _find_run_id(self, triggered_after: float) -> Optional[str]:
        """
        Poll the workflow's run list until we find a run created at or after
        triggered_after (UTC epoch seconds).  Returns the run ID as a string,
        or None if not found within the retry window.
        """
        url = f"{GITHUB_API}/repos/{self.owner}/{self.repo}/actions/workflows/{self.workflow_file}/runs"
        for _ in range(RUN_SEARCH_TRIES):
            resp = requests.get(url, headers=self._headers, params={"per_page": 5})
            if resp.status_code == 200:
                for run in resp.json().get("workflow_runs", []):
                    # GitHub returns ISO-8601 UTC, e.g. "2026-03-16T12:00:00Z"
                    created_ts = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00")).timestamp()
                    if created_ts >= triggered_after:
                        return str(run["id"])
            time.sleep(5)

        self._log("Could not locate the dispatched run ID after polling — treating as failure.")
        return None

    def _wait_for_run(self, run_id: str) -> bool:
        """Poll until the run is in a terminal state. Returns True only on 'success'."""
        url = f"{GITHUB_API}/repos/{self.owner}/{self.repo}/actions/runs/{run_id}"
        while True:
            resp = requests.get(url, headers=self._headers)
            if resp.status_code != 200:
                self._log(f"Failed to poll run {run_id}: HTTP {resp.status_code}")
                return False
            data = resp.json()
            status = data.get("status", "")
            if status == "completed":
                conclusion = data.get("conclusion", "")
                return conclusion == "success"
            time.sleep(POLL_INTERVAL)


# ---------------------------------------------------------------------------
# Build graph  (thread-safe)
# ---------------------------------------------------------------------------


class BuildGraph:
    """
    Thread-safe directed acyclic graph of build dependencies.

    After construction, call `initial_ready()` to seed the work queue.
    Use `on_success()` / `on_failure()` from worker threads as builds finish.
    """

    def __init__(self, deps: Dict[str, List[str]], skip: Set[str]) -> None:
        self._lock = threading.Lock()

        all_images = set(deps.keys())

        # Normalise the skip set: accept both "org/name" and bare "name".
        self.skipped: Set[str] = {img for img in all_images if img in skip}

        # Active = everything we actually intend to build.
        active = all_images - self.skipped

        # dependents[a] = images that have 'a' as a direct dependency
        #                 i.e. images that can only start AFTER 'a' is done.
        self._dependents: Dict[str, Set[str]] = defaultdict(set)

        # indegree[img] = number of unsatisfied local dependencies.
        self._indegree: Dict[str, int] = {}

        for img in active:
            local_deps = [d for d in deps.get(img, []) if d in active]
            self._indegree[img] = len(local_deps)
            for dep in local_deps:
                self._dependents[dep].add(img)

        self.completed: Set[str] = set()
        self.failed: Set[str] = set()

    # ------------------------------------------------------------------
    # Queue seeding
    # ------------------------------------------------------------------

    def initial_ready(self) -> List[str]:
        """Images with no local dependencies — the first wave to build."""
        with self._lock:
            return [img for img, deg in self._indegree.items() if deg == 0]

    # ------------------------------------------------------------------
    # Build outcome handlers
    # ------------------------------------------------------------------

    def on_success(self, img: str) -> List[str]:
        """
        Record a successful build.
        Returns the list of images whose dependency count just hit zero
        (i.e. they are now ready to be enqueued).
        """
        with self._lock:
            self.completed.add(img)
            newly_ready: List[str] = []
            for child in self._dependents.get(img, set()):
                if child in self.skipped or child in self.failed:
                    continue
                self._indegree[child] -= 1
                if self._indegree[child] == 0:
                    newly_ready.append(child)
            return newly_ready

    def on_failure(self, img: str) -> List[str]:
        """
        Record a permanent failure (all retries exhausted).
        Cascade-skips every downstream dependent recursively.
        Returns the full list of images that were skipped as a result.
        """
        with self._lock:
            self.failed.add(img)
            return self._cascade_skip(img)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _cascade_skip(self, img: str) -> List[str]:
        """Recursively skip dependents of img.  Caller must hold self._lock."""
        newly_skipped: List[str] = []
        for child in self._dependents.get(img, set()):
            if child not in self.skipped and child not in self.failed:
                self.skipped.add(child)
                newly_skipped.append(child)
                newly_skipped.extend(self._cascade_skip(child))
        return newly_skipped

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def summary(self) -> Dict[str, int]:
        with self._lock:
            return {
                "total": len(self._indegree),
                "completed": len(self.completed),
                "failed": len(self.failed),
                "skipped": len(self.skipped),
            }


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


class BuildDispatcher:
    """
    Manages a thread-per-slot worker pool backed by a single shared Queue.

    Flow:
      1. Seed the queue with `graph.initial_ready()`.
      2. Each worker pulls a WorkItem, triggers a build on its slot, and:
           - on success  → unlocks dependents into the queue.
           - on retry    → re-enqueues the same image with attempt+1.
           - on failure  → cascade-skips dependents via the graph.
      3. `queue.Queue.join()` blocks until every task_done() has been called,
         which only happens when there is genuinely no more work to do.
    """

    def __init__(
        self,
        graph: BuildGraph,
        slots: List[GitHubBuildSlot],
        org: str,
    ) -> None:
        self.graph = graph
        self.slots = slots
        self.org = org.rstrip("/")
        self._queue: queue.Queue = queue.Queue()

    def run(self) -> None:
        """Seed, start workers, block until done."""
        for img in self.graph.initial_ready():
            self._queue.put(WorkItem(image=img))

        threads = []
        for slot in self.slots:
            t = threading.Thread(
                target=self._worker,
                args=(slot,),
                daemon=True,
                name=f"slot-{slot.slot_number}",
            )
            t.start()
            threads.append(t)

        # Block until every item (including dynamically added dependents) is done.
        self._queue.join()

        # Send a sentinel None to each worker so they exit cleanly.
        for _ in self.slots:
            self._queue.put(None)
        for t in threads:
            t.join()

    # ------------------------------------------------------------------
    # Worker
    # ------------------------------------------------------------------

    def _worker(self, slot: GitHubBuildSlot) -> None:
        while True:
            item = self._queue.get()
            if item is None:  # sentinel — time to exit
                self._queue.task_done()
                break

            img = item.image
            attempt = item.attempt
            container_name = self._to_container_name(img)

            slot._log(f"Building '{container_name}'  " f"(attempt {attempt}/{MAX_ATTEMPTS})")

            success = slot.build(container_name)

            if success:
                slot._log(f"✓ '{container_name}' succeeded")
                for new_img in self.graph.on_success(img):
                    self._queue.put(WorkItem(image=new_img))

            elif attempt < MAX_ATTEMPTS:
                slot._log(f"✗ '{container_name}' failed on attempt {attempt} — retrying …")
                self._queue.put(WorkItem(image=img, attempt=attempt + 1))

            else:
                slot._log(
                    f"✗ '{container_name}' failed after {MAX_ATTEMPTS} attempts — " f"cascade-skipping dependents"
                )
                skipped = self.graph.on_failure(img)
                if skipped:
                    print(
                        f"  Cascade-skipped ({len(skipped)}): " + ", ".join(sorted(skipped)),
                        flush=True,
                    )

            self._queue.task_done()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _to_container_name(self, image: str) -> str:
        """Strip 'org/' prefix — build-container.sh expects the bare folder name."""
        prefix = self.org + "/"
        return image[len(prefix) :] if image.startswith(prefix) else image


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _normalise_skip(raw_skip: List[str], org: str, all_images: Set[str]) -> Set[str]:
    """
    Accept both 'org/name' and bare 'name' forms in the skip list.
    Returns a set of full 'org/name' keys that exist in all_images.
    """
    result: Set[str] = set()
    for s in raw_skip:
        if s in all_images:
            result.add(s)
        else:
            full = f"{org}/{s}"
            if full in all_images:
                result.add(full)
    return result


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "Dispatch container builds to GitHub Actions slots "
            "in dependency order, with retries and cascade failure."
        )
    )
    ap.add_argument(
        "deps_json",
        help="Path to the JSON dependency file produced by docker-build-order_ad.py.",
    )
    ap.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub personal access token. Defaults to $GITHUB_TOKEN.",
    )
    ap.add_argument(
        "--repo",
        help="GitHub repository in 'owner/repo' format, e.g. sourcemation/images.",
        default="sourcemation/images",
    )
    ap.add_argument(
        "--ref",
        default="main",
        help="Git branch or ref to build against. Default: main.",
    )
    ap.add_argument(
        "--org",
        default="sourcemation",
        help="Image org prefix used in the dependency JSON. Default: sourcemation.",
    )
    ap.add_argument(
        "--slots",
        type=int,
        default=8,
        choices=range(1, 9),
        metavar="N",
        help="Number of build slots to use (1–8). Default: 8.",
    )
    ap.add_argument(
        "--skip",
        action="append",
        default=[],
        metavar="IMAGE",
        help=(
            "Image to skip (org/name or bare name). "
            "Can be passed multiple times. Skipped images and their "
            "dependents will not be built."
        ),
    )
    ap.add_argument(
        "--out-failed",
        default="build-orders/failed_images.txt",
        help="File to write the failed/skipped image report to. " "Default: build-orders/failed_images.txt.",
    )
    args = ap.parse_args()

    # --- Validate -------------------------------------------------------
    if not args.token:
        ap.error("GitHub token is required: use --token or set $GITHUB_TOKEN.")

    owner, sep, repo_name = args.repo.partition("/")
    if not sep or not repo_name:
        ap.error("--repo must be in 'owner/repo' format.")

    # --- Load dependencies ----------------------------------------------
    with open(args.deps_json, "r", encoding="utf-8") as fh:
        raw_deps: Dict[str, List[str]] = json.load(fh)

    org = args.org.strip().strip("/")
    all_images = set(raw_deps.keys())
    skip_set = _normalise_skip(args.skip, org, all_images)

    # --- Build graph ----------------------------------------------------
    graph = BuildGraph(raw_deps, skip_set)

    ready_count = len(graph.initial_ready())
    print(
        f"Loaded {len(all_images)} images. "
        f"Pre-skipped: {len(graph.skipped)}. "
        f"First wave ready to build: {ready_count}."
    )
    if ready_count == 0:
        print("Nothing to build.")
        sys.exit(0)

    # --- Build slots ----------------------------------------------------
    slots = [
        GitHubBuildSlot(
            slot_number=i,
            token=args.token,
            owner=owner,
            repo=repo_name,
            ref=args.ref,
        )
        for i in range(1, args.slots + 1)
    ]

    # --- Dispatch -------------------------------------------------------
    print(f"Starting dispatch with {args.slots} slot(s) …\n")
    start = time.monotonic()

    dispatcher = BuildDispatcher(graph=graph, slots=slots, org=org)
    dispatcher.run()

    elapsed = time.monotonic() - start

    # --- Summary --------------------------------------------------------
    summary = graph.summary()
    print(f"\n{'─' * 50}")
    print(f"Build complete in {elapsed:.1f}s")
    print(f"  Total    : {summary['total']}")
    print(f"  Completed: {summary['completed']}")
    print(f"  Failed   : {summary['failed']}")
    print(f"  Skipped  : {summary['skipped']}")
    print(f"{'─' * 50}")

    # --- Write failed/skipped report ------------------------------------
    out_dir = os.path.dirname(args.out_failed)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    failed_and_skipped = sorted(graph.failed | graph.skipped)
    with open(args.out_failed, "w", encoding="utf-8") as fh:
        for img in failed_and_skipped:
            reason = "failed" if img in graph.failed else "skipped"
            fh.write(f"{img}\t{reason}\n")

    if failed_and_skipped:
        print(f"\nFailed/skipped report: {args.out_failed}")
        for img in failed_and_skipped:
            tag = "FAILED " if img in graph.failed else "skipped"
            print(f"  [{tag}] {img}")
    else:
        print("\nAll images built successfully! 🎉")


if __name__ == "__main__":
    main()
