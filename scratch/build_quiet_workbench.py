import re

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    full_text = f.read()

# Extract the script
idx_script = full_text.find('<script>')
script_block = full_text[idx_script:]

# Extract modals and drawers
idx_drawers = full_text.find('<!-- ====================================================================\n             弹窗 1：添加费用抽屉')
modals_block = full_text[idx_drawers:idx_script]

print("Successfully extracted script and modals")
