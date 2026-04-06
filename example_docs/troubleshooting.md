## Troubleshooting

Common issues and their solutions.

---

## Validation Errors

### "Unresolved link" Error

Error message:
```
ERROR: Unresolved link
  concepts.md:25
  [Neural Nets](./concepts.md#neural-nets)
  Header not found: "neural-nets"
```

Causes and fixes:

**Typo in anchor name**:
```
✗ [Neural Nets](./concepts.md#neural-nets)
✓ [Neural Nets](./concepts.md#neural-networks)
```
Check exact spelling of target header.

**Header doesn't exist**:
```bash
# List all headers in file
python3 src/mem_graph.py --root docs headers --file concepts.md
```

Verify target header exists in output.

**Case sensitivity**:
```markdown
Header: ## Neural Networks
Link: [Link](#neural-network)  ✗ Wrong singular

Fix: [Link](#neural-networks)  ✓
```

Slugs preserve capitalization (becomes lowercase).

---

### "Missing file" Error

Error message:
```
ERROR: Missing file
  process.md:42
  [Algorithm](./missing.md#algorithm)
  File not found: ./missing.md
```

Causes and fixes:

**File doesn't exist**:
```bash
# Check file
ls docs/missing.md
```

If missing, create it:
```bash
touch docs/missing.md
```

**Wrong path**:
```
Current file: docs/ml/concepts.md
Link: [Concept](./file.md#concept)     ✗ Looks in ml/file.md
Fix: [Concept](../file.md#concept)     ✓ Looks in docs/file.md
```

Relative paths are relative to current file's directory.

**Committed but not pulled**:
```bash
# In version control, file not yet synced
git pull
python3 src/mem_graph.py --root docs check
```

Update repository before validation.

---

### "Invalid syntax" Error

Error message:
```
ERROR: Invalid link syntax
  math.md:8
  [Text}(file.md#concept)
  Malformed markdown link
```

Causes and fixes:

**Mismatched brackets**:
```
✗ [Text}(file.md#concept)     Closing } instead of ]
✓ [Text](file.md#concept)     Correct brackets
```

**Space before parenthesis**:
```
✗ [Text] (file.md#concept)    Space breaks syntax
✓ [Text](file.md#concept)     No space
```

**Missing components**:
```
✗ [Text
✗ (file.md#concept)
✓ [Text](file.md#concept)     Both brackets and parens
```

---

### "Duplicate node ID" Error

Error message:
```
ERROR: Duplicate node ID
  concepts.md#neural-networks
  networks.md#neural-networks
```

Causes and fixes:

**Same concept in two files**:
```bash
# Rename in one file
# Option 1: More specific name
## Neural Networks (Fundamentals)

# Option 2: Move to one file
# Delete one, update links
```

**Forward reference before creation**:
```markdown
## Concept A

Uses [Concept B](#concept-b).

---

## Concept B

(This concept must exist)
```

Create all referenced concepts.

---

## Link Resolution Issues

### Links work locally but fail in CI/CD

**Platform differences** (Windows vs Unix):
```
Windows: docs\file.md#anchor
Unix:    docs/file.md#anchor

Always use forward slash (/) in links
```

**Path differences in CI**:
```bash
# CI runs from root
python3 src/mem_graph.py --root docs check

# But you ran from docs/
cd docs
python3 ../src/mem_graph.py --root . check  ✗

# Always use absolute paths or run from project root
```

**Files not committed**:
```bash
# Forgot to git add new file
git add docs/new-file.md
git commit -m "Add new documentation"
```

Validation fails if files aren't in repository.

---

### Relative path confusion

**Current file location matters**:

```
File structure:
docs/
  ├── concepts.md
  └── ml/
      ├── networks.md
      └── algorithms.md

From docs/concepts.md:
  [link](./ml/networks.md#header)    ✓ Goes to ml/networks.md

From docs/ml/networks.md:
  [link](./algorithms.md#header)     ✓ Goes to ml/algorithms.md
  [link](../concepts.md#header)      ✓ Goes to docs/concepts.md
```

Always relative to the file containing the link.

**Fix relative paths**:

```bash
# Find what directory a file is in
find docs -name "networks.md"
# docs/ml/networks.md

# From concepts.md to networks.md:
#   concepts.md is in docs/
#   networks.md is in docs/ml/
#   Relative path: ./ml/networks.md
```

---

### Links in code blocks being parsed

Error: Validation finds fake links inside code:

