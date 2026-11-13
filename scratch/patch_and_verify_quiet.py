import re

with open('scratch/quiet_payment_edit.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Set default activeDeckTab to 'invoice'
html = html.replace("const activeDeckTab = ref('workflow');", "const activeDeckTab = ref('invoice');")
html = html.replace("activeDeckTab.value = 'workflow';", "activeDeckTab.value = key === 'S3' ? 'workflow' : 'invoice';")

# 2. Fix date width and add payment memo to Row 2 of Header
old_row2_mid = '''              <span class="pa-flow-label" style="margin-left: 6px;">时效:</span>
              <a-date-picker
                v-model:value="formState.latestPaymentDate"
                size="small"
                value-format="YYYY-MM-DD"
                placeholder="最晚付款"
                style="width: 95px;"
                :disabled="!isMainFormEditable"
                @change="markMainFormDirty"
              ></a-date-picker>
              <span style="color: #cbd5e1;">~</span>
              <a-date-picker
                v-model:value="formState.predictReturnDate"
                size="small"
                value-format="YYYY-MM-DD"
                placeholder="预计回款"
                style="width: 95px;"
                :disabled="!isMainFormEditable"
                @change="markMainFormDirty"
              ></a-date-picker>'''

new_row2_mid = '''              <span class="pa-flow-label" style="margin-left: 6px;">付款日:</span>
              <a-date-picker
                v-model:value="formState.latestPaymentDate"
                size="small"
                value-format="YYYY-MM-DD"
                placeholder="最晚付款"
                style="width: 105px;"
                :disabled="!isMainFormEditable"
                @change="markMainFormDirty"
              ></a-date-picker>
              <span style="color: #cbd5e1;">~</span>
              <a-date-picker
                v-model:value="formState.predictReturnDate"
                size="small"
                value-format="YYYY-MM-DD"
                placeholder="预计回款"
                style="width: 105px;"
                :disabled="!isMainFormEditable"
                @change="markMainFormDirty"
              ></a-date-picker>

              <a-input
                v-model:value="formState.paymentDemand"
                size="small"
                placeholder="附言/支付要求..."
                :title="formState.paymentDemand"
                style="width: 120px;"
                :disabled="!isMainFormEditable"
                allow-clear
                @change="markMainFormDirty"
              ></a-input>'''

if old_row2_mid in html:
    html = html.replace(old_row2_mid, new_row2_mid)
    print("Replaced row2 date & memo")
else:
    print("WARNING: old_row2_mid not found")

# 3. Update pa-dock-card height to 260px
html = html.replace(
    'flex: 0 0 240px;\n      height: 240px;',
    'flex: 0 0 260px;\n      height: 260px;'
)

with open('scratch/quiet_payment_edit.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Also copy this into pages/payment-application-edit.html directly
with open('pages/payment-application-edit.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Applied quiet layout directly to pages/payment-application-edit.html!")
