"""
mem_graph - Knowledge graph nodes and edges extraction from markdown
"""

from pathlib import Path
import re
import json
import argparse
from utils import SEMANTIC_LINK_RE, HEADER_RE, FENCE_RE_1, FENCE_RE_2


def normalized_id(fpath: Path, heading: str) -> str:
    return f"{fpath.resolve()}::{heading.strip()}"


def short_id(node_id: str, root: Path) -> str:
    if '::' not in node_id:
        return node_id
    fpath, header = node_id.rsplit('::', 1)
    try:
        fpath = str(Path(fpath).relative_to(root.resolve()))
    except ValueError:
        pass
    return f'{fpath}::{header}'


def resolve_link(target: str, current_file: Path, heading_index: dict) -> str:
    """
    Resolve a wiki-style link to a node ID.
    
    Supports:
    - [[path::heading | rel]] - explicit file::heading
    - [[file.md#heading | rel]] - file#heading syntax
    - [[#heading | rel]] - same-file heading
    - [[heading | rel]] - global heading lookup
    """
    target = target.strip()
    
    # Format: "path::heading"
    if '::' in target:
        fpath, header = target.rsplit('::', 1)
        return normalized_id(Path(fpath), header)
    
    # Format: "path#heading" or "#heading"
    if '#' in target:
        fpath, header = target.rsplit('#', 1)
        p = Path(fpath) if fpath else current_file
        if not p.is_absolute():
            p = Path(current_file.parent / p).resolve()
        return normalized_id(p, header)
    
    # Format: "heading" - global lookup
    if target in heading_index and heading_index[target]:
        matches = heading_index[target]
        # Prefer match in current file
        for match_id in matches:
            if str(current_file.resolve()) in match_id:
                return match_id
        return matches[0]
    
    # Unresolved - create stub
    return normalized_id(current_file, target)


def extract_edges(root: Path) -> tuple[dict, list]:
    """
    Extract nodes and edges from markdown files.
    Only processes [[target | relation]] syntax for relations.
    """
    nodes = {}
    edges = []
    heading_index = {}
    
    # 1) Create all nodes and build heading index
    file_contents = {}
    
    for _fpath in root.rglob('*.md'):
        try:
            text = _fpath.read_text(encoding='utf-8')
        except Exception:
            continue

        # Remove fenced code blocks
        clean = re.sub(FENCE_RE_1, '', text, flags=re.MULTILINE | re.DOTALL)
        clean = re.sub(FENCE_RE_2, '', clean, flags=re.MULTILINE | re.DOTALL)
        
        file_contents[_fpath] = clean

        # Find all headers
        headers = list(HEADER_RE.finditer(clean))

        if not headers:
            # No headers -> treat file as single node
            file_heading = _fpath.stem
            node_id = normalized_id(_fpath, file_heading)
            nodes[node_id] = {'heading': file_heading, 'file': str(_fpath.resolve())}
            heading_index.setdefault(file_heading, []).append(node_id)
            continue

        # Create nodes for each heading
        for m in headers:
            heading_text = m.group(2).strip()
            node_id = normalized_id(_fpath, heading_text)
            nodes[node_id] = {'heading': heading_text, 'file': str(_fpath.resolve())}
            heading_index.setdefault(heading_text, []).append(node_id)
    
    # 2) Extract ONLY semantic links
    for _fpath, clean in file_contents.items():
        headers = list(HEADER_RE.finditer(clean))
        
        if not headers:
            # Single file-level node
            file_heading = _fpath.stem
            node_id = normalized_id(_fpath, file_heading)
            block_text = clean
            
            # Extract ONLY semantic links [[target | relation]]
            for match in SEMANTIC_LINK_RE.finditer(block_text):
                target, relation = match.group(1).strip(), match.group(2).strip()
                dst = resolve_link(target, _fpath, heading_index)
                edges.append((node_id, dst, relation))
            continue

        # Process each heading section
        for i, m in enumerate(headers):
            heading_text = m.group(2).strip()
            start = m.end()
            end = headers[i+1].start() if i+1 < len(headers) else len(clean)
            section = clean[start:end]

            node_id = normalized_id(_fpath, heading_text)
            
            # Extract ONLY semantic links [[target | relation]]
            for match in SEMANTIC_LINK_RE.finditer(section):
                target, relation = match.group(1).strip(), match.group(2).strip()
                dst = resolve_link(target, _fpath, heading_index)
                edges.append((node_id, dst, relation))

    # Create stub nodes for unresolved targets
    for src, dst, rel in edges:
        if dst not in nodes:
            nodes[dst] = {'heading': dst.split('::')[-1], 'file': None}

    # Make bidirectional reverse edges
    reverse_edges = []
    for src, dst, rel in list(edges):
        if rel.startswith('~'):
            reverse_edges.append((dst, src, rel[1:]))
        else:
            reverse_edges.append((dst, src, f'~{rel}'))
    
    edges.extend(reverse_edges)

    # Remove duplicates
    edges = list(set(edges))

    # Deterministic ordering
    nodes_sorted = dict(sorted(nodes.items()))
    edges_sorted = sorted(edges)
    return nodes_sorted, edges_sorted


def print_graph_cli(nodes: dict, edges: list, root: Path):
    print(f"graph: {root}")
    print()

    by_src = {}
    for src, dst, rel in edges:
        by_src.setdefault(src, []).append((dst, rel))

    for node_id, data in nodes.items():
        print(f"node: {data['heading']}")
        print(f"  file: {data['file'] or 'UNRESOLVED'}")

        for dst, rel in by_src.get(node_id, []):
            rel_name = rel.lstrip("~")
            direction = "->" if not rel.startswith("~") else "<-"
            dst_h = nodes.get(dst, {}).get("heading", dst.split('::')[-1])

            print(f"  edge: {rel_name} {direction} {dst_h}")

        print()


def traverse_cli(nodes, edges, start, relation=None):
    start_id = next(
        (nid for nid, d in nodes.items()
        if start.lower() in d["heading"].lower()),
        None
    )

    if not start_id:
        print(f"error: node not found: {start}")
        return

    print(f"node: {nodes[start_id]['heading']}")
    print(f"file: {nodes[start_id]['file']}")

    for src, dst, rel in edges:
        if src != start_id:
            continue
        if relation and relation not in rel:
            continue

        rel_name = rel.lstrip("~")
        direction = "->" if not rel.startswith("~") else "<-"
        dst_h = nodes.get(dst, {}).get("heading", dst.split("::")[-1])

        print(f"edge: {rel_name} {direction} {dst_h}")


def export_json(nodes: dict, edges: list, outpath: Path, root: Path):
    payload = {
        "nodes": [{"id": short_id(nid, root), **data} for nid, data in nodes.items()],
        "edges": [{"src": short_id(s, root), "dst": short_id(d, root), "rel": r} for s, d, r in edges],
    }
    outpath.write_text(json.dumps(payload, indent=2))
    print(f"Exported: {outpath}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=str)
    ap.add_argument("--export", type=str)
    ap.add_argument("--traverse", type=str)
    ap.add_argument("--relation", type=str)
    args = ap.parse_args()

    root = Path(args.root)
    nodes, edges = extract_edges(root)

    if args.export:
        export_json(nodes, edges, Path(args.export), root)
    elif args.traverse:
        traverse_cli(nodes, edges, args.traverse, args.relation)
    else:
        print_graph_cli(nodes, edges, root)


if __name__ == "__main__":
    main()
