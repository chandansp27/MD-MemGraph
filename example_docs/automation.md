## Automation

Scripts and tooling for automating md-graph operations.

---

## Graph Analysis Scripts

### Find Orphaned Concepts

Identify concepts with no links:

```bash
#!/bin/bash
# orphan-finder.sh

echo "Finding orphaned concepts..."

python3 src/mem_graph.py --root docs headers --all | while read concept; do
    file=$(echo "$concept" | cut -d'#' -f1)
    header=$(echo "$concept" | cut -d'#' -f2)
    
    # Count links to this concept
    incoming=$(grep -r "\[$header\](" docs --include="*.md" | grep -v "^$file:" | wc -l)
    
    # Count links from this concept  
    outgoing=$(grep "\[$header\]" "docs/$file" | grep "\[.*\](.*)" | wc -l)
    
    if [ $incoming -eq 0 ] && [ $outgoing -eq 0 ]; then
        echo "Orphaned: $concept"
    fi
done
```

Run:
```bash
bash orphan-finder.sh
```

### Find Hub Concepts

Identify most-connected concepts:

```bash
#!/bin/bash
# hub-finder.sh

echo "Finding hub concepts (highly connected)..."

python3 src/mem_graph.py --root docs headers --all | while read concept; do
    links=$(python3 src/mem_graph.py --root docs graph --header "${concept##*#}" 2>/dev/null | \
            grep -c "→\|←")
    
    if [ $links -gt 5 ]; then
        echo "$concept: $links connections"
    fi
done | sort -t: -k2 -rn
```

Run:
```bash
bash hub-finder.sh
```

### Analyze Link Patterns

Find common reference patterns:

```python
#!/usr/bin/env python3
# analyze-links.py

import re
import os
from collections import defaultdict

links_by_type = defaultdict(int)

for root, dirs, files in os.walk("docs"):
    for file in files:
        if not file.endswith(".md"):
            continue
        
        path = os.path.join(root, file)
        with open(path) as f:
            content = f.read()
        
        # Find all links
        pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        for match in re.finditer(pattern, content):
            link_text = match.group(1)
            link_target = match.group(2)
            
            # Categorize
            if link_target.startswith("http"):
                links_by_type["external"] += 1
            elif link_target.startswith("#"):
                links_by_type["same-file"] += 1
            elif link_target.startswith("./"):
                links_by_type["same-dir"] += 1
            elif link_target.startswith("../"):
                links_by_type["parent-dir"] += 1
            else:
                links_by_type["other"] += 1

print("Link distribution:")
for link_type, count in sorted(links_by_type.items(), key=lambda x: -x[1]):
    print(f"  {link_type}: {count}")
```

Run:
```bash
python3 analyze-links.py
```

---

## Batch Operations

### Rename Concept Everywhere

Change a concept name across all files:

```bash
#!/bin/bash
# rename-concept.sh

OLD_CONCEPT="$1"
NEW_CONCEPT="$2"

if [ -z "$OLD_CONCEPT" ] || [ -z "$NEW_CONCEPT" ]; then
    echo "Usage: $0 old-name new-name"
    exit 1
fi

# Convert to slug
OLD_SLUG=$(echo "$OLD_CONCEPT" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')
NEW_SLUG=$(echo "$NEW_CONCEPT" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')

echo "Renaming: $OLD_CONCEPT → $NEW_CONCEPT"
echo "Slug: $OLD_SLUG → $NEW_SLUG"

# Update headers
find docs -name "*.md" -exec sed -i \
  "s/^## $OLD_CONCEPT$/## $NEW_CONCEPT/" {} \;

# Update links
find docs -name "*.md" -exec sed -i \
  "s/#$OLD_SLUG/#$NEW_SLUG/g" {} \;

echo "Renamed. Validating..."
python3 src/mem_graph.py --root docs check
```

Run:
```bash
bash rename-concept.sh "Old Name" "New Name"
```

### Merge Two Concepts

Combine related concepts:

