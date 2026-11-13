import re

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Header Actions: New Blank button wrapped in a-popconfirm
old_new_blank = '''            <a-button size="small" @click="handleOpenBlankNew">
              <template #icon><iconify-icon icon="ant-design:plus-outlined"></iconify-icon></template>
              新建空白
            </a-button>'''

new_new_blank = '''            <a-popconfirm
              title="确认新建空白申请单？"
              description="新建将重置当前编辑态并创建空白单据，未保存数据将丢失。"
              ok-text="确认新建"
              cancel-text="取消"
              @confirm="handleOpenBlankNew"
            >
              <a-button size="small">
                <template #icon><iconify-icon icon="ant-design:plus-outlined"></iconify-icon></template>
                新建空白
              </a-button>
            </a-popconfirm>'''

if old_new_blank in html:
    html = html.replace(old_new_blank, new_new_blank)
    print("Replaced handleOpenBlankNew with Popconfirm")
else:
    print("WARNING: old_new_blank not found!")

# 2. Update Column 2 bank card icon & border style
old_col2_card = '''            <div class="pa-acc-card" :title="myCompanyBank.bankName + ' · ' + myCompanyBank.accountNo">
              <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                <iconify-icon icon="ant-design:bank-outlined" style="margin-right: 3px; color: #64748b;"></iconify-icon>
                <strong>{{ myCompanyBank.shortName }}</strong>
                <span class="tabular-nums" style="margin-left: 4px; font-family: monospace;">{{ myCompanyBank.accountNo }}</span>
              </div>
              <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-btn" @click="copyText(myCompanyBank.accountNo, '我司付款账号')"></iconify-icon>
            </div>'''

new_col2_card = '''            <div class="pa-acc-card" :title="myCompanyBank.bankName + ' · ' + myCompanyBank.accountNo">
              <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: flex; align-items: center; gap: 4px;">
                <iconify-icon icon="ant-design:bank-outlined" style="color: #2563eb;"></iconify-icon>
                <strong>{{ myCompanyBank.shortName }}</strong>
                <span class="tabular-nums" style="font-family: monospace; font-weight: 600;">{{ myCompanyBank.accountNo }}</span>
              </div>
              <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-btn" @click="copyText(myCompanyBank.accountNo, '我司付款账号')"></iconify-icon>
            </div>'''

if old_col2_card in html:
    html = html.replace(old_col2_card, new_col2_card)
    print("Replaced col2 bank card")
else:
    print("WARNING: old_col2_card not found!")

# 3. Update Column 4 date inputs with ~ connector and memo title
old_col4_dates = '''            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
              <a-date-picker
                v-model:value="formState.latestPaymentDate"
                size="small"
                value-format="YYYY-MM-DD"
                style="width: 100%;"
                :disabled="!isMainFormEditable"
                placeholder="最晚付款日"
                @change="markMainFormDirty"
              ></a-date-picker>
              <a-date-picker
                v-model:value="formState.predictReturnDate"
                size="small"
                value-format="YYYY-MM-DD"
                style="width: 100%;"
                :disabled="!isMainFormEditable"
                placeholder="预计回款日"
                @change="markMainFormDirty"
              ></a-date-picker>
            </div>
            <a-input
              v-model:value="formState.paymentDemand"
              size="small"
              placeholder="汇款附言/支付要求 (限1024字)..."
              :disabled="!isMainFormEditable"
              @change="markMainFormDirty"
            ></a-input>'''

new_col4_dates = '''            <div style="display: flex; align-items: center; gap: 4px;">
              <a-date-picker
                v-model:value="formState.latestPaymentDate"
                size="small"
                value-format="YYYY-MM-DD"
                style="flex: 1; min-width: 0;"
                :disabled="!isMainFormEditable"
                placeholder="最晚付款日"
                @change="markMainFormDirty"
              ></a-date-picker>
              <span style="color: #94a3b8; font-size: 11px;">~</span>
              <a-date-picker
                v-model:value="formState.predictReturnDate"
                size="small"
                value-format="YYYY-MM-DD"
                style="flex: 1; min-width: 0;"
                :disabled="!isMainFormEditable"
                placeholder="预计回款日"
                @change="markMainFormDirty"
              ></a-date-picker>
            </div>
            <a-input
              v-model:value="formState.paymentDemand"
              size="small"
              :title="formState.paymentDemand"
              placeholder="汇款附言/支付要求 (限1024字)..."
              :disabled="!isMainFormEditable"
              @change="markMainFormDirty"
            ></a-input>'''

