# coding: utf-8
import os
from generate_helpers import wrap_page, get_top_action_bar, get_status_alert

# ==============================================================================
# Direction 6: Dual-Ledger Reconciliation Deck (50% / 50%)
# ==============================================================================
dir6_css = """
    .reconcile-split { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; flex: 1; overflow: hidden; }
    .rec-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 1px 2px rgba(15,23,42,0.03); }
    .rec-meter { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; padding: 6px 12px; display: flex; justify-content: space-between; align-items: center; font-size: 11px; flex-shrink: 0; }
"""

dir6_body = f"""
      {get_status_alert()}
      <div class="pa-voucher-card">
        {get_top_action_bar()}
      </div>

      <!-- 中央动态勾稽平衡仪 -->
      <div class="rec-meter">
        <div style="display: flex; align-items: center; gap: 8px;">
          <iconify-icon icon="ant-design:sync-outlined" style="color: #16a34a; font-size: 14px;"></iconify-icon>
          <strong style="color: #166534;">票费动态对账平衡仪：</strong>
          <span>业务应付: <strong>¥ {{{{ formatDecimal(totalPayAmountRMB) }}}}</strong></span>
          <span style="color: #cbd5e1;">⟷</span>
          <span>录入发票: <strong>¥ {{{{ formatDecimal(totalInvoiceAmount) }}}}</strong></span>
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
          <span>勾稽差额:</span>
          <strong :style="{{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#d97706', fontSize: '13px' }}">
            {{{{ invoiceDiffAmount === 0 ? '✓ 票费已平 (¥0.00)' : ('差额: ¥' + formatDecimal(invoiceDiffAmount)) }}}}
          </strong>
        </div>
      </div>

      <!-- 左右双联对账台 (左费用 50% ⟷ 右发票 50%) -->
      <div class="reconcile-split">
        <!-- 左侧：费用清单 -->
        <div class="rec-card">
          <div style="padding: 6px 10px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
            <strong>左联：待付款业务费用明细 ({{{{ totalFeeCount }}}} 笔)</strong>
            <a-button type="primary" size="small" @click="handleOpenAddFeeDrawer">+ 添加费用</a-button>
          </div>
          <div style="flex: 1; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
              <tr style="background: #f1f5f9; border-bottom: 1px solid #cbd5e1; text-align: left;">
                <th style="padding: 6px;">单号</th><th style="padding: 6px;">费用名</th><th style="padding: 6px;">币别</th><th style="padding: 6px; text-align: right;">本次出款</th><th style="padding: 6px;">垫资风险</th>
              </tr>
              <template v-for="g in orderFeeGroups" :key="g.groupId">
                <tr v-for="f in g.fees" :key="f.id" style="border-bottom: 1px solid #f1f5f9;">
                  <td style="padding: 6px;"><a class="pa-link">{{{{ g.commissionNum }}}}</a></td>
                  <td style="padding: 6px;"><strong>{{{{ f.feeCodeName }}}}</strong></td>
                  <td style="padding: 6px;">{{{{ f.currencyCode }}}}</td>
                  <td style="padding: 6px; text-align: right;"><strong style="color: #2563eb;">{{{{ formatMoney(f.appliedAmount, f.currencyCode) }}}}</strong></td>
                  <td style="padding: 6px;">{{{{ g.unSettledReceiveList.length > 0 ? '⚠️ 未结垫资' : '✓ 客户已结' }}}}</td>
                </tr>
              </template>
            </table>
          </div>
        </div>

        <!-- 右侧：发票凭据与 OCR -->
        <div class="rec-card">
          <div style="padding: 6px 10px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
            <strong>右联：发票核验与进项池 ({{{{ formState.invoiceRows.length }}}} 张)</strong>
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

with open('pages/payment-app-dir6-invoice-matching-deck.html', 'w', encoding='utf-8') as f:
    f.write(wrap_page('付费申请 · 方向6：票费双联对账台 (Reconciliation Deck)', '方向 6: 双联对账', dir6_css, dir6_body))
print("Created pages/payment-app-dir6-invoice-matching-deck.html")

# ==============================================================================
# Direction 7: Freight Container Kanban Cards
# ==============================================================================
dir7_css = """
    .kanban-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 10px; flex: 1; overflow-y: auto; padding-right: 4px; }
    .container-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 1px 3px rgba(15,23,42,0.04); }
    .container-card-head { background: #1e293b; color: #fff; padding: 6px 10px; display: flex; justify-content: space-between; align-items: center; }
"""

dir7_body = f"""
      {get_status_alert()}
      <div class="pa-voucher-card">
        {get_top_action_bar()}
      </div>

      <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 12px; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; gap: 10px; align-items: center;">
          <strong style="font-size: 13px;">货运提单集装箱卡片流 (Container Stubs)</strong>
          <span style="color: #64748b;">共 {{ orderFeeGroups.length }} 票待付业务单据</span>
        </div>
        <a-button type="primary" size="small" @click="handleOpenAddFeeDrawer">+ 引入集装箱业务</a-button>
      </div>

      <!-- 卡片流展示 -->
      <div class="kanban-grid">
        <div v-for="grp in orderFeeGroups" :key="grp.groupId" class="container-card">
          <div class="container-card-head">
            <div style="display: flex; align-items: center; gap: 6px;">
              <iconify-icon icon="ant-design:code-sandbox-outlined" style="color: #38bdf8; font-size: 14px;"></iconify-icon>
              <strong style="font-family: monospace;">{{{{ grp.commissionNum }}}}</strong>
            </div>
            <span style="font-size: 10px; background: rgba(255,255,255,0.15); padding: 1px 5px; border-radius: 2px;">{{{{ grp.podName }}}} · {{{{ grp.carrierName }}}}</span>
          </div>

          <div style="padding: 8px 10px; flex: 1; display: flex; flex-direction: column; gap: 6px;">
            <div style="display: flex; justify-content: space-between; color: #64748b; font-size: 10px;">
              <span>主单: {{{{ grp.mblNum || '-' }}}}</span>
              <span>箱型: {{{{ grp.totalCtn || '-' }}}}</span>
            </div>
            <div style="color: #334155; font-size: 11px;">
              客户: <strong>{{{{ grp.clientName }}}}</strong>
            </div>

            <!-- 费用项清单 -->
            <div style="border-top: 1px dashed #e2e8f0; padding-top: 6px; display: flex; flex-direction: column; gap: 4px;">
              <div v-for="f in grp.fees" :key="f.id" style="display: flex; justify-content: space-between; align-items: center; background: #f8fafc; padding: 3px 6px; border-radius: 3px;">
                <span>{{{{ f.feeCodeName }}}}</span>
                <strong style="color: #2563eb;">{{{{ f.currencyCode }}}} {{{{ formatDecimal(f.appliedAmount) }}}}</strong>
              </div>
            </div>

            <div style="margin-top: auto; border-top: 1px solid #f1f5f9; padding-top: 6px; display: flex; justify-content: space-between; font-size: 10px;">
              <span :style="{{ color: grp.unSettledReceiveList.length > 0 ? '#d97706' : '#16a34a', fontWeight: 600 }}">
                {{{{ grp.unSettledReceiveList.length > 0 ? '⚠️ 未结垫资风险' : '✓ 应收已结清' }}}}
              </span>
              <span>本单合计: <strong style="color: #0f172a; font-size: 12px;">¥ {{{{ formatDecimal(grp.fees.reduce((a,b)=>a+b.appliedAmount, 0)) }}}}</strong></span>
            </div>
          </div>
        </div>
      </div>
"""

with open('pages/payment-app-dir7-kanban-cards.html', 'w', encoding='utf-8') as f:
    f.write(wrap_page('付费申请 · 方向7：货运集装箱卡片流 (Kanban Cards)', '方向 7: 集装箱卡片', dir7_css, dir7_body))
print("Created pages/payment-app-dir7-kanban-cards.html")

# ==============================================================================
# Direction 8: Ant Design Pro Classic Clean Tabs
# ==============================================================================
dir8_css = """
    .pro-tabs-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; flex: 1; display: flex; flex-direction: column; overflow: hidden; }
