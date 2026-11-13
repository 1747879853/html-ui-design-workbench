# Verify all state and helper functions that must be preserved
with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Length of file:", len(text))
# Check what modals exist
modals = re.findall(r'<a-modal[^>]*|<a-drawer[^>]*', text)
print("Modals & Drawers:", len(modals))
for m in modals:
    print("  ", m[:60])
