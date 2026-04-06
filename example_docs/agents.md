## Agents

Using md-graph knowledge bases with AI agents and LLM-based systems.

---

## Agent Integration Overview

md-graph provides structured knowledge that AI agents can query and use during reasoning and planning.

Key capabilities:
- **Graph queries**: Access related concepts
- **Link exploration**: Follow reasoning paths
- **Structured retrieval**: Get relevant context
- **Contextual boundaries**: Know what's documented

---

## Knowledge Extraction Formats

### JSON Graph Export

Export for programmatic use:

```bash
python3 src/mem_graph.py --root docs graph --header "Concept" --format json
```

Output:
```json
{
  "node": "file.md#concept",
  "title": "Concept Name",
  "content": "Concept description...",
  "outgoing": [
    "file.md#related-concept-1",
    "file.md#related-concept-2"
  ],
  "incoming": [
    "other.md#concept"
  ],
  "metadata": {
    "file": "file.md",
    "header": "Concept Name",
    "depth": 0
  }
}
```

### Line-Delimited Format

For streaming/agents:

```
NODE: file.md#concept
TITLE: Concept Name
CONTENT: Concept description...
LINK: OUT → file.md#related-1
LINK: OUT → file.md#related-2
LINK: IN ← other.md#concept
```

### Structured Context

Include concept with neighbors:

```bash
python3 src/mem_graph.py --root docs graph --header "Concept" --depth 1
```

Provides:
- Central concept details
- All directly connected concepts
- Complete local context

Ideal for agent queries: "What's related to X?"

---

## Agent Query Patterns

### Pattern 1: Concept Lookup

Agent question: "What is [concept]?"

Process:
1. Parse question to extract concept name
2. Query: `python3 src/mem_graph.py --root docs view --header "[concept]"`
3. Return concept definition and links
4. Agent uses for reasoning

### Pattern 2: Related Concepts

Agent question: "What's related to [concept]?"

Process:
1. Query: `python3 src/mem_graph.py --root docs graph --header "[concept]" --depth 1`
2. Parse outgoing/incoming links
3. Fetch each related concept
4. Provide as context

### Pattern 3: Knowledge Navigation

Agent question: "How do [A] and [B] relate?"

Process:
1. Query A: `graph --header "[A]" --depth 2`
2. Query B: `graph --header "[B]" --depth 2`
3. Find common connections
4. Trace path from A to B if exists
5. Explain relationship chain

### Pattern 4: Validation

Agent question: "Is [statement] documented?"

Process:
1. Parse statement to extract concepts
2. Check each concept exists: `headers --all`
3. Verify links between them
4. Return True/False with evidence

---

## Prompt Engineering for Agents

### System Prompt Example

```
You have access to a structured knowledge graph about [domain].

The knowledge graph contains:
- Atomic concepts (one idea per block)
- Explicit links between related concepts
- Organized in markdown files

To query the knowledge:
1. List concepts: python3 src/mem_graph.py --root docs headers --all
2. Find concept: python3 src/mem_graph.py --root docs view --file [file] --header "[header]"
3. Explore relationships: python3 src/mem_graph.py --root docs graph --header "[concept]"
4. Validate links: python3 src/mem_graph.py --root docs check

When reasoning:
- Ground answers in documented concepts
- Cite which concept file supports your claim
- Explore related concepts for context
- Note when something isn't documented
```

### Task Prompt Example

```
Question: How does [topic] relate to [other topic]?

Use the knowledge graph to:
1. Look up both topics
2. Explore their connections
3. Find common related concepts
4. Trace the path(s) between them
5. Explain the relationship

Format: [Topic A] → [Connection] → [Topic B]
Include concept links from the knowledge graph.
```

---

## Integration Patterns

### Direct CLI Integration

Agent calls CLI directly:

```python
import subprocess
import json

def query_concept(name):
    result = subprocess.run(
        ["python3", "src/mem_graph.py", "--root", "docs", 
         "view", "--header", name, "--format", "json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def explore_neighbors(name, depth=1):
    result = subprocess.run(
        ["python3", "src/mem_graph.py", "--root", "docs",
         "graph", "--header", name, "--depth", str(depth)],
        capture_output=True,
        text=True
    )
    return parse_graph_output(result.stdout)
```

