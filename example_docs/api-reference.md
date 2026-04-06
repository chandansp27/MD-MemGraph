## API Reference

Technical documentation for md-graph internals and programmatic access.

---

## Python Module

### mem_graph Module

The core module providing all graph functionality.

```bash
python3 src/mem_graph.py --help
```

### Core Classes

#### Graph

Main class representing a knowledge graph.

```python
from mem_graph import Graph

graph = Graph(root="docs")
```

**Methods**:

- `headers(file=None)` → List[str]
  List all headers, optionally filtered by file
  
- `view(file, header)` → Dict
  Get a single concept's content and links
  
- `graph(header, depth=1)` → Dict
  Get concept with neighbors at specified depth
  
- `check(file=None, strict=False)` → Tuple[bool, List[Error]]
  Validate graph structure

### Node Structure

Node IDs are formatted as: `file.md#header-slug`

Python representation:
```python
{
    "id": "file.md#concept",
    "file": "file.md",
    "header": "Concept Name",
    "slug": "concept-name",
    "content": "Concept description...",
    "outgoing": ["file.md#related-1", "file.md#related-2"],
    "incoming": ["other.md#concept"],
}
```

### Graph Structure

The graph object contains:

```python
{
    "nodes": {
        "file.md#concept": {...},
        ...
    },
    "edges": {
        ("file.md#a", "file.md#b"): {...},
        ...
    }
}
```

---

## CLI Interface

### Command Structure

```
python3 src/mem_graph.py --root [ROOT] [COMMAND] [OPTIONS]
```

Where:
- `--root`: Path to docs directory (required)
- `COMMAND`: Operation to perform
- `OPTIONS`: Command-specific flags

### Headers Command

```bash
python3 src/mem_graph.py --root docs headers [OPTIONS]
```

Options:
- `--file FILE`: List headers in specific file
- `--all`: List headers in all files

Output format: `file.md#header-slug`

### View Command

```bash
python3 src/mem_graph.py --root docs view [OPTIONS]
```

Options:
- `--file FILE`: Source file (with `--header`)
- `--header NAME`: Header name (with `--file`)
- `--id NODE_ID`: Alternative to file+header

Output:
```
NODE: file.md#concept-name
TITLE: Concept Name
CONTENT: [full block text]
LINKS:
  OUT: file.md#related-1
  OUT: file.md#related-2
  IN: other.md#concept
```

### Graph Command

```bash
python3 src/mem_graph.py --root docs graph [OPTIONS]
```

Options:
- `--header NAME`: Central concept (or use `--id`)
- `--id NODE_ID`: Node ID to explore
- `--depth N`: Depth of traversal (default: 1)
- `--format FORMAT`: Output format (json, text, etc.)

Output (JSON):
```json
{
  "node": "file.md#concept",
  "title": "Concept Name",
  "outgoing": ["file.md#related-1"],
  "incoming": ["other.md#back-ref"]
}
```

### Check Command

```bash
python3 src/mem_graph.py --root docs check [OPTIONS]
```

Options:
- `--file FILE`: Validate single file only
- `--strict`: Enable strict checks
- `--format FORMAT`: Output format

Exit codes:
- `0`: Valid
- `1`: General error
- `2`: Validation failed
- `3`: Invalid syntax

---

## Link Resolution Algorithm

### URL Generation

Header text → URL slug conversion:

```python
def header_to_slug(header):
    # Lowercase
    slug = header.lower()
    
    # Remove special characters
    import re
    slug = re.sub(r'[^a-z0-9\- ]', '', slug)
    
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    
    # Remove duplicate hyphens
    slug = re.sub(r'-+', '-', slug)
    
    # Strip leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug
```

### Link Target Resolution

Given a link `[text](target)` from file `current.md`:

```python
def resolve_link(target, current_file):
    if target.startswith("http"):
        return ("external", target)
    
    if "#" not in target:
        # No anchor
        if "/" in target:
            # File only
            file_path = resolve_path(target, current_file)
            return ("file", file_path)
        else:
            # Invalid
            return ("invalid", target)
    
    file_part, anchor_part = target.split("#", 1)
    
    if not file_part:
        # Same file
        file_path = current_file
    else:
        # Different file
        file_path = resolve_path(file_part, current_file)
    
    # Return full node ID
    return ("node", f"{file_path}#{anchor_part}")

def resolve_path(path, current_file):
    """Resolve relative path from current file"""
    current_dir = os.path.dirname(current_file)
    
    if path.startswith("./"):
        return os.path.join(current_dir, path[2:])
    elif path.startswith("../"):
        return os.path.join(current_dir, path)
    else:
        # Relative to current directory
        return os.path.join(current_dir, path)
```

---

## Data Structures

### File Structure

Each file contains blocks separated by `---`:

```
## Block 1 Header

Block 1 content

---

## Block 2 Header

Block 2 content
```

### Concept Block

```
## [Header Name]

[Content with optional [links](./file.md#target)]

[Code fences and other markdown]
```

Parsed to:

```python
{
    "header": "Header Name",
    "slug": "header-name",
    "content": "Content with optional [links](...)",
    "links": [
        {
            "text": "links",
            "target": "./file.md#target",
            "type": "node" | "external" | "invalid"
        }
    ]
}
```

