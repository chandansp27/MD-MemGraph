---
name: markdown-memory-graph
description: "Use when the agent needs lightweight memory across tasks: recall prior notes, preserve important facts or decisions, record semantic connections, add atomic markdown memory blocks, or link related concepts so future agents can navigate them more efficiently. Use this as a continual memory for the user, project and knowledge base."
---

# Markdown Memory and Knowledge Graph

Use this skill when a markdown corpus can help the current task: prior decisions, implementation notes, research findings, project conventions, related files, or reusable context. The goal is fast recall and navigation while the main work continues.

## Format Rules

- **Block separator**: `---` on its own line between blocks
- **Node definition**: First heading (`##`) in each block defines the node
- **Link syntax**: Standard markdown only: `[text](#anchor)` or `[text](./file.md#anchor)`
- **Link scope**: Links outside code fences only; fenced code blocks are ignored
- **Node IDs**: Generated as `file.md#header-slug` from heading text

## Retrieval Loop

Start with normal file and text tools. Use the graph CLI when you have a candidate node and want its full block, outgoing links, or backlinks.

```bash
# Find likely files or nodes.
rg "topic|symbol|error" docs/
grep -REIn "topic|symbol|error" docs/
find docs -type f -name '*.md'

# Inspect headings, nearby lines, or a whole candidate file.
rg '^## ' docs/
grep -RIn '^## ' docs/
sed -n '1,160p' docs/file.md
nl -ba docs/file.md | sed -n '40,120p'

# Once a candidate node is known, use node-aware views.
python3 src/mem_graph.py --root docs view --id file.md#node
python3 src/mem_graph.py --root docs graph --id file.md#node --depth 1
```

Use `rg` when available because it is fast; `grep`, `find`, `sed`, `nl`, `awk`, and short Python scripts are all fine when they fit the job. Prefer `graph --depth 1-2` for quick context; go deeper only when the next hop is clearly relevant.

## Write Markdown

Create new concepts by adding atomic blocks to files in your graph root:

```markdown
## Concept Name

Natural prose explaining one reusable idea.
Reference related concepts with standard links: [Other Concept](./file.md#other-concept).
Link within the same file when appropriate: [Local Concept](#local-concept).

---

## Another Concept

Start the next node after a `---` separator.
```

Good blocks are small enough to retrieve whole and specific enough to be useful later.

**Atomic block rules**:

- One reusable idea, decision, workflow, or constraint per block
- Use concrete headings: `Token Refresh Flow`, not `Notes`
- Keep the block low-to-mid token length: enough detail to be useful, not a transcript or essay
- Link to nearby concepts instead of duplicating their full explanation
- Add or update memory only when it is likely to help future work
- Keep code examples in fenced blocks

## Atomic Block Examples

Example: implementation memory plus a related design memory.

```markdown
## Token Refresh Flow

Access tokens expire quickly, so API callers should refresh through the auth client instead of retrying raw requests. The refresh path updates the stored session before the original operation is attempted again.

Related: [Session Storage](./auth.md#session-storage), [API Retry Policy](./api.md#api-retry-policy).

---

## Retrieval Before Traversal

Start with lexical search when the target is unknown, then open the best matching node and inspect direct neighbors. This keeps context small while still using the graph structure when the first result exposes useful adjacent concepts.

Related: [Attention Budget](./agents.md#attention-budget), [Backlinks](./links.md#backlinks).
```

## CLI Commands

Set your graph root first. In this repo, use `example_docs/`; in other projects, use the dedicated folder for the corpus.

Show all commands:

```bash
python3 src/mem_graph.py --help
```

**Common operations**:

List block headers in a file:

```bash
python3 src/mem_graph.py --root example_docs headers --file FILE.md --all
```

View a specific block:

```bash
python3 src/mem_graph.py --root example_docs view --id file.md#header-slug
python3 src/mem_graph.py --root example_docs view --file FILE.md --header "Header Name"
```

Show graph neighbors (connections):

```bash
python3 src/mem_graph.py --root example_docs graph --header "Concept" --depth 1
```

Validate links and structure:

```bash
python3 src/mem_graph.py --root example_docs check
```

Use `check` after editing graph links, when a link fails to resolve, or before relying on a changed corpus. It does not need to run before every read-only lookup.

## Complementary Bash Traversal

The graph CLI is best for node-aware navigation; shell tools are best for fast ad-hoc exploration.

List all nodes quickly:

```bash
rg '^## ' example_docs/
grep -RIn '^## ' example_docs/
```

Find all markdown links:

```bash
rg -o '\]\([^)]*\.md#[^)]*\)' example_docs/
grep -Roh '\]\([^)]*\.md#[^)]*\)' example_docs/
```

Find files mentioning a topic:

```bash
rg -l 'attention' example_docs/
grep -Ril 'attention' example_docs/
find example_docs -name '*.md'
```

Use `awk`, `sed`, `nl`, `sort`, `uniq`, or a short Python script for filtering and reshaping results when that is faster than adding a CLI feature.

## Link Resolution

Links resolve as follows:

1. **Same file**: `[Text](#header)` → `file.md#header`
2. **Same directory**: `[Text](./other.md#header)` → `other.md#header`
3. **Relative path**: `[Text](../folder/file.md#header)`
4. **External URLs**: `[Text](https://...)` → ignored (not graphed)

## Workflow

1. Search with shell tools for candidate terms, files, or headings
2. Use `view` to read the most relevant block once you know its ID or file/header
3. Use `graph --depth 1` to inspect direct outgoing links and backlinks
4. Add or update an atomic block only when the new context is reusable
5. Run `check` after link edits or when validation matters