### Caching for Performance

Agent pre-loads graph:

```python
class KnowledgeGraph:
    def __init__(self, root="docs"):
        self.cache = self._load_graph(root)
    
    def _load_graph(self, root):
        # Load all concepts once at startup
        concepts = {}
        links = {}
        # ... parsing logic ...
        return {"concepts": concepts, "links": links}
    
    def lookup(self, name):
        return self.cache["concepts"].get(name)
    
    def neighbors(self, name, depth=1):
        # Navigate pre-loaded cache
        return self._traverse(name, depth, self.cache["links"])
```

### REST API Wrapper

Expose graph as API:

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/api/concept/<name>")
def get_concept(name):
    concept = query_concept(name)
    return jsonify(concept)

@app.route("/api/neighbors/<name>")
def get_neighbors(name):
    neighbors = explore_neighbors(name)
    return jsonify(neighbors)

@app.route("/api/validate/<name>")
def validate_concept(name):
    exists = concept_exists(name)
    return jsonify({"exists": exists})
```

---

## Agent Reasoning Examples

### Example 1: Dependency Understanding

Agent task: "Explain the dependency chain for [concept]"

1. Query concept
2. Identify incoming links (concepts that depend on it)
3. Recursively explore each dependency
4. Build tree structure
5. Explain in natural language

Output:
```
[Advanced Concept] depends on:
  → [Intermediate Concept] which depends on:
    → [Basic Concept 1]
    → [Basic Concept 2]
```

### Example 2: Contradiction Detection

Agent task: "Find contradictions in the knowledge graph"

1. Extract all concepts
2. For each concept, extract claims
3. Compare claims across related concepts
4. Flag contradictions
5. Report with evidence

Useful for: Knowledge base quality assurance

### Example 3: Gap Identification

Agent task: "What's not documented?"

1. Identify major concepts
2. Check for expected related concepts
3. Flag missing links or concepts
4. Report gaps with context

Example output:
```
Gap detected:
  [Concept A] links to [Concept B]
  [Concept B] links to [Concept C]
  But [Concept A] doesn't directly link to [Concept C]
  Consider adding explicit link
```

### Example 4: Explanation Generation

Agent task: "Explain [topic] to a beginner"

1. Look up concept
2. Find prerequisite concepts
3. Look up prerequisites
4. Build progression from simple to complex
5. Generate narrative using links as guide

Output:
```
To understand [Topic], you first need:
1. [Foundation] - the basic building block
2. [Intermediate] - builds on [Foundation]
3. [Advanced] - combines multiple concepts

