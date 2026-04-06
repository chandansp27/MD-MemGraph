## Format

The md-graph format is a lightweight extension of markdown with specific rules for blocks, headers, and links. Understanding these rules ensures your knowledge graph works correctly.

---

## Block Separation

Blocks are separated by three hyphens (`---`) on their own line. Each block represents one atomic concept:

```markdown
## Concept A

Content for concept A.

---

## Concept B

Content for concept B.
```

Rules:
- `---` must be on its own line (no surrounding text)
- At least one space before and after (blank lines recommended)
- Blocks can be short (2-3 sentences) or longer (several paragraphs)

See [Atomicity](./knowledge-design.md#atomicity) for principles on block size.

---

## Node Definition

The first heading (`##`) in each block defines the node ID. This becomes the anchor for linking:

```markdown
## My Concept Name

Content follows...
```

Node ID generation:
- Heading text: "My Concept Name"
- Converted to slug: `my-concept-name`
- Full node ID: `file.md#my-concept-name`

Rules:
- Must use `##` (level 2 heading), not `#` or `###`
- First heading in block only (other headings ignored)
- Use clear, descriptive names (2-5 words ideal)
- Avoid special characters; use hyphens instead

---

## Markdown Content

Between the header and the next block separator, write natural markdown:

- Paragraphs and lists: Standard markdown
- Code fences: Triple backticks with language tag
- Emphasis: `**bold**` and `*italic*`
- Tables: Standard markdown tables

Example:

```markdown
## Example Concept

Main paragraph explaining the concept clearly.

### Sub-heading (ignored for node ID)

Additional details:
1. First point
2. Second point

**Important**: Fenced code blocks below are ignored.

\`\`\`python
def ignored():
    # [[Fake Links | in code are ignored]]
    return "code fences are transparent"
\`\`\`
```

---

## Link Syntax

Use standard markdown link syntax. Links are only recognized outside code fences:

### Same-file links

```markdown
See [Concept Name](#concept-name)
```

Resolves to the same file with the given anchor.

### Cross-file links

```markdown
See [Concept Name](./other.md#concept-name)
```

Resolves to `other.md` in the same directory with the given anchor.

### Relative paths

```markdown
See [Concept](../subfolder/file.md#concept)
See [Concept](../../concepts/file.md#concept)
```

### External URLs

```markdown
See [External Site](https://example.com)
```

External URLs are not graphed (no validation or querying).

---

## Link Resolution Rules

The system resolves links as follows:

1. **Anchor-only**: `[text](#anchor)` → same file
2. **File path**: `[text](./file.md#anchor)` → resolve relative to current directory
3. **Directory traversal**: `[text](../file.md#anchor)` → parent directory
4. **Absolute to docs root**: Files are always resolved relative to `--root docs/`

See [Links](./links.md#links) for complete resolution specification.

---

## Code Fences

Content inside fenced code blocks is completely ignored:

```markdown
## Example

Real link: [Valid](./file.md#valid)

\`\`\`
Fake links are ignored: [Fake](./file.md#fake)
[[Bracket syntax | also ignored]]
\`\`\`

Real link again: [Also Valid](./file.md#also-valid)
```

- Fenced blocks: ` ``` ` or `~~~`
- Must have complete open/close
- Partial or malformed fences don't disable link detection

---

## Comment Syntax

HTML comments are treated as regular content (links inside are parsed):

```markdown
<!-- This link is parsed: [Concept](./file.md#concept) -->
```

Use code fences if you want to hide links from the graph entirely.

---

## File Organization

Files live in the docs directory specified by `--root`. Structure example:

```
docs/
├── concepts.md          # Core terminology
├── process.md           # Procedural knowledge
├── math.md              # Mathematical foundations
└── workflows/
    ├── research.md      # Research workflow
    └── training.md      # Training workflow
```

Nested directories are supported:

```markdown
[Concept](../concepts.md#concept)
[Workflow](./workflows/research.md#workflow)
```

---

## Header Naming Conventions

Best practices for header names (node IDs):

- **Use nouns**: "Backpropagation" not "How to compute gradients"
- **Be specific**: "Attention Mechanism" not "Attention"
- **Avoid articles**: "Neural Network" not "The Neural Network"
- **Singular preferred**: "Concept" not "Concepts"
- **Clear scope**: "Training Data Validation" not "Validation"

These conventions make nodes easier to reference and understand.

---

## Special Cases

**Empty blocks** (header only):
```markdown
## Placeholder

---
```

Valid but empty. Use for stubs or forward references.

**Blocks with only code**:
```markdown
## Algorithm

\`\`\`python
def algorithm():
    pass
\`\`\`

---
```

Valid. Descriptive paragraphs before code recommended.

**Headers with symbols**:
```markdown
## C++ Standard Library
## OAuth 2.0
## SQL/NoSQL
```

Symbols are preserved in display but converted to URL-safe slugs in node IDs:
- "C++ Standard Library" → `c-standard-library`
- "OAuth 2.0" → `oauth-20`

See [Best Practices](./best-practices.md#naming-conventions) for detailed naming guidance.
