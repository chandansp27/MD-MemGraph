# mem-graph

A filesystem-based memory and knowledge graph system for AI agents. Build interconnected documentation that agents can query and navigate using standard markdown links.

## Overview

fs-memory treats your documentation as a knowledge graph where:

- **Nodes** are atomic concepts defined by `##` headings in markdown files
- **Edges** are standard markdown links between concepts
- **Blocks** are content sections separated by `---`

This gives you a lightweight, plain-text knowledge base that remains human-readable while being machine-queryable.

## Quick Start

```bash
# Validate your knowledge graph
python3 src/mem_graph.py --root example_docs check

# List all concepts in a file
python3 src/mem_graph.py --root example_docs headers --file overview.md --all

# View a specific concept
python3 src/mem_graph.py --root example_docs view --id overview.md#what-is-md-graph

# Explore graph connections
python3 src/mem_graph.py --root example_docs graph --header "Overview" --depth 2
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

## Documentation

The `example_docs/` directory contains the full knowledge base:

- [Getting Started](example_docs/getting-started.md) - Hands-on introduction
- [Format](example_docs/format.md) - Block and link syntax
- [Knowledge Design](example_docs/knowledge-design.md) - Best practices
- [Graph Theory](example_docs/graph-theory.md) - How the graph works
- [Workflows](example_docs/workflows.md) - Common usage patterns
- [Troubleshooting](example_docs/troubleshooting.md) - Problem solving

## For AI Agents

See [.agents/skills/md-graph/SKILL.md](.agents/skills/md-graph/SKILL.md) for agent-specific instructions on integrating this knowledge graph.

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
