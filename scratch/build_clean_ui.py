import re

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    orig_html = f.read()

# Extract JavaScript block from orig_html
js_match = re.search(r'(<script>\s*const\s*\{\s*createApp.*?</script>)', orig_html, re.DOTALL)
if not js_match:
    print("ERROR: could not find script block")
    exit(1)
js_code = js_match.group(1)

# Extract modals and drawers from orig_html
modals_match = re.search(r'(<!--\s*抽屉与弹窗.*?)(?=</div>\s*<!--\s*end\s*pa-workbench|\s*</div>\s*</a-config-provider>)', orig_html, re.DOTALL)
if not modals_match:
    print("ERROR: could not find modals block")
    # try alternative pattern
    idx = orig_html.find('<!-- 抽屉 1：添加业务费用抽屉')
    if idx != -1:
        end_idx = orig_html.find('</div>\n    </a-config-provider>')
        modals_code = orig_html[idx:end_idx]
    else:
        print("Fallback search for drawers failed")
        exit(1)
else:
    modals_code = modals_match.group(1)

print("Extracted JS (length:", len(js_code), ") and Modals (length:", len(modals_code), ")")