Then [Topic] makes sense because...
```

---

## Knowledge Base Construction for Agents

### Structuring for Agent Use

Design knowledge graph with agents in mind:

1. **Clear atomicity**: One concept per block
   - Easier for agents to reference
   - Unambiguous concept boundaries

2. **Explicit relationships**: Use links generously
   - Agents follow links to understand context
   - More links = more reasoning paths

3. **Semantic link text**: Meaningful descriptions
   - Agents can infer relationship type
   - Natural language guides reasoning

```markdown
✓ Built on: [Foundation Concept](./file.md#foundation)
✗ Related: [Thing](./file.md#thing)
```

4. **Consistent naming**: Reduce ambiguity
   - Agents match concept names reliably
   - Synonyms documented in links

### Agent-Specific Files

Create files optimized for agent use:

```
docs/
├── concepts/          # Core definitions
├── relationships/     # Explicit relationship docs
├── examples/         # Concrete examples
├── applications/     # Use cases and applications
├── edge-cases.md     # Special situations
└── FAQ/             # Common questions
```

### Metadata for Agents

Optionally add structured metadata:

```markdown
## Concept Name

[metadata]
difficulty: intermediate
prerequisites: [Foundation](./file.md#foundation)
applications: [Use Case 1](./use-cases.md#use-case-1)
[/metadata]

Concept description...
```

Not part of standard md-graph but agents can parse.

---

## Performance Optimization for Agents

### Caching Strategy

Agent should cache at multiple levels:

```
Level 1: All concepts (in memory)
Level 2: Recently queried concepts (fast recall)
Level 3: Graph structure (connectivity info)
```

Reduces repeated queries to disk.

### Batch Operations

Minimize CLI calls:

```python
# Instead of:
for concept in concepts:
    query_concept(concept)  # N CLI calls

# Do:
all_concepts = load_all_concepts()  # 1 call
```

### Query Optimization

Cache depth-based queries:

```python
# Pre-compute for common depths
depth1_cache = graph_all_with_depth(1)  # Cache once
depth2_cache = graph_all_with_depth(2)  # Cache once
```

Subsequent queries hit cache instantly.

---

## Error Handling

### Invalid Concept References

Agent handles gracefully:

```python
def safe_lookup(name):
    try:
        return query_concept(name)
    except ConceptNotFound:
        return None  # Return None, don't crash

# In prompt:
if concept is None:
    return f"Concept '{name}' not found in knowledge base"
```

### Incomplete Knowledge

Agent acknowledges gaps:

```
Question: How does [X] relate to [Y]?

Found [X] (documented)
Found [Y] (documented)
No direct link between them in knowledge base
Possible related concepts: [Z1], [Z2]

The knowledge base doesn't explicitly document this relationship.
```

### Stale Links

Agent detects broken references:

```python
def validate_link(source, target):
    try:
        query_concept(target)
        return True
    except:
        return False  # Link broken

# Report during queries
if not validate_link(source, target):
    log_warning(f"Broken link: {source} → {target}")
```

---

## Privacy and Security

### Sensitive Knowledge

Protect sensitive information:

```bash
# Create separate graph for sensitive info
docs/public/
docs/private/
```

Agent accesses only permitted graph:

```python
accessible_root = "docs/public"  # For this agent
```

### Access Control

Implement graph-level access:

```python
class ProtectedGraph:
    def __init__(self, root, allowed_concepts=None):
        self.allowed = allowed_concepts or set()
    
    def lookup(self, name):
        if name not in self.allowed:
            raise PermissionError(f"Access denied: {name}")
        return query_concept(name)
```

### Audit Logging

Track agent queries:

```python
def tracked_query(agent_id, concept_name):
    log(f"Agent {agent_id} queried {concept_name}")
    return query_concept(concept_name)
```

---

## Multi-Agent Collaboration

### Shared Knowledge Graph

Multiple agents access same graph:

```
Shared: docs/
  ├── shared-concepts.md
  ├── shared-theory.md
  └── ...

Agent A: docs/ + docs-private-a/
Agent B: docs/ + docs-private-b/
```

### Distributed Knowledge

Agents maintain separate sub-graphs:

```
Global Index: /agent-index.md
Links to each agent's knowledge

[Agent A Knowledge](./agents/a-knowledge/index.md)
[Agent B Knowledge](./agents/b-knowledge/index.md)
```

### Cross-Agent Learning

Agents document shared learnings:

```markdown
## Observation: X leads to Y

Observed by: Agent A
Confirmed by: Agent B  
Status: Validated

Add to shared knowledge when enough evidence accumulates.
```

---

## Testing and Validation

### Agent Knowledge Tests

Verify agent can use knowledge correctly:

```python
def test_agent_lookup():
    agent = create_agent()
    result = agent.query("What is [Concept]?")
    assert "[Concept]" in result
    assert "related" in result.lower()

def test_agent_reasoning():
    agent = create_agent()
    result = agent.query("Why does [A] affect [B]?")
    assert graph_linked("[A]", "[B]")  # Verify knowledge base supports answer
```

### Knowledge Completeness

Verify agent has full picture:

```python
def test_knowledge_coverage():
    agent = create_agent()
    concepts = get_all_concepts()
    for concept in concepts:
        result = agent.lookup(concept)
        assert result is not None
```

### Link Correctness

Validate knowledge base before deployment:

```bash
python3 src/mem_graph.py --root docs check --strict
```

All links valid before agents use them.

---

## Integration with OpenCode

md-graph works with OpenCode agents:

1. **Load knowledge**: Agent loads graph at startup
2. **Query during planning**: Agent asks graph for context
3. **Reason with structure**: Agent uses links to inform decisions
4. **Update knowledge**: Agent can propose new concepts/links
5. **Validate before adding**: Validate proposed changes maintain consistency

See [Workflows](./workflows.md#integration-with-agents) for detailed workflow.
