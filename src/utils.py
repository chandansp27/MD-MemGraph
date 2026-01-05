import re

# ONLY semantic links: [[target | relation]]
SEMANTIC_LINK_RE = re.compile(r'\[\[([^\]|]+)\|([^\]]+)\]\]')
PLAIN_LINK_RE = re.compile(r'\[\[([^\]|]+)\]\]')

# Header matching: lines like "# Heading" (1-6 #)
HEADER_RE = re.compile(r'^\s{0,3}(#{1,6})\s*(.+)$', re.MULTILINE)

# code-fence remover: triple backticks or ~~~ with optional language
FENCE_RE_1 = r'^```[^\n]*$.*?^```\s*$'
FENCE_RE_2 = r'^~~~[^\n]*$.*?^~~~\s*$'