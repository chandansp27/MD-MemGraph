## Graph Theory

Understanding the graph theory concepts underlying md-graph and how knowledge is modeled as a graph structure.

---

## What is a Graph?

A graph is a mathematical structure consisting of nodes (vertices) and edges (connections between nodes).

In md-graph:
- **Nodes**: Concepts defined by headers (e.g., `concepts.md#neural-networks`)
- **Edges**: Links between concepts (`[text](./file.md#target)`)
- **Directed**: Links have direction (from source to target)

Visual representation: concepts (nodes) connected by links (directed edges).

For example, a concept about attention mechanisms might link to 
concepts about transformers, neural networks, and optimization techniques.

---

## Nodes and Node IDs

### Node Anatomy

Each node in md-graph consists of:

1. **File path**: Which document the concept lives in
2. **Header slug**: URL-safe name derived from heading text
3. **Full ID**: Combined format `file.md#header-slug`

Example:

```markdown
File: docs/ml/fundamentals.md
Header: ## Neural Networks
Node ID: fundamentals.md#neural-networks
Full path: ml/fundamentals.md#neural-networks
```

### Node Properties

Each node has metadata:

- **Content**: The concept description (paragraph text)
- **Outgoing edges**: Links this concept points to
- **Incoming edges**: Links pointing to this concept
- **Degree**: Total connections (in + out)

Query example:

```bash
python3 src/mem_graph.py --root docs graph --header "Neural Networks"
```

---

## Edges and Links

### Edge Representation

Edges are markdown links in concept text:

```markdown
## Source Concept

Text mentioning [Target](./file.md#target).
```

This creates one directed edge: Source → Target

### Edge Properties

- **Source**: The concept containing the link
- **Target**: The linked concept (must exist)
- **Direction**: One-way (source → target)
- **Type**: Implicit (not labeled in basic md-graph)

### Relationship Semantics

Links represent relationships but don't specify type:

```markdown
[Related Concept](./file.md#related)     # Generic relationship
[Builds On](./file.md#foundation)       # Link text hints at relationship type
[See Also](./file.md#similar)           # Similar relationship
```

Link text is semantic hint but not machine-enforced.