```markdown
\`\`\`python
# This link is in code
data = fetch_from([API](./api.md#fetch))
\`\`\`

ERROR: Header not found: fetch
```

**Fix**: Ensure code fence is complete:

```markdown
\`\`\`python
# This link is NOT parsed if fence is valid
data = fetch_from([API](./api.md#fetch))
\`\`\`
```

Code fence rules:
- Opening ` ``` ` must match closing ` ``` `
- Language specifier optional: ` ```python `
- No text after closing fence on same line

---

## Broken Links

### Finding Broken Links

```bash
# Validation will find them
python3 src/mem_graph.py --root docs check

# Or manually search
grep -r "\[" docs --include="*.md" | grep -o "\[.*\](.*)" | sort -u
```

### Fixing Broken Links Systematically

1. Get error list:
   ```bash
   python3 src/mem_graph.py --root docs check > errors.txt
   ```

2. For each error:
   ```bash
   # Check if header exists
   python3 src/mem_graph.py --root docs headers --file target.md | grep "exact-header"
   
   # If not found, either:
   # - Create the header
   # - Update the link to existing header
   # - Delete the link if no longer relevant
   ```

3. Re-validate:
   ```bash
   python3 src/mem_graph.py --root docs check
   ```

### Batch Fix Pattern

Script to find and list all issues:

```bash
#!/bin/bash
python3 src/mem_graph.py --root docs check | grep "ERROR:" | \
  sed 's/.*\[\(.*\)\](\(.*\)).*/Link: [\1](\2)/' | \
  sort -u
```

---

## Performance Issues

### Validation Takes Too Long

**Symptom**: `check` command takes > 5 seconds

**Causes**:
- Too many concepts (1000+)
- Large files (100KB+)
- Deep directory nesting
- Many links to traverse

**Solutions**:

1. Check file sizes:
   ```bash
   ls -lh docs/**/*.md | sort -k5 -hr | head
   ```
   
   Files > 100KB: split them

2. Check link count:
   ```bash
   grep -r "\[.*\](" docs --include="*.md" | wc -l
   ```
   
   If very high: remove non-essential links

3. Simplify structure:
   ```bash
   # Before: deeply nested
   docs/domain/sub/detail/file.md
   
   # After: flatter
   docs/domain/file.md
   ```

4. Use file-specific check:
   ```bash
   python3 src/mem_graph.py --root docs check --file target.md
   ```
   
   Only validate one file if testing specific changes.

---

### Queries Are Slow

**Symptom**: `graph` command takes > 2 seconds

**Causes**:
- Large graph (10,000+ concepts)
- High link density
- Deep traversal depth

**Solutions**:

1. Reduce depth:
   ```bash
   ✓ --depth 2
   ✗ --depth 10
   ```

2. Query specific nodes instead of traversing far

3. Cache results locally:
   ```python
   # Python wrapper caches results
   ```

See [Scalability](./scalability.md#performance-characteristics) for optimization strategies.

---

## Organization Issues

### Orphaned Concepts

**Problem**: Concept not linked from anywhere

```bash
python3 src/mem_graph.py --root docs check --strict
```

Output:
```
⚠ Orphaned blocks (5):
  - concepts.md#disconnected
  - ideas.md#future-work
