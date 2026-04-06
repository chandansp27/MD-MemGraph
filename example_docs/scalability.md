## Scalability

Performance considerations and optimization strategies for large knowledge graphs.

---

## Performance Characteristics

### Query Performance

md-graph operations scale with graph size:

**Small graphs** (< 100 concepts):
- Check: < 100ms
- Graph query: < 50ms
- Headers listing: < 20ms

**Medium graphs** (100-1000 concepts):
- Check: 100-500ms
- Graph query: 50-300ms
- Headers listing: 20-100ms

**Large graphs** (1000+ concepts):
- Check: 500ms-3s
- Graph query: 300ms-1000ms
- Headers listing: 100-500ms

See [CLI Reference](./cli-reference.md#performance-notes) for benchmarks.

### Factors Affecting Performance

1. **Number of concepts**: More nodes = longer traversal
2. **Link density**: More edges = more processing
3. **File count**: More files = more I/O
4. **Path complexity**: Deeper directories = slower path resolution
5. **Validation depth**: Strict mode checks more things

---

## Optimization Strategies

### 1. File Organization

**Avoid flat structure**:
```
✗ docs/ (100+ files)
  ├── concept-001.md
  ├── concept-002.md
  ├── concept-003.md
  └── ... lots more
```

**Use hierarchical organization**:
```
✓ docs/
  ├── domain-a/
  │   ├── concepts.md
  │   └── algorithms.md
  ├── domain-b/
  │   ├── theory.md
  │   └── applications.md
  └── domain-c/
      └── foundations.md
```

Benefits:
- Filesystem caching works better
- Conceptually clearer
- Easier to navigate
- Better for teams

### 2. File Size

**Keep files focused** (5-30 concepts per file):

Size impact:
```
✓ 15 concepts per file: Good performance
✗ 200 concepts per file: Parsing slow, searching slow
✗ 1 concept per file: Too many file operations
```

Why? Each file parsed fully even if accessing one concept.

**Benchmarks**:
- 5KB file: < 1ms parse
- 50KB file: 5-10ms parse
- 500KB file: 50-100ms parse

If file exceeds 100KB, consider splitting.

### 3. Link Density

**Moderate connectivity** (2-4 links per concept):

```
Sparse: 0.5 links/concept → Fast but hard to navigate
Optimal: 2-4 links/concept → Balance of clarity and speed
Dense: 10+ links/concept → Slow, confusing, hard to maintain
```

Why high density slows things down?
- More links to validate
- More concepts to traverse
- More potential for circular references
- Harder for humans to understand (slows review)

**Management**:
- Use `check --strict` to find over-linked areas
- Delete non-essential links
- Use taxonomy files instead of connecting everything

### 4. Path Resolution

**Use relative paths wisely**:

Fast:
```markdown
[Concept](./same-file.md#concept)          ✓ One directory
[Concept](../sibling/file.md#concept)     ✓ Parent + one level
```

Slower:
```markdown
[Concept](../../../../../../deep/path/file.md#concept)  ✗ Many levels
```

Deep traversal requires resolving each directory component.

**Minimize path depth**:
- Limit nesting to 2-3 levels
- Use meaningful directory names
- Avoid deeply nested subdirectories

### 5. Query Depth

**Limit graph traversal depth**:

```bash
Fast:    python3 src/mem_graph.py --root docs graph --depth 1
Medium:  python3 src/mem_graph.py --root docs graph --depth 2
Slow:    python3 src/mem_graph.py --root docs graph --depth 5
```

Depth search complexity: O(n^depth) where n = avg edges per node

**Recommendations**:
- Interactive queries: depth 1-2
- Analysis: depth 2-3
- Full exploration: depth 3-4 max

---

## Memory Considerations

### Large Graph Memory Usage

Graph loaded entirely into memory:

```
1000 concepts with 3000 links:
- Graph data: ~500KB
- Caches: ~200KB
- Total: ~1MB
```

Even very large graphs stay small. Modern systems handle 10M+ links easily.

### File System Limits

Practical limits per directory:

- **100 files per directory**: Safe
- **500 files per directory**: Getting slow on some filesystems
- **1000+ files per directory**: Performance degrades

**Solution**: Use subdirectories
```
✗ docs/ (500+ files)
✓ docs/a/, docs/b/, docs/c/ (50-100 files each)
```

---

## Validation Performance

### Full Graph Check

```bash
python3 src/mem_graph.py --root docs check
```

Time breakdown for 1000 concepts:
- Parse all files: 60%
- Validate links: 30%
- Report results: 10%

Bottleneck: Parsing markdown files

### Incremental Validation

Check single file:
```bash
python3 src/mem_graph.py --root docs check --file one-file.md
```

Much faster (only validates one file).

### Strict Mode Overhead

```bash
python3 src/mem_graph.py --root docs check
# Fast: just validates structure

python3 src/mem_graph.py --root docs check --strict
# Slower: checks for orphans, quality metrics
```

Strict mode adds 20-50% overhead.

---

## Scaling Strategies

### Small to Medium (< 1000 concepts)

Simple flat organization works:

```
docs/
├── fundamentals.md
├── intermediate.md
├── advanced.md
└── references.md
```

Validation: 100-500ms (acceptable)

### Medium to Large (1000-10000 concepts)

Add directory structure:

```
docs/
├── domain-a/
├── domain-b/
├── domain-c/
└── domain-d/
```

Validation: 500ms-2s (monitor)

### Very Large (10000+ concepts)

Use multiple roots:

```
docs/
├── knowledge-a/        # Separate graph
├── knowledge-b/        # Separate graph
└── index.md           # Master index linking them
```

Run separate validation per graph.

Or split into sub-projects:
```
project-a/docs/
project-b/docs/
project-c/docs/
```

Each validated independently.

---

## CI/CD Optimization

### GitHub Actions Example

**Basic (every change)**:
```yaml
- name: Validate
  run: python3 src/mem_graph.py --root docs check
  timeout-minutes: 1
```

**For large graphs**:
```yaml
- name: Validate  
  run: python3 src/mem_graph.py --root docs check
  timeout-minutes: 5

- name: Cache validation
  uses: actions/cache@v2
  with:
    path: docs/.cache
    key: graph-${{ hashFiles('docs/**') }}
```

### Pre-commit Hook Optimization

**Validate only changed files**:
```bash
#!/bin/bash
changed_files=$(git diff --cached --name-only --diff-filter=AM *.md)
for file in $changed_files; do
    python3 src/mem_graph.py --root docs check --file "$file"
    if [ $? -ne 0 ]; then exit 1; fi
done
```

Much faster than validating entire graph.

---

## Monitoring and Metrics

### Collect Performance Data

```bash
#!/bin/bash
time python3 src/mem_graph.py --root docs check > /dev/null
```

Output: real time shows actual performance

### Track Graph Growth

```bash
python3 src/mem_graph.py --root docs headers --all | wc -l
```

Track over time:
```
Week 1: 100 concepts
Week 4: 150 concepts
Month 2: 200 concepts
...
```

When performance degrades (should correlate with growth), time to optimize.

### Identify Hotspots

```bash
# Find most-linked-to concepts
python3 src/mem_graph.py --root docs headers --all | while read concept; do
    python3 src/mem_graph.py --root docs graph --header "$concept" 2>/dev/null | grep -o "IN.*" | wc -l
done | sort -rn
```

High-density hub concepts might need splitting.

---

## Refactoring for Performance

### Scenario: Performance Degradation

Graph was fast, now slow. What happened?

1. **Check growth**:
   ```bash
   python3 src/mem_graph.py --root docs headers --all | wc -l
   ```
   
   If doubled: Normal, expected slowdown

2. **Check file sizes**:
   ```bash
   ls -lah docs/*.md | awk '{print $5, $NF}'
   ```
   
   Any file > 100KB? Split it

3. **Check link density**:
   ```bash
   grep -r "\[" docs/ --include="*.md" | wc -l
   ```
   
   Relative to concept count, is it higher than before?

4. **Optimize most impactful first**:
   - Fix over-large files (biggest impact)
   - Reduce high-density hubs (moderate impact)
   - Reorganize directory structure (small impact)

### Example Refactoring

Before (slow):
```
docs/concepts.md (800 concepts, 5KB)
```

After (fast):
```
docs/
  ├── fundamentals/
  │   ├── ml.md (150 concepts)
  │   ├── statistics.md (100 concepts)
  │   └── math.md (200 concepts)
  ├── algorithms/
  │   ├── supervised.md (150 concepts)
  │   └── unsupervised.md (200 concepts)
```

Result:
- Check time: 2s → 300ms
- Easier to navigate
- Better for team collaboration

---

## Benchmarking

### Standard Graph

Create test graph:

```bash
# Generate test markdown
python3 -c "
for i in range(100):
    print(f'## Concept {i}')
    print(f'Description {i}.')
    print('---')
    print()
" > docs/test.md
```

Run benchmarks:

```bash
time python3 src/mem_graph.py --root docs headers --all > /dev/null
time python3 src/mem_graph.py --root docs graph --header "Concept 50" --depth 2 > /dev/null
time python3 src/mem_graph.py --root docs check > /dev/null
```

Compare results:
- Before optimization
- After optimization
- Baseline (expected)

---

## When to Optimize

**Don't optimize if**:
- Validation completes in < 1s
- Interactive queries are responsive
- No team performance complaints

**Do optimize if**:
- Validation takes > 5s
- Queries are sluggish
- CI/CD timing out
- Team reports slowness

See [Knowledge Design](./knowledge-design.md#scalability-considerations) for structural optimization principles.
