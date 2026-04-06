## Workflows

Common patterns and workflows for using md-graph effectively.

---

## Building a Knowledge Base from Scratch

Step-by-step process for starting a new knowledge graph:

1. **Identify domain**: What concepts do you need to document?
   ```
   Example: Machine Learning → models, training, evaluation, deployment
   ```

2. **Create core files** (one per major area):
   ```bash
   touch docs/concepts.md docs/theory.md docs/practice.md
   ```

3. **Add core concepts** to each file:
   ```markdown
   ## Machine Learning
   
   Definition and overview.
   
   ---
   
   ## Supervised Learning
   
   Learning with labeled examples.
   ```

4. **Connect with forward references**:
   ```markdown
   See [Supervised Learning](#supervised-learning) for details.
   ```

5. **Validate as you go**:
   ```bash
   python3 src/mem_graph.py --root docs check
   ```

6. **Expand gradually**: Add related concepts and deepen connections.

See [Getting Started](./getting-started.md#getting-started) for concrete example.

---

## Refactoring and Reorganization

When your knowledge graph grows, structure may need adjustment:

### Identify problem areas:

```bash
python3 src/mem_graph.py --root docs check --strict
```

Look for:
- Orphaned concepts
- Heavily interconnected clusters
- Deep nesting

### Split large files:

If one file exceeds 20-30 concepts, split by theme:

Before:
```
docs/ml.md (40+ concepts)
```

After:
```
docs/ml/
  ├── fundamentals.md (core concepts)
  ├── neural-networks.md (NN-specific)
  └── training.md (training algorithms)
```

Update links:
```markdown
Before: [Neural Network](./ml.md#neural-network)
After:  [Neural Network](./ml/neural-networks.md#neural-network)
```

### Merge related concepts:

If files are too small/fragmented, consolidate:

Before:
```
docs/
  ├── attention.md (2 concepts)
  ├── positional.md (1 concept)
  └── embeddings.md (3 concepts)
```

After:
```
docs/
  ├── transformers.md (contains attention, positional encoding)
  └── embeddings.md (3 concepts)
```

See [Knowledge Design](./knowledge-design.md#organization-patterns) for structural principles.

---

## Research Notes Workflow

Building a knowledge graph of research papers and ideas:

1. **Create file per paper** (or group by theme):
   ```
   docs/papers/
     ├── attention-is-all-you-need.md
     ├── bert.md
     └── gpt-overview.md
   ```

2. **One concept per key idea**:
   ```markdown
   ## Self-Attention Mechanism
   
   Key innovation from the Transformer paper.
   Allows each token to attend to all other tokens.
   
   ---
   
   ## Scaled Dot-Product Attention
   
   Specific formula used in Transformer.
   ```

3. **Link to related papers**:
   ```markdown
   Builds on: [Previous Work](../papers/earlier-work.md#key-idea)
   Related: [Similar Approach](../papers/similar.md#approach)
   ```

4. **Create taxonomy file**:
   ```
   docs/taxonomy.md
   ```
   
   With overview of all papers:
   ```markdown
   ## Architecture Papers
   
   - [Attention](./papers/attention-is-all-you-need.md#self-attention)
   - [BERT](./papers/bert.md#model-design)
   - [GPT](./papers/gpt-overview.md#gpt-architecture)
   ```

See [Examples](./examples.md#research-paper-knowledge-base) for full example.

---

## Project Documentation Workflow

Documenting a software project's architecture and design:

1. **Structure by module**:
   ```
   docs/
     ├── architecture.md (system overview)
     ├── core/
     │   ├── engine.md (core components)
     │   └── api.md (public APIs)
     ├── features/
     │   ├── auth.md (authentication)
     │   └── caching.md (caching system)
     └── deployment.md (ops and deployment)
   ```

2. **Each module has concepts**:
   ```markdown
   ## Authentication Flow
   
   Three-step process: login, token generation, verification.
   
   ---
   
   ## Token Validation
   
   Checks JWT signature and expiration.
   ```

3. **Link to requirements**:
   ```markdown
   ## Rate Limiting
   
   Implements [Sliding Window](./algorithms.md#sliding-window).
   Uses [Redis Cache](./infrastructure.md#redis).
   ```

4. **Cross-reference decisions**:
   ```markdown
   ## Architecture Choice: Microservices
   
   Rationale: [Scalability Requirements](#scalability-requirements).
   Trade-off: [Operational Complexity](#operational-complexity).
   ```

---

## Team Collaboration

Using md-graph in a team environment:

1. **Establish conventions**:
   - File naming: `snake_case.md`
   - Header format: "Noun Phrase" style
   - Link text: Descriptive, not "click here"

   See [Best Practices](./best-practices.md#naming-conventions) for full guidelines.

2. **Create CONTRIBUTING.md**:
   ```markdown
   # Contributing to Knowledge Base
   
   1. Run `check` before pushing: `python3 src/mem_graph.py --root docs check`
   2. Use [Format](../docs/format.md#format) rules
   3. Link new concepts to existing ones
   4. One concept per block
   ```

3. **Use pre-commit hooks**:
   ```bash
   python3 src/mem_graph.py --root docs check --strict
   ```

   Prevents invalid graphs in repository.

4. **Review changes**:
   - Check `git diff` shows valid links
   - Verify new files follow structure
   - Validate before merge

---

## Learning and Teaching

Using md-graph as a learning tool:

1. **Create learning path** (topological order):
   ```markdown
   ## Learning Roadmap
   
   1. Start: [Foundations](#foundations)
   2. Build: [Intermediate](#intermediate)
   3. Advanced: [Specialist Topics](#specialist-topics)
   ```

2. **Progressive linking**:
   - Foundational concepts have few references
   - Builds complexity as you link deeper

3. **Add explanations at multiple levels**:
   ```markdown
   ## Concept (Beginner)
   
   Simple explanation and basic links.
   
   ---
   
   ## Concept (Advanced)
   
   Mathematical details and advanced references.
   ```

4. **Create study guides**:
   ```markdown
   ## Module 1: Fundamentals
   
   Study these in order:
   1. [Concept A](#concept-a)
   2. [Concept B](#concept-b)
   3. [Concept C](#concept-c)
   ```

---

## Maintaining Quality

Regular maintenance practices:

1. **Weekly validation**:
   ```bash
   python3 src/mem_graph.py --root docs check
   ```

2. **Monthly review** of:
   - Orphaned blocks
   - Unclear connections
   - Outdated content

3. **Quarterly refactoring**:
   - Split oversized files
   - Merge fragmented groups
   - Improve organization

4. **Annual audit**:
   - Full graph restructure if needed
   - Update deprecated concepts
   - Archive obsolete sections

---

## Integration with Agents

Using knowledge graph with AI agents:

1. **Export graph for agent**:
   ```bash
   python3 src/mem_graph.py --root docs graph --header "Concept" --format json
   ```

2. **Create agent prompts**:
   ```markdown
   ## Agent Memory
   
   Agent has access to:
   - [Knowledge Graph](../docs/overview.md#overview)
   - [API Reference](../docs/api-reference.md#api-reference)
   ```

3. **Agent query patterns**:
   ```
   Query: "What's related to Machine Learning?"
   Response: [concept], [concept], [concept]
   ```

See [Agents](./agents.md#agents) for full integration details.

---

## Search and Discovery

Finding concepts in large graphs:

1. **Find by keyword**:
   ```bash
   grep -r "keyword" docs/ --include="*.md"
   ```

2. **Find orphaned concepts**:
   ```bash
   python3 src/mem_graph.py --root docs check --strict | grep "orphaned"
   ```

3. **Explore neighborhood**:
   ```bash
   python3 src/mem_graph.py --root docs graph --header "Concept" --depth 3
   ```

4. **List all concepts**:
   ```bash
   python3 src/mem_graph.py --root docs headers --all | sort
   ```

---

## Backup and Recovery

Protecting your knowledge graph:

1. **Version control** (recommended):
   ```bash
   git init docs/
   git add .
   git commit -m "Initial knowledge graph"
   ```

2. **Automated backups**:
   ```bash
   cp -r docs/ docs.backup.$(date +%Y%m%d)/
   ```

3. **Recovery workflow**:
   - Fix errors: `python3 src/mem_graph.py --root docs check`
   - Restore from backup if needed
   - Update links: `python3 src/mem_graph.py --root docs check`

See [Troubleshooting](./troubleshooting.md#recovery-procedures) for disaster recovery.
