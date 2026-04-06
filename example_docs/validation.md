## Validation

The validation system checks your knowledge graph for consistency, correctness, and structural issues.

---

## Running Validation

Validate your entire graph:

```bash
python3 src/mem_graph.py --root docs check
```

Output on success:

```
Checking /path/to/docs...
✓ Graph is valid
  Files: 12
  Blocks: 247
  Links: 1,842
  All links resolved
```

Output with errors:

```
✗ Found 3 errors:

  concepts.md:25
    ERROR: Unresolved link
    [Neural Nets](./concepts.md#neural-nets)
    Reason: Header "Neural Nets" not found

  process.md:42
    ERROR: Missing file
    [Algorithm](./missing.md#algorithm)
    Reason: File not found

  math.md:8
    ERROR: Invalid link syntax
    [Text}(file.md#concept)
    Reason: Malformed markdown link
```

---

## Error Types

### Unresolved Headers

A link points to a header that doesn't exist:

```markdown
## Example

See [Concept](./file.md#concept-name)  # ✗ "Concept Name" doesn't exist
```

Fix:
1. Verify header exists: `python3 src/mem_graph.py --root docs headers --file file.md`
2. Check exact spelling and case
3. Ensure anchor matches header slug

**Common causes**:
- Typo in anchor name
- Forgot to create the concept block
- Header slug doesn't match link text

### Missing Files

A link points to a file that doesn't exist:

```markdown
## Example

See [Concept](./missing.md#concept)  # ✗ missing.md doesn't exist
```

Fix:
1. Check file exists: `ls docs/missing.md`
2. Verify relative path is correct
3. Create missing file if needed

**Common causes**:
- Filename typo
- Incorrect relative path (../ vs ./)
- File deleted but links remain

### Invalid Syntax

Link syntax is malformed:

```markdown
See [Concept}(./file.md#concept)     # ✗ Mismatched brackets
See [Concept] (./file.md#concept)    # ✗ Space before paren
See [Concept(./file.md#concept)      # ✗ Missing opening bracket
```

Fix:
1. Verify standard markdown syntax: `[text](url)`
2. Check brackets and parentheses match
3. No spaces between `]` and `(`

**Common causes**:
- Copy-paste errors
- Special characters in link text
- Manual editing mistakes

### Duplicate Node IDs

Same concept defined in multiple places:

```
ERROR: Duplicate node ID
  concepts.md#neural-networks
  theory.md#neural-networks
```

Fix:
1. Rename one concept to be more specific
2. Merge content if they're the same concept
3. Move one to a different file

**Common causes**:
- Creating concepts with identical names
- Refactoring without renaming
- Copy-paste duplication

### Circular References

Not necessarily an error, but worth noting:

```
A → B → C → A (cycle detected)
```

Cycles are allowed and sometimes meaningful:

```markdown
## Concept A

See [Concept B](#concept-b).

---

## Concept B

Relates to [Concept A](#concept-a).
```

This is fine (bidirectional relationships are normal).

---

## Validation Modes

### Basic Check

```bash
python3 src/mem_graph.py --root docs check
```

Validates:
- Link syntax correctness
- File existence
- Header existence
- Node ID uniqueness

### Strict Mode

```bash
python3 src/mem_graph.py --root docs check --strict
```

Treats warnings as errors:
- Orphaned nodes (no links in/out)
- Very long blocks (readability)
- Unused concepts

Recommended before publishing.

### File-Specific Check

```bash
python3 src/mem_graph.py --root docs check --file concepts.md
```

Validate single file:
- Links from this file only
- Headers in this file
- Local validation

---

## Interpreting Results

### Valid Graph

```
✓ Graph is valid
  Files: 12
  Blocks: 247
  Links: 1,842
```

Metrics:
- **Files**: Number of `.md` files
- **Blocks**: Total concept blocks (separated by `---`)
- **Links**: Total internal links found

### Orphaned Blocks

A block with no incoming or outgoing links:

```
⚠ Orphaned blocks (1):
  - concepts.md#disconnected-concept
```

These are valid but suggest:
- Concept not yet integrated
- Placeholder for future work
- Organizational issue

Fix by:
1. Adding links to/from the concept
2. Moving to an "Abandoned" or "Ideas" section
3. Deleting if no longer relevant

### Warnings

Non-fatal issues that should be addressed:

```
⚠ Found 2 warnings:

  - 15 orphaned blocks (not linked)
  - 1 block with unusual size (2048 chars)
```

Warnings don't break validation but indicate:
- Potential organizational issues
- Readability concerns
- Incomplete integration

---

## Fixing Common Errors

### "Unresolved link" fix workflow:

1. Identify error location: `concepts.md:25`
2. Open file and view line 25
3. Check target file and header name:
   ```bash
   python3 src/mem_graph.py --root docs headers --file target.md
   ```
4. Update link to match exact header name
5. Re-run validation: `python3 src/mem_graph.py --root docs check`

### "Missing file" fix workflow:

1. Identify error in validation output showing missing file
2. Create the file or fix the path:
   ```bash
   touch docs/new-file.md
   ```
3. Add content with the concept:
   ```bash
   echo "## Concept Name" >> docs/new-file.md
   ```
4. Re-run validation

### "Duplicate node ID" fix workflow:

1. Identify duplicates:
   ```bash
   python3 src/mem_graph.py --root docs headers --all | sort | uniq -d
   ```
2. Rename one concept to be more specific
3. Update all links to use new name
4. Re-run validation

---

## Pre-Commit Validation

Use this git hook to prevent broken graphs:

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
python3 src/mem_graph.py --root docs check
if [ $? -ne 0 ]; then
    echo "✗ Graph validation failed. Fix errors before committing."
    exit 1
fi
```

Make executable:

```bash
chmod +x .git/hooks/pre-commit
```

Now commits fail if graph is invalid.

---

## CI/CD Integration

Validate graph in continuous integration:

GitHub Actions example:

```yaml
- name: Validate knowledge graph
  run: python3 src/mem_graph.py --root docs check --strict
```

This ensures:
- No broken links in pull requests
- Consistent quality standards
- Documentation stays accurate

---

## Statistics and Metrics

Check graph health:

```bash
python3 src/mem_graph.py --root docs headers --all | wc -l
```

Count nodes:
```bash
python3 src/mem_graph.py --root docs check
```

Provides total blocks and links.

Average links per block:
```
total_links / total_blocks = avg_connectivity
```

Healthy graphs typically have:
- **avg_links**: 2-5 per block
- **orphaned**: < 5% of blocks
- **avg_block_size**: 150-400 words

---

## Troubleshooting Validation

**Validation runs slow**:
- Split large files into multiple concepts
- See [Scalability](./scalability.md#scalability)

**Too many warnings**:
- Run strict mode to understand issues
- Prioritize orphaned blocks
- Reorganize if structure is unclear

**Links valid locally but fail in CI**:
- Check relative paths work from project root
- Ensure all files committed to repo
- Verify path separators (/ vs \)

See [Troubleshooting](./troubleshooting.md#validation-errors) for more help.
