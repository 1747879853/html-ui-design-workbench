# coding: utf-8
import os
from generate_helpers import wrap_page, get_top_action_bar, get_status_alert

# ==============================================================================
# Direction 1: Linear / Stripe Split (64% / 36%)
# ==============================================================================
dir1_css = """
    .dir1-split { display: grid; grid-template-columns: minmax(0, 64%) minmax(0, 36%); gap: 8px; flex: 1; overflow: hidden; }
    .dir1-left { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03); }
    .dir1-right { display: flex; flex-direction: column; gap: 8px; overflow-y: auto; }
    .dir1-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px; box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03); }
    .dir1-card-head { font-size: 12px; font-weight: 700; color: #0f172a; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
"""

dir1_body = f"""
      {get_status_alert()}
      <div class="pa-voucher-card" style="background:#fff; border:1px solid #e2e8f0; border-radius:6px;">
        {get_top_action_bar()}
      </div>

      <div class="dir1-split">
        <!-- 左栏 64%：费用主舞台，100% 满高垂直滚动，无底栏挤压 -->
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

        <!-- 右栏 36%：垂直一体化资金底账、发票与审批流转 -->
        <div class="dir1-right">
          <!-- 卡片 1: 凭证结算路由 -->
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

          <!-- 卡片 2: 发票核对中心 -->
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
              <div style="display: flex; gap: 4px;">
                <a-button size="small" type="primary" ghost style="font-size: 10px; height: 20px; padding: 0 4px;" @click="handleAddInvoiceRow">+ 录票</a-button>
              </div>
            </div>
            <div style="font-size: 11px; margin-bottom: 6px; display: flex; justify-content: space-between; color: #64748b;">
              <span>已录: ¥{{ formatDecimal(totalInvoiceAmount) }}</span>
              <span>差额: <strong :style="{{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#d97706' }}">{{ invoiceDiffAmount === 0 ? '✓ 票费已平' : ('待补 ¥' + formatDecimal(invoiceDiffAmount)) }}</strong></span>
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

          <!-- 卡片 3: 审批流转与电子签名 -->
          <div class="dir1-card">
            <div class="dir1-card-head">
              <span>审批流转跟踪</span>
              <span class="pa-status-tag" :class="'pa-status-' + formState.status" style="font-size: 10px;">{{ currentStatusMeta.stampText }}</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 4px;">
              <div v-for="node in workflowNodes" :key="node.nodeName" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 5px 8px; font-size: 11px;">
                <div style="display: flex; justify-content: space-between;">
                  <strong>{{ node.nodeName }} ({{ node.operatorName }})</strong>
                  <span :style="{{ color: node.status === 'passed' ? '#16a34a' : (node.status === 'rejected' ? '#dc2626' : '#64748b'), fontWeight: 600, fontSize: '10px' }}">{{ node.statusText }}</span>
                </div>
                <div v-if="node.comment" style="color: #dc2626; margin-top: 2px;">{{ node.comment }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
"""

with open('pages/payment-app-dir1-linear-split.html', 'w', encoding='utf-8') as f:
    f.write(wrap_page('付费申请 · 方向1：全屏左右双栏流式工作台 (Linear Split)', '方向 1: 左右流式', dir1_css, dir1_body))
print("Created pages/payment-app-dir1-linear-split.html")