```bash
#!/bin/bash
# merge-concepts.sh

FILE1="$1"
HEADER1="$2"
FILE2="$3"
HEADER2="$4"

echo "Merging $HEADER2 (from $FILE2) into $HEADER1 (in $FILE1)"

# Extract target concept
TARGET=$(python3 src/mem_graph.py --root docs view \
  --file "$FILE1" --header "$HEADER1")

# Extract source concept
SOURCE=$(python3 src/mem_graph.py --root docs view \
  --file "$FILE2" --header "$HEADER2")

# Combine content (manual step needed)
echo "$TARGET" > /tmp/merge-source.txt
echo "$SOURCE" >> /tmp/merge-source.txt

echo "Combined content in /tmp/merge-source.txt"
echo "Review and update $FILE1 manually"

# Update all links pointing to source to point to target
SOURCE_SLUG=$(echo "$HEADER2" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')
TARGET_SLUG=$(echo "$HEADER1" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')

find docs -name "*.md" -exec sed -i \
  "s/#$SOURCE_SLUG/#$TARGET_SLUG/g; s/(\./$FILE2/#/(\./$FILE1/#/g" {} \;

echo "Updated all links"
```

### Split Large Concept

Break one concept into multiple:

```bash
#!/bin/bash
# split-concept.sh

FILE="$1"
HEADER="$2"

echo "Splitting $HEADER in $FILE"
echo "Edit the file manually:"
echo "  1. Copy content to split"
echo "  2. Create new ## headers for each part"
echo "  3. Add --- between parts"

# Show the concept
python3 src/mem_graph.py --root docs view --file "$FILE" --header "$HEADER"

# Open for editing
${EDITOR:-vim} "docs/$FILE"

# Validate after editing
python3 src/mem_graph.py --root docs check
```

---

## Continuous Integration

### Pre-Commit Hook

Validate before commits:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Validating knowledge graph..."
python3 src/mem_graph.py --root docs check

if [ $? -ne 0 ]; then
    echo "❌ Graph validation failed!"
    echo "Fix errors before committing"
    exit 1
fi

echo "✓ Graph is valid"
```

Install:
```bash
chmod +x .git/hooks/pre-commit
```

### GitHub Actions

Validate in CI/CD:

```yaml
# .github/workflows/validate-docs.yml

name: Validate Knowledge Graph

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Validate graph
        run: python3 src/mem_graph.py --root docs check
      
      - name: Check for orphans
        run: python3 src/mem_graph.py --root docs check --strict
```

---

## Monitoring and Metrics

### Growth Tracking

Monitor graph growth over time:

```bash
#!/bin/bash
# track-growth.sh

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
CONCEPTS=$(python3 src/mem_graph.py --root docs headers --all | wc -l)
LINKS=$(grep -r "\[.*\](" docs --include="*.md" | wc -l)

echo "$TIMESTAMP | Concepts: $CONCEPTS | Links: $LINKS" >> docs.metrics.log
tail -10 docs.metrics.log
```

Run regularly (e.g., daily cron):
```bash
0 9 * * * cd /path/to/project && bash track-growth.sh
```

### Health Dashboard

Generate metrics report:

```python
#!/usr/bin/env python3
# health-report.py

import subprocess
import json
from datetime import datetime

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

concepts = int(run_cmd("python3 src/mem_graph.py --root docs headers --all | wc -l"))
links = int(run_cmd("grep -r '\\[.*\\](.*' docs --include='*.md' | wc -l"))

avg_links_per_concept = links / concepts if concepts > 0 else 0

report = {
    "timestamp": datetime.now().isoformat(),
    "concepts": concepts,
    "links": links,
    "avg_links_per_concept": round(avg_links_per_concept, 2),
    "link_density": "optimal" if 2 <= avg_links_per_concept <= 4 else "warning"
}

print(json.dumps(report, indent=2))
```

Run:
```bash
python3 health-report.py
```

---

## Content Generation

### Generate Table of Contents

Create TOC from headers:

```python
#!/usr/bin/env python3
# generate-toc.py

import subprocess
import sys

def get_headers(file):
    cmd = f"python3 src/mem_graph.py --root docs headers --file {file} --all"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip().split('\n')

if len(sys.argv) < 2:
    print("Usage: generate-toc.py <file>")
    sys.exit(1)

file = sys.argv[1]
headers = get_headers(file)

print(f"# {file}\n")
for header in headers:
    if header.strip():
        slug = header.lower().replace(" ", "-")
        print(f"- [{header}](#{slug})")
```

Run:
```bash
python3 generate-toc.py concepts.md
```

### Generate Summary Index

Create index of all concepts:

```bash
#!/bin/bash
# generate-index.sh