"""

dir8_body = f"""
      {get_status_alert()}
      <div class="pa-voucher-card">
        {get_top_action_bar()}
        <!-- 极简单行底账栏 -->
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); padding: 8px 12px; gap: 12px; background: #fafbfc; border-top: 1px solid #f1f5f9; font-size: 11px;">
          <div><span style="color:#64748b;">出款公司:</span> <strong>{{{{ formState.companyName }}}}</strong></div>
          <div><span style="color:#64748b;">收款对象:</span> <strong>{{{{ formState.settlementName }}}}</strong></div>
          <div><span style="color:#64748b;">付款排期:</span> <span>{{{{ formState.latestPaymentDate }}}} 至 {{{{ formState.predictReturnDate }}}}</span></div>
          <div style="text-align: right;"><span style="color:#64748b;">净付金额:</span> <strong style="color: #2563eb; font-size: 14px;">¥ {{{{ formatMoney(currencySummaryList[0]?.netAmount || 0) }}}}</strong></div>
        </div>
      </div>

      <!-- 主体：Ant Design 原生大全宽标签页 -->
      <div class="pro-tabs-card">
        <a-tabs default-active-key="1" style="height: 100%; display: flex; flex-direction: column;" :tab-bar-style="{{ margin: '0', padding: '0 12px', background: '#f8fafc' }}">
          <a-tab-pane key="1" tab="业务费用明细 (共 {{ totalFeeCount }} 笔)">
            <div style="padding: 10px; height: 100%; overflow-y: auto;">
              <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
                <tr style="background: #f1f5f9; border-bottom: 1px solid #e2e8f0; text-align: left;">
                  <th style="padding: 6px;">委托号</th><th style="padding: 6px;">提单号</th><th style="padding: 6px;">港口</th><th style="padding: 6px;">费用名称</th><th style="padding: 6px;">币别</th><th style="padding: 6px; text-align: right;">本次申请</th><th style="padding: 6px;">风控</th>
                </tr>
                <template v-for="g in orderFeeGroups" :key="g.groupId">
                  <tr v-for="f in g.fees" :key="f.id" style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 6px;"><a class="pa-link">{{{{ g.commissionNum }}}}</a></td>
                    <td style="padding: 6px; font-family: monospace;">{{{{ g.mblNum || '-' }}}}</td>
                    <td style="padding: 6px;">{{{{ g.podName }}}}</td>
                    <td style="padding: 6px;"><strong>{{{{ f.feeCodeName }}}}</strong></td>
                    <td style="padding: 6px;">{{{{ f.currencyCode }}}}</td>
                    <td style="padding: 6px; text-align: right;"><strong style="color: #2563eb;">{{{{ formatMoney(f.appliedAmount, f.currencyCode) }}}}</strong></td>
                    <td style="padding: 6px;">{{{{ g.unSettledReceiveList.length > 0 ? '⚠️ 垫资' : '✓ 结清' }}}}</td>
                  </tr>
                </template>
              </table>
            </div>
          </a-tab-pane>

          <a-tab-pane key="2" tab="发票核对中心 ({{ formState.invoiceRows.length }} 张)">
            <div style="padding: 12px;">
              <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
                <tr style="background: #f8fafc; border-bottom: 1px solid #e2e8f0; text-align: left;">
                  <th style="padding: 6px;">发票代码/号码</th><th style="padding: 6px;">开票日期</th><th style="padding: 6px;">销售方企业</th><th style="padding: 6px; text-align: right;">发票金额</th>
                </tr>
                <tr v-for="(inv, idx) in formState.invoiceRows" :key="idx" style="border-bottom: 1px solid #f1f5f9;">
                  <td style="padding: 6px; font-family: monospace;">{{{{ inv.invoiceNo }}}}</td>
                  <td style="padding: 6px;">{{{{ inv.invoiceDate }}}}</td>
                  <td style="padding: 6px;">{{{{ inv.sellerName }}}}</td>
                  <td style="padding: 6px; text-align: right; font-weight: 700;">¥ {{{{ formatDecimal(inv.invoiceAmount) }}}}</td>
                </tr>
              </table>
            </div>
          </a-tab-pane>

          <a-tab-pane key="3" tab="审批流转跟踪与节点">
            <div style="padding: 12px;">
              <div v-for="node in workflowNodes" :key="node.nodeName" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 6px 10px; margin-bottom: 6px;">
                <div style="display: flex; justify-content: space-between;">
                  <strong>{{{{ node.nodeName }}}} ({{{{ node.operatorName }}}})</strong>
                  <span :style="{{ color: node.status === 'passed' ? '#16a34a' : (node.status === 'rejected' ? '#dc2626' : '#64748b') }}">{{{{ node.statusText }}}}</span>
                </div>
                <div v-if="node.comment" style="color: #dc2626; margin-top: 3px;">{{{{ node.comment }}}}</div>
              </div>
            </div>
          </a-tab-pane>
        </a-tabs>
      </div>