if old_col4_dates in html:
    html = html.replace(old_col4_dates, new_col4_dates)
    print("Replaced col4 dates and memo")
else:
    print("WARNING: old_col4_dates not found!")

# 4. Update Column 5 difference row when invoiceProcess === 2
old_col5_diff = '''            <div v-else style="font-size: 10px; color: #64748b; display: flex; align-items: center; justify-content: space-between;">
              <span>发票差额：¥{{ formatDecimal(invoiceDiffAmount) }}</span>
              <span :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#ea580c' }">
                {{ invoiceDiffAmount === 0 ? '票费已平' : '有差额' }}
              </span>
            </div>'''

new_col5_diff = '''            <div v-else-if="formState.invoiceProcess === 2" style="font-size: 10px; color: #15803d; display: flex; align-items: center; justify-content: space-between;">
              <span>发票核对：免开票业务</span>
              <a-tag color="success" style="font-size: 9px; line-height: 14px; margin: 0; padding: 0 4px;">免开票已合规</a-tag>
            </div>
            <div v-else style="font-size: 10px; color: #64748b; display: flex; align-items: center; justify-content: space-between;">
              <span>发票差额：¥{{ formatDecimal(invoiceDiffAmount) }}</span>
              <span :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#ea580c', fontWeight: 600 }">
                {{ invoiceDiffAmount === 0 ? '票费已平' : '待补票差' }}
              </span>
            </div>'''

if old_col5_diff in html:
    html = html.replace(old_col5_diff, new_col5_diff)
    print("Replaced col5 difference row")
else:
    print("WARNING: old_col5_diff not found!")

# 5. Insert Telemetry Strip above pa-fee-footer
old_fee_footer = '          <!-- 费用底部汇总栏 -->\n          <div class="pa-fee-footer">'

telemetry_strip = '''          <!-- 金融往来底账与风控透视条 (充实决策上下文 · 消灭纯白大黑洞) -->
          <div class="pa-telemetry-strip">
            <div class="pa-telem-card">
              <div class="pa-telem-icon" style="background: #eff6ff; color: #2563eb;">
                <iconify-icon icon="ant-design:history-outlined"></iconify-icon>
              </div>
              <div class="pa-telem-info">
                <div class="pa-telem-label">本月往来规模 (已付款)</div>
                <div class="pa-telem-val">
                  <strong class="tabular-nums">¥18,520.00</strong>
                  <span class="pa-telem-sub">共 6 笔 · 履约率 100%</span>
                </div>
              </div>
            </div>

            <div class="pa-telem-card">
              <div class="pa-telem-icon" style="background: #f0fdf4; color: #16a34a;">
                <iconify-icon icon="ant-design:safety-certificate-outlined"></iconify-icon>
              </div>
              <div class="pa-telem-info">
                <div class="pa-telem-label">授信额度与合作账期</div>
                <div class="pa-telem-val">
                  <strong class="tabular-nums">月结 30 天</strong>
                  <span class="pa-telem-sub">剩余额度 ¥81,480.00</span>
                </div>
              </div>
            </div>

            <div class="pa-telem-card">
              <div class="pa-telem-icon" style="background: #fff7ed; color: #ea580c;">
                <iconify-icon icon="ant-design:alert-outlined"></iconify-icon>
              </div>
              <div class="pa-telem-info">
                <div class="pa-telem-label">垫资风控与未结敞口</div>
                <div class="pa-telem-val">
                  <strong class="tabular-nums" :style="{ color: formState.isReceiveAllSettled ? '#16a34a' : '#ea580c' }">
                    {{ formState.isReceiveAllSettled ? '已结清 (无敞口)' : ('未结 ' + unSettledReceiveSummaryText) }}
                  </strong>
                  <span class="pa-telem-sub">关联合同应收已审</span>
                </div>
              </div>
            </div>

            <div class="pa-telem-card">
              <div class="pa-telem-icon" style="background: #f5f3ff; color: #7c3aed;">
                <iconify-icon icon="ant-design:audit-outlined"></iconify-icon>
              </div>
              <div class="pa-telem-info">
                <div class="pa-telem-label">在途审批付款单</div>
                <div class="pa-telem-val">
                  <strong class="tabular-nums">2 笔在途</strong>
                  <span class="pa-telem-sub">冻结敞口 ¥3,200.00</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 费用底部汇总栏 -->
          <div class="pa-fee-footer">'''

