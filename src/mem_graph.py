"""Minimal CLI for block-based markdown knowledge graphs."""

from pathlib import Path
import argparse
import re
import sys


HEADER_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SEPARATOR_RE = re.compile(r"^\s*---\s*$")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def eprint(*args, **kwargs) -> None:
    print(*args, file=sys.stderr, **kwargs)


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[`*_~\[\](){}<>"]', "", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def rel_path(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def split_blocks(text: str) -> list[tuple[int, str]]:
    blocks = []
    current_lines = []
    block_start_line = 1
    in_fence = False
    current_line_num = 0

    for line in text.splitlines(keepends=True):
        current_line_num += 1
        if FENCE_RE.match(line):
            in_fence = not in_fence

        if not in_fence and SEPARATOR_RE.match(line):
            block = "".join(current_lines).strip()
            if block:
                blocks.append((block_start_line, block))
            current_lines = []
            block_start_line = current_line_num + 1
            continue

        current_lines.append(line)

    block = "".join(current_lines).strip()
    if block:
        blocks.append((block_start_line, block))
    return blocks


def first_heading(block: str) -> tuple[str | None, int]:
    for line in block.splitlines():
        match = HEADER_RE.match(line)
        if match:
            level = len(match.group(1))
            if level == 2:
                return match.group(2).strip(), level
    return None, 0


def extract_links(block: str) -> list[tuple[int, str]]:
    links = []
    in_fence = False

    for line_num, line in enumerate(block.splitlines(), start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        cleaned = INLINE_CODE_RE.sub("", line)
        for match in LINK_RE.finditer(cleaned):
            links.append((line_num, match.group(1).strip()))

    return links


def parse_file(path: Path, root: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []

    file_nodes = []
    file_name = rel_path(path, root)

    for block_num, (block_start, block) in enumerate(split_blocks(text), start=1):
        header, level = first_heading(block)
        if not header or level != 2:
            continue

        slug = slugify(header)
        if not slug:
            continue

        links_with_lines = extract_links(block)
        raw_links = [target for _, target in links_with_lines]
        link_entries = [
            {"line": line_num, "target": target}
            for line_num, target in links_with_lines
        ]

        file_nodes.append(
            {
                "id": f"{file_name}#{slug}",
                "file": file_name,
                "path": path.resolve(),
                "header": header,
                "slug": slug,
                "index": block_num,
                "block_start": block_start,
                "block": block,
                "links": raw_links,
                "link_entries": link_entries,
            }
        )

    return file_nodes


def resolve_link(node: dict, raw_target: str, root: Path) -> str | None:
    target = raw_target.strip()
    if not target or SCHEME_RE.match(target):
        return None

    if target.startswith("#"):
        anchor = slugify(target[1:])
        return f"{node['file']}#{anchor}" if anchor else None

    if "#" not in target:
        return None

    file_part, anchor_part = target.split("#", 1)
    anchor = slugify(anchor_part)
    if not file_part or not anchor:
        return None

    target_path = (node["path"].parent / file_part).resolve()
    try:
        return f"{rel_path(target_path, root)}#{anchor}"
    except ValueError:
        return None


def build_graph(root: Path) -> dict:
    nodes = {}
    duplicates = []

    for path in sorted(root.rglob("*.md")):
        for node in parse_file(path, root):
            if node["id"] in nodes:
                duplicates.append(node["id"])
                continue
            nodes[node["id"]] = node

    outgoing = {node_id: set() for node_id in nodes}
    incoming = {node_id: set() for node_id in nodes}
    unresolved = []

    for node in nodes.values():
        for link_entry in node["link_entries"]:
            raw_target = link_entry["target"]
            target_id = resolve_link(node, raw_target, root)
            if not target_id:
                unresolved.append(
                    {
                        "source_id": node["id"],
                        "source_file": node["file"],
                        "source_line": link_entry["line"],
                        "raw_target": raw_target,
                        "target_id": target_id,
                    }
                )
                continue
            outgoing[node["id"]].add(target_id)
            if target_id in incoming:
                incoming[target_id].add(node["id"])
            else:
                unresolved.append(
                    {
                        "source_id": node["id"],
                        "source_file": node["file"],
                        "source_line": link_entry["line"],
                        "raw_target": raw_target,
                        "target_id": target_id,
                    }
                )

    return {
        "root": root.resolve(),
        "nodes": nodes,
        "outgoing": {key: sorted(value) for key, value in outgoing.items()},
        "incoming": {key: sorted(value) for key, value in incoming.items()},
        "duplicates": sorted(duplicates),
        "unresolved": unresolved,
    }


def normalize_file(file_arg: str, root: Path) -> str:
    path = Path(file_arg)
    if not path.is_absolute():
        path = root / path
    return rel_path(path, root)


def describe_node(graph: dict, node_id: str) -> str:
    node = graph["nodes"].get(node_id)
    if not node:
        return node_id
    return f"{node['header']} ({node_id})"


def select_nodes(graph: dict, file_arg: str | None, header: str | None, node_id: str | None) -> list[str]:
    if node_id:
        return [node_id] if node_id in graph["nodes"] else []

    matches = list(graph["nodes"])
    if file_arg:
        file_name = normalize_file(file_arg, graph["root"])
        matches = [match for match in matches if graph["nodes"][match]["file"] == file_name]
    if header:
        wanted = header.strip().lower()
        matches = [match for match in matches if graph["nodes"][match]["header"].lower() == wanted]

    return sorted(matches, key=lambda match: (graph["nodes"][match]["file"], graph["nodes"][match]["index"]))


def print_connections(graph: dict, node_id: str, indent: str = "") -> None:
    for target_id in graph["outgoing"].get(node_id, []):
        print(f"{indent}-> {describe_node(graph, target_id)}")
    for source_id in graph["incoming"].get(node_id, []):
        print(f"{indent}<- {describe_node(graph, source_id)}")


def cmd_headers(args: argparse.Namespace, graph: dict) -> int:
    matches = select_nodes(graph, args.file, None, None)
    if not matches:
        eprint(f"error: no blocks found in {args.file}")
        return 1

    print(normalize_file(args.file, graph["root"]))
    print()
    for node_id in matches:
        node = graph["nodes"][node_id]
        line = f"- {node['header']}"
        if args.all:
            line += f" [{node_id}]"
        print(line)
        if args.all:
            print_connections(graph, node_id, indent="  ")
    return 0


def cmd_view(args: argparse.Namespace, graph: dict) -> int:
    if not any([args.file, args.header, args.id]):
        eprint("error: pass --file, --header, or --id")
        return 1

    matches = select_nodes(graph, args.file, args.header, args.id)
    if not matches:
        eprint("error: no matching block found")
        if args.header:
            eprint(f"  (header: '{args.header}' not found)")
        elif args.id:
            eprint(f"  (id: '{args.id}' not found)")
        elif args.file:
            eprint(f"  (file: '{args.file}' has no blocks)")
        return 1

    if len(matches) > 1:
        eprint("error: multiple blocks matched; use --file or --id to disambiguate")
        for node_id in matches:
            print(f"- {describe_node(graph, node_id)}")
        return 1

    node_id = matches[0]
    node = graph["nodes"][node_id]
    print(node_id)
    print()
    print(node["block"])
    print()
    print_connections(graph, node_id)

    return 0


def cmd_graph(args: argparse.Namespace, graph: dict) -> int:
    if not any([args.file, args.header, args.id]):
        eprint("error: pass --file, --header, or --id")
        return 1

    matches = select_nodes(graph, args.file, args.header, args.id)
    if not matches:
        eprint("error: no matching block found")
        if args.header:
            eprint(f"  (header: '{args.header}' not found)")
            suggestions = [
                m for m in graph["nodes"]
                if args.header.lower() in graph["nodes"][m]["header"].lower()
            ]
            if suggestions:
                eprint("  similar headers:")
                for s in suggestions[:5]:
                    eprint(f"    - {graph['nodes'][s]['header']} ({s})")
        elif args.id:
            eprint(f"  (id: '{args.id}' not found)")
        elif args.file:
            eprint(f"  (file: '{args.file}' has no blocks)")
        return 1

    if len(matches) > 1:
        eprint("error: multiple blocks matched; use --file or --id to disambiguate")
        for node_id in matches:
            print(f"- {describe_node(graph, node_id)}")
        return 1

    start = matches[0]
    visited = {start}
    frontier = [start]

    print(describe_node(graph, start))
    for level in range(1, max(args.depth, 1) + 1):
        next_frontier = []
        indent = "  " * level
        for node_id in frontier:
            neighbors = graph["outgoing"].get(node_id, []) + graph["incoming"].get(node_id, [])
            for neighbor_id in neighbors:
                if neighbor_id in visited:
                    continue
                arrow = "->" if neighbor_id in graph["outgoing"].get(node_id, []) else "<-"
                print(f"{indent}{arrow} {describe_node(graph, neighbor_id)}")
                visited.add(neighbor_id)
                next_frontier.append(neighbor_id)
        if not next_frontier:
            break
        frontier = next_frontier
    return 0


def cmd_check(_args: argparse.Namespace, graph: dict) -> int:
    issues = 0

    for node_id in graph["duplicates"]:
        node = graph["nodes"].get(node_id)
        eprint(f"duplicate block id: {node_id}")
        if node:
            eprint(f"  first defined in: {node['file']}, block starts at line {node['block_start']}")
        issues += 1

    for item in graph["unresolved"]:
        eprint(
            f"unresolved: {item['source_file']}:{item['source_line']} "
            f"[link to {item['raw_target']}] -> {item['target_id'] or '?'}"
        )
        issues += 1

    if issues == 0:
        print("OK")
        return 0

    print(f"Found {issues} issue(s)")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Markdown graph CLI",
        epilog=(
            "Examples:\n"
            "  python3 src/mem_graph.py --root docs check\n"
            "  python3 src/mem_graph.py --root docs headers --file attention.md --all\n"
            "  python3 src/mem_graph.py --root docs view --id embeddings.md#token-budget\n"
            "  python3 src/mem_graph.py --root docs graph --header 'Embedding Capacity' --depth 2"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--root", default=".", help="Directory to scan")
    subparsers = parser.add_subparsers(dest="command", required=True)

    headers = subparsers.add_parser("headers", help="List block headers in a file")
    headers.add_argument("--file", required=True)
    headers.add_argument("--all", action="store_true", help="Include ids and direct links")
    headers.set_defaults(func=cmd_headers)

    view = subparsers.add_parser("view", help="Show one block or all blocks in a file")
    view.add_argument("--file")
    view.add_argument("--header")
    view.add_argument("--id")
    view.set_defaults(func=cmd_view)

    graph_cmd = subparsers.add_parser("graph", help="Show graph neighbors")
    graph_cmd.add_argument("--file")
    graph_cmd.add_argument("--header")
    graph_cmd.add_argument("--id")
    graph_cmd.add_argument("--depth", type=int, default=1)
    graph_cmd.set_defaults(func=cmd_graph)

    check = subparsers.add_parser("check", help="Validate links and duplicate ids")
    check.set_defaults(func=cmd_check)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    root = Path(args.root).resolve()
    graph = build_graph(root)
    raise SystemExit(args.func(args, graph))


if __name__ == "__main__":
    main()