```

**Solutions**:

1. **Add links to it**:
   ```markdown
   ## Related Concepts
   
   See also: [Orphaned Concept](./file.md#orphaned)
   ```

2. **Create "Abandoned" section** if intentionally unused:
   ```markdown
   ## Abandoned Ideas
   
   Previously considered: [Concept](./file.md#concept)
   ```

3. **Delete** if no longer relevant:
   ```bash
   git rm docs/file.md
   git commit -m "Remove obsolete concept"
   ```

---

### Disconnected Components

**Problem**: Some concepts form isolated cluster

```
Cluster A: Concept 1 ↔ Concept 2 ↔ Concept 3
Cluster B: Concept 4 ↔ Concept 5
Isolated: Concept 6
```

**Find disconnected components**:

```bash
# No automatic tool, but check for isolated files:
ls docs/ | while read file; do
  grep -c "\[.*\](.*file.md#" docs/*.md || echo "$file: no links"
done
```

**Connect them**:

```markdown
## Bridge Concept

Connects [Cluster A](./file-a.md#concept-1) to [Cluster B](./file-b.md#concept-4)
```

---

### Unclear Structure

**Problem**: Hard to understand document organization

**Fix**: Create navigation file:

```markdown
## Navigation

### Fundamentals
- [Basic Concepts](./fundamentals.md#concepts)
- [Mathematics](./fundamentals.md#mathematics)

### Advanced
- [Algorithms](./advanced.md#algorithms)
- [Optimization](./advanced.md#optimization)
```

Place at `docs/README.md` or `docs/index.md`.

---

## Header Parsing Issues

### "Invalid header name" Error

Most headers work fine, but special cases:

**Symbols in headers**:
```markdown
## C++ Programming      ✓ Accepted
## OAuth 2.0           ✓ Accepted
## (Advanced) Concepts ✓ Accepted
```

All convert to URL-safe slugs automatically.

**Headers that might cause issues**:
```markdown
## [Square Brackets]   # Ambiguous - avoid
## (Only Parens)      # Works but odd
## No content         # Valid but empty, unusual
```

---

### Duplicate Headers in Same File

**Error**:
```
ERROR: Duplicate header
  concepts.md#concept
  Appears twice in same file
```

**Fix**: Headers must be unique within a file (but can repeat across files):

```markdown
✗ File: concepts.md
## Topic
...
---
## Topic              (Duplicate!)

✓ File A: concepts.md
## Topic
...

File B: other.md
## Topic              (OK, different file)
```

---

## Git and Version Control Issues

### "Links break after rebase"

**Problem**: Moved file, links now broken

**Example**:
```bash
# Before: docs/ml/concepts.md
# After: docs/concepts.md (moved up one level)

# Links in other files still point to old path:
[Concept](./ml/concepts.md#concept)  ✗
```

**Solution**: Update all links after moving file:

```bash
# Find all references to old path
grep -r "ml/concepts.md" docs/

# Update them:
sed -i 's|ml/concepts\.md|concepts.md|g' docs/*.md

# Validate
python3 src/mem_graph.py --root docs check
```

### "Merge conflicts in documentation"

**Problem**: Both branches modified same document

```markdown
<<<<<<< HEAD
## Concept A

Definition from main branch.
=======
## Concept A  

Definition from feature branch.
>>>>>>> feature-branch
```

**Solution**:

1. Look at both versions
2. Decide which is correct (or merge manually)
3. Remove conflict markers
4. Validate: `python3 src/mem_graph.py --root docs check`

---

## Recovery Procedures

### Backup and Restore

**Create backup**:
```bash
cp -r docs docs.backup.$(date +%Y%m%d)
```

**Restore from backup**:
```bash
rm -rf docs
cp -r docs.backup.20240206 docs
```

### Recover from Accidental Delete

```bash
# Check git history
git log --oneline -- docs/deleted-file.md

# Restore from commit
git checkout COMMIT_HASH -- docs/deleted-file.md
```

### Rebuild Broken Graph

If structure is corrupted:

```bash
# Start fresh, keep content
mkdir docs.new
# Manually reorganize concepts
# Then validate
python3 src/mem_graph.py --root docs.new check
```

---

## Getting Help

### Run Comprehensive Diagnostics

```bash
#!/bin/bash
echo "=== File count ==="
find docs -name "*.md" | wc -l

echo "=== Concept count ==="
python3 src/mem_graph.py --root docs headers --all | wc -l

echo "=== Link count ==="
grep -r "\[.*\](" docs --include="*.md" | wc -l

echo "=== Largest files ==="
ls -lhS docs/**/*.md | head -5

echo "=== Validation ==="
python3 src/mem_graph.py --root docs check

echo "=== Performance ==="
time python3 src/mem_graph.py --root docs check > /dev/null
```

### Common Questions

**Q: How do I list all concepts?**
```bash
python3 src/mem_graph.py --root docs headers --all
```

**Q: How do I view a specific concept?**
```bash
python3 src/mem_graph.py --root docs view --file file.md --header "Concept Name"
```

**Q: How do I find what links to a concept?**
```bash
python3 src/mem_graph.py --root docs graph --header "Concept" | grep "IN"
```

**Q: How do I verify all links are valid?**
```bash
python3 src/mem_graph.py --root docs check
```

See [CLI Reference](./cli-reference.md#cli-reference) for full command documentation.

---

## Reporting Issues

For bugs or unexpected behavior:

1. **Run validation**: `python3 src/mem_graph.py --root docs check`
2. **Note error message** and line number
3. **Try simple reproduction**: Create minimal test case
4. **Check existing issues**: Might already be documented
5. **Report with context**: File, command, error message

Check the project repository for issue tracking and contribution guidelines.
