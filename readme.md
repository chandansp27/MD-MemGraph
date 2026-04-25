# mem-graph

A lightweight markdown memory graph for AI agents. Use plain files, atomic blocks, and standard links to preserve reusable context and semantic connections while staying easy to search with normal shell tools.

## Overview

mem-graph treats a markdown corpus as a small knowledge graph where:

- **Nodes** are atomic concepts defined by `##` headings in markdown files
- **Edges** are standard markdown links between concepts
- **Blocks** are content sections separated by `---`

This gives agents a plain-text memory that remains human-readable, grep-friendly, and navigable with a small CLI when links and backlinks matter.

## Quick Start

```bash
# List concepts in a file
python3 src/mem_graph.py --root example_docs headers --file overview.md --all

# Search first with normal shell tools
rg "attention|embedding" example_docs/
grep -RIn "attention" example_docs/

# View a specific concept
python3 src/mem_graph.py --root example_docs view --id overview.md#what-is-md-graph

# Inspect direct graph connections
python3 src/mem_graph.py --root example_docs graph --id overview.md#what-is-md-graph --depth 1

# Validate links after edits or when correctness matters
python3 src/mem_graph.py --root example_docs check
```

## Format

Create knowledge blocks using markdown:

```markdown
## Concept Name

Description of the concept. Link to related concepts:
- [Related Concept](./other-file.md#related-concept)
- [Another Concept](#another-concept)

More explanation here.

---

## Another Concept

Another atomic concept connected to the first.
```

### Rules

- Blocks are separated by `---` on its own line
- Only `##` headings define graph nodes (not `#` or `###`)
- Links use standard markdown: `[text](./file.md#header)`
- Links inside inline code spans are ignored

## CLI Reference

| Command | Description |
|---------|-------------|
| `check` | Validate links and report broken references |
| `headers --file <file> --all` | List all concept headers with connections |
| `view --id <file.md#header>` | View a specific concept's content |
| `graph --header <Name> --depth N` | Explore N-level graph neighborhood |

Full reference: [CLI Reference](example_docs/cli-reference.md)

## CLI + Bash Traversal

Use shell tools for first-pass discovery, then use the graph CLI for node-aware navigation.

```bash
# quick node listing
rg '^## ' example_docs/
grep '^## ' example_docs/*.md

# quick link extraction
rg -o '\]\([^)]*\.md#[^)]*\)' example_docs/
grep -Rho '\]\([^)]*\.md#[^)]*\)' example_docs/

# topic search across docs
rg -l 'attention' example_docs/
grep -Ril 'attention' example_docs/

# file and line inspection
find example_docs -type f -name '*.md'
sed -n '1,160p' example_docs/overview.md
nl -ba example_docs/overview.md | sed -n '1,120p'
```

`rg` is fastest when available. `grep`, `find`, `sed`, `nl`, `awk`, and short scripts are useful companions because the graph is just markdown.

## Documentation

The `example_docs/` directory contains the full knowledge base:

- [Getting Started](example_docs/getting-started.md) - Hands-on introduction
- [Format](example_docs/format.md) - Block and link syntax
- [Knowledge Design](example_docs/knowledge-design.md) - Best practices
- [Graph Theory](example_docs/graph-theory.md) - How the graph works
- [Workflows](example_docs/workflows.md) - Common usage patterns
- [Troubleshooting](example_docs/troubleshooting.md) - Problem solving

## For AI Agents

Use this as lightweight memory: recall prior context, record reusable decisions or discoveries, and link related concepts so future agents can navigate them. Only write memory when the context is likely to help later work.

See [.agents/skills/md-graph/SKILL.md](.agents/skills/md-graph/SKILL.md) for agent-specific instructions and complementary CLI + shell traversal patterns.

## Project Structure

```
.
├── src/
│   └── mem_graph.py      # CLI tool
├── example_docs/          # Example knowledge base
├── tests/
│   └── test_mem_graph.py # Regression tests
├── .agents/
│   └── skills/
│       └── md-graph/
│           └── SKILL.md  # Agent integration guide
└── README.md             # This file
```

## Testing

```bash
python3 tests/test_mem_graph.py
```