See [Best Practices](./best-practices.md#linking-practices) for naming conventions.

---

## Graph Structure

### Connectivity Patterns

Different graph structures emerge:

**Linear chain**:
```
A → B → C → D
```
Concept D depends on A through chain.

**Hub and spoke**:
```
    ↓ ↓ ↓
    B C D
    ↓ ↓ ↓
    A
```
Central concept with many incoming links.

**Mesh**:
```
A ↔ B
↕   ↕
C ↔ D
```
Highly interconnected concepts.

**Forest** (multiple isolated trees):
```
Tree 1: A → B → C
Tree 2: D → E
Isolated: F
```

Real knowledge graphs typically have mixed patterns.

---

## Paths and Traversal

### Paths

A path is a sequence of edges connecting nodes:

```
Start: ML Fundamentals
Path:  ML Fund. → Neural Networks → Backpropagation → Optimization
Length: 3 hops
```

Query example:

```bash
python3 src/mem_graph.py --root docs graph --header "ML Fundamentals" --depth 3
```

### Depth

Depth measures how far you traverse from a starting node:

- **Depth 1**: Direct neighbors only (1 hop away)
- **Depth 2**: Neighbors' neighbors (2 hops away)
- **Depth 3+**: Further transitive connections

### Breadth-First Search

When exploring, md-graph expands breadth-first:

```
Depth 1: [B, C, D]
Depth 2: [E, F, G, H, I]
Depth 3: [J, K, L, M, N, O, P]
```

Level by level from starting node.

---

## Graph Properties

### Size

Basic metrics about graph:

```bash
python3 src/mem_graph.py --root docs check
```

Provides:
- **Nodes**: Total concepts
- **Edges**: Total links
- **Files**: Markdown documents

### Density

How connected the graph is:

```
Density = actual_edges / possible_edges

Sparse graph: 0.1 (10% of possible connections)
Dense graph: 0.8 (80% of possible connections)
```

Typical knowledge graphs: 0.2-0.4 (moderately connected)

### Degree Distribution

How many connections each node has:

```
Average degree = 2 * edges / nodes

Typical: 2-5 connections per concept
Isolated: 0 connections (orphaned nodes)
Hub: 10+ connections (central concepts)
```

### Clustering

How tightly related concepts group together:

```
High clustering: Concepts in communities
Low clustering: Evenly distributed connections
```

Real-world knowledge graphs show both.

---

## Cycles and Circular References

### Cycles Explained

A cycle is a path that returns to its starting node:

```
A → B → C → A
```

Three-node cycle.

### Self-Loops

A concept linking to itself:

```markdown
## Recursion

Recursion is the process of [Recursion](#recursion) calling itself.
```

Valid but unusual. Indicates self-reference (should be rare).

### Bidirectional Links

Two concepts linking to each other:

```markdown
## Concept A

Related to [Concept B](#concept-b).

---

## Concept B

Related to [Concept A](#concept-a).
```

Bidirectional edge: A ↔ B (cycles of length 2)

### Acyclic Graphs

Some knowledge graphs avoid cycles (DAG - Directed Acyclic Graph):

```
Foundations → Intermediate → Advanced
```

No path returns to starting point.

Advantage: Clear progression and prerequisites.
Trade-off: Can't express bidirectional relationships.

See [Knowledge Design](./knowledge-design.md#cyclicity) for design guidance.

---

## Connectivity Components

### Connected Components

Subgraphs where all nodes are reachable from each other:

```
Component 1: A ↔ B → C
Component 2: D → E ↔ F
Isolated:    G
```

Three components (G is isolated single node).

### Finding Isolated Nodes

```bash
python3 src/mem_graph.py --root docs check --strict
```

Reports orphaned concepts (0 connections).

### Strongly Connected Components

Subgraphs where every node reaches every other node:

```
SCC: A ↔ B ↔ C ↔ A (all reach each other)
Weakly connected: A → B ↔ C (not all reachable)
```

Useful for identifying core concept clusters.

---

## Centrality Measures

### Node Importance

Different ways to measure which concepts are central:

**In-degree centrality**: How many concepts link TO this concept
```
High: Fundamental concepts (many depend on)
Low: Specialized or new concepts
```

**Out-degree centrality**: How many concepts this concept links TO
```
High: Connecting/overview concepts
Low: Leaf concepts (depend on others)
```

**Betweenness centrality**: How often this concept is on paths between others
```
High: Bridge concepts connecting distinct domains
Low: Isolated or leaf concepts
```

### Finding Central Concepts

```bash
python3 src/mem_graph.py --root docs headers --all | while read line; do
    python3 src/mem_graph.py --root docs graph --header "$line" | grep -c "IN"
done | sort -rn | head
```

Shows most-referenced concepts.

---

## Network Motifs

### Common Patterns

**Hierarchy**:
```
Root → Middle → Leaf → Leaf
```
Clear dependencies.

**Fan-out**:
```
    ├─ B
A ─┼─ C
    └─ D
```
One concept explains multiple related ones.

**Fan-in**:
```
  ┌─ B
D ├─ C
  └─ E
```
Multiple concepts build toward one.

**Cross-connections**:
```
A ↔ C
B ↔ D
A → B, D → C
```
Multiple domains with bridges.

---

## Graph Algorithms

### Breadth-First Search (BFS)

md-graph uses BFS for graph traversal:

```bash
python3 src/mem_graph.py --root docs graph --header "Start" --depth 2
```

Algorithm:
1. Start at node
2. Visit all depth-1 neighbors
3. Visit all depth-2 neighbors
4. Continue to requested depth

### Cycle Detection

Check for cycles:

```bash
python3 src/mem_graph.py --root docs check --strict
```

Detects self-references and circular relationships (warns but allows them).

### Transitive Closure

All reachable concepts from starting point:

```bash
python3 src/mem_graph.py --root docs graph --header "ML" --depth 10
```

With large depth, finds all transitively connected concepts.

---

## Design Implications

### Graph Properties to Maintain

Good knowledge graphs typically have:

1. **Moderate connectivity**: 2-5 edges per node average
2. **Few isolated components**: Most concepts connected
3. **Clear hierarchy**: Some level structure (few cycles)
4. **Identifiable clusters**: Domain-specific groups

See [Knowledge Design](./knowledge-design.md#scalability-considerations) for structural guidelines.

### Performance Implications

- **Large graphs** (1000+ nodes): Queries may slow down
- **Dense graphs**: More connections = more computation
- **Deep hierarchies**: Traversal to great depths expensive

See [Scalability](./scalability.md#scalability) for performance tips.