# ==============================================================================
# Direction 2: Bank Paper Check Voucher + Ledger Tabs
# ==============================================================================
dir2_css = """
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

dir2_body = f"""
      {get_status_alert()}
      <!-- 仿真古典银行付款凭证折头 -->
      <div class="voucher-paper">
        <div class="voucher-title">企业对外付款申请记账凭证 (PAYMENT VOUCHER)</div>
        <div class="voucher-grid">
          <div class="voucher-box">
            <span style="color: #92400e;">申请单号: </span><strong>{{{{ formState.applicationNo }}}}</strong>
            <div style="margin-top: 3px; color: #64748b;">申请人: {{{{ formState.creatorUserName }}}} · 提交: {{{{ formState.submitTime || '草稿' }}}}</div>
          </div>
          <div class="voucher-box">
            <span style="color: #92400e;">付款抬头 (我司): </span><strong style="color: #0f172a;">{{{{ formState.companyName }}}}</strong>
            <div style="margin-top: 3px; color: #64748b;">账号: {{{{ myCompanyBank.shortName }}}} {{{{ myCompanyBank.accountNo }}}}</div>
          </div>
          <div class="voucher-box">
            <span style="color: #92400e;">收款对象 (往来): </span><strong style="color: #0f172a;">{{{{ formState.settlementName }}}}</strong>
            <div style="margin-top: 3px; color: #64748b;">账号: CMB 122908764510001</div>
          </div>
          <div class="voucher-box" style="background: #fefce8; border-color: #f59e0b; text-align: right;">
            <div style="color: #92400e; font-size: 10px;">申请出款净额 (人民币)</div>
            <strong style="font-size: 18px; color: #b45309; font-family: monospace;">¥ {{{{ formatMoney(currencySummaryList[0]?.netAmount || 0) }}}}</strong>
          </div>
        </div>
      </div>

      <!-- 下半部：全屏 Tabs 切换 -->
      <div class="tabs-card">
        <a-tabs default-active-key="1" style="height: 100%; display: flex; flex-direction: column;" :tab-bar-style="{{ margin: '0', padding: '0 12px', background: '#f8fafc' }}">
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
                      <td style="padding: 6px;">{{{{ fIdx + 1 }}}}</td>
                      <td style="padding: 6px;"><a class="pa-link">{{{{ group.commissionNum }}}}</a></td>
                      <td style="padding: 6px; font-family: monospace;">{{{{ group.mblNum || '-' }}}}</td>
                      <td style="padding: 6px;"><strong>{{{{ f.feeCodeName }}}}</strong></td>
                      <td style="padding: 6px;">{{{{ f.currencyCode }}}}</td>
                      <td style="padding: 6px; text-align: right;">{{{{ formatMoney(f.amount, f.currencyCode) }}}}</td>
                      <td style="padding: 6px; text-align: right;">{{{{ formatMoney(f.unRqstPaymentAmount, f.currencyCode) }}}}</td>
                      <td style="padding: 6px; text-align: right;"><strong style="color: #2563eb; font-size: 13px;">{{{{ formatMoney(f.appliedAmount, f.currencyCode) }}}}</strong></td>
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
                <span>发票总额: ¥{{{{ formatDecimal(totalInvoiceAmount) }}}} · 应付总额: ¥{{{{ formatDecimal(totalPayAmountRMB) }}}} (差额: ¥{{{{ formatDecimal(invoiceDiffAmount) }}}})</span>
                <a-button type="primary" size="small" @click="handleAddInvoiceRow">+ 录入发票</a-button>
              </div>
              <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
                <tr style="background: #f8fafc; border-bottom: 1px solid #e2e8f0; text-align: left;">
                  <th style="padding: 6px;">发票代码/号码</th><th style="padding: 6px;">开票日期</th><th style="padding: 6px;">销售方抬头</th><th style="padding: 6px; text-align: right;">发票金额</th><th style="padding: 6px;">附件状态</th>
                </tr>
                <tr v-for="(inv, i) in formState.invoiceRows" :key="i" style="border-bottom: 1px solid #f1f5f9;">
                  <td style="padding: 6px; font-family: monospace;">{{{{ inv.invoiceNo }}}}</td>
                  <td style="padding: 6px;">{{{{ inv.invoiceDate }}}}</td>
                  <td style="padding: 6px;">{{{{ inv.sellerName }}}}</td>
                  <td style="padding: 6px; text-align: right; font-weight: 700;">¥{{{{ formatDecimal(inv.invoiceAmount) }}}}</td>
                  <td style="padding: 6px;"><a-tag color="success">已识别附件</a-tag></td>
                </tr>
              </table>
            </div>
          </a-tab-pane>

          <a-tab-pane key="3" tab="审批流转跟踪与盖章">
            <div style="padding: 16px;">
              <div v-for="node in workflowNodes" :key="node.nodeName" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 8px 12px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between;">
                  <strong>{{{{ node.nodeName }}}} ({{{{ node.operatorName }}}})</strong>
                  <span :style="{{ color: node.status === 'passed' ? '#16a34a' : (node.status === 'rejected' ? '#dc2626' : '#64748b') }}">{{{{ node.statusText }}}}</span>
                </div>
                <div v-if="node.comment" style="color: #dc2626; margin-top: 4px;">意见/驳回原因: {{{{ node.comment }}}}</div>
              </div>
            </div>
          </a-tab-pane>
        </a-tabs>
      </div>
