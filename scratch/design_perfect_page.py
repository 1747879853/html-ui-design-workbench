# Let's write the complete, immaculate implementation
import re

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_script = text.find('<script>')
script_block = text[idx_script:]

idx_drawers = text.find('<!-- ====================================================================\n             弹窗 1：添加费用抽屉')
modals_block = text[idx_drawers:idx_script]

print("Script length:", len(script_block))
print("Modals length:", len(modals_block))
