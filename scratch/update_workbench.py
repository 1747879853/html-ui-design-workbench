import re

with open('scratch/build_comprehensive_workbench.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's replace the self-closing tags with explicit closing tags and optimize the 3 compound controls
