## Links

Link syntax and resolution is the core of md-graph. This document explains how links work and how they're resolved.

---

## Link Syntax

md-graph uses standard markdown link syntax with optional anchors:

### Basic link format:

```markdown
[Display Text](target)
```

Where `target` is one of:
- `#anchor`: Same file
- `./file.md#anchor`: Relative file and anchor
- `../parent/file.md#anchor`: Relative with directory traversal
- `https://...`: External URL (not graphed)

---

## Within-File Links

Link to another concept in the same file:

```markdown
## Concept A

Text mentioning [Concept B](#concept-b).

---

## Concept B

Referenced from [Concept A](#concept-a).
```

Resolution:
- `[text](#anchor)` links to the header in the same file
- Anchor is generated from header (slug form)
- Header must exist in same file

---

## Cross-File Links

Link to concepts in other files:

```markdown
## ML Theory

See [Neural Networks](./networks.md#neural-networks).
Also compare [Deep Learning](./learning.md#deep-learning).
```

Resolution from the current file's directory:
- `[text](./networks.md#anchor)` links to a concept in `networks.md` (same directory)
- `[text](./learning.md#anchor)` links to a concept in `learning.md` (same directory)

Files are resolved relative to the current file's location.

---

## Relative Paths

Navigate directory hierarchy:

```markdown
## Module A

Parent concept: [Core](../core.md#concept)
Sibling doc: [Related](./related.md#concept)
Nested child: [Detailed](./details/example.md#concept)
```

Path rules:
- `./file.md`: Current directory
- `../file.md`: Parent directory  
- `../../file.md`: Grandparent directory
- `./subfolder/file.md`: Subdirectory
- `../other-folder/file.md`: Sibling directory

Example structure:

```
docs/
├── core.md                    # In root
├── ml/
│   ├── concepts.md            # In ml/
│   └── advanced/
│       └── details.md         # In ml/advanced/
```

From `ml/concepts.md`:
- Link to `core.md`: `[link](../core.md#anchor)`
- Link to `details.md`: `[link](./advanced/details.md#anchor)`

---

## External URLs

External links are recognized but not validated or graphed:

```markdown
See [Wikipedia](https://en.wikipedia.org/wiki/Neural_network)
See [Paper](https://arxiv.org/abs/1706.03762)
```

External links:
- Not checked during validation
- Not included in graph structure
- Pass through as-is
- Don't count as graph edges

Use external links for:
- References and citations
- Off-site resources
- Third-party documentation

---

## Anchor Generation

Headers are converted to URL-safe anchors (slugs):

| Header | Anchor |
|--------|--------|
| `## Concept` | `concept` |
| `## My Concept` | `my-concept` |
| `## Concept-Name` | `concept-name` |
| `## C++ Programming` | `c-programming` |
| `## REST API v2.0` | `rest-api-v20` |
| `## (Advanced) Techniques` | `advanced-techniques` |

Rules:
- Convert to lowercase
- Replace spaces with hyphens
- Remove/convert special characters
- Keep alphanumerics and hyphens only
- Remove leading/trailing hyphens

---

## Link Detection

Links are detected using regex pattern matching:

```regex
\[([^\]]+)\]\(([^\)]+)\)
```

This matches standard markdown: `[text](url)`

### Outside code fences

Links are only parsed in regular markdown content:

```markdown
## Example

Real link: [Valid](./file.md#valid)

\`\`\`
Ignored: [Fake](./file.md#fake)
[[Bracket syntax | ignored]]
\`\`\`

Real link: [Also Valid](./file.md#also-valid)
```

### Code fence markers:

Recognized as code fences:
- ` ``` ` with optional language: ` ```python `
- ` ~~~ ` with optional language: ` ~~~yaml `

Content between matching fences is ignored.

### Partial or broken fences

If fences don't match (unclosed), link detection continues:

```markdown
\`\`\`
Broken fence start

[This is parsed] (./file.md#concept)
```

Recommendation: Use complete, matched fences.

---

## Valid Link Examples

These links resolve correctly:

```markdown
## Concept Page

Paragraph one: [Related](./related.md#related).

Paragraph two: [Local](#local-concept).

Inline mention: [Theory](../theory/principles.md#principles).

With punctuation: See [this concept](./file.md#concept).

Multiple per line: [Link A](#a) and [Link B](#b).

---

## Local Concept

This is a local concept linked from above.
```

---

## Invalid Link Examples

These links will cause validation errors:

```markdown
## Example

Missing anchor: [Concept](./file.md)           # ✗ No anchor
Missing file: [Concept](#missing-header)      # ✗ Header doesn't exist
Bad syntax: [Concept] (./file.md#concept)     # ✗ Space before paren
Broken: [Concept](./file.md#missing)          # ✗ Header not found

In code (ignored): [Fake](./file.md#fake)
\`\`\`
\`\`\`
```

---

## Resolution Algorithm

When resolving a link from `current.md`:

1. Parse link: `[text](target)`
2. Extract components:
   - `target = path#anchor` (if `#` present)
   - `path = ./relative/path.md` or `#anchor-only`
3. If anchor-only (`#anchor`):
   - Search in `current.md`
4. If path provided:
   - Resolve path relative to current file directory
   - Validate file exists
   - Search for anchor in target file
5. Return node ID: `resolved-path.md#anchor`

Example:

```
File: docs/ml/concepts.md
Link: [Backprop](../../core/algorithms.md#backprop)

Resolution:
  1. Current: ml/concepts.md
  2. Go up 2 levels: docs/
  3. Enter core/: core/algorithms.md
  4. Search anchor: #backprop
  5. Result: core/algorithms.md#backprop
```

---

## Best Practices

**Use clear link text**:
```markdown
✓ [Neural Networks](./file.md#neural-networks)
✗ [click here](./file.md#neural-networks)
```

**Link to specific anchors**:
```markdown
✓ [Backpropagation](./file.md#backpropagation)
✗ [See](./file.md)
```

**Prefer relative paths**:
```markdown
✓ [Concept](./other.md#concept)
✗ [Concept](/Users/name/docs/other.md#concept)
```

**Keep link text descriptive**:
```markdown
✓ Related: [Attention Mechanisms](./file.md#attention)
✗ [click](./file.md#attention)
```

See [Best Practices](./best-practices.md#linking-practices) for more guidance.

---

## Troubleshooting

**Link appears but doesn't resolve**:
- Check anchor exists: `python3 src/mem_graph.py --root docs headers --file target.md`
- Verify spelling and case
- Ensure file path is correct

**Link in code is being parsed**:
- Use complete code fence: ` ``` ` before and after
- Ensure no spaces or characters between ` ``` ` and fence boundary

**Relative path doesn't work**:
- Run from project root: `python3 src/mem_graph.py --root docs check`
- Verify file structure matches path

See [Troubleshooting](./troubleshooting.md#broken-links) for more help.
