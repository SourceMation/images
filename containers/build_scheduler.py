#!/usr/bin/env python3
import argparse
import json
import time
import random
import sys
from enum import Enum
from typing import Dict, List, Set, Optional

class BuildStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"  # Dependent on failed build

class GithubActionDispatcher:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    def dispatch(self, image_name: str, spot_name: str) -> bool:
        """
        Invokes the GitHub Action.
        Returns True if successfully dispatched (mocked).
        """
        print(f"[{spot_name}] Dispatching build for {image_name}...")
        if self.dry_run:
            return True

        # TODO: Implement actual GitHub API call here
        # api_url = f"https://api.github.com/repos/.../actions/workflows/{spot_name}.yml/dispatches"
        # requests.post(api_url, ...)
        return True

    def check_status(self, image_name: str) -> BuildStatus:
        """
        Mock status check. In reality, this would query the specific run ID.
        """
        # Randomly decide status for simulation
        r = random.random()
        if r < 0.1:
            return BuildStatus.FAILED
        elif r < 0.4:
            return BuildStatus.RUNNING
        else:
            return BuildStatus.COMPLETED

class BuildManager:
    def __init__(self, dependencies: Dict[str, List[str]], state_file: str, max_spots: int = 6):
        self.dependencies = dependencies
        self.dependents = self._calculate_dependents(dependencies)
        self.state_file = state_file
        self.max_spots = max_spots
        self.image_states: Dict[str, str] = {img: BuildStatus.PENDING.value for img in dependencies}
        self.dispatcher = GithubActionDispatcher()
        self.running_jobs: Dict[str, str] = {} # image -> spot_name

        self.load_state()

    def _calculate_dependents(self, dependencies: Dict[str, List[str]]) -> Dict[str, List[str]]:
        dependents = {img: [] for img in dependencies}
        for img, deps in dependencies.items():
            for dep in deps:
                if dep in dependents:
                    dependents[dep].append(img)
        return dependents

    def load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                saved_states = json.load(f)
                # Merge saved states. If an image is missing, it remains PENDING (default)
                for img, status in saved_states.items():
                    if img in self.image_states:
                        self.image_states[img] = status
            print(f"Loaded state from {self.state_file}")
        except FileNotFoundError:
            print("No previous state found. Starting fresh.")

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.image_states, f, indent=2)
        print(f"State saved to {self.state_file}")

    def get_spot_name(self, index: int) -> str:
        return f"build-spot-{index + 1}"

    def is_runnable(self, image: str) -> bool:
        if self.image_states[image] != BuildStatus.PENDING.value:
            return False

        deps = self.dependencies.get(image, [])
        for dep in deps:
            # If dependency is external (not in our map), we assume it's available or we can't track it.
            # But based on the json format, external deps might not be keys?
            # Let's check if dep is in our system.
            if dep in self.image_states:
                if self.image_states[dep] != BuildStatus.COMPLETED.value:
                    return False
        return True

    def mark_failed_recursive(self, image: str):
        """Mark image and all its dependents as SKIPPED (due to failure)"""
        if self.image_states[image] == BuildStatus.SKIPPED.value:
            return

        self.image_states[image] = BuildStatus.SKIPPED.value
        print(f"Skipping {image} due to dependency failure.")

        for child in self.dependents.get(image, []):
            self.mark_failed_recursive(child)

    def run_loop(self):
        iteration = 0
        while True:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # 1. Check running jobs
            completed_in_this_tick = []
            failed_in_this_tick = []
            
            # Create a copy to iterate safely
            for image, spot in list(self.running_jobs.items()):
                status = self.dispatcher.check_status(image)
                if status == BuildStatus.COMPLETED:
                    print(f"Image {image} completed on {spot}.")
                    self.image_states[image] = BuildStatus.COMPLETED.value
                    del self.running_jobs[image]
                    completed_in_this_tick.append(image)
                elif status == BuildStatus.FAILED:
                    print(f"Image {image} FAILED on {spot}.")
                    self.image_states[image] = BuildStatus.FAILED.value
                    del self.running_jobs[image]
                    failed_in_this_tick.append(image)
                else:
                    print(f"Image {image} is still running on {spot}...")

            # 2. Handle failures (prune tree)
            for failed_img in failed_in_this_tick:
                # Mark all dependents as skipped
                for child in self.dependents.get(failed_img, []):
                    self.mark_failed_recursive(child)

            # 3. Find runnable images
            runnable = []
            pending_count = 0
            for img, status in self.image_states.items():
                if status == BuildStatus.PENDING.value:
                    pending_count += 1
                    if self.is_runnable(img):
                        runnable.append(img)
            
            print(f"Pending: {pending_count}, Runnable: {len(runnable)}, Running: {len(self.running_jobs)}")

            if pending_count == 0 and len(self.running_jobs) == 0:
                print("All jobs finished (completed, failed, or skipped).")
                break

            if len(runnable) == 0 and len(self.running_jobs) == 0 and pending_count > 0:
                # This might happen if there's a cycle or stuck dependency, but we handled cycles in the build order script.
                # Or if external dependencies are missing from the map?
                print("Deadlock detected? No running jobs and no runnable images.")
                break

            # 4. Dispatch new jobs
            # Sort runnable to be deterministic (or priority based?)
            runnable.sort()
            
            # Find free spots
            used_spots = set(self.running_jobs.values())
            available_spots = []
            for i in range(self.max_spots):
                spot = self.get_spot_name(i)
                if spot not in used_spots:
                    available_spots.append(spot)

            while available_spots and runnable:
                image = runnable.pop(0)
                spot = available_spots.pop(0)

                self.dispatcher.dispatch(image, spot)
                self.image_states[image] = BuildStatus.RUNNING.value
                self.running_jobs[image] = spot

            self.save_state()

            # Wait a bit before next tick (simulated)
            time.sleep(2)

def main():
    parser = argparse.ArgumentParser(description="Build Scheduler")
    parser.add_argument("--dependencies", required=True, help="JSON file with dependencies")
    parser.add_argument("--state-file", default="build_state.json", help="File to save/load state")
    parser.add_argument("--spots", type=int, default=6, help="Number of build spots")
    args = parser.parse_args()

    with open(args.dependencies, 'r') as f:
        dependencies = json.load(f)

    manager = BuildManager(dependencies, args.state_file, args.spots)
    manager.run_loop()

if __name__ == "__main__":
    main()
