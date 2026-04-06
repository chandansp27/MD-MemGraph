---
name: md-graph
description: Write and navigate markdown knowledge graphs. Use when creating blocks in docs/, editing markdown files, or exploring the knowledge graph structure. Blocks are separated by ---, first heading defines the node, standard markdown links create edges.
---

# Markdown Knowledge Graph

A lightweight filesystem-based knowledge graph using plain markdown blocks and standard links.

## Format Rules

- **Block separator**: `---` on its own line between blocks
- **Node definition**: First heading (`##`) in each block defines the node
- **Link syntax**: Standard markdown only: `[text](#anchor)` or `[text](./file.md#anchor)`
- **Link scope**: Links outside code fences only; fenced code blocks are ignored
- **Node IDs**: Generated as `file.md#header-slug` from heading text

## Write Markdown

Create new concepts by adding blocks to files in `docs/`:

```markdown
## Concept Name

Prose explaining the concept. Natural writing first.
Reference related concepts: [Other Concept](./file.md#other-concept)
Or link within same file: [Local Concept](#local-concept)

More explanation follows.
```

**Tips**:
- One concept per block
- Write clear, focused prose (2-5 sentences per paragraph)
- Use meaningful heading names
- Link to related concepts naturally
- Keep code examples in fenced blocks

## CLI Commands

Show all commands:
```bash
python3 src/mem_graph.py --help
```

**Common operations**:

List block headers in a file:
```bash
python3 src/mem_graph.py --root docs headers --file FILE.md --all
```

View a specific block:
```bash
python3 src/mem_graph.py --root docs view --id file.md#header-slug
python3 src/mem_graph.py --root docs view --file FILE.md --header "Header Name"
```

Show graph neighbors (connections):
```bash
python3 src/mem_graph.py --root docs graph --header "Concept" --depth 2
```

Validate links and structure:
```bash
python3 src/mem_graph.py --root docs check
```

## Link Resolution

Links resolve as follows:

1. **Same file**: `[Text](#header)` → `file.md#header`
2. **Same directory**: `[Text](./other.md#header)` → `other.md#header`
3. **Relative path**: `[Text](../folder/file.md#header)`
4. **External URLs**: `[Text](https://...)` → ignored (not graphed)

## Workflow

1. Run `check` to see current issues: `python3 src/mem_graph.py --root docs check`
2. Create new concepts as blocks in files under `docs/`
3. Use standard markdown links to connect them
4. Run `check` again to validate
5. Use `headers`, `view`, `graph` to explore

## Example

```markdown
## Attention Mechanisms

Attention allows models to focus on relevant parts of sequences.
See [Transformer Architecture](#transformer) for implementation details.
Compare to [RNN Approaches](./other.md#rnns).

---

## Transformer Architecture

Uses attention layers exclusively for sequential processing.
Built on [Attention Mechanisms](#attention-mechanisms).
```

Then validate:
```bash
python3 src/mem_graph.py --root docs check
```
