import re

with open('pages/comprehensive-business-edit.html', 'r', encoding='utf-8') as f:
    content = f.read()

# find any <(a-[a-z0-9-]+|iconify-icon)[^>]*/>
matches = list(re.finditer(r'<((?:a-[a-z0-9-]+|iconify-icon)[^>]*?)/>', content, re.DOTALL))
print(f"Found {len(matches)} self-closing custom tags:")
for m in matches:
    tag_content = m.group(1).strip()
    tag_name = tag_content.split()[0]
    first_line = tag_content.split('\n')[0]
    print(f"Tag: <{tag_name}> -> {first_line[:60]}...")