if old_fee_footer in html:
    html = html.replace(old_fee_footer, telemetry_strip)
    print("Inserted telemetry strip")
else:
    print("WARNING: old_fee_footer not found!")

# 6. Update inner child table settledAmount color (neutralize bright green)
old_settled = '<td style="text-align: right; color: #16a34a;" class="tabular-nums">{{ formatMoney(fee.settledAmount, fee.currencyCode) }}</td>'
new_settled = '<td style="text-align: right; color: #64748b;" class="tabular-nums">{{ formatMoney(fee.settledAmount, fee.currencyCode) }}</td>'
if old_settled in html:
    html = html.replace(old_settled, new_settled)
    print("Neutralized settledAmount color")

# 7. Update Bottom Left Invoice Center: Discrepancy header and buttons disabled when invoiceProcess === 2
old_inv_deck_header = '''              <div style="display: flex; align-items: center; gap: 6px;">
                <!-- 票费实时对比 -->
                <span style="font-size: 11px; color: #64748b;">
                  票 ¥{{ formatDecimal(totalInvoiceAmount) }} / 应付 ¥{{ formatDecimal(totalPayAmountRMB) }}
                  <span :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#ea580c', fontWeight: 600, marginLeft: '4px' }">
                    (差额: ¥{{ formatDecimal(invoiceDiffAmount) }})
                  </span>
                </span>

                <a-tag :color="formState.isInvoiceAttachmentDown ? 'cyan' : 'default'" style="font-size: 10px; line-height: 16px; margin: 0;">
                  {{ formState.isInvoiceAttachmentDown ? '发票附件已打包' : '未下载' }}
                </a-tag>

                <a-space size="small" v-if="formState.invoiceProcess !== 2">
                  <a-button size="small" style="font-size: 11px; height: 22px; padding: 0 6px;" @click="showInputInvoicePicker = true">
                    从进项池选
                  </a-button>
                  <a-button size="small" type="primary" ghost style="font-size: 11px; height: 22px; padding: 0 6px;" @click="handleAddInvoiceRow">
                    + 录发票
                  </a-button>
                </a-space>
              </div>'''

new_inv_deck_header = '''              <div style="display: flex; align-items: center; gap: 6px;">
                <!-- 票费实时对比 / 免票指示 -->
                <template v-if="formState.invoiceProcess === 2">
                  <span style="font-size: 11px; color: #15803d; font-weight: 500;">
                    <iconify-icon icon="ant-design:safety-certificate-filled" style="margin-right: 3px;"></iconify-icon>
                    不开票业务 · 免核验发票
                  </span>
                  <a-tag color="success" style="font-size: 10px; line-height: 16px; margin: 0;">已合规豁免</a-tag>
                </template>
                <template v-else>
                  <span style="font-size: 11px; color: #64748b;">
                    票 ¥{{ formatDecimal(totalInvoiceAmount) }} / 应付 ¥{{ formatDecimal(totalPayAmountRMB) }}
                    <span :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#ea580c', fontWeight: 600, marginLeft: '4px' }">
                      (差额: ¥{{ formatDecimal(invoiceDiffAmount) }})
                    </span>
                  </span>
                  <a-tag :color="formState.isInvoiceAttachmentDown ? 'cyan' : 'default'" style="font-size: 10px; line-height: 16px; margin: 0;">
                    {{ formState.isInvoiceAttachmentDown ? '发票附件已打包' : '未下载' }}
                  </a-tag>
                </template>

                <a-space size="small">
                  <a-button size="small" style="font-size: 11px; height: 22px; padding: 0 6px;" :disabled="formState.invoiceProcess === 2" @click="showInputInvoicePicker = true">
                    从进项池选
                  </a-button>
                  <a-button size="small" type="primary" ghost style="font-size: 11px; height: 22px; padding: 0 6px;" :disabled="formState.invoiceProcess === 2" @click="handleAddInvoiceRow">
                    + 录发票
                  </a-button>
                </a-space>
              </div>'''

if old_inv_deck_header in html:
    html = html.replace(old_inv_deck_header, new_inv_deck_header)
    print("Replaced invoice deck header")
else:
    print("WARNING: old_inv_deck_header not found!")