"""

with open('pages/payment-app-dir2-voucher-card.html', 'w', encoding='utf-8') as f:
    f.write(wrap_page('付费申请 · 方向2：金融仿真主凭证工作台 (Voucher Tabs)', '方向 2: 凭证标签页', dir2_css, dir2_body))
print("Created pages/payment-app-dir2-voucher-card.html")

# ==============================================================================
# Direction 3: Stepper Guided Wizard (3-Step)
# ==============================================================================
dir3_css = """
    .wizard-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; flex: 1; display: flex; flex-direction: column; overflow: hidden; padding: 12px; }
"""

dir3_script = """
        const currentWizardStep = ref(0);
"""

dir3_body = f"""
      {get_status_alert()}
      <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 16px; flex-shrink: 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <div style="display: flex; gap: 8px; align-items: center;">
            <strong style="font-size: 14px;">向导式付费流转处理</strong>
            <span class="pa-status-tag" :class="'pa-status-' + formState.status">{{{{ currentStatusMeta.stampText }}}}</span>
          </div>
          <span style="font-size: 12px; color: #64748b;">单号: {{{{ formState.applicationNo }}}}</span>
        </div>
        <a-steps :current="currentWizardStep" size="small">
          <a-step title="Step 1: 费用核对与垫资排查" description="确认付款委托与金额"></a-step>
          <a-step title="Step 2: 发票匹配与税金勾稽" description="录入或从进项池选票"></a-step>
          <a-step title="Step 3: 账户路由与签字送审" description="核对出入账银行并提交"></a-step>
        </a-steps>
      </div>

      <div class="wizard-card">
        <!-- Step 1: 费用确认 -->
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
                  <td style="padding: 6px;">{{{{ g.commissionNum }}}}</td>
                  <td style="padding: 6px; font-family: monospace;">{{{{ g.mblNum || '-' }}}}</td>
                  <td style="padding: 6px;">{{{{ g.podName }}}}</td>
                  <td style="padding: 6px;"><strong>{{{{ f.feeCodeName }}}}</strong></td>
                  <td style="padding: 6px; text-align: right;"><strong style="color: #2563eb;">{{{{ formatMoney(f.appliedAmount, f.currencyCode) }}}}</strong></td>
                  <td style="padding: 6px;">{{{{ g.unSettledReceiveList.length > 0 ? '⚠️ 未结垫资' : '✓ 客户已结清' }}}}</td>
                </tr>
              </template>
            </table>
          </div>
        </div>

        <!-- Step 2: 发票匹配 -->
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

        <!-- Step 3: 送审确认 -->
        <div v-else style="height: 100%; display: flex; flex-direction: column; gap: 10px;">
          <strong style="font-size: 13px;">请核对资金账户并签字送审：</strong>
          <div style="background: #f8fafc; padding: 12px; border-radius: 4px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div>我司出款账户: <strong>{{{{ myCompanyBank.shortName }}}} {{{{ myCompanyBank.accountNo }}}}</strong></div>
            <div>对方收款单位: <strong>{{{{ formState.settlementName }}}}</strong></div>
            <div>本次申请出款净额: <strong style="color: #2563eb; font-size: 16px;">¥ {{{{ formatMoney(currencySummaryList[0]?.netAmount || 0) }}}}</strong></div>
            <div>发票与费用勾稽: <strong style="color: #16a34a;">✓ 票费已平 (无差额)</strong></div>
          </div>
          <div>汇款附言: <a-input v-model:value="formState.paymentDemand"></a-input></div>
        </div>
      </div>

      <!-- 向导翻页底栏 -->
      <div style="display: flex; justify-content: space-between; align-items: center; background: #fff; padding: 8px 16px; border: 1px solid #e2e8f0; border-radius: 6px;">
        <a-button :disabled="currentWizardStep === 0" @click="currentWizardStep--">上一步</a-button>
        <div>
          <a-button v-if="currentWizardStep < 2" type="primary" @click="currentWizardStep++">下一步</a-button>
          <a-button v-else type="primary" @click="handleSubmitAudit">确认送审</a-button>
        </div>
      </div>