"""

with open('pages/payment-app-dir8-compact-tabbed-pro.html', 'w', encoding='utf-8') as f:
    f.write(wrap_page('付费申请 · 方向8：极致极简标签页工作台 (AntD Pro Pure)', '方向 8: 官方Tabs', dir8_css, dir8_body))
print("Created pages/payment-app-dir8-compact-tabbed-pro.html")

# ==============================================================================
# Direction 9: Executive Dashboard + Drawer Focused
# ==============================================================================
dir9_css = """
    .dash-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; flex: 1; }
    .dash-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 16px; display: flex; flex-direction: column; justify-content: space-between; }
"""

dir9_body = f"""
      {get_status_alert()}
      <div class="pa-voucher-card">
        {get_top_action_bar()}
      </div>

      <div class="dash-grid">
        <!-- 卡片 1: 往来资金路由 -->
        <div class="dash-card">
          <div>
            <div style="font-weight: 700; font-size: 13px; color: #0f172a; margin-bottom: 8px;">1. 往来资金账户路由</div>
            <div style="line-height: 1.8; color: #475569;">
              <div>我司出款公司: <strong>{{{{ formState.companyName }}}}</strong></div>
              <div>我司出款账户: {{{{ myCompanyBank.shortName }}}} ({{{{ myCompanyBank.accountNo }}}})</div>
              <div>对方收款单位: <strong>{{{{ formState.settlementName }}}}</strong></div>
              <div>最晚出款时限: {{{{ formState.latestPaymentDate || '未指定' }}}}</div>
            </div>
          </div>
          <div style="border-top: 1px solid #f1f5f9; padding-top: 6px; text-align: right;">
            <a-tag color="blue">结算档案直连已锁定</a-tag>
          </div>
        </div>

        <!-- 卡片 2: 业务费用与风控 -->
        <div class="dash-card">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-weight: 700; font-size: 13px;">2. 待付业务费用清单</span>
              <a-button type="primary" size="small" @click="handleOpenAddFeeDrawer">增删费用抽屉</a-button>
            </div>
            <div style="line-height: 1.8;">
              <div>关联业务票数: <strong>{{{{ orderFeeGroups.length }}}} 票</strong> · 费用笔数: <strong>{{{{ totalFeeCount }}}} 笔</strong></div>
              <div>本次申请净额: <strong style="color: #2563eb; font-size: 16px;">¥ {{{{ formatMoney(currencySummaryList[0]?.netAmount || 0) }}}}</strong></div>
              <div>垫资风险状态: <span :style="{{ color: formState.isReceiveAllSettled ? '#16a34a' : '#d97706', fontWeight: 600 }}">{{{{ formState.isReceiveAllSettled ? '✓ 无垫资风险' : '⚠️ 存在未结垫资' }}}}</span></div>
            </div>
          </div>
          <div style="border-top: 1px solid #f1f5f9; padding-top: 6px; display: flex; justify-content: space-between;">
            <span style="color: #64748b;">点击右上角滑出全屏明细抽屉</span>
          </div>
        </div>

        <!-- 卡片 3: 发票核验中心 -->
        <div class="dash-card">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-weight: 700; font-size: 13px;">3. 发票核对与勾稽中心</span>
              <a-button size="small" @click="showInputInvoicePicker = true">进项发票池</a-button>
            </div>
            <div style="line-height: 1.8;">
              <div>发票录入模式: <strong>{{{{ formState.invoiceProcess === 1 ? '先票后付' : (formState.invoiceProcess === 0 ? '先付后票' : '不开票') }}}}</strong></div>
              <div>已录发票张数: <strong>{{{{ formState.invoiceRows.length }}}} 张</strong> · 发票总额: <strong>¥ {{{{ formatDecimal(totalInvoiceAmount) }}}}</strong></div>
              <div>勾稽差额判定: <strong :style="{{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#d97706' }}">{{{{ invoiceDiffAmount === 0 ? '✓ 票费已平' : ('待补 ¥' + formatDecimal(invoiceDiffAmount)) }}}}</strong></div>
            </div>
          </div>
          <div style="border-top: 1px solid #f1f5f9; padding-top: 6px; text-align: right;">
            <a-button size="small" type="primary" ghost @click="handleAddInvoiceRow">+ 录入单张发票</a-button>
          </div>
        </div>

        <!-- 卡片 4: 审批与单据档案 -->
        <div class="dash-card">
          <div>
            <div style="font-weight: 700; font-size: 13px; margin-bottom: 8px;">4. 审批流程与单据档案</div>
            <div style="line-height: 1.8;">
              <div>当前流转状态: <span class="pa-status-tag" :class="'pa-status-' + formState.status">{{{{ currentStatusMeta.stampText }}}}</span></div>
              <div v-if="workflowNodes[1]?.comment" style="color: #dc2626;">驳回原因: {{{{ workflowNodes[1].comment }}}}</div>
              <div>归档单据附件: <strong>{{{{ applicationAttachmentGroups.reduce((acc, g) => acc + g.items.length, 0) }}}} 份</strong></div>
            </div>
          </div>
          <div style="border-top: 1px solid #f1f5f9; padding-top: 6px; text-align: right;">
            <a-button type="primary" size="small" @click="handleSubmitAudit">立即送审</a-button>
          </div>
        </div>
      </div>
