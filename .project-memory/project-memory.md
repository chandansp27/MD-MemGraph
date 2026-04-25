## Lightweight Memory Graph Purpose

This project is intended to be a lightweight memory and knowledge graph for agents working across large corpora of documents, files, code, and research context. The graph should help an agent preserve and traverse important semantic connections during inference while the main task continues.

Related: [Simplicity Constraint](#simplicity-constraint), [Agent Retrieval Workflow](#agent-retrieval-workflow).

---

## Simplicity Constraint

The memory graph should stay simple and efficient rather than accumulating many features. Markdown blocks, standard links, shell tools, and a small graph CLI are preferred over heavier infrastructure because the agent's main attention should remain on the user's task.

Related: [Lightweight Memory Graph Purpose](#lightweight-memory-graph-purpose), [Use Bash With Graph CLI](#use-bash-with-graph-cli).

---

## Agent Retrieval Workflow

Agents should use normal text and file tools first to find candidate context, then use the graph CLI to inspect a specific block and its direct neighbors. Shallow traversal is preferred unless the next linked concept is clearly useful.

Related: [Use Bash With Graph CLI](#use-bash-with-graph-cli), [Simplicity Constraint](#simplicity-constraint).

---

## Use Bash With Graph CLI

The markdown format is intentionally compatible with shell exploration. Agents can use tools such as `rg`, `grep`, `find`, `sed`, `nl`, `awk`, `sort`, `uniq`, and short Python scripts to quickly filter files, headings, links, and surrounding lines before switching to node-aware graph commands.

Related: [Agent Retrieval Workflow](#agent-retrieval-workflow), [Skill Description Purpose](#skill-description-purpose).

---

## Atomic Memory Blocks

Memory entries should be atomic blocks: one reusable idea, decision, relationship, workflow, constraint, or discovery per block. Blocks should be low-to-mid token length, specific enough to help future work, and connected with standard markdown links instead of duplicating nearby concepts.

Related: [Simplicity Constraint](#simplicity-constraint), [Skill Description Purpose](#skill-description-purpose).

---

## Skill Description Purpose

The skill description should act as an activation trigger for the agent, not as full documentation. It should make clear that the skill is for recalling prior memory, preserving important facts or decisions, recording semantic connections, adding atomic markdown memory blocks, and linking related concepts for future navigation.

Related: [Atomic Memory Blocks](#atomic-memory-blocks), [Use Bash With Graph CLI](#use-bash-with-graph-cli).
