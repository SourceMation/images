#!/usr/bin/env python3
import argparse
import os
import re
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple


FROM_RE = re.compile(r"^\s*FROM\s+(?P<rest>.+?)\s*$", re.IGNORECASE)
ARG_RE = re.compile(r"^\s*ARG\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*(?:=\s*(?P<val>.*?))?\s*$", re.IGNORECASE)
COPY_RE = re.compile(r"^\s*COPY\s+(?P<rest>.+?)\s*$", re.IGNORECASE)


def strip_full_line_comment(line: str) -> str:
    s = line.strip()
    if not s or s.startswith("#"):
        return ""
    return line.rstrip("\n")


def docker_var_subst(s: str, args_defaults: Dict[str, str]) -> str:
    # Minimal ${VAR} and $VAR substitution using ARG defaults (static only)
    def repl(m):
        var = m.group(1) or m.group(2)
        return args_defaults.get(var, m.group(0))
    return re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)", repl, s)


def strip_tag_digest(image: str) -> str:
    # Remove @sha256:... and :tag (only if : is after last /)
    img = image.split("@", 1)[0]
    last_slash = img.rfind("/")
    last_colon = img.rfind(":")
    if last_colon > last_slash:
        img = img[:last_colon]
    return img


def parse_from_line(rest: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Parses: FROM [--platform=...] <image-or-stage> [AS <alias>]
    Returns (base, alias)
    """
    tokens = rest.strip().split()
    if not tokens:
        return None, None

    i = 0
    while i < len(tokens) and tokens[i].startswith("--"):
        i += 1
    if i >= len(tokens):
        return None, None

    base = tokens[i]
    alias = None

    for j in range(i + 1, len(tokens) - 1):
        if tokens[j].lower() == "as":
            alias = tokens[j + 1]
            break

    return base, alias


def extract_copy_from(rest: str) -> Optional[str]:
    """
    Finds --from=... in COPY instruction.
    Returns the value or None.
    """
    parts = rest.split()
    for idx, p in enumerate(parts):
        if p.startswith("--from="):
            return p.split("=", 1)[1]
        if p == "--from" and idx + 1 < len(parts):
            return parts[idx + 1]
    return None


@dataclass
class DockerfileDeps:
    local_deps: Set[str]
    external_deps: Set[str]


def discover_dockerfiles(root: str, names: List[str]) -> List[Tuple[str, str]]:
    """
    Returns list of (image_rel_dir, dockerfile_path)
    """
    found: List[Tuple[str, str]] = []
    for dirpath, _, filenames in os.walk(root):
        for n in names:
            if n in filenames:
                rel_dir = os.path.relpath(dirpath, root)
                found.append((rel_dir, os.path.join(dirpath, n)))
                break
    return found


def normalize_local_ref(dep: str, org: str, local_images: Set[str], local_short: Set[str]) -> Optional[str]:
    dep0 = strip_tag_digest(dep)

    # Exact match (full org/name)
    if dep0 in local_images:
        return dep0

    # If it starts with org/ and matches known local images
    if dep0.startswith(org + "/") and dep0 in local_images:
        return dep0

    # Short-name match: dep == rel_dir (folder path)
    if dep0 in local_short:
        full = f"{org}/{dep0}".replace("\\", "/")
        if full in local_images:
            return full

    return None


def parse_dockerfile(path: str, org: str, local_images: Set[str], local_short: Set[str]) -> DockerfileDeps:
    stage_aliases: Set[str] = set()
    args_defaults: Dict[str, str] = {}

    local_deps: Set[str] = set()
    external_deps: Set[str] = set()

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = strip_full_line_comment(raw)
            if not line.strip():
                continue

            m_arg = ARG_RE.match(line)
            if m_arg:
                name = m_arg.group("name")
                val = m_arg.group("val")
                if val is not None:
                    args_defaults[name] = val.strip()
                continue

            m_from = FROM_RE.match(line)
            if m_from:
                rest = docker_var_subst(m_from.group("rest"), args_defaults).strip()
                base, alias = parse_from_line(rest)
                if base:
                    base_clean = strip_tag_digest(base)

                    # If base is a previous stage alias or numeric index => not an image dep
                    if base_clean in stage_aliases or base_clean.isdigit():
                        pass
                    else:
                        local = normalize_local_ref(base_clean, org, local_images, local_short)
                        if local:
                            local_deps.add(local)
                        else:
                            external_deps.add(base_clean)

                if alias:
                    stage_aliases.add(alias)
                continue

            m_copy = COPY_RE.match(line)
            if m_copy:
                rest = docker_var_subst(m_copy.group("rest"), args_defaults).strip()
                frm = extract_copy_from(rest)
                if frm:
                    frm_clean = strip_tag_digest(frm)
                    if frm_clean in stage_aliases or frm_clean.isdigit():
                        pass
                    else:
                        local = normalize_local_ref(frm_clean, org, local_images, local_short)
                        if local:
                            local_deps.add(local)
                        else:
                            external_deps.add(frm_clean)

    return DockerfileDeps(local_deps=local_deps, external_deps=external_deps)


def topo_sort(nodes: Set[str], deps: Dict[str, Set[str]]) -> Tuple[List[str], Set[str]]:
    indeg = {n: 0 for n in nodes}
    children = defaultdict(set)

    for n in nodes:
        for d in deps.get(n, set()):
            if d not in nodes:
                continue
            indeg[n] += 1
            children[d].add(n)

    q = deque([n for n in nodes if indeg[n] == 0])
    order: List[str] = []

    while q:
        x = q.popleft()
        order.append(x)
        for c in children.get(x, set()):
            indeg[c] -= 1
            if indeg[c] == 0:
                q.append(c)

    leftover = {n for n in nodes if indeg[n] > 0}
    return order, leftover


def print_forest_as_tree(local_images: Set[str], deps_local: Dict[str, Set[str]]) -> str:
    # Build edges dep -> dependent
    children = defaultdict(set)
    parents = defaultdict(set)
    for img in local_images:
        for dep in deps_local.get(img, set()):
            if dep in local_images:
                children[dep].add(img)
                parents[img].add(dep)

    roots = [img for img in sorted(local_images) if not parents.get(img)]

    # If cycles exist, we may have no roots for some nodes; show them as extra roots
    seen_in_roots = set(roots)
    for img in sorted(local_images):
        if img not in seen_in_roots and img not in parents:
            roots.append(img)
            seen_in_roots.add(img)

    lines: List[str] = []
    seen_global: Set[str] = set()

    def dfs(node: str, prefix: str, is_last: bool):
        connector = "└── " if is_last else "├── "
        label = node
        if node in seen_global:
            label += " (shared)"
        else:
            seen_global.add(node)

        lines.append(prefix + connector + label)

        kids = sorted(children.get(node, set()))
        for i, k in enumerate(kids):
            last = i == (len(kids) - 1)
            new_prefix = prefix + ("    " if is_last else "│   ")
            dfs(k, new_prefix, last)

    for r_i, r in enumerate(roots):
        label = r
        if r in seen_global:
            label += " (shared)"
        else:
            seen_global.add(r)

        lines.append(label)
        kids = sorted(children.get(r, set()))
        for i, k in enumerate(kids):
            dfs(k, "", i == (len(kids) - 1))
        if r_i != len(roots) - 1:
            lines.append("")

    return "\n".join(lines) + "\n"


def dot_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def render_dot(local_images: Set[str],
               deps_local: Dict[str, Set[str]],
               deps_external: Dict[str, Set[str]]) -> str:
    """
    DOT graph where edges are: base -> dependent
    Includes external bases as separate nodes (dashed ellipse).
    """
    external_nodes: Set[str] = set()
    edges: Set[Tuple[str, str]] = set()

    for img in local_images:
        for dep in deps_local.get(img, set()):
            if dep in local_images:
                edges.add((dep, img))
        for ext in deps_external.get(img, set()):
            external_nodes.add(ext)
            edges.add((ext, img))

    out: List[str] = []
    out.append("digraph build_order {")
    out.append("  rankdir=LR;")
    out.append('  node [fontsize=10];')

    # Local nodes
    out.append("  // Local images")
    for img in sorted(local_images):
        out.append(f'  "{dot_escape(img)}" [shape=box];')

    # External nodes
    if external_nodes:
        out.append("")
        out.append("  // External base images")
        for ext in sorted(external_nodes):
            out.append(f'  "{dot_escape(ext)}" [shape=ellipse, style=dashed];')

    # Edges
    out.append("")
    out.append("  // Dependencies: base -> dependent")
    for a, b in sorted(edges):
        out.append(f'  "{dot_escape(a)}" -> "{dot_escape(b)}";')

    out.append("}")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(
        description="Compute docker build order (multi-stage aware) and write flat + tree + dot outputs."
    )
    ap.add_argument("images_dir", help="Root directory containing image subdirs (Dockerfile/Containerfile).")
    ap.add_argument("org", help="Local image namespace/prefix, e.g. 'sourcemation'.")
    ap.add_argument("--dockerfile", action="append", default=["Dockerfile", "Containerfile"],
                    help="Dockerfile names to look for (can be passed multiple times). Default: Dockerfile + Containerfile")
    ap.add_argument("--out-flat", default="build_order.txt", help="Flat output file (topological order).")
    ap.add_argument("--out-tree", default="build_order.tree.txt", help="Tree/forest output file.")
    ap.add_argument("--out-dot", default="build_order.dot", help="Graphviz DOT output file.")
    args = ap.parse_args()

    images_dir = os.path.abspath(args.images_dir)
    org = args.org.strip().strip("/")

    discovered = discover_dockerfiles(images_dir, args.dockerfile)
    if not discovered:
        raise SystemExit(f"No Dockerfile/Containerfile found under: {images_dir}")

    # Local images are identified by folder path relative to images_dir:
    # image name = org/<rel_dir>
    local_images: Set[str] = set()
    local_short: Set[str] = set()
    df_by_image: Dict[str, str] = {}

    for rel_dir, df_path in discovered:
        rel_norm = rel_dir.replace("\\", "/")
        img = f"{org}/{rel_norm}".replace("//", "/")
        local_images.add(img)
        local_short.add(rel_norm)
        df_by_image[img] = df_path

    deps_local: Dict[str, Set[str]] = {}
    deps_external: Dict[str, Set[str]] = {}

    for img, df_path in sorted(df_by_image.items()):
        d = parse_dockerfile(df_path, org, local_images, local_short)
        deps_local[img] = set(d.local_deps)
        deps_external[img] = set(d.external_deps)

    # Flat order (local-only topo sort)
    order, leftover = topo_sort(local_images, deps_local)
    if leftover:
        # deterministic fallback: append remaining nodes
        for n in sorted(leftover):
            if n not in order:
                order.append(n)

    with open(args.out_flat, "w", encoding="utf-8") as f:
        for img in order:
            f.write(img + "\n")

    # Tree/forest (local deps)
    tree_txt = ""
    if leftover:
        tree_txt += "WARNING: cycle detected among these images (tree may be misleading):\n"
        for x in sorted(leftover):
            tree_txt += f"  - {x}\n"
        tree_txt += "\n"
    tree_txt += print_forest_as_tree(local_images, deps_local)

    with open(args.out_tree, "w", encoding="utf-8") as f:
        f.write(tree_txt)

    # DOT (includes external bases)
    dot_txt = render_dot(local_images, deps_local, deps_external)
    with open(args.out_dot, "w", encoding="utf-8") as f:
        f.write(dot_txt)

    print(f"Wrote flat build order to: {args.out_flat} ({len(order)} images)")
    print(f"Wrote tree build forest to: {args.out_tree}")
    print(f"Wrote graphviz dot to: {args.out_dot}")


if __name__ == "__main__":
    main()