cat > docs/_index.md << 'EOF'
# Complete Index

This is an auto-generated index of all concepts.

EOF

python3 src/mem_graph.py --root docs headers --all | while read concept; do
    file=$(echo "$concept" | cut -d'#' -f1)
    header=$(echo "$concept" | cut -d'#' -f2)
    slug=$(echo "$header" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')
    
    echo "- [$header](./$file#$slug)" >> docs/_index.md
done

echo "Generated docs/_index.md"
```

---

## Backup and Sync

### Automated Backups

Regular backup script:

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/docs_$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"
tar czf "$BACKUP_FILE" docs/

# Keep only last 10 backups
ls -t "$BACKUP_DIR"/*.tar.gz | tail -n +11 | xargs rm -f

echo "Backed up to $BACKUP_FILE"
```

Run as cron job:
```bash
# Daily at 3 AM
0 3 * * * cd /path/to/project && bash backup.sh
```

### Sync to Remote

Sync graph to cloud storage:

```bash
#!/bin/bash
# sync-remote.sh

TARGET="s3://my-bucket/docs"

echo "Syncing docs to $TARGET"
aws s3 sync docs/ "$TARGET" --delete

echo "Synced"
```

---

## Search and Query Tools

### Full-Text Search

Find concepts by content:

```bash
#!/bin/bash
# search.sh

QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 <search-term>"
    exit 1
fi

echo "Searching for: $QUERY"
grep -r "$QUERY" docs --include="*.md" -l | while read file; do
    echo "- $file"
done
```

### Concept Cross-Linker

Suggest missing links:

```python
#!/usr/bin/env python3
# suggest-links.py

import os
import re

# Get all concept names
concepts = {}
for root, dirs, files in os.walk("docs"):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            with open(path) as f:
                for match in re.finditer(r'^## (.+)$', f.read(), re.MULTILINE):
                    concept = match.group(1)
                    slug = concept.lower().replace(" ", "-")
                    concepts[concept.lower()] = (path, slug)

# Find unlinked mentions
for root, dirs, files in os.walk("docs"):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            with open(path) as f:
                content = f.read()
            
            for concept_lower, (target_file, slug) in concepts.items():
                # Check if mentioned but not linked
                pattern = rf'\b{concept_lower}\b(?!\])'
                matches = re.finditer(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    # Skip if already linked
                    if f']{slug}' in content[max(0, match.start()-50):match.end()]:
                        continue
                    
                    print(f"Suggest linking '{concept_lower}' in {path}")
```

---

## Documentation Generation

### API Reference Auto-Generator

Generate reference from docstrings:

```python
#!/usr/bin/env python3
# generate-api-docs.py

import ast
import inspect

def generate_md(module_path):
    with open(module_path) as f:
        tree = ast.parse(f.read())
    
    output = f"# API Reference\n\n"
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            output += f"## {node.name}\n\n"
            if ast.get_docstring(node):
                output += f"{ast.get_docstring(node)}\n\n"
    
    return output

# Generate and save
output = generate_md("src/mem_graph.py")
with open("docs/api-reference.md", "w") as f:
    f.write(output)
```

---

## Debugging Tools

### Link Validator Debug

Detailed link validation:

```python
#!/usr/bin/env python3
# debug-links.py

import re
import os
from pathlib import Path

def find_links(content):
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    return re.findall(pattern, content)

def validate_link(link, current_file):
    text, target = link
    
    if target.startswith("http"):
        return "external", True
    
    if target.startswith("#"):
        return "same-file", True  # Simplified
    
    if "/" in target:
        file_path, anchor = target.split("#") if "#" in target else (target, "")
        full_path = os.path.join(os.path.dirname(current_file), file_path)
        exists = os.path.exists(full_path)
        return f"file:{target}", exists
    
    return "other", False

# Check all links
for root, dirs, files in os.walk("docs"):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            with open(path) as f:
                content = f.read()
            
            links = find_links(content)
            for link in links:
                link_type, valid = validate_link(link, path)
                status = "✓" if valid else "✗"
                print(f"{status} {path}: {link_type} - [{link[0]}]({link[1]})")
```

See [Workflows](./workflows.md#maintaining-quality) for maintaining and organizing knowledge.
