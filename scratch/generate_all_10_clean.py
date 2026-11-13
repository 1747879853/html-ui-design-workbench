# coding: utf-8
import os

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    orig_text = f.read()

idx_drawers = orig_text.find('<!-- ====================================================================\n             弹窗 1：添加费用抽屉')
idx_script = orig_text.find('<script>')

modals_block = orig_text[idx_drawers:idx_script]
script_block = orig_text[idx_script:]

base_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITLE__</title>
  <link rel="stylesheet" href="../assets/vendor/reset.css">
  <link rel="stylesheet" href="../assets/css/common.css">
  <script src="../assets/vendor/dayjs-bundle.min.js"></script>
  <script src="../assets/vendor/vue.global.prod.js"></script>
  <script src="../assets/vendor/antd.min.js"></script>
  <script src="../assets/vendor/iconify-icon.min.js"></script>
  <script src="../assets/js/common.js"></script>
  <style>
    [v-cloak] { display: none !important; }
    body {
      background-color: #f8fafc;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
      margin: 0; padding: 0; font-size: 12px; overflow-x: hidden;
    }
    .tabular-nums { font-variant-numeric: tabular-nums; font-feature-settings: "tnum"; }
    .wb-scenario-bar {
      display: flex; align-items: center; justify-content: space-between; gap: 8px;
      background: #0f172a; color: #f8fafc; border-radius: 4px; padding: 3px 10px; flex-shrink: 0;
    }
    .wb-scenario-left, .wb-scenario-right { display: flex; align-items: center; gap: 6px; }
    .wb-scenario-title { font-size: 11px; font-weight: 600; color: #38bdf8; display: inline-flex; align-items: center; gap: 4px; }
    .wb-scenario-pill {
      display: inline-flex; align-items: center; gap: 4px; padding: 1px 7px; border-radius: 3px;
      font-size: 11px; cursor: pointer; background: rgba(255, 255, 255, 0.08); color: #cbd5e1;
      border: 1px solid rgba(255, 255, 255, 0.12); transition: all 0.15s ease; user-select: none;
    }
    .wb-scenario-pill:hover { background: rgba(255, 255, 255, 0.15); color: #fff; }
    .wb-scenario-pill.active { background: #2563eb; color: #ffffff; border-color: #3b82f6; font-weight: 600; }
    .dir-badge-pill {
      background: #3b82f6; color: #fff; font-size: 10px; padding: 1px 6px; border-radius: 3px; font-weight: 600;
    }
    .pa-status-tag { display: inline-flex; align-items: center; gap: 3px; padding: 1px 6px; border-radius: 3px; font-size: 11px; font-weight: 600; }
    .pa-status-0 { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
    .pa-status-1 { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }
    .pa-status-2 { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
    .pa-status-3 { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
    .pa-status-4 { background: #ecfeff; color: #0e7490; border: 1px solid #a5f3fc; }
    .pa-status-5 { background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; }
    .pa-link { color: #2563eb; font-weight: 600; cursor: pointer; text-decoration: none; }
    .pa-link:hover { text-decoration: underline; }
    .pa-copy-icon { color: #94a3b8; cursor: pointer; margin-left: 3px; font-size: 11px; }
    .pa-copy-icon:hover { color: #2563eb; }
    .pa-dir-badge { display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 2px; font-size: 10px; font-weight: 700; }
    .pa-dir-pay { background: #fff7ed; color: #ea580c; border: 1px solid #fdba74; }
    .pa-dir-rec { background: #eff6ff; color: #2563eb; border: 1px solid #93c5fd; }
    .pa-status-alert {
      padding: 4px 12px; border-radius: 4px; display: flex; align-items: center; justify-content: space-between; gap: 8px; font-size: 11px; flex-shrink: 0;
    }
    .pa-alert-reject { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; }
    .pa-doc-code { font-family: ui-monospace, SFMono-Regular, monospace; font-size: 14px; font-weight: 700; color: #0f172a; }
    .pa-voucher-toolbar { padding: 5px 12px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #f1f5f9; background: #ffffff; border-radius: 6px 6px 0 0; }
    __EXTRA_CSS__
  </style>
</head>
<body>
  <div id="app" v-cloak>
    <div style="height: 100vh; max-height: 1080px; padding: 6px 12px 10px; box-sizing: border-box; display: flex; flex-direction: column; gap: 6px; max-width: 1920px; margin: 0 auto; overflow: hidden;">
      <!-- 场景沙盒栏 -->
      <div class="wb-scenario-bar">
        <div class="wb-scenario-left">
          <span class="wb-scenario-title">业务沙盒:</span>
          <div
            v-for="s in scenarioList"
            :key="s.key"
            class="wb-scenario-pill"
            :class="{ active: currentScenarioKey === s.key }"
            @click="switchScenario(s.key)"
          >
            <span>{{ s.label }}</span>
          </div>
        </div>
        <div class="wb-scenario-right">
          <span class="dir-badge-pill">__DIR_TAG__</span>
          <a-button size="small" type="primary" ghost style="font-size: 10px; height: 20px; padding: 0 6px;" @click="showAddFeeDrawer = true">
            + 选费测试
          </a-button>
          <a-button size="small" type="primary" style="font-size: 10px; height: 20px; padding: 0 6px;" @click="showHandoffDrawer = true">
            交接文档
          </a-button>
        </div>
      </div>

      __BODY__

    </div>
    __MODALS__
    __SCRIPT__
  </div>
</body>
</html>"""

top_bar = """
      <div class="pa-voucher-toolbar">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="color: #64748b;">申请单号:</span>
          <span class="pa-doc-code">{{ formState.applicationNo }}</span>
          <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-icon" @click="copyText(formState.applicationNo, '申请单号')"></iconify-icon>

          <span class="pa-status-tag" :class="'pa-status-' + formState.status">
            <iconify-icon :icon="getStatusIcon(formState.status)"></iconify-icon>
            {{ currentStatusMeta.stampText }}
          </span>

          <span style="color: #cbd5e1;">|</span>
          <span style="color: #64748b;">申请人:</span>
          <strong style="color: #334155;">{{ formState.creatorUserName }}</strong>

          <template v-if="formState.submitTime">
            <span style="color: #64748b; margin-left: 4px;">提交:</span>
            <span class="tabular-nums" style="color: #64748b;">{{ formState.submitTime }}</span>
          </template>
        </div>

        <div style="display: flex; align-items: center; gap: 6px;">
          <a-button size="small" style="font-size: 11px;" @click="handleCreateBlank">新建空白</a-button>
          <a-button size="small" style="font-size: 11px;" :disabled="!isMainFormEditable" @click="handleSaveDraft">保存草稿</a-button>
          <a-button size="small" type="primary" style="font-size: 11px;" :disabled="!canSubmit" @click="handleSubmitAudit">
            {{ formState.status === 2 ? '重新送审' : '提交送审' }}
          </a-button>
          <a-dropdown>
            <template #overlay>
              <a-menu @click="handleExportAction">
                <a-menu-item key="excel">导出 Excel</a-menu-item>
                <a-menu-item key="pdf">导出 PDF</a-menu-item>
              </a-menu>
            </template>
            <a-button size="small" style="font-size: 11px;">
              导出 <iconify-icon icon="ant-design:down-outlined" style="font-size: 9px;"></iconify-icon>
            </a-button>
          </a-dropdown>
          <a-button size="small" style="font-size: 11px;" @click="handlePrintDoc">打印</a-button>
        </div>
      </div>
"""

rejection_alert = """
      <div v-if="formState.status === 2" class="pa-status-alert pa-alert-reject">
        <div style="display: flex; align-items: center; gap: 6px;">
          <iconify-icon icon="ant-design:close-circle-filled" style="color: #dc2626; font-size: 13px;"></iconify-icon>
          <strong>审批已驳回：</strong>
          <span>{{ (workflowNodes[1] || {}).comment || '请补充水单盖章件后重新提交。' }}</span>
          <span style="color: #64748b; margin-left: 8px;">(审核人: {{ (workflowNodes[1] || {}).operatorName }} · {{ (workflowNodes[1] || {}).operateTime }})</span>
        </div>
        <a-tag color="error" style="font-size: 10px; line-height: 16px; margin: 0;">需修改后重新送审</a-tag>
      </div>
"""

def generate_file(filename, title, dir_tag, extra_css, body_html, extra_script="", extra_returns=""):
    s_block = script_block
    if extra_script:
        idx_ret = s_block.rfind('return {')
        s_block = s_block[:idx_ret] + extra_script + "\n" + s_block[idx_ret:]
    if extra_returns:
        idx_ret_brace = s_block.rfind('return {') + len('return {')
        s_block = s_block[:idx_ret_brace] + "\n          " + extra_returns + "," + s_block[idx_ret_brace:]

    full_html = base_template.replace('__TITLE__', title)\
                             .replace('__DIR_TAG__', dir_tag)\
                             .replace('__EXTRA_CSS__', extra_css)\
                             .replace('__BODY__', body_html)\
                             .replace('__MODALS__', modals_block)\
                             .replace('__SCRIPT__', s_block)

    with open(os.path.join('pages', filename), 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Generated {filename}")

# ==============================================================================
# 1. Linear Split (64% / 36%)
# ==============================================================================
css_1 = """
    .dir1-split { display: grid; grid-template-columns: minmax(0, 64%) minmax(0, 36%); gap: 8px; flex: 1; overflow: hidden; }
    .dir1-left { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; flex-direction: column; overflow: hidden; }
    .dir1-right { display: flex; flex-direction: column; gap: 8px; overflow-y: auto; }
    .dir1-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px; }
    .dir1-card-head { font-size: 12px; font-weight: 700; color: #0f172a; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
"""

body_1 = rejection_alert + """
      <div class="pa-voucher-card" style="background:#fff; border:1px solid #e2e8f0; border-radius:6px;">
""" + top_bar + """
      </div>
      <div class="dir1-split">
        <div class="dir1-left">
          <div style="padding: 6px 12px; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <strong style="font-size: 13px; color: #0f172a;">业务费用明细主舞台</strong>
              <span style="color: #64748b; font-size: 11px;">共 {{ orderFeeGroups.length }} 票业务 · {{ totalFeeCount }} 笔费用</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
              <a-input v-model:value="feeFilters.orderNo" size="small" placeholder="搜索单号/提单/费用..." style="width: 170px;" allow-clear></a-input>
              <a-button size="small" type="primary" :disabled="!isMainFormEditable" @click="handleOpenAddFeeDrawer">+ 添加费用</a-button>
              <a-button size="small" @click="toggleAllFeeGroups">{{ isAllFeeGroupsExpanded ? '全部折叠' : '全部展开' }}</a-button>
            </div>
          </div>

          <div style="flex: 1; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
              <thead>
                <tr style="background: #f8fafc; color: #475569; position: sticky; top: 0; z-index: 2; border-bottom: 1px solid #e2e8f0;">
                  <th style="padding: 6px 8px; text-align: center; width: 32px;"><a-checkbox :checked="isAllFeesSelected" :indeterminate="isFeesPartiallySelected" :disabled="!isMainFormEditable" @change="handleSelectAllFees"></a-checkbox></th>
                  <th style="padding: 6px 8px; text-align: center; width: 32px;">序</th>
                  <th style="padding: 6px 8px; text-align: center; width: 45px;">收付</th>
                  <th style="padding: 6px 8px; text-align: left; width: 140px;">费用名称</th>
                  <th style="padding: 6px 8px; text-align: left; width: 55px;">币别</th>
                  <th style="padding: 6px 8px; text-align: right; width: 95px;">原金额</th>
                  <th style="padding: 6px 8px; text-align: right; width: 75px;">汇率</th>
                  <th style="padding: 6px 8px; text-align: right; width: 95px;">可申请余额</th>
                  <th style="padding: 6px 8px; text-align: right; width: 110px; background: #eff6ff; color: #1d4ed8;">本次申请金额</th>
                  <th style="padding: 6px 8px; text-align: left;">费用备注</th>
                  <th style="padding: 6px 8px; text-align: center; width: 50px;">操作</th>
                </tr>
              </thead>
              <tbody>
                <template v-for="(group, gIdx) in filteredOrderFeeGroups" :key="group.groupId || gIdx">
                  <tr style="background: #f1f5f9; border-top: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;">
                    <td style="text-align: center;"><a-checkbox :checked="isGroupAllSelected(group)" :indeterminate="isGroupPartiallySelected(group)" :disabled="!isMainFormEditable" @change="(e) => handleSelectGroupFees(group, e.target.checked)"></a-checkbox></td>
                    <td colspan="10" style="padding: 4px 8px;">
                      <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                          <span style="cursor: pointer;" @click="group.isExpanded = !group.isExpanded">
                            <iconify-icon :icon="group.isExpanded ? 'ant-design:down-outlined' : 'ant-design:right-outlined'" style="color:#64748b;"></iconify-icon>
                            <strong>业务 {{ gIdx + 1 }}:</strong>
                          </span>
                          <span>委托: <a class="pa-link" @click="handlePenetrateOrder(group.commissionNum)">{{ group.commissionNum }}</a></span>
                          <span v-if="group.mblNum">主单: <strong style="font-family: monospace;">{{ group.mblNum }}</strong></span>
                          <span>港口: {{ group.podName || '-' }} ({{ group.carrierName || '-' }} · {{ group.totalCtn || '-' }})</span>
                          <span>客户: {{ group.clientName || '-' }}</span>
                        </div>
                        <div>
                          <span v-if="group.unSettledReceiveList && group.unSettledReceiveList.some(r => r.amount > 0)" style="color: #d97706; font-weight: 700; font-size: 10px;">
                            ⚠️ 垫资: {{ group.unSettledReceiveList.filter(r => r.amount > 0).map(r => r.currency + ' ' + formatDecimal(r.amount)).join(', ') }}
                          </span>
                          <span v-else style="color: #16a34a; font-size: 10px;">✓ 客户已结清</span>
                        </div>
                      </div>
                    </td>
                  </tr>
                  <template v-if="group.isExpanded">
                    <tr v-for="(fee, fIdx) in group.filteredFees" :key="fee.id" style="border-bottom: 1px solid #f1f5f9;">
                      <td style="text-align: center;"><a-checkbox :checked="selectedFeeIds.includes(fee.id)" :disabled="!isMainFormEditable" @change="(e) => handleToggleFeeSelection(fee.id, e.target.checked)"></a-checkbox></td>
                      <td style="text-align: center;">{{ fIdx + 1 }}</td>
                      <td style="text-align: center;"><span class="pa-dir-badge" :class="fee.feeDirection === 1 ? 'pa-dir-pay' : 'pa-dir-rec'">{{ fee.feeDirection === 1 ? '付' : '收' }}</span></td>
                      <td><strong>{{ fee.feeCodeName }}</strong></td>
                      <td>{{ fee.currencyCode }}</td>
                      <td style="text-align: right;" class="tabular-nums">{{ formatMoney(fee.amount, fee.currencyCode) }}</td>
                      <td style="text-align: right;" class="tabular-nums">{{ Number(fee.exchangeRate || 1).toFixed(4) }}</td>
                      <td style="text-align: right;" class="tabular-nums">{{ formatMoney(fee.unRqstPaymentAmount, fee.currencyCode) }}</td>
                      <td style="text-align: right; background: #eff6ff;"><strong class="tabular-nums" style="color: #1d4ed8; font-size: 13px;">{{ formatMoney(fee.appliedAmount, fee.currencyCode) }}</strong></td>
                      <td style="color: #64748b;">{{ fee.itemRemark || '-' }}</td>
                      <td style="text-align: center;"><a-button type="link" danger size="small" style="padding:0;" @click="handleRemoveSelectedFees([fee.id])">移出</a-button></td>
                    </tr>
                  </template>
                </template>
              </tbody>
            </table>
          </div>

          <div style="padding: 6px 12px; background: #f8fafc; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 11px;">
            <span style="color: #64748b;">已勾选 {{ selectedFeeIds.length }} 笔费用</span>
            <div style="display: flex; gap: 10px;">
              <span v-for="cur in currencySummaryList" :key="cur.currencyCode">
                {{ cur.currencyCode }} 净付: <strong style="color: #0f172a; font-size: 13px;">{{ formatMoney(cur.netAmount, cur.currencyCode) }}</strong>
              </span>
            </div>
          </div>
        </div>

        <div class="dir1-right">
          <div class="dir1-card">
            <div class="dir1-card-head">
              <span>资金结算路由</span>
              <span style="color: #2563eb; font-weight: 700; font-size: 15px;">{{ primaryCurrencyCode }} {{ formatMoney(currencySummaryList[0]?.netAmount || 0, primaryCurrencyCode) }}</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 6px; font-size: 11px;">
              <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #64748b;">所属公司:</span>
                <a-select v-model:value="formState.companyId" size="small" style="width: 210px;" :disabled="!isMainFormEditable" :options="companyOptions" @change="handleCompanyChange"></a-select>
              </div>
              <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #64748b;">出款账户:</span>
                <span style="background: #f1f5f9; padding: 2px 6px; border-radius: 3px; font-family: monospace; width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ myCompanyBank.shortName }} {{ myCompanyBank.accountNo }}</span>
              </div>
              <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #64748b;">往来结算:</span>
                <strong style="width: 210px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ formState.settlementName }}</strong>
              </div>
              <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #64748b;">对方账户:</span>
                <a-select v-model:value="formState.bankAccountMap[primaryCurrencyCode]" size="small" style="width: 210px;" :disabled="!isMainFormEditable" :options="getPayeeBankOptions(primaryCurrencyCode)" @change="markMainFormDirty"></a-select>
              </div>
              <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #64748b;">付款排期:</span>
                <div style="display: flex; gap: 4px; width: 210px;">
                  <a-date-picker v-model:value="formState.latestPaymentDate" size="small" value-format="YYYY-MM-DD" style="flex:1;" placeholder="最晚出款" :disabled="!isMainFormEditable"></a-date-picker>
                  <a-date-picker v-model:value="formState.predictReturnDate" size="small" value-format="YYYY-MM-DD" style="flex:1;" placeholder="预计回款" :disabled="!isMainFormEditable"></a-date-picker>
                </div>
              </div>
            </div>
          </div>

          <div class="dir1-card" style="flex: 1; display: flex; flex-direction: column;">
            <div class="dir1-card-head">
              <div style="display: flex; align-items: center; gap: 6px;">
                <span>发票核对 ({{ formState.invoiceRows.length }})</span>
                <a-radio-group v-model:value="formState.invoiceProcess" size="small" :disabled="!isMainFormEditable" @change="handleInvoiceProcessChange">
                  <a-radio :value="1">先票后付</a-radio>
                  <a-radio :value="0">先付后票</a-radio>
                  <a-radio :value="2">不开票</a-radio>
                </a-radio-group>
              </div>
              <a-button size="small" type="primary" ghost style="font-size: 10px; height: 20px; padding: 0 4px;" @click="handleAddInvoiceRow">+ 录票</a-button>
            </div>
            <div style="font-size: 11px; margin-bottom: 6px; display: flex; justify-content: space-between; color: #64748b;">
              <span>已录: ¥{{ formatDecimal(totalInvoiceAmount) }}</span>
              <span>差额: <strong :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#d97706' }">{{ invoiceDiffAmount === 0 ? '✓ 票费已平' : ('待补 ¥' + formatDecimal(invoiceDiffAmount)) }}</strong></span>
            </div>
            <div style="flex: 1; overflow-y: auto;">
              <div v-for="(inv, idx) in formState.invoiceRows" :key="idx" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 6px; margin-bottom: 4px; font-size: 11px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                  <strong style="font-family: monospace;">{{ inv.invoiceNo || '待填发票号' }}</strong>
                  <strong style="color: #0f172a;">¥{{ formatDecimal(inv.invoiceAmount) }}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; color: #64748b; font-size: 10px; margin-top: 2px;">
                  <span>{{ inv.sellerName || '-' }}</span>
                  <span>{{ inv.invoiceDate || '-' }}</span>
                </div>
              </div>
              <div v-if="formState.invoiceRows.length === 0" style="text-align: center; color: #94a3b8; padding: 16px;">
                暂无录入发票
              </div>
            </div>
          </div>

          <div class="dir1-card">
            <div class="dir1-card-head">
              <span>审批流转跟踪</span>
              <span class="pa-status-tag" :class="'pa-status-' + formState.status" style="font-size: 10px;">{{ currentStatusMeta.stampText }}</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 4px;">
              <div v-for="node in workflowNodes" :key="node.nodeName" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 5px 8px; font-size: 11px;">
                <div style="display: flex; justify-content: space-between;">
                  <strong>{{ node.nodeName }} ({{ node.operatorName }})</strong>
                  <span :style="{ color: node.status === 'passed' ? '#16a34a' : (node.status === 'rejected' ? '#dc2626' : '#64748b'), fontWeight: 600, fontSize: '10px' }">{{ node.statusText }}</span>
                </div>
                <div v-if="node.comment" style="color: #dc2626; margin-top: 2px;">{{ node.comment }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
"""

generate_file('payment-app-dir1-linear-split.html', '付费申请 · 方向1：全屏左右双栏流式工作台 (Linear Split)', '方向 1: 左右流式', css_1, body_1)

# ==============================================================================
# 2. Bank Paper Check Voucher + Ledger Tabs
# ==============================================================================
css_2 = """
    .voucher-paper {
      background: #fffdf9; border: 2px solid #b45309; border-radius: 6px; padding: 10px 16px;
      position: relative; box-shadow: 0 4px 6px -1px rgba(180, 83, 9, 0.05); flex-shrink: 0;
    }
    .voucher-title {
      font-size: 15px; font-weight: 800; color: #92400e; letter-spacing: 2px; text-align: center;
      border-bottom: 2px double #b45309; padding-bottom: 4px; margin-bottom: 8px;
    }
    .voucher-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
    .voucher-box { background: #fff; border: 1px solid #fde68a; border-radius: 4px; padding: 4px 8px; font-size: 11px; }
    .tabs-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; flex: 1; display: flex; flex-direction: column; overflow: hidden; }
"""

body_2 = rejection_alert + """
      <div class="voucher-paper">
        <div class="voucher-title">企业对外付款申请记账凭证 (PAYMENT VOUCHER)</div>
        <div class="voucher-grid">
          <div class="voucher-box">
            <span style="color: #92400e;">申请单号: </span><strong>{{ formState.applicationNo }}</strong>
            <div style="margin-top: 3px; color: #64748b;">申请人: {{ formState.creatorUserName }} · 提交: {{ formState.submitTime || '草稿' }}</div>
          </div>
          <div class="voucher-box">
            <span style="color: #92400e;">付款抬头 (我司): </span><strong style="color: #0f172a;">{{ formState.companyName }}</strong>
            <div style="margin-top: 3px; color: #64748b;">账号: {{ myCompanyBank.shortName }} {{ myCompanyBank.accountNo }}</div>
          </div>
          <div class="voucher-box">
            <span style="color: #92400e;">收款对象 (往来): </span><strong style="color: #0f172a;">{{ formState.settlementName }}</strong>
            <div style="margin-top: 3px; color: #64748b;">账号: CMB 122908764510001</div>
          </div>
          <div class="voucher-box" style="background: #fefce8; border-color: #f59e0b; text-align: right;">
            <div style="color: #92400e; font-size: 10px;">申请出款净额 (人民币)</div>
            <strong style="font-size: 18px; color: #b45309; font-family: monospace;">¥ {{ formatMoney(currencySummaryList[0]?.netAmount || 0) }}</strong>
          </div>
        </div>
      </div>

      <div class="tabs-card">
        <a-tabs default-active-key="1" style="height: 100%; display: flex; flex-direction: column;" :tab-bar-style="{ margin: '0', padding: '0 12px', background: '#f8fafc' }">
          <a-tab-pane key="1" tab="业务费用明细清单">
            <div style="padding: 10px; height: 100%; overflow-y: auto;">
              <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
                <thead>
                  <tr style="background: #f1f5f9; border-bottom: 1px solid #cbd5e1; text-align: left;">
                    <th style="padding: 6px;">序</th>
                    <th style="padding: 6px;">业务委托编号</th>
                    <th style="padding: 6px;">提单号</th>
                    <th style="padding: 6px;">费用名称</th>
                    <th style="padding: 6px;">币别</th>
                    <th style="padding: 6px; text-align: right;">原金额</th>
                    <th style="padding: 6px; text-align: right;">可申请余额</th>
                    <th style="padding: 6px; text-align: right;">本次申请金额</th>
                    <th style="padding: 6px;">垫资风险</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(group, gIdx) in orderFeeGroups" :key="gIdx">
                    <tr v-for="(f, fIdx) in group.fees" :key="f.id" style="border-bottom: 1px solid #f1f5f9;">
                      <td style="padding: 6px;">{{ fIdx + 1 }}</td>
                      <td style="padding: 6px;"><a class="pa-link">{{ group.commissionNum }}</a></td>
                      <td style="padding: 6px; font-family: monospace;">{{ group.mblNum || '-' }}</td>
                      <td style="padding: 6px;"><strong>{{ f.feeCodeName }}</strong></td>
                      <td style="padding: 6px;">{{ f.currencyCode }}</td>
                      <td style="padding: 6px; text-align: right;">{{ formatMoney(f.amount, f.currencyCode) }}</td>
                      <td style="padding: 6px; text-align: right;">{{ formatMoney(f.unRqstPaymentAmount, f.currencyCode) }}</td>
                      <td style="padding: 6px; text-align: right;"><strong style="color: #2563eb; font-size: 13px;">{{ formatMoney(f.appliedAmount, f.currencyCode) }}</strong></td>
                      <td style="padding: 6px;"><span v-if="group.unSettledReceiveList.length > 0" style="color: #d97706; font-weight: 600;">⚠️ 未结垫资</span><span v-else style="color: #16a34a;">✓ 客户已结清</span></td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
          </a-tab-pane>

          <a-tab-pane key="2" tab="发票核验中心">
            <div style="padding: 16px;">
              <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span>发票总额: ¥{{ formatDecimal(totalInvoiceAmount) }} · 应付总额: ¥{{ formatDecimal(totalPayAmountRMB) }} (差额: ¥{{ formatDecimal(invoiceDiffAmount) }})</span>
                <a-button type="primary" size="small" @click="handleAddInvoiceRow">+ 录入发票</a-button>
              </div>
              <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
                <tr style="background: #f8fafc; border-bottom: 1px solid #e2e8f0; text-align: left;">
                  <th style="padding: 6px;">发票代码/号码</th><th style="padding: 6px;">开票日期</th><th style="padding: 6px;">销售方抬头</th><th style="padding: 6px; text-align: right;">发票金额</th><th style="padding: 6px;">附件状态</th>
                </tr>
                <tr v-for="(inv, i) in formState.invoiceRows" :key="i" style="border-bottom: 1px solid #f1f5f9;">
                  <td style="padding: 6px; font-family: monospace;">{{ inv.invoiceNo }}</td>
                  <td style="padding: 6px;">{{ inv.invoiceDate }}</td>
                  <td style="padding: 6px;">{{ inv.sellerName }}</td>
                  <td style="padding: 6px; text-align: right; font-weight: 700;">¥{{ formatDecimal(inv.invoiceAmount) }}</td>
                  <td style="padding: 6px;"><a-tag color="success">已识别附件</a-tag></td>
                </tr>
              </table>
            </div>
          </a-tab-pane>

          <a-tab-pane key="3" tab="审批流转跟踪与盖章">
            <div style="padding: 16px;">
              <div v-for="node in workflowNodes" :key="node.nodeName" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 8px 12px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between;">
                  <strong>{{ node.nodeName }} ({{ node.operatorName }})</strong>
                  <span :style="{ color: node.status === 'passed' ? '#16a34a' : (node.status === 'rejected' ? '#dc2626' : '#64748b') }">{{ node.statusText }}</span>
                </div>
                <div v-if="node.comment" style="color: #dc2626; margin-top: 4px;">意见/驳回原因: {{ node.comment }}</div>
              </div>
            </div>
          </a-tab-pane>
        </a-tabs>
      </div>
"""

generate_file('payment-app-dir2-voucher-card.html', '付费申请 · 方向2：金融仿真主凭证工作台 (Voucher Tabs)', '方向 2: 凭证标签页', css_2, body_2)

# ==============================================================================
# 3. Stepper Guided Wizard (3-Step)
# ==============================================================================
css_3 = """
    .wizard-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; flex: 1; display: flex; flex-direction: column; overflow: hidden; padding: 12px; }
"""
script_3 = "        const currentWizardStep = ref(0);"
body_3 = rejection_alert + """
      <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 16px; flex-shrink: 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <div style="display: flex; gap: 8px; align-items: center;">
            <strong style="font-size: 14px;">向导式付费流转处理</strong>
            <span class="pa-status-tag" :class="'pa-status-' + formState.status">{{ currentStatusMeta.stampText }}</span>
          </div>
          <span style="font-size: 12px; color: #64748b;">单号: {{ formState.applicationNo }}</span>
        </div>
        <a-steps :current="currentWizardStep" size="small">
          <a-step title="Step 1: 费用核对与垫资排查" description="确认付款委托与金额"></a-step>
          <a-step title="Step 2: 发票匹配与税金勾稽" description="录入或从进项池选票"></a-step>
          <a-step title="Step 3: 账户路由与签字送审" description="核对出入账银行并提交"></a-step>
        </a-steps>
      </div>

      <div class="wizard-card">
        <div v-if="currentWizardStep === 0" style="height: 100%; display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <strong style="font-size: 13px;">请核对需要支付的业务费用：</strong>
            <a-button type="primary" size="small" @click="handleOpenAddFeeDrawer">+ 增选其他订单费用</a-button>
          </div>
          <div style="flex: 1; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
              <tr style="background: #f8fafc; border-bottom: 1px solid #e2e8f0; text-align: left;">
                <th style="padding: 6px;">业务单号</th><th style="padding: 6px;">提单号</th><th style="padding: 6px;">港口</th><th style="padding: 6px;">费用名称</th><th style="padding: 6px; text-align: right;">本次申请金额</th><th style="padding: 6px;">垫资风险</th>
              </tr>
              <template v-for="g in orderFeeGroups" :key="g.groupId">
                <tr v-for="f in g.fees" :key="f.id" style="border-bottom: 1px solid #f1f5f9;">
                  <td style="padding: 6px;">{{ g.commissionNum }}</td>
                  <td style="padding: 6px; font-family: monospace;">{{ g.mblNum || '-' }}</td>
                  <td style="padding: 6px;">{{ g.podName }}</td>
                  <td style="padding: 6px;"><strong>{{ f.feeCodeName }}</strong></td>
                  <td style="padding: 6px; text-align: right;"><strong style="color: #2563eb;">{{ formatMoney(f.appliedAmount, f.currencyCode) }}</strong></td>
                  <td style="padding: 6px;">{{ g.unSettledReceiveList.length > 0 ? '⚠️ 未结垫资' : '✓ 客户已结清' }}</td>
                </tr>
              </template>
            </table>
          </div>
        </div>

        <div v-else-if="currentWizardStep === 1" style="height: 100%; display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <strong style="font-size: 13px;">请录入对应发票凭据：</strong>
            <a-button type="primary" size="small" @click="handleAddInvoiceRow">+ 新增发票行</a-button>
          </div>
          <div style="flex: 1; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
              <tr style="background: #f8fafc; border-bottom: 1px solid #e2e8f0; text-align: left;">
                <th style="padding: 6px;">发票代码/号码</th><th style="padding: 6px;">销售方企业</th><th style="padding: 6px; text-align: right;">发票金额</th><th style="padding: 6px;">操作</th>
              </tr>
              <tr v-for="(inv, idx) in formState.invoiceRows" :key="idx" style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 6px;"><a-input v-model:value="inv.invoiceNo" size="small"></a-input></td>
                <td style="padding: 6px;"><a-input v-model:value="inv.sellerName" size="small"></a-input></td>
                <td style="padding: 6px; text-align: right;"><a-input-number v-model:value="inv.invoiceAmount" size="small"></a-input-number></td>
                <td style="padding: 6px;"><a-button type="link" danger size="small" @click="handleDeleteInvoiceRow(idx)">删除</a-button></td>
              </tr>
            </table>
          </div>
        </div>

        <div v-else style="height: 100%; display: flex; flex-direction: column; gap: 10px;">
          <strong style="font-size: 13px;">请核对资金账户并签字送审：</strong>
          <div style="background: #f8fafc; padding: 12px; border-radius: 4px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div>我司出款账户: <strong>{{ myCompanyBank.shortName }} {{ myCompanyBank.accountNo }}</strong></div>
            <div>对方收款单位: <strong>{{ formState.settlementName }}</strong></div>
            <div>本次申请出款净额: <strong style="color: #2563eb; font-size: 16px;">¥ {{ formatMoney(currencySummaryList[0]?.netAmount || 0) }}</strong></div>
            <div>发票与费用勾稽: <strong style="color: #16a34a;">✓ 票费已平 (无差额)</strong></div>
          </div>
          <div>汇款附言: <a-input v-model:value="formState.paymentDemand"></a-input></div>
        </div>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; background: #fff; padding: 8px 16px; border: 1px solid #e2e8f0; border-radius: 6px;">
        <a-button :disabled="currentWizardStep === 0" @click="currentWizardStep--">上一步</a-button>
        <div>
          <a-button v-if="currentWizardStep < 2" type="primary" @click="currentWizardStep++">下一步</a-button>
          <a-button v-else type="primary" @click="handleSubmitAudit">确认送审</a-button>
        </div>
      </div>
"""

generate_file('payment-app-dir3-stepper-wizard.html', '付费申请 · 方向3：向导式分步流转工作台 (3-Step Wizard)', '方向 3: 向导步骤', css_3, body_3, script_3, "currentWizardStep")

# ==============================================================================
# 4. Master-Detail Order Switcher (28% / 72%)
# ==============================================================================
css_4 = """
    .md-split { display: grid; grid-template-columns: 310px 1fr; gap: 8px; flex: 1; overflow: hidden; }
    .md-left { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; flex-direction: column; overflow: hidden; }
    .md-right { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; flex-direction: column; overflow: hidden; }
    .order-item-card { padding: 8px 10px; border-bottom: 1px solid #f1f5f9; cursor: pointer; transition: all 0.15s; }
    .order-item-card:hover { background: #f8fafc; }
    .order-item-card.is-active { background: #eff6ff; border-left: 3px solid #2563eb; }
"""
script_4 = "        const activeOrderIndex = ref(0);"
body_4 = rejection_alert + """
      <div class="pa-voucher-card">
""" + top_bar + """
      </div>

      <div class="md-split">
        <div class="md-left">
          <div style="padding: 8px 10px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; font-weight: 700;">
            关联业务委托列表 ({{ orderFeeGroups.length }})
          </div>
          <div style="flex: 1; overflow-y: auto;">
            <div
              v-for="(grp, idx) in orderFeeGroups"
              :key="grp.groupId"
              class="order-item-card"
              :class="{ 'is-active': activeOrderIndex === idx }"
              @click="activeOrderIndex = idx"
            >
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #0f172a;">{{ grp.commissionNum }}</strong>
                <span style="font-weight: 700; color: #2563eb;">¥ {{ formatDecimal(grp.fees.reduce((acc, f) => acc + f.appliedAmount, 0)) }}</span>
              </div>
              <div style="color: #64748b; font-size: 10px; margin-top: 2px;">
                提单: {{ grp.mblNum || '-' }} · 目的港: {{ grp.podName || '-' }}
              </div>
              <div style="display: flex; justify-content: space-between; margin-top: 4px; font-size: 10px;">
                <span>{{ grp.carrierName }} · {{ grp.totalCtn }}</span>
                <span :style="{ color: grp.unSettledReceiveList.length > 0 ? '#d97706' : '#16a34a' }">
                  {{ grp.unSettledReceiveList.length > 0 ? '⚠️ 垫资' : '✓ 客户已结' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="md-right" v-if="orderFeeGroups[activeOrderIndex]">
          <div style="padding: 8px 12px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
            <div>
              <strong style="font-size: 13px;">委托详情: {{ orderFeeGroups[activeOrderIndex].commissionNum }}</strong>
              <span style="margin-left: 10px; color: #64748b;">客户: {{ orderFeeGroups[activeOrderIndex].clientName }}</span>
            </div>
            <a-button type="primary" size="small" @click="handleOpenAddFeeDrawer">+ 为本单加费</a-button>
          </div>

          <div style="padding: 10px; flex: 1; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
              <tr style="background: #f1f5f9; border-bottom: 1px solid #cbd5e1; text-align: left;">
                <th style="padding: 6px;">费用名称</th><th style="padding: 6px;">收付</th><th style="padding: 6px;">币别</th><th style="padding: 6px; text-align: right;">原金额</th><th style="padding: 6px; text-align: right;">本次出款金额</th><th style="padding: 6px;">备注</th>
              </tr>
              <tr v-for="fee in orderFeeGroups[activeOrderIndex].fees" :key="fee.id" style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 6px;"><strong>{{ fee.feeCodeName }}</strong></td>
                <td style="padding: 6px;"><span class="pa-dir-badge" :class="fee.feeDirection === 1 ? 'pa-dir-pay' : 'pa-dir-rec'">{{ fee.feeDirection === 1 ? '付' : '收' }}</span></td>
                <td style="padding: 6px;">{{ fee.currencyCode }}</td>
                <td style="padding: 6px; text-align: right;">{{ formatMoney(fee.amount, fee.currencyCode) }}</td>
                <td style="padding: 6px; text-align: right;"><strong style="color: #2563eb; font-size: 13px;">{{ formatMoney(fee.appliedAmount, fee.currencyCode) }}</strong></td>
                <td style="padding: 6px; color: #64748b;">{{ fee.itemRemark || '-' }}</td>
              </tr>
            </table>
          </div>
        </div>
      </div>
"""

generate_file('payment-app-dir4-master-detail-side.html', '付费申请 · 方向4：主从联动订单切换台 (Master-Detail Side)', '方向 4: 主从切换', css_4, body_4, script_4, "activeOrderIndex")

# ==============================================================================
# 5. Bloomberg Financial Full-Screen Grid
# ==============================================================================
css_5 = """
    .grid-card { background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; flex: 1; display: flex; flex-direction: column; overflow: hidden; }
    .pro-ticker { background: #0f172a; color: #f8fafc; padding: 4px 12px; display: flex; justify-content: space-between; align-items: center; border-radius: 4px; font-size: 11px; }
"""

body_5 = rejection_alert + """
      <div class="pro-ticker">
        <div style="display: flex; gap: 14px; align-items: center;">
          <span>申请单: <strong style="color: #38bdf8;">{{ formState.applicationNo }}</strong></span>
          <span>出款: {{ myCompanyBank.shortName }} ({{ myCompanyBank.accountNo }})</span>
          <span>收款: {{ formState.settlementName }}</span>
          <span>最晚出款: {{ formState.latestPaymentDate || '-' }}</span>
        </div>
        <div style="display: flex; gap: 12px; align-items: center;">
          <span style="color: #cbd5e1;">净付合计: <strong style="color: #4ade80; font-size: 14px; font-family: monospace;">¥ {{ formatMoney(currencySummaryList[0]?.netAmount || 0) }}</strong></span>
          <a-button size="small" type="primary" @click="handleSubmitAudit">送审</a-button>
        </div>
      </div>

      <div class="grid-card">
        <div style="padding: 6px 10px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between;">
          <strong>全量费用明细账表 (高密度无阻碍录入)</strong>
          <div style="display: flex; gap: 6px;">
            <a-button size="small" type="primary" ghost @click="handleOpenAddFeeDrawer">+ 引入费用</a-button>
            <a-button size="small" @click="showInputInvoicePicker = true">核对发票池</a-button>
          </div>
        </div>

        <div style="flex: 1; overflow-y: auto;">
          <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
            <thead>
              <tr style="background: #f1f5f9; border-bottom: 1px solid #cbd5e1; text-align: left;">
                <th style="padding: 6px;">业务委托</th><th style="padding: 6px;">提单号</th><th style="padding: 6px;">港口</th><th style="padding: 6px;">费用名</th><th style="padding: 6px;">币别</th><th style="padding: 6px; text-align: right;">原金额</th><th style="padding: 6px; text-align: right;">汇率</th><th style="padding: 6px; text-align: right;">可申请额</th><th style="padding: 6px; text-align: right; background: #eff6ff;">本次申请</th><th style="padding: 6px;">备注</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="g in orderFeeGroups" :key="g.groupId">
                <tr v-for="f in g.fees" :key="f.id" style="border-bottom: 1px solid #f1f5f9;">
                  <td style="padding: 6px;"><a class="pa-link">{{ g.commissionNum }}</a></td>
                  <td style="padding: 6px; font-family: monospace;">{{ g.mblNum || '-' }}</td>
                  <td style="padding: 6px;">{{ g.podName }}</td>
                  <td style="padding: 6px;"><strong>{{ f.feeCodeName }}</strong></td>
                  <td style="padding: 6px;">{{ f.currencyCode }}</td>
                  <td style="padding: 6px; text-align: right;">{{ formatMoney(f.amount, f.currencyCode) }}</td>
                  <td style="padding: 6px; text-align: right;">{{ Number(f.exchangeRate || 1).toFixed(4) }}</td>
                  <td style="padding: 6px; text-align: right;">{{ formatMoney(f.unRqstPaymentAmount, f.currencyCode) }}</td>
                  <td style="padding: 6px; text-align: right; background: #eff6ff;"><strong style="color: #2563eb; font-size: 13px;">{{ formatMoney(f.appliedAmount, f.currencyCode) }}</strong></td>
                  <td style="padding: 6px; color: #64748b;">{{ f.itemRemark || '-' }}</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
"""

generate_file('payment-app-dir5-high-density-excel.html', '付费申请 · 方向5：大宽屏高密度金融表格 (Bloomberg Grid)', '方向 5: 高密表格', css_5, body_5)

# ==============================================================================
# 6. Dual-Ledger Reconciliation Deck (50% / 50%)
# ==============================================================================
css_6 = """
    .reconcile-split { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; flex: 1; overflow: hidden; }
    .rec-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; flex-direction: column; overflow: hidden; }
    .rec-meter { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; padding: 6px 12px; display: flex; justify-content: space-between; align-items: center; font-size: 11px; flex-shrink: 0; }
"""

body_6 = rejection_alert + """
      <div class="pa-voucher-card">
""" + top_bar + """
      </div>

      <div class="rec-meter">
        <div style="display: flex; align-items: center; gap: 8px;">
          <iconify-icon icon="ant-design:sync-outlined" style="color: #16a34a; font-size: 14px;"></iconify-icon>
          <strong style="color: #166534;">票费动态对账平衡仪：</strong>
          <span>业务应付: <strong>¥ {{ formatDecimal(totalPayAmountRMB) }}</strong></span>
          <span style="color: #cbd5e1;">⟷</span>
          <span>录入发票: <strong>¥ {{ formatDecimal(totalInvoiceAmount) }}</strong></span>
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
          <span>勾稽差额:</span>
          <strong :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#d97706', fontSize: '13px' }">
            {{ invoiceDiffAmount === 0 ? '✓ 票费已平 (¥0.00)' : ('差额: ¥' + formatDecimal(invoiceDiffAmount)) }}
          </strong>
        </div>
      </div>

      <div class="reconcile-split">
        <div class="rec-card">
          <div style="padding: 6px 10px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
            <strong>左联：待付款业务费用明细 ({{ totalFeeCount }} 笔)</strong>
            <a-button type="primary" size="small" @click="handleOpenAddFeeDrawer">+ 添加费用</a-button>
          </div>
          <div style="flex: 1; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
              <tr style="background: #f1f5f9; border-bottom: 1px solid #cbd5e1; text-align: left;">
                <th style="padding: 6px;">单号</th><th style="padding: 6px;">费用名</th><th style="padding: 6px;">币别</th><th style="padding: 6px; text-align: right;">本次出款</th><th style="padding: 6px;">垫资风险</th>
              </tr>
              <template v-for="g in orderFeeGroups" :key="g.groupId">
                <tr v-for="f in g.fees" :key="f.id" style="border-bottom: 1px solid #f1f5f9;">
                  <td style="padding: 6px;"><a class="pa-link">{{ g.commissionNum }}</a></td>
                  <td style="padding: 6px;"><strong>{{ f.feeCodeName }}</strong></td>
                  <td style="padding: 6px;">{{ f.currencyCode }}</td>
                  <td style="padding: 6px; text-align: right;"><strong style="color: #2563eb;">{{ formatMoney(f.appliedAmount, f.currencyCode) }}</strong></td>
                  <td style="padding: 6px;">{{ g.unSettledReceiveList.length > 0 ? '⚠️ 未结垫资' : '✓ 客户已结' }}</td>
                </tr>
              </template>
            </table>
          </div>
        </div>

        <div class="rec-card">
          <div style="padding: 6px 10px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
            <strong>右联：发票核验与进项池 ({{ formState.invoiceRows.length }} 张)</strong>
            <div style="display: flex; gap: 4px;">
              <a-button size="small" @click="showInputInvoicePicker = true">进项池</a-button>
              <a-button type="primary" size="small" @click="handleAddInvoiceRow">+ 录发票</a-button>
            </div>
          </div>
          <div style="flex: 1; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
              <tr style="background: #f1f5f9; border-bottom: 1px solid #cbd5e1; text-align: left;">
                <th style="padding: 6px;">发票号码</th><th style="padding: 6px;">开票日期</th><th style="padding: 6px;">销售方</th><th style="padding: 6px; text-align: right;">发票金额</th><th style="padding: 6px;">操作</th>
              </tr>
              <tr v-for="(inv, idx) in formState.invoiceRows" :key="idx" style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 6px;"><a-input v-model:value="inv.invoiceNo" size="small"></a-input></td>
                <td style="padding: 6px;"><a-date-picker v-model:value="inv.invoiceDate" size="small" value-format="YYYY-MM-DD"></a-date-picker></td>
                <td style="padding: 6px;"><a-input v-model:value="inv.sellerName" size="small"></a-input></td>
                <td style="padding: 6px; text-align: right;"><a-input-number v-model:value="inv.invoiceAmount" size="small"></a-input-number></td>
                <td style="padding: 6px;"><a-button type="link" danger size="small" @click="handleDeleteInvoiceRow(idx)">删</a-button></td>
              </tr>
            </table>
          </div>
        </div>
      </div>
"""

generate_file('payment-app-dir6-invoice-matching-deck.html', '付费申请 · 方向6：票费双联对账台 (Reconciliation Deck)', '方向 6: 双联对账', css_6, body_6)

# ==============================================================================
# 7. Freight Container Kanban Cards
# ==============================================================================
css_7 = """
    .kanban-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 10px; flex: 1; overflow-y: auto; }
    .container-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; flex-direction: column; overflow: hidden; }
    .container-card-head { background: #1e293b; color: #fff; padding: 6px 10px; display: flex; justify-content: space-between; align-items: center; }
"""

body_7 = rejection_alert + """
      <div class="pa-voucher-card">
""" + top_bar + """
      </div>

      <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 12px; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; gap: 10px; align-items: center;">
          <strong style="font-size: 13px;">货运提单集装箱卡片流 (Container Stubs)</strong>
          <span style="color: #64748b;">共 {{ orderFeeGroups.length }} 票待付业务单据</span>
        </div>
        <a-button type="primary" size="small" @click="handleOpenAddFeeDrawer">+ 引入集装箱业务</a-button>
      </div>

      <div class="kanban-grid">
        <div v-for="grp in orderFeeGroups" :key="grp.groupId" class="container-card">
          <div class="container-card-head">
            <div style="display: flex; align-items: center; gap: 6px;">
              <iconify-icon icon="ant-design:code-sandbox-outlined" style="color: #38bdf8; font-size: 14px;"></iconify-icon>
              <strong style="font-family: monospace;">{{ grp.commissionNum }}</strong>
            </div>
            <span style="font-size: 10px; background: rgba(255,255,255,0.15); padding: 1px 5px; border-radius: 2px;">{{ grp.podName }} · {{ grp.carrierName }}</span>
          </div>

          <div style="padding: 8px 10px; flex: 1; display: flex; flex-direction: column; gap: 6px;">
            <div style="display: flex; justify-content: space-between; color: #64748b; font-size: 10px;">
              <span>主单: {{ grp.mblNum || '-' }}</span>
              <span>箱型: {{ grp.totalCtn || '-' }}</span>
            </div>
            <div style="color: #334155; font-size: 11px;">
              客户: <strong>{{ grp.clientName }}</strong>
            </div>

            <div style="border-top: 1px dashed #e2e8f0; padding-top: 6px; display: flex; flex-direction: column; gap: 4px;">
              <div v-for="f in grp.fees" :key="f.id" style="display: flex; justify-content: space-between; align-items: center; background: #f8fafc; padding: 3px 6px; border-radius: 3px;">
                <span>{{ f.feeCodeName }}</span>
                <strong style="color: #2563eb;">{{ f.currencyCode }} {{ formatDecimal(f.appliedAmount) }}</strong>
              </div>
            </div>

            <div style="margin-top: auto; border-top: 1px solid #f1f5f9; padding-top: 6px; display: flex; justify-content: space-between; font-size: 10px;">
              <span :style="{ color: grp.unSettledReceiveList.length > 0 ? '#d97706' : '#16a34a', fontWeight: 600 }">
                {{ grp.unSettledReceiveList.length > 0 ? '⚠️ 未结垫资风险' : '✓ 应收已结清' }}
              </span>
              <span>本单合计: <strong style="color: #0f172a; font-size: 12px;">¥ {{ formatDecimal(grp.fees.reduce((a,b)=>a+b.appliedAmount, 0)) }}</strong></span>
            </div>
          </div>
        </div>
      </div>
"""

generate_file('payment-app-dir7-kanban-cards.html', '付费申请 · 方向7：货运集装箱卡片流 (Kanban Cards)', '方向 7: 集装箱卡片', css_7, body_7)

# ==============================================================================
# 8. Ant Design Pro Classic Clean Tabs
# ==============================================================================
css_8 = """
    .pro-tabs-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; flex: 1; display: flex; flex-direction: column; overflow: hidden; }
"""

body_8 = rejection_alert + """
      <div class="pa-voucher-card">
""" + top_bar + """
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); padding: 8px 12px; gap: 12px; background: #fafbfc; border-top: 1px solid #f1f5f9; font-size: 11px;">
          <div><span style="color:#64748b;">出款公司:</span> <strong>{{ formState.companyName }}</strong></div>
          <div><span style="color:#64748b;">收款对象:</span> <strong>{{ formState.settlementName }}</strong></div>
          <div><span style="color:#64748b;">付款排期:</span> <span>{{ formState.latestPaymentDate }} 至 {{ formState.predictReturnDate }}</span></div>
          <div style="text-align: right;"><span style="color:#64748b;">净付金额:</span> <strong style="color: #2563eb; font-size: 14px;">¥ {{ formatMoney(currencySummaryList[0]?.netAmount || 0) }}</strong></div>
        </div>
      </div>

      <div class="pro-tabs-card">
        <a-tabs default-active-key="1" style="height: 100%; display: flex; flex-direction: column;" :tab-bar-style="{ margin: '0', padding: '0 12px', background: '#f8fafc' }">
          <a-tab-pane key="1" :tab="'业务费用明细 (共 ' + totalFeeCount + ' 笔)'">
            <div style="padding: 10px; height: 100%; overflow-y: auto;">
              <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
                <tr style="background: #f1f5f9; border-bottom: 1px solid #e2e8f0; text-align: left;">
                  <th style="padding: 6px;">委托号</th><th style="padding: 6px;">提单号</th><th style="padding: 6px;">港口</th><th style="padding: 6px;">费用名称</th><th style="padding: 6px;">币别</th><th style="padding: 6px; text-align: right;">本次申请</th><th style="padding: 6px;">风控</th>
                </tr>
                <template v-for="g in orderFeeGroups" :key="g.groupId">
                  <tr v-for="f in g.fees" :key="f.id" style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 6px;"><a class="pa-link">{{ g.commissionNum }}</a></td>
                    <td style="padding: 6px; font-family: monospace;">{{ g.mblNum || '-' }}</td>
                    <td style="padding: 6px;">{{ g.podName }}</td>
                    <td style="padding: 6px;"><strong>{{ f.feeCodeName }}</strong></td>
                    <td style="padding: 6px;">{{ f.currencyCode }}</td>
                    <td style="padding: 6px; text-align: right;"><strong style="color: #2563eb;">{{ formatMoney(f.appliedAmount, f.currencyCode) }}</strong></td>
                    <td style="padding: 6px;">{{ g.unSettledReceiveList.length > 0 ? '⚠️ 垫资' : '✓ 结清' }}</td>
                  </tr>
                </template>
              </table>
            </div>
          </a-tab-pane>

          <a-tab-pane key="2" :tab="'发票核对中心 (' + formState.invoiceRows.length + ' 张)'">
            <div style="padding: 12px;">
              <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
                <tr style="background: #f8fafc; border-bottom: 1px solid #e2e8f0; text-align: left;">
                  <th style="padding: 6px;">发票代码/号码</th><th style="padding: 6px;">开票日期</th><th style="padding: 6px;">销售方企业</th><th style="padding: 6px; text-align: right;">发票金额</th>
                </tr>
                <tr v-for="(inv, idx) in formState.invoiceRows" :key="idx" style="border-bottom: 1px solid #f1f5f9;">
                  <td style="padding: 6px; font-family: monospace;">{{ inv.invoiceNo }}</td>
                  <td style="padding: 6px;">{{ inv.invoiceDate }}</td>
                  <td style="padding: 6px;">{{ inv.sellerName }}</td>
                  <td style="padding: 6px; text-align: right; font-weight: 700;">¥ {{ formatDecimal(inv.invoiceAmount) }}</td>
                </tr>
              </table>
            </div>
          </a-tab-pane>

          <a-tab-pane key="3" tab="审批流程跟踪与节点">
            <div style="padding: 12px;">
              <div v-for="node in workflowNodes" :key="node.nodeName" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 6px 10px; margin-bottom: 6px;">
                <div style="display: flex; justify-content: space-between;">
                  <strong>{{ node.nodeName }} ({{ node.operatorName }})</strong>
                  <span :style="{ color: node.status === 'passed' ? '#16a34a' : (node.status === 'rejected' ? '#dc2626' : '#64748b') }">{{ node.statusText }}</span>
                </div>
                <div v-if="node.comment" style="color: #dc2626; margin-top: 3px;">{{ node.comment }}</div>
              </div>
            </div>
          </a-tab-pane>
        </a-tabs>
      </div>
"""

generate_file('payment-app-dir8-compact-tabbed-pro.html', '付费申请 · 方向8：极致极简标签页工作台 (AntD Pro Pure)', '方向 8: 官方Tabs', css_8, body_8)

# ==============================================================================
# 9. Executive Dashboard + Drawer Focused
# ==============================================================================
css_9 = """
    .dash-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; flex: 1; }
    .dash-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 16px; display: flex; flex-direction: column; justify-content: space-between; }
"""

body_9 = rejection_alert + """
      <div class="pa-voucher-card">
""" + top_bar + """
      </div>

      <div class="dash-grid">
        <div class="dash-card">
          <div>
            <div style="font-weight: 700; font-size: 13px; color: #0f172a; margin-bottom: 8px;">1. 往来资金账户路由</div>
            <div style="line-height: 1.8; color: #475569;">
              <div>我司出款公司: <strong>{{ formState.companyName }}</strong></div>
              <div>我司出款账户: {{ myCompanyBank.shortName }} ({{ myCompanyBank.accountNo }})</div>
              <div>对方收款单位: <strong>{{ formState.settlementName }}</strong></div>
              <div>最晚出款时限: {{ formState.latestPaymentDate || '未指定' }}</div>
            </div>
          </div>
          <div style="border-top: 1px solid #f1f5f9; padding-top: 6px; text-align: right;">
            <a-tag color="blue">结算档案直连已锁定</a-tag>
          </div>
        </div>

        <div class="dash-card">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-weight: 700; font-size: 13px;">2. 待付业务费用清单</span>
              <a-button type="primary" size="small" @click="handleOpenAddFeeDrawer">增删费用抽屉</a-button>
            </div>
            <div style="line-height: 1.8;">
              <div>关联业务票数: <strong>{{ orderFeeGroups.length }} 票</strong> · 费用笔数: <strong>{{ totalFeeCount }} 笔</strong></div>
              <div>本次申请净额: <strong style="color: #2563eb; font-size: 16px;">¥ {{ formatMoney(currencySummaryList[0]?.netAmount || 0) }}</strong></div>
              <div>垫资风险状态: <span :style="{ color: formState.isReceiveAllSettled ? '#16a34a' : '#d97706', fontWeight: 600 }">{{ formState.isReceiveAllSettled ? '✓ 无垫资风险' : '⚠️ 存在未结垫资' }}</span></div>
            </div>
          </div>
          <div style="border-top: 1px solid #f1f5f9; padding-top: 6px; display: flex; justify-content: space-between;">
            <span style="color: #64748b;">点击右上角滑出全屏明细抽屉</span>
          </div>
        </div>

        <div class="dash-card">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-weight: 700; font-size: 13px;">3. 发票核对与勾稽中心</span>
              <a-button size="small" @click="showInputInvoicePicker = true">进项发票池</a-button>
            </div>
            <div style="line-height: 1.8;">
              <div>发票录入模式: <strong>{{ formState.invoiceProcess === 1 ? '先票后付' : (formState.invoiceProcess === 0 ? '先付后票' : '不开票') }}</strong></div>
              <div>已录发票张数: <strong>{{ formState.invoiceRows.length }} 张</strong> · 发票总额: <strong>¥ {{ formatDecimal(totalInvoiceAmount) }}</strong></div>
              <div>勾稽差额判定: <strong :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#d97706' }">{{ invoiceDiffAmount === 0 ? '✓ 票费已平' : ('待补 ¥' + formatDecimal(invoiceDiffAmount)) }}</strong></div>
            </div>
          </div>
          <div style="border-top: 1px solid #f1f5f9; padding-top: 6px; text-align: right;">
            <a-button size="small" type="primary" ghost @click="handleAddInvoiceRow">+ 录入单张发票</a-button>
          </div>
        </div>

        <div class="dash-card">
          <div>
            <div style="font-weight: 700; font-size: 13px; margin-bottom: 8px;">4. 审批流程与单据档案</div>
            <div style="line-height: 1.8;">
              <div>当前流转状态: <span class="pa-status-tag" :class="'pa-status-' + formState.status">{{ currentStatusMeta.stampText }}</span></div>
              <div v-if="workflowNodes[1]?.comment" style="color: #dc2626;">驳回原因: {{ workflowNodes[1].comment }}</div>
              <div>归档单据附件: <strong>{{ applicationAttachmentGroups.reduce((acc, g) => acc + g.items.length, 0) }} 份</strong></div>
            </div>
          </div>
          <div style="border-top: 1px solid #f1f5f9; padding-top: 6px; text-align: right;">
            <a-button type="primary" size="small" @click="handleSubmitAudit">立即送审</a-button>
          </div>
        </div>
      </div>
"""

generate_file('payment-app-dir9-drawer-focused.html', '付费申请 · 方向9：全景看板 + 侧滑抽屉工作台 (Drawer Focused)', '方向 9: 仪表大盘', css_9, body_9)

# ==============================================================================
# 10. Global Multi-Currency Freight Forex Voucher
# ==============================================================================
css_10 = """
    .forex-banner { background: #0f172a; color: #fff; padding: 6px 12px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }
    .forex-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; flex: 1; display: flex; flex-direction: column; overflow: hidden; }
"""

body_10 = rejection_alert + """
      <div class="forex-banner">
        <div style="display: flex; gap: 14px; align-items: center;">
          <strong style="color: #38bdf8; font-size: 13px;">GLOBAL MULTI-CURRENCY VOUCHER</strong>
          <span style="color: #94a3b8;">原币多币别结算口径</span>
        </div>
        <div style="display: flex; gap: 14px; align-items: center;">
          <span v-for="c in currencySummaryList" :key="c.currencyCode">
            {{ c.currencyCode }}: <strong style="font-family: monospace; font-size: 13px; color: #4ade80;">{{ formatMoney(c.netAmount, c.currencyCode) }}</strong>
          </span>
          <a-tag color="purple">折算汇率已锁</a-tag>
        </div>
      </div>

      <div class="pa-voucher-card">
""" + top_bar + """
      </div>

      <div class="forex-card">
        <div style="padding: 6px 12px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between;">
          <strong>跨国货运费用多币别清算清单 (Foreign Exchange Ledger)</strong>
          <a-button type="primary" size="small" @click="handleOpenAddFeeDrawer">+ 添加外币费用</a-button>
        </div>
        <div style="flex: 1; overflow-y: auto;">
          <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
            <thead>
              <tr style="background: #f1f5f9; border-bottom: 1px solid #cbd5e1; text-align: left;">
                <th style="padding: 6px;">业务单号</th><th style="padding: 6px;">主提单 (MBL)</th><th style="padding: 6px;">费用名称</th><th style="padding: 6px;">币别</th><th style="padding: 6px; text-align: right;">原币金额</th><th style="padding: 6px; text-align: right;">海关/现汇率</th><th style="padding: 6px; text-align: right; background: #eff6ff;">折合本位币 (RMB)</th><th style="padding: 6px;">垫资风控</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="g in orderFeeGroups" :key="g.groupId">
                <tr v-for="f in g.fees" :key="f.id" style="border-bottom: 1px solid #f1f5f9;">
                  <td style="padding: 6px;"><a class="pa-link">{{ g.commissionNum }}</a></td>
                  <td style="padding: 6px; font-family: monospace;">{{ g.mblNum || '-' }}</td>
                  <td style="padding: 6px;"><strong>{{ f.feeCodeName }}</strong></td>
                  <td style="padding: 6px;"><a-tag color="blue">{{ f.currencyCode }}</a-tag></td>
                  <td style="padding: 6px; text-align: right;">{{ formatMoney(f.amount, f.currencyCode) }}</td>
                  <td style="padding: 6px; text-align: right;">{{ Number(f.exchangeRate || 1).toFixed(4) }}</td>
                  <td style="padding: 6px; text-align: right; background: #eff6ff;"><strong style="color: #2563eb;">¥ {{ formatDecimal(f.appliedAmount * (f.exchangeRate || 1)) }}</strong></td>
                  <td style="padding: 6px;">{{ g.unSettledReceiveList.length > 0 ? '⚠️ 未结垫资' : '✓ 客户已结' }}</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
"""

generate_file('payment-app-dir10-executive-bilingual.html', '付费申请 · 方向10：国际多币别外贸对账凭证 (Global Multi-Currency)', '方向 10: 多币对账', css_10, body_10)

print("All 10 directions generated cleanly.")