"""

with open('pages/payment-app-dir3-stepper-wizard.html', 'w', encoding='utf-8') as f:
    f.write(wrap_page('付费申请 · 方向3：向导式分步流转工作台 (3-Step Wizard)', '方向 3: 向导步骤', dir3_css, dir3_body, dir3_script))
print("Created pages/payment-app-dir3-stepper-wizard.html")

# ==============================================================================
# Direction 4: Master-Detail Order Switcher (28% / 72%)
# ==============================================================================
dir4_css = """
    .md-split { display: grid; grid-template-columns: 310px 1fr; gap: 8px; flex: 1; overflow: hidden; }
    .md-left { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; flex-direction: column; overflow: hidden; }
    .md-right { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; flex-direction: column; overflow: hidden; }
    .order-item-card { padding: 8px 10px; border-bottom: 1px solid #f1f5f9; cursor: pointer; transition: all 0.15s; }
    .order-item-card:hover { background: #f8fafc; }
    .order-item-card.is-active { background: #eff6ff; border-left: 3px solid #2563eb; }
"""

dir4_script = """
        const activeOrderIndex = ref(0);
"""

dir4_body = f"""
      {get_status_alert()}
      <div class="pa-voucher-card">
        {get_top_action_bar()}
      </div>

      <div class="md-split">
        <!-- 左侧 310px：业务委托单切换列表 -->
        <div class="md-left">
          <div style="padding: 8px 10px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; font-weight: 700;">
            关联业务委托列表 ({{{{ orderFeeGroups.length }}}})
          </div>
          <div style="flex: 1; overflow-y: auto;">
            <div
              v-for="(grp, idx) in orderFeeGroups"
              :key="grp.groupId"
              class="order-item-card"
              :class="{{ 'is-active': activeOrderIndex === idx }}"
              @click="activeOrderIndex = idx"
            >
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #0f172a;">{{{{ grp.commissionNum }}}}</strong>
                <span style="font-weight: 700; color: #2563eb;">¥ {{{{ formatDecimal(grp.fees.reduce((acc, f) => acc + f.appliedAmount, 0)) }}}}</span>
              </div>
              <div style="color: #64748b; font-size: 10px; margin-top: 2px;">
                提单: {{{{ grp.mblNum || '-' }}}} · 目的港: {{{{ grp.podName || '-' }}}}
              </div>
              <div style="display: flex; justify-content: space-between; margin-top: 4px; font-size: 10px;">
                <span>{{{{ grp.carrierName }}}} · {{{{ grp.totalCtn }}}}</span>
                <span :style="{{ color: grp.unSettledReceiveList.length > 0 ? '#d97706' : '#16a34a' }}">
                  {{{{ grp.unSettledReceiveList.length > 0 ? '⚠️ 垫资' : '✓ 客户已结' }}}}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：当前选中委托的专属费用与发票核对 -->
        <div class="md-right" v-if="orderFeeGroups[activeOrderIndex]">
          <div style="padding: 8px 12px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
            <div>
              <strong style="font-size: 13px;">委托详情: {{{{ orderFeeGroups[activeOrderIndex].commissionNum }}}}</strong>
              <span style="margin-left: 10px; color: #64748b;">客户: {{{{ orderFeeGroups[activeOrderIndex].clientName }}}}</span>
            </div>
            <a-button type="primary" size="small" @click="handleOpenAddFeeDrawer">+ 为本单加费</a-button>
          </div>

          <div style="padding: 10px; flex: 1; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
              <tr style="background: #f1f5f9; border-bottom: 1px solid #cbd5e1; text-align: left;">
                <th style="padding: 6px;">费用名称</th><th style="padding: 6px;">收付</th><th style="padding: 6px;">币别</th><th style="padding: 6px; text-align: right;">原金额</th><th style="padding: 6px; text-align: right;">本次出款金额</th><th style="padding: 6px;">备注</th>
              </tr>
              <tr v-for="fee in orderFeeGroups[activeOrderIndex].fees" :key="fee.id" style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 6px;"><strong>{{{{ fee.feeCodeName }}}}</strong></td>
                <td style="padding: 6px;"><span class="pa-dir-badge" :class="fee.feeDirection === 1 ? 'pa-dir-pay' : 'pa-dir-rec'">{{{{ fee.feeDirection === 1 ? '付' : '收' }}}}</span></td>
                <td style="padding: 6px;">{{{{ fee.currencyCode }}}}</td>
                <td style="padding: 6px; text-align: right;">{{{{ formatMoney(fee.amount, fee.currencyCode) }}}}</td>
                <td style="padding: 6px; text-align: right;"><strong style="color: #2563eb; font-size: 13px;">{{{{ formatMoney(fee.appliedAmount, fee.currencyCode) }}}}</strong></td>
                <td style="padding: 6px; color: #64748b;">{{{{ fee.itemRemark || '-' }}}}</td>
              </tr>
            </table>
          </div>
        </div>
      </div>
"""

with open('pages/payment-app-dir4-master-detail-side.html', 'w', encoding='utf-8') as f:
    f.write(wrap_page('付费申请 · 方向4：主从联动订单切换台 (Master-Detail Side)', '方向 4: 主从切换', dir4_css, dir4_body, dir4_script))
print("Created pages/payment-app-dir4-master-detail-side.html")

# ==============================================================================
# Direction 5: Bloomberg Financial Full-Screen Grid
# ==============================================================================
dir5_css = """
    .grid-card { background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; flex: 1; display: flex; flex-direction: column; overflow: hidden; }
    .pro-ticker { background: #0f172a; color: #f8fafc; padding: 4px 12px; display: flex; justify-content: space-between; align-items: center; border-radius: 4px; font-size: 11px; }
"""

dir5_body = f"""
      {get_status_alert()}
      <div class="pro-ticker">
        <div style="display: flex; gap: 14px; align-items: center;">
          <span>申请单: <strong style="color: #38bdf8;">{{{{ formState.applicationNo }}}}</strong></span>
          <span>出款: {{{{ myCompanyBank.shortName }}}} ({{{{ myCompanyBank.accountNo }}}})</span>
          <span>收款: {{{{ formState.settlementName }}}}</span>
          <span>最晚出款: {{{{ formState.latestPaymentDate || '-' }}}}</span>
        </div>
        <div style="display: flex; gap: 12px; align-items: center;">
          <span style="color: #cbd5e1;">净付合计: <strong style="color: #4ade80; font-size: 14px; font-family: monospace;">¥ {{{{ formatMoney(currencySummaryList[0]?.netAmount || 0) }}}}</strong></span>
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
                  <td style="padding: 6px;"><a class="pa-link">{{{{ g.commissionNum }}}}</a></td>
                  <td style="padding: 6px; font-family: monospace;">{{{{ g.mblNum || '-' }}}}</td>
                  <td style="padding: 6px;">{{{{ g.podName }}}}</td>
                  <td style="padding: 6px;"><strong>{{{{ f.feeCodeName }}}}</strong></td>
                  <td style="padding: 6px;">{{{{ f.currencyCode }}}}</td>
                  <td style="padding: 6px; text-align: right;">{{{{ formatMoney(f.amount, f.currencyCode) }}}}</td>
                  <td style="padding: 6px; text-align: right;">{{{{ Number(f.exchangeRate || 1).toFixed(4) }}}}</td>
                  <td style="padding: 6px; text-align: right;">{{{{ formatMoney(f.unRqstPaymentAmount, f.currencyCode) }}}}</td>
                  <td style="padding: 6px; text-align: right; background: #eff6ff;"><strong style="color: #2563eb; font-size: 13px;">{{{{ formatMoney(f.appliedAmount, f.currencyCode) }}}}</strong></td>
                  <td style="padding: 6px; color: #64748b;">{{{{ f.itemRemark || '-' }}}}</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
"""

with open('pages/payment-app-dir5-high-density-excel.html', 'w', encoding='utf-8') as f:
    f.write(wrap_page('付费申请 · 方向5：大宽屏高密度金融表格 (Bloomberg Grid)', '方向 5: 高密表格', dir5_css, dir5_body))
print("Created pages/payment-app-dir5-high-density-excel.html")

print("Directions 1 to 5 built successfully.")