"""

with open('pages/payment-app-dir9-drawer-focused.html', 'w', encoding='utf-8') as f:
    f.write(wrap_page('付费申请 · 方向9：全景看板 + 侧滑抽屉工作台 (Drawer Focused)', '方向 9: 仪表大盘', dir9_css, dir9_body))
print("Created pages/payment-app-dir9-drawer-focused.html")

# ==============================================================================
# Direction 10: Global Multi-Currency Freight Forex Voucher
# ==============================================================================
dir10_css = """
    .forex-banner { background: #0f172a; color: #fff; padding: 6px 12px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }
    .forex-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; flex: 1; display: flex; flex-direction: column; overflow: hidden; }
"""

dir10_body = f"""
      {get_status_alert()}
      <!-- 国际多币别头寸与汇率锁定看板 -->
      <div class="forex-banner">
        <div style="display: flex; gap: 14px; align-items: center;">
          <strong style="color: #38bdf8; font-size: 13px;">GLOBAL MULTI-CURRENCY VOUCHER</strong>
          <span style="color: #94a3b8;">原币多币别结算口径</span>
        </div>
        <div style="display: flex; gap: 14px; align-items: center;">
          <span v-for="c in currencySummaryList" :key="c.currencyCode">
            {{{{ c.currencyCode }}}}: <strong style="font-family: monospace; font-size: 13px; color: #4ade80;">{{{{ formatMoney(c.netAmount, c.currencyCode) }}}}</strong>
          </span>
          <a-tag color="purple">折算汇率已锁</a-tag>
        </div>
      </div>

      <div class="pa-voucher-card">
        {get_top_action_bar()}
      </div>

      <!-- 多币别费用双轨核算大表 -->
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
                  <td style="padding: 6px;"><a class="pa-link">{{{{ g.commissionNum }}}}</a></td>
                  <td style="padding: 6px; font-family: monospace;">{{{{ g.mblNum || '-' }}}}</td>
                  <td style="padding: 6px;"><strong>{{{{ f.feeCodeName }}}}</strong></td>
                  <td style="padding: 6px;"><a-tag color="blue">{{{{ f.currencyCode }}}}</a-tag></td>
                  <td style="padding: 6px; text-align: right;">{{{{ formatMoney(f.amount, f.currencyCode) }}}}</td>
                  <td style="padding: 6px; text-align: right;">{{{{ Number(f.exchangeRate || 1).toFixed(4) }}}}</td>
                  <td style="padding: 6px; text-align: right; background: #eff6ff;"><strong style="color: #2563eb;">¥ {{{{ formatDecimal(f.appliedAmount * (f.exchangeRate || 1)) }}}}</strong></td>
                  <td style="padding: 6px;">{{{{ g.unSettledReceiveList.length > 0 ? '⚠️ 未结垫资' : '✓ 客户已结' }}}}</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
"""

with open('pages/payment-app-dir10-executive-bilingual.html', 'w', encoding='utf-8') as f:
    f.write(wrap_page('付费申请 · 方向10：国际多币别外贸对账凭证 (Global Multi-Currency)', '方向 10: 多币对账', dir10_css, dir10_body))
print("Created pages/payment-app-dir10-executive-bilingual.html")

print("All 10 directions generated successfully.")