### Graph Serialization

Complete graph JSON representation:

```json
{
  "metadata": {
    "root": "docs",
    "file_count": 12,
    "concept_count": 247,
    "link_count": 1842,
    "generated": "2024-02-06T10:30:00Z"
  },
  "nodes": {
    "file.md#concept": {
      "id": "file.md#concept",
      "file": "file.md",
      "header": "Concept",
      "slug": "concept",
      "content": "...",
      "outgoing": ["file.md#related"],
      "incoming": []
    }
  },
  "edges": {
    "file.md#concept|file.md#related": {
      "source": "file.md#concept",
      "target": "file.md#related",
      "label": "related"
    }
  }
}
```

---

## Validation Rules

### Link Validation

For each link, check:

1. **Syntax**: Matches markdown pattern `[text](target)`
2. **File existence**: If file path specified, must exist
3. **Anchor validity**: If anchor specified, must have matching header
4. **No duplicates**: Same target from same source appears once

### Structure Validation

Check:

1. **Unique headers**: No duplicate headers in same file
2. **Block format**: Blocks separated by `---`
3. **Block headers**: Each block has at least one header
4. **No cycles**: Optional, can flag circular references

### Quality Checks (Strict Mode)

Additional checks:

1. **Orphaned nodes**: Concepts with no in/out links
2. **Block size**: Very long or very short blocks
3. **File organization**: Structure consistency
4. **Link density**: Average connections per concept

---

## Error Types

### Error Codes

```python
class ErrorType:
    SYNTAX_ERROR = 1000
    FILE_NOT_FOUND = 1001
    HEADER_NOT_FOUND = 1002
    DUPLICATE_NODE = 1003
    INVALID_LINK = 1004
    ORPHANED_NODE = 1005
    FILE_NOT_FOUND = 1006
```

### Error Format

```python
{
    "type": "HEADER_NOT_FOUND",
    "code": 1002,
    "file": "concepts.md",
    "line": 25,
    "message": "Header 'neural-nets' not found",
    "link": "[Neural Nets](./concepts.md#neural-nets)",
    "suggestion": "Did you mean 'neural-networks'?"
}
```

---

## Performance Metrics

### Complexity Analysis

- **Parse single file**: O(n) where n = file size
- **List headers**: O(F × n) where F = file count
- **Validate links**: O(L) where L = link count
- **Graph traversal**: O(V + E × d) where V = nodes, E = edges, d = depth
- **Full check**: O(F × n + L)

### Benchmarks

Standard system (MacBook Pro M1):

| Operation | 100 concepts | 1000 concepts | 10000 concepts |
|-----------|-------------|---------------|----------------|
| Parse | <10ms | 50ms | 500ms |
| Headers | 5ms | 20ms | 200ms |
| Graph (depth 1) | 2ms | 10ms | 100ms |
| Graph (depth 2) | 5ms | 50ms | 500ms |
| Check | 50ms | 300ms | 2000ms |

---

## Extension Points

### Custom Output Formats

Add support for additional output formats:

```python
class Formatter:
    def format_graph(self, graph_data):
        raise NotImplementedError
    
    def format_list(self, items):
        raise NotImplementedError

class JSONFormatter(Formatter):
    def format_graph(self, graph_data):
        import json
        return json.dumps(graph_data, indent=2)

# Register formatter
formatters = {
    "json": JSONFormatter(),
    "text": TextFormatter(),
}
```

### Custom Validators

Add validation rules:

```python
class Validator:
    def validate_link(self, link):
        raise NotImplementedError
    
    def validate_block(self, block):
        raise NotImplementedError

class LinkQualityValidator(Validator):
    def validate_link(self, link):
        """Check link text is meaningful"""
        if link["text"] in ["click here", "link", "here"]:
            return Error("Link text not descriptive")
        return None
```

### Custom Graph Algorithms

Implement custom graph algorithms:

```python
def find_shortest_path(graph, source, target):
    """BFS to find shortest path between concepts"""
    from collections import deque
    
    queue = deque([(source, [source])])
    visited = {source}
    
    while queue:
        node, path = queue.popleft()
        if node == target:
            return path
        
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None

def find_clusters(graph):
    """Find connected components"""
    visited = set()
    clusters = []
    
    for node in graph.nodes:
        if node not in visited:
            cluster = dfs_component(graph, node, visited)
            clusters.append(cluster)
    
    return clusters
```

---

## Configuration

### Configuration File

Optional `graph.config.json`:

```json
{
  "root": "docs",
  "validation": {
    "strict": false,
    "check_orphans": true,
    "check_duplicates": true
  },
  "output": {
    "format": "text",
    "verbose": false
  },
  "performance": {
    "max_depth": 10,
    "cache_results": true
  }
}
```

Load:
```python
import json
with open("graph.config.json") as f:
    config = json.load(f)
graph = Graph(root=config["root"])
```

---

## Backward Compatibility

### Version 1.0 API

Current API stable and will remain compatible.

Breaking changes (if any) will:
1. Increment major version
2. Be announced in advance
3. Include migration guide
4. Support legacy API for 2 versions

### Deprecation Policy

Deprecated features:
1. Documented as deprecated
2. Emit warnings when used
3. Supported for at least 1 version
4. Then removed

See the version history in the project repository.
