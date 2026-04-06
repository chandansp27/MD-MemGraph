## Overview

Markdown Knowledge Graph (md-graph) is a lightweight, filesystem-based system for building interconnected knowledge bases using plain markdown and standard links. It treats your documentation as a graph where files contain atomic blocks of information connected through hyperlinks.

---

## What is md-graph?

md-graph is a tool that transforms your markdown documentation into a queryable knowledge graph. Instead of flat, isolated documents, you create small, focused blocks within files and link them together using standard markdown syntax. The system then validates, visualizes, and lets you query relationships between concepts.

Key insight: **Knowledge is relational**. By making connections explicit through links, you create a structured knowledge base that's both human-readable and machine-queryable.

---

## Core Philosophy

The design follows these principles:

- **Plain text first**: Uses standard markdown syntax, no special formats
- **Filesystem-native**: One block per concept, organized in `.md` files
- **Link-based structure**: Standard markdown links `[text](./file.md#anchor)` define relationships
- **Minimal tooling**: Single Python script for all operations
- **Human-readable**: Documentation remains readable as markdown, not opaque serialization

See [Getting Started](./getting-started.md#getting-started) to begin building your knowledge graph.

---

## Problem it Solves

Traditional documentation suffers from:

1. **Isolation**: Concepts are scattered across files with unclear relationships
2. **Maintenance burden**: Changing a concept requires manually updating multiple places
3. **No structure**: Links are informal, making it hard to query concepts programmatically
4. **Scale issues**: Large docs become unwieldy without clear organization

md-graph addresses these by making relationships explicit and queryable. See [Knowledge Design](./knowledge-design.md#knowledge-design) for deeper context on structuring knowledge.

---

## Use Cases

- **Research notes**: Build interconnected notes on papers, concepts, and experiments
- **Technical documentation**: Create structured reference docs with clear dependencies
- **Learning materials**: Link concepts together to show how they relate
- **Project memory**: Document decisions, designs, and reasoning with full traceability
- **Agent memory**: Provide AI agents with structured, queryable knowledge bases

See [Workflows](./workflows.md#workflows) for concrete examples of how to use md-graph effectively.

---

## Core Components

The system has three main pieces:

1. **Format specification**: Rules for blocks, links, and structure ([Format](./format.md#format))
2. **CLI tool**: Python script for querying and validating ([CLI Reference](./cli-reference.md#cli-reference))
3. **Link resolution**: How references are parsed and validated ([Links](./links.md#links))

These work together to let you write documentation naturally while maintaining a queryable graph structure underneath.

---

## Quick Comparison

| Aspect | Regular Markdown | md-graph |
|--------|-----------------|----------|
| **Links** | Free-form, informal | Standardized, validated |
| **Structure** | Implicit | Explicit as graph |
| **Querying** | No | Full graph queries |
| **Maintenance** | Manual | Automatic validation |
| **Learning curve** | None | Very minimal |

---

## Next Steps

- Read [Getting Started](./getting-started.md#getting-started) for a hands-on introduction
- Review [Format](./format.md#format) to understand the syntax
- Explore [Examples](./examples.md#examples) to see real knowledge graphs
- Check [CLI Reference](./cli-reference.md#cli-reference) for available commands