# 8. Update Invoice Empty Box when invoiceProcess === 2
old_inv_empty = '''            <div v-else style="padding: 24px; text-align: center; color: #94a3b8; font-size: 12px;">
              当前单据选择「不开票」，无需提供发票明细。
            </div>'''

new_inv_empty = '''            <div v-else class="pa-no-invoice-box">
              <div class="pa-no-inv-icon">
                <iconify-icon icon="ant-design:safety-certificate-outlined"></iconify-icon>
              </div>
              <div class="pa-no-inv-content">
                <div class="pa-no-inv-title">
                  <span>当前业务适用「不开票」付款通道</span>
                  <a-tag color="success" style="font-size: 10px; line-height: 16px;">免除进项票勾稽</a-tag>
                </div>
                <div class="pa-no-inv-desc">
                  根据企业财务结算制度，本单属于港口安保规费 / 行政性收费 / 免税业务，无需提供进项增值税专用发票。
                  系统在发起送审、财务初审及出纳付款全流程中已自动豁免发票差额拦截，审核通过后可直接安排打款。
                </div>
                <div class="pa-no-inv-actions">
                  <span style="font-size: 11px; color: #64748b;">如供货方后续补开发票，可随时切换：</span>
                  <a-button size="small" type="link" style="font-size: 11px; padding: 0;" @click="formState.invoiceProcess = 1; markMainFormDirty();">
                    切换为「先票后付」录入发票
                  </a-button>
                  <span style="color: #cbd5e1;">|</span>
                  <a-button size="small" type="link" style="font-size: 11px; padding: 0;" @click="formState.invoiceProcess = 0; markMainFormDirty();">
                    切换为「先付后票」
                  </a-button>
                </div>
              </div>
            </div>'''

if old_inv_empty in html:
    html = html.replace(old_inv_empty, new_inv_empty)
    print("Replaced invoice empty compliance card")
else:
    print("WARNING: old_inv_empty not found!")

# 9. Dynamic Draft Node Comment in Workflow
old_node_comment = '''                  <div v-if="node.comment" style="margin-top: 3px; padding: 3px 6px; border-radius: 3px; font-size: 10px;" :style="{ background: node.status === 'rejected' ? '#fee2e2' : '#f1f5f9', color: node.status === 'rejected' ? '#991b1b' : '#334155' }">
                    {{ node.comment }}
                  </div>'''

new_node_comment = '''                  <div v-if="node.comment || (nIdx === 0 && formState.status === 0)" style="margin-top: 3px; padding: 3px 6px; border-radius: 3px; font-size: 10px;" :style="{ background: node.status === 'rejected' ? '#fee2e2' : '#f1f5f9', color: node.status === 'rejected' ? '#991b1b' : '#334155' }">
                    <span v-if="nIdx === 0 && formState.status === 0">{{ draftNodeComment }}</span>
                    <span v-else>{{ node.comment }}</span>
                  </div>'''

if old_node_comment in html:
    html = html.replace(old_node_comment, new_node_comment)
    print("Replaced workflow node dynamic comment")
else:
    print("WARNING: old_node_comment not found!")

# 10. Add draftNodeComment computed in JS
old_computed = "const isMainFormEditable = computed(() => {"
new_computed = """const draftNodeComment = computed(() => {
          if (formState.invoiceProcess === 2) {
            return '草稿已生成，不开票业务送审将直接进入初审并免除发票勾稽。';
          } else if (formState.invoiceProcess === 0) {
            return '草稿已生成，先付后票业务出款后须在规定账期内补齐发票。';
          } else {
            return '草稿已生成，先票后付业务送审前须补齐发票明细。';
          }
        });

        const isMainFormEditable = computed(() => {"""

if old_computed in html:
    html = html.replace(old_computed, new_computed, 1)
    print("Added draftNodeComment computed property")
else:
    print("WARNING: old_computed not found!")

# 11. Add Toast in copyText
old_copy = """const copyText = (text, label) => {
          if (!text) return;
          if (navigator.clipboard) {
            navigator.clipboard.writeText(String(text));
          }"""

new_copy = """const copyText = (text, label) => {
          if (!text) return;
          if (navigator.clipboard) {
            navigator.clipboard.writeText(String(text));
          }
          antd.message.success(`${label || '内容'}已复制到剪贴板`);"""

if old_copy in html:
    html = html.replace(old_copy, new_copy, 1)
    print("Updated copyText with AntD message success toast")
else:
    print("WARNING: old_copy not found!")

with open('pages/payment-application-edit.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("All refinements applied!")
