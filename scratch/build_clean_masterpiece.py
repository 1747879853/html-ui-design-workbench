# coding: utf-8
import re

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_script = text.find('<script>')
script_block = text[idx_script:]

idx_drawers = text.find('<!-- ====================================================================\n             弹窗 1：添加费用抽屉')
modals_block = text[idx_drawers:idx_script]

clean_masterpiece = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>付费申请编辑详情 - 费用管理 (PaymentApplicationForm · 极致清爽金融对账台)</title>

  <!-- 核心样式：Ant Design Vue 4 重置样式与通用规范 -->
  <link rel="stylesheet" href="../assets/vendor/reset.css">
  <link rel="stylesheet" href="../assets/css/common.css">

  <!-- 本地核心依赖 (Dayjs、Vue 3、Ant Design Vue 4.2.6、Iconify 图标) -->
  <script src="../assets/vendor/dayjs-bundle.min.js"></script>
  <script src="../assets/vendor/vue.global.prod.js"></script>
  <script src="../assets/vendor/antd.min.js"></script>
  <script src="../assets/vendor/iconify-icon.min.js"></script>
  <script src="../assets/js/common.js"></script>

  <style>
    /* ==========================================================================
       付费申请编辑详情 (PaymentApplicationForm)
       全新极简秩序重构 · 彻底告别“太乱”：
       1. 【色彩克制】：彻底剔除花哨撞色（紫卡、青标、深蓝、墨绿等全部收敛），全站以高质感冷灰+商务深蓝为基调；
       2. 【剔除噪音】：彻底删减所有设计自嗨文案（“出款责任方”、“实时生效”、“双签核标准版”等无意义元信息）；
       3. 【单表一体化】：彻底消灭嵌套子表格与虚线树，将订单与费用合一，视线一览到底；
       4. 【底栏 50/50 绝对平衡】：左发票 (50%) + 右流转 (50%) 严格等宽等高对齐，告别畸形比例与半截空洞！
       ========================================================================== */

    [v-cloak] {
      display: none !important;
    }

    body {
      background-color: #f8fafc;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
      margin: 0;
      padding: 0;
      font-size: 12px;
      overflow-x: hidden;
    }

    .tabular-nums {
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum";
    }

    .pa-workbench {
      height: 100vh;
      max-height: 1080px;
      padding: 6px 12px 10px;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      gap: 6px;
      max-width: 1920px;
      margin: 0 auto;
      overflow: hidden;
    }

    /* 1. 顶部场景沙盘栏 (纯粹极简单行) */
    .wb-scenario-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      background: #1e293b;
      color: #f8fafc;
      border-radius: 4px;
      padding: 3px 10px;
      flex-shrink: 0;
    }

    .wb-scenario-left,
    .wb-scenario-right {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .wb-scenario-title {
      font-size: 11px;
      font-weight: 600;
      color: #94a3b8;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .wb-scenario-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 1px 7px;
      border-radius: 3px;
      font-size: 11px;
      cursor: pointer;
      background: rgba(255, 255, 255, 0.08);
      color: #cbd5e1;
      border: 1px solid rgba(255, 255, 255, 0.12);
      transition: all 0.15s ease;
      user-select: none;
    }

    .wb-scenario-pill:hover {
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
    }

    .wb-scenario-pill.active {
      background: #2563eb;
      color: #ffffff;
      border-color: #3b82f6;
      font-weight: 600;
    }

    /* 2. 状态警示通知条 (极简内敛) */
    .pa-status-alert {
      padding: 4px 12px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      font-size: 11px;
      flex-shrink: 0;
    }
    .pa-alert-reject {
      background: #fef2f2;
      border: 1px solid #fecaca;
      color: #991b1b;
    }
    .pa-alert-pending {
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1e40af;
    }
    .pa-alert-supplement {
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      color: #166534;
    }

    /* 3. 主凭证底账面板 (一体化白底 · 统一四列 · 零多层嵌套) */
    .pa-voucher-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
      flex-shrink: 0;
      overflow: hidden;
    }

    .pa-voucher-toolbar {
      padding: 5px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #f1f5f9;
      background: #ffffff;
    }

    .pa-doc-code {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 14px;
      font-weight: 700;
      color: #0f172a;
    }

    .pa-status-tag {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      padding: 1px 6px;
      border-radius: 3px;
      font-size: 11px;
      font-weight: 600;
    }
    .pa-status-0 { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
    .pa-status-1 { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }
    .pa-status-2 { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
    .pa-status-3 { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
    .pa-status-4 { background: #ecfeff; color: #0e7490; border: 1px solid #a5f3fc; }
    .pa-status-5 { background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; }

    /* 四列平齐底账栅格 */
    .pa-ledger-row {
      display: grid;
      grid-template-columns: minmax(300px, 1.25fr) minmax(340px, 1.4fr) minmax(300px, 1.25fr) 260px;
      padding: 6px 12px;
      gap: 12px;
      background: #ffffff;
    }

    .pa-ledger-block {
      display: flex;
      flex-direction: column;
      gap: 4px;
      border-right: 1px solid #f1f5f9;
      padding-right: 12px;
    }
    .pa-ledger-block:last-child {
      border-right: none;
      padding-right: 0;
    }

    .pa-block-head {
      font-size: 11px;
      font-weight: 600;
      color: #64748b;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 18px;
    }

    .pa-field-line {
      display: flex;
      align-items: center;
      gap: 6px;
      height: 24px;
      font-size: 11px;
    }

    .pa-field-label {
      color: #64748b;
      white-space: nowrap;
      width: 52px;
      flex-shrink: 0;
      font-size: 11px;
    }

    .pa-bank-text {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 3px;
      padding: 0 6px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      box-sizing: border-box;
      font-size: 11px;
      color: #1e293b;
    }

    .pa-hero-amount {
      font-size: 18px;
      font-weight: 800;
      color: #0f172a;
      font-family: ui-monospace, monospace;
      line-height: 1;
    }

    /* 4. 中部费用主舞台 (单表合一 · 消除套娃表格) */
    .pa-fee-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
      flex: 1 1 auto;
      min-height: 260px;
      overflow: hidden;
    }

    .pa-fee-toolbar {
      padding: 5px 12px;
      background: #ffffff;
      border-bottom: 1px solid #f1f5f9;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }

    .pa-section-name {
      font-size: 13px;
      font-weight: 600;
      color: #0f172a;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .pa-section-name::before {
      content: "";
      width: 3px;
      height: 12px;
      background: #2563eb;
      border-radius: 2px;
    }

    .pa-table-wrapper {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
    }

    .pa-pure-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
      table-layout: fixed;
    }

    .pa-pure-table th {
      position: sticky;
      top: 0;
      z-index: 5;
      background: #f8fafc;
      color: #475569;
      font-weight: 600;
      padding: 6px 8px;
      border-bottom: 1px solid #e2e8f0;
      text-align: left;
      white-space: nowrap;
    }

    /* 订单委托分组隔条 (极简统合行) */
    .pa-order-banner td {
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      border-bottom: 1px solid #e2e8f0;
      padding: 4px 8px;
      font-size: 11px;
      color: #334155;
    }

    /* 费用明细行 */
    .pa-fee-row td {
      padding: 6px 8px;
      border-bottom: 1px solid #f1f5f9;
      vertical-align: middle;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      background: #ffffff;
    }
    .pa-fee-row:hover td {
      background: #fafbfc;
    }

    .pa-dir-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 18px;
      height: 18px;
      border-radius: 2px;
      font-size: 10px;
      font-weight: 700;
    }
    .pa-dir-pay { background: #fff7ed; color: #ea580c; border: 1px solid #fdba74; }
    .pa-dir-rec { background: #eff6ff; color: #2563eb; border: 1px solid #93c5fd; }

    .pa-fee-footer {
      padding: 5px 12px;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      font-size: 11px;
    }

    /* 5. 底部双翼协同区 (严格 50% / 50% 均分 · 高度 250px · 左右视觉绝对对称) */
    .pa-bottom-split {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      flex: 0 0 240px;
      height: 240px;
      box-sizing: border-box;
      overflow: hidden;
    }

    .pa-dock-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
      height: 100%;
      overflow: hidden;
      box-sizing: border-box;
    }

    .pa-dock-header {
      padding: 5px 10px;
      background: #f8fafc;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      height: 34px;
      box-sizing: border-box;
    }

    .pa-dock-body {
      flex: 1;
      overflow-y: auto;
      padding: 6px 10px;
    }

    .pa-dock-footer {
      padding: 4px 10px;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
      color: #64748b;
      flex-shrink: 0;
      height: 26px;
      box-sizing: border-box;
    }

    /* 发票表格 */
    .pa-inv-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
    }
    .pa-inv-table th {
      background: #f8fafc;
      color: #475569;
      font-weight: 600;
      padding: 4px 6px;
      border-bottom: 1px solid #e2e8f0;
      text-align: left;
      white-space: nowrap;
    }
    .pa-inv-table td {
      padding: 3px 6px;
      border-bottom: 1px solid #f1f5f9;
      vertical-align: middle;
      white-space: nowrap;
    }

    /* 审批流转节点卡片 (极简内敛) */
    .pa-step-card {
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 5px 8px;
      margin-bottom: 6px;
      background: #ffffff;
      font-size: 11px;
    }
    .pa-step-reject {
      background: #fffbfa;
      border-color: #fecaca;
    }
    .pa-step-pass {
      background: #f8fafc;
      border-color: #e2e8f0;
    }

    .pa-link {
      color: #2563eb;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
    }
    .pa-link:hover {
      text-decoration: underline;
    }
    .pa-copy-icon {
      color: #94a3b8;
      cursor: pointer;
      margin-left: 3px;
      font-size: 11px;
    }
    .pa-copy-icon:hover {
      color: #2563eb;
    }
  </style>
</head>
<body>
  <div id="app" v-cloak>
    <div class="pa-workbench">

      <!-- ====================================================================
           1. 顶部场景沙盘栏 (开发验收极简单行)
           ==================================================================== -->
      <div class="wb-scenario-bar">
        <div class="wb-scenario-left">
          <span class="wb-scenario-title">业务场景沙盒:</span>
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
          <a-switch
            v-model:checked="simulateSubmitStepFail"
            size="small"
            checked-children="模拟送审失败"
            un-checked-children="正常送审"
          ></a-switch>
          <a-button size="small" type="primary" ghost style="font-size: 10px; height: 20px; padding: 0 6px;" @click="showAddFeeDrawer = true">
            添加费用测试
          </a-button>
          <a-button size="small" type="primary" style="font-size: 10px; height: 20px; padding: 0 6px;" @click="showHandoffDrawer = true">
            交接文档
          </a-button>
        </div>
      </div>

      <!-- ====================================================================
           2. 关键业务状态通知条 (仅当需要时出现，内敛克制)
           ==================================================================== -->
      <div v-if="formState.status === 2" class="pa-status-alert pa-alert-reject">
        <div style="display: flex; align-items: center; gap: 6px;">
          <iconify-icon icon="ant-design:close-circle-filled" style="color: #dc2626; font-size: 13px;"></iconify-icon>
          <strong>审批已驳回：</strong>
          <span>{{ (workflowNodes[1] || {}).comment || '请补充水单盖章件后重新提交。' }}</span>
          <span style="color: #64748b; margin-left: 8px;">(审核人: {{ (workflowNodes[1] || {}).operatorName }} · {{ (workflowNodes[1] || {}).operateTime }})</span>
        </div>
        <a-tag color="error" style="font-size: 10px; line-height: 16px; margin: 0;">需修改后重新送审</a-tag>
      </div>

      <div v-else-if="formState.status === 1" class="pa-status-alert pa-alert-pending">
        <div style="display: flex; align-items: center; gap: 6px;">
          <iconify-icon icon="ant-design:clock-circle-filled" style="color: #2563eb; font-size: 13px;"></iconify-icon>
          <strong>当前状态：财务初审中</strong>
          <span>特批垫资审批流转中，单据字段已被工作流锁定。</span>
        </div>
        <a-button size="small" danger ghost style="font-size: 10px; height: 18px; padding: 0 6px;" @click="handleWithdrawAudit">
          撤回送审
        </a-button>
      </div>

      <div v-else-if="formState.status === 4 && invoiceDiffAmount > 0" class="pa-status-alert pa-alert-supplement">
        <div style="display: flex; align-items: center; gap: 6px;">
          <iconify-icon icon="ant-design:info-circle-filled" style="color: #16a34a; font-size: 13px;"></iconify-icon>
          <strong>后补发票通道：</strong>
          <span>首笔出款已结算，待补发票差额 <strong>¥{{ formatDecimal(invoiceDiffAmount) }}</strong>。</span>
        </div>
        <a-button size="small" type="primary" style="font-size: 10px; height: 18px; padding: 0 6px;" @click="handleAddInvoiceRow">
          立即补票
        </a-button>
      </div>

      <!-- ====================================================================
           3. 主凭证底账面板 (一体白底 · 统一 4 列 · 极致平齐)
           ==================================================================== -->
      <div class="pa-voucher-card">
        <!-- 凭证操作标头 -->
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

          <!-- 右侧动作按钮 -->
          <div style="display: flex; align-items: center; gap: 6px;">
            <a-button size="small" style="font-size: 11px;" @click="handleCreateBlank">
              新建空白
            </a-button>
            <a-button size="small" style="font-size: 11px;" :disabled="!isMainFormEditable" @click="handleSaveDraft">
              保存草稿
            </a-button>
            <a-button size="small" type="primary" style="font-size: 11px;" :disabled="!canSubmit" @click="handleSubmitAudit">
              {{ formState.status === 2 ? '重新送审' : '提交送审' }}
            </a-button>
            <a-dropdown>
              <template #overlay>
                <a-menu @click="handleExportAction">
                  <a-menu-item key="excel">导出 Excel 对账凭证</a-menu-item>
                  <a-menu-item key="pdf">导出 PDF 付款凭证单</a-menu-item>
                </a-menu>
              </template>
              <a-button size="small" style="font-size: 11px;">
                导出 <iconify-icon icon="ant-design:down-outlined" style="font-size: 9px;"></iconify-icon>
              </a-button>
            </a-dropdown>
            <a-button size="small" style="font-size: 11px;" @click="handlePrintDoc">
              打印
            </a-button>
          </div>
        </div>

        <!-- 四列平齐底账表单 (严格无多层卡片嵌套) -->
        <div class="pa-ledger-row">
          <!-- Col 1: 付款主体 -->
          <div class="pa-ledger-block">
            <div class="pa-block-head">
              <span>付款主体 (我司出款)</span>
            </div>
            <div class="pa-field-line">
              <span class="pa-field-label">所属公司:</span>
              <a-select
                v-model:value="formState.companyId"
                size="small"
                style="flex: 1; min-width: 0;"
                :disabled="!isMainFormEditable"
                :options="companyOptions"
                @change="handleCompanyChange"
              ></a-select>
            </div>
            <div class="pa-field-line">
              <span class="pa-field-label">出款账户:</span>
              <div class="pa-bank-text" :title="myCompanyBank.bankName + ' · ' + myCompanyBank.accountNo">
                <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                  <strong>{{ myCompanyBank.shortName }}</strong>
                  <span class="tabular-nums" style="margin-left: 4px; color: #64748b;">{{ myCompanyBank.accountNo }}</span>
                </span>
                <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-icon" @click="copyText(myCompanyBank.accountNo, '我司付款账号')"></iconify-icon>
              </div>
            </div>
          </div>

          <!-- Col 2: 收款对象 -->
          <div class="pa-ledger-block">
            <div class="pa-block-head">
              <span>收款对象 (往来结算单位)</span>
              <a-tag v-if="orderFeeGroups.length > 0" color="blue" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">
                已锁定
              </a-tag>
            </div>
            <div class="pa-field-line">
              <span class="pa-field-label">往来单位:</span>
              <strong style="color: #0f172a; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 11px;" :title="formState.settlementName">
                {{ formState.settlementName }}
              </strong>
            </div>
            <div class="pa-field-line">
              <span class="pa-field-label">对方账户:</span>
              <a-select
                v-model:value="formState.bankAccountMap[primaryCurrencyCode]"
                size="small"
                style="flex: 1; min-width: 0;"
                :disabled="!isMainFormEditable"
                :options="getPayeeBankOptions(primaryCurrencyCode)"
                @change="markMainFormDirty"
              ></a-select>
            </div>
          </div>

          <!-- Col 3: 付款排期与附言 -->
          <div class="pa-ledger-block">
            <div class="pa-block-head">
              <span>付款排期与附言</span>
            </div>
            <div class="pa-field-line">
              <span class="pa-field-label">付款排期:</span>
              <a-date-picker
                v-model:value="formState.latestPaymentDate"
                size="small"
                value-format="YYYY-MM-DD"
                style="flex: 1; min-width: 0;"
                placeholder="最晚出款日"
                :disabled="!isMainFormEditable"
                @change="markMainFormDirty"
              ></a-date-picker>
              <span style="color: #cbd5e1; font-size: 10px;">至</span>
              <a-date-picker
                v-model:value="formState.predictReturnDate"
                size="small"
                value-format="YYYY-MM-DD"
                style="flex: 1; min-width: 0;"
                placeholder="预计回款日"
                :disabled="!isMainFormEditable"
                @change="markMainFormDirty"
              ></a-date-picker>
            </div>
            <div class="pa-field-line">
              <span class="pa-field-label">汇款附言:</span>
              <a-input
                v-model:value="formState.paymentDemand"
                size="small"
                :title="formState.paymentDemand"
                placeholder="注明提单号及业务编号..."
                :disabled="!isMainFormEditable"
                allow-clear
                @change="markMainFormDirty"
              ></a-input>
            </div>
          </div>

          <!-- Col 4: 申请结算净额 (纯白一体 · 拒绝突兀彩色) -->
          <div class="pa-ledger-block">
            <div class="pa-block-head">
              <span>申请结算净额 (付 - 收)</span>
              <span style="font-size: 10px; color: #64748b;">
                {{ formState.isCurrencyFixed ? ('固定币 · ' + formState.currencyCode) : '按原票币' }}
              </span>
            </div>
            <div class="pa-field-line" style="justify-content: space-between;">
              <span class="pa-field-label">本次净付:</span>
              <div style="display: flex; align-items: baseline; gap: 4px;">
                <span style="font-weight: 700; color: #64748b;">{{ primaryCurrencyCode }}</span>
                <span class="pa-hero-amount">{{ formatMoney(currencySummaryList[0]?.netAmount || 0, primaryCurrencyCode) }}</span>
              </div>
            </div>
            <div class="pa-field-line" style="justify-content: space-between; font-size: 10px;">
              <span v-if="!formState.isReceiveAllSettled" style="color: #d97706; font-weight: 600;">
                ⚠️ 垫资: {{ unSettledReceiveSummaryText }}
              </span>
              <span v-else style="color: #16a34a; font-weight: 500;">
                ✓ 客户已结清 (无垫资)
              </span>
              <span :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#d97706', fontWeight: 600 }">
                {{ formState.invoiceProcess === 2 ? '免开票' : (invoiceDiffAmount === 0 ? '✓ 票费已平' : '待补票差') }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- ====================================================================
           4. 业务费用明细主舞台 (单表合一 · 订单分组条 + 费用明细行 · 零嵌套表格)
           ==================================================================== -->
      <div class="pa-fee-card">
        <div class="pa-fee-toolbar">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span class="pa-section-name">业务费用明细</span>
            <span style="font-size: 11px; color: #64748b;">
              共 <strong>{{ orderFeeGroups.length }}</strong> 票业务 · <strong>{{ totalFeeCount }}</strong> 笔费用
            </span>
          </div>

          <div style="display: flex; align-items: center; gap: 6px;">
            <a-input
              v-model:value="feeFilters.orderNo"
              size="small"
              placeholder="快速筛选委托号/提单号/费用名..."
              style="width: 210px;"
              allow-clear
            >
              <template #prefix><iconify-icon icon="ant-design:search-outlined" style="color: #94a3b8;"></iconify-icon></template>
            </a-input>

            <a-button size="small" type="primary" style="font-size: 11px;" :disabled="!isMainFormEditable" @click="handleOpenAddFeeDrawer">
              + 添加费用
            </a-button>

            <a-popconfirm
              title="确认从本单移除勾选费用？"
              ok-text="确认移除"
              cancel-text="取消"
              :disabled="selectedFeeIds.length === 0 || !isMainFormEditable"
              @confirm="handleRemoveSelectedFees"
            >
              <a-button size="small" danger ghost style="font-size: 11px;" :disabled="selectedFeeIds.length === 0 || !isMainFormEditable">
                移除 ({{ selectedFeeIds.length }})
              </a-button>
            </a-popconfirm>

            <a-button size="small" style="font-size: 11px;" @click="toggleAllFeeGroups">
              {{ isAllFeeGroupsExpanded ? '全部折叠' : '全部展开' }}
            </a-button>
          </div>
        </div>

        <!-- 单表合一：订单分组隔条 + 费用数据行 (视线极度聚焦) -->
        <div class="pa-table-wrapper">
          <table class="pa-pure-table">
            <thead>
              <tr>
                <th style="width: 32px; text-align: center;">
                  <a-checkbox
                    :checked="isAllFeesSelected"
                    :indeterminate="isFeesPartiallySelected"
                    :disabled="!isMainFormEditable"
                    @change="handleSelectAllFees"
                  ></a-checkbox>
                </th>
                <th style="width: 32px; text-align: center;">序</th>
                <th style="width: 45px; text-align: center;">收付</th>
                <th style="width: 150px;">费用名称</th>
                <th style="width: 60px;">币别</th>
                <th style="width: 110px; text-align: right;">原金额</th>
                <th style="width: 85px; text-align: right;">原始汇率</th>
                <th style="width: 110px; text-align: right;">已核销金额</th>
                <th style="width: 110px; text-align: right;">可申请余额</th>
                <th v-if="formState.isCurrencyFixed" style="width: 105px; text-align: right;">申请汇率</th>
                <th v-if="formState.isCurrencyFixed" style="width: 115px; text-align: right;">折币 ({{ formState.currencyCode }})</th>
                <th style="width: 130px; text-align: right; background: #f0f7ff; color: #1e40af;">本次申请金额</th>
                <th>费用备注</th>
                <th style="width: 50px; text-align: center;">操作</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(group, gIdx) in filteredOrderFeeGroups" :key="group.groupId || gIdx">
                <!-- 订单委托分组条 (替代原先复杂的主单行，极简贯穿，承载订单暗号) -->
                <tr class="pa-order-banner">
                  <td style="text-align: center;">
                    <a-checkbox
                      :checked="isGroupAllSelected(group)"
                      :indeterminate="isGroupPartiallySelected(group)"
                      :disabled="!isMainFormEditable"
                      @change="(e) => handleSelectGroupFees(group, e.target.checked)"
                    ></a-checkbox>
                  </td>
                  <td colspan="13">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                      <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                        <span style="cursor: pointer; display: inline-flex; align-items: center; gap: 4px;" @click="group.isExpanded = !group.isExpanded">
                          <iconify-icon :icon="group.isExpanded ? 'ant-design:down-outlined' : 'ant-design:right-outlined'" style="font-size: 10px; color: #64748b;"></iconify-icon>
                          <strong style="color: #0f172a;">业务 {{ gIdx + 1 }}:</strong>
                        </span>

                        <span>
                          <span style="color: #64748b;">委托: </span>
                          <a class="pa-link" @click="handlePenetrateOrder(group.commissionNum)">{{ group.commissionNum }}</a>
                          <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-icon" @click="copyText(group.commissionNum, '委托号')"></iconify-icon>
                        </span>

                        <span v-if="group.mblNum">
                          <span style="color: #64748b;">主单: </span>
                          <strong style="font-family: monospace; color: #1e293b;">{{ group.mblNum }}</strong>
                          <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-icon" @click="copyText(group.mblNum, '主提单号')"></iconify-icon>
                        </span>

                        <span style="color: #64748b;">
                          港口: <strong style="color: #1e293b;">{{ group.podName || '-' }}</strong>
                          <span style="margin-left: 6px;">{{ group.carrierName || '-' }} · {{ group.totalCtn || '-' }}</span>
                        </span>

                        <span style="color: #64748b;">
                          客户: <span style="color: #1e293b;" :title="group.clientName">{{ group.clientName || '-' }}</span>
                        </span>
                      </div>

                      <!-- 右侧风控状态 -->
                      <div style="display: flex; align-items: center; gap: 8px;">
                        <template v-if="group.unSettledReceiveList && group.unSettledReceiveList.some(r => r.amount > 0)">
                          <span
                            v-for="unRec in group.unSettledReceiveList.filter(r => r.amount > 0)"
                            :key="unRec.currency"
                            style="color: #d97706; font-weight: 700; background: #fffbeb; border: 1px solid #fef3c7; padding: 1px 5px; border-radius: 3px; font-size: 10px;"
                          >
                            ⚠️ 垫资: {{ unRec.currency }} {{ formatDecimal(unRec.amount) }}
                          </span>
                        </template>
                        <span v-else style="color: #16a34a; font-size: 10px; font-weight: 600;">
                          ✓ 客户已结清
                        </span>

                        <span style="color: #cbd5e1;">|</span>

                        <span style="font-size: 11px; color: #475569;">
                          单计:
                          <strong v-for="(sumAmt, cCode) in group.groupCurrencySum" :key="cCode" class="tabular-nums" style="margin-left: 3px; color: #0f172a;">
                            {{ cCode }} {{ formatDecimal(sumAmt) }}
                          </strong>
                        </span>
                      </div>
                    </div>
                  </td>
                </tr>

                <!-- 费用明细行 (平铺于同一张表格，无套娃表头) -->
                <template v-if="group.isExpanded">
                  <tr
                    v-for="(fee, fIdx) in group.filteredFees"
                    :key="fee.id"
                    :id="'fee-row-' + fee.id"
                    class="pa-fee-row"
                  >
                    <td style="text-align: center;">
                      <a-checkbox
                        :checked="selectedFeeIds.includes(fee.id)"
                        :disabled="!isMainFormEditable"
                        @change="(e) => handleToggleFeeSelection(fee.id, e.target.checked)"
                      ></a-checkbox>
                    </td>
                    <td style="text-align: center;" class="tabular-nums">{{ fIdx + 1 }}</td>
                    <td style="text-align: center;">
                      <span class="pa-dir-badge" :class="fee.feeDirection === 1 ? 'pa-dir-pay' : 'pa-dir-rec'">
                        {{ fee.feeDirection === 1 ? '付' : '收' }}
                      </span>
                    </td>
                    <td><strong style="color: #0f172a;">{{ fee.feeCodeName }}</strong></td>
                    <td><span style="font-weight: 600; font-family: monospace;">{{ fee.currencyCode }}</span></td>
                    <td style="text-align: right;" class="tabular-nums">{{ formatMoney(fee.amount, fee.currencyCode) }}</td>
                    <td style="text-align: right;" class="tabular-nums">{{ Number(fee.exchangeRate || 1).toFixed(4) }}</td>
                    <td style="text-align: right; color: #64748b;" class="tabular-nums">{{ formatMoney(fee.settledAmount, fee.currencyCode) }}</td>
                    <td style="text-align: right; font-weight: 600; color: #475569;" class="tabular-nums">{{ formatMoney(fee.unRqstPaymentAmount, fee.currencyCode) }}</td>
                    <td v-if="formState.isCurrencyFixed" style="text-align: right;" class="tabular-nums">
                      <span v-if="fee.currencyCode === formState.currencyCode">1.000000</span>
                      <span v-else style="color: #7c3aed; font-weight: 600;">{{ Number(fee.rate || 0.15).toFixed(6) }}</span>
                    </td>
                    <td v-if="formState.isCurrencyFixed" style="text-align: right; color: #7c3aed; font-weight: 600;" class="tabular-nums">
                      {{ formatMoney(fee.appliedAmountConverted, formState.currencyCode) }}
                    </td>
                    <td style="text-align: right; background: #f0f7ff;">
                      <strong class="tabular-nums" style="font-size: 13px; color: #1d4ed8;">
                        {{ formatMoney(fee.appliedAmount, fee.currencyCode) }}
                      </strong>
                    </td>
                    <td style="color: #64748b;">{{ fee.itemRemark || '-' }}</td>
                    <td style="text-align: center;">
                      <a-popconfirm title="确认移出此费用？" ok-text="移出" cancel-text="取消" @confirm="handleRemoveSelectedFees([fee.id])">
                        <a-button type="link" danger size="small" style="padding: 0 2px;">移出</a-button>
                      </a-popconfirm>
                    </td>
                  </tr>
                </template>
              </template>

              <tr v-if="filteredOrderFeeGroups.length === 0">
                <td colspan="14" style="text-align: center; color: #94a3b8; padding: 32px;">
                  暂无业务费用明细。点击右上角「+ 添加费用」引入订单费用
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 费用底部汇总栏 -->
        <div class="pa-fee-footer">
          <div style="color: #64748b;">
            已勾选 <strong>{{ selectedFeeIds.length }}</strong> 笔费用
          </div>

          <div style="display: flex; align-items: center; gap: 14px;">
            <div v-for="cur in currencySummaryList" :key="cur.currencyCode">
              <span style="color: #64748b;">{{ cur.currencyCode }} 申请净付合计:</span>
              <strong class="tabular-nums" style="font-size: 14px; color: #0f172a; margin-left: 3px;">
                {{ formatMoney(cur.netAmount, cur.currencyCode) }}
              </strong>
            </div>

            <div v-if="formState.isCurrencyFixed" style="border-left: 1px solid #cbd5e1; padding-left: 10px;">
              <span style="color: #7c3aed;">固定币总计 ({{ formState.currencyCode }}):</span>
              <strong class="tabular-nums" style="font-size: 15px; color: #7c3aed; margin-left: 3px;">
                {{ formatMoney(fixedCurrencyGrandTotal, formState.currencyCode) }}
              </strong>
            </div>
          </div>
        </div>
      </div>

      <!-- ====================================================================
           5. 底部双翼协同区 (严格 50% / 50% 均分 · 高度严格统合 240px)
           ==================================================================== -->
      <div class="pa-bottom-split">
        <!-- 左翼：发票核对中心 (50% 宽 · 结构自洽) -->
        <div class="pa-dock-card">
          <div class="pa-dock-header">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-weight: 600; color: #0f172a;">发票核对中心 ({{ formState.invoiceRows.length }})</span>
              <a-radio-group
                v-model:value="formState.invoiceProcess"
                size="small"
                :disabled="!isMainFormEditable"
                @change="handleInvoiceProcessChange"
              >
                <a-radio :value="1">先票后付</a-radio>
                <a-radio :value="0">先付后票</a-radio>
                <a-radio :value="2">不开票</a-radio>
              </a-radio-group>
            </div>

            <div style="display: flex; align-items: center; gap: 6px;">
              <template v-if="formState.invoiceProcess !== 2">
                <span style="font-size: 11px; color: #64748b;">
                  票 ¥{{ formatDecimal(totalInvoiceAmount) }} / 应付 ¥{{ formatDecimal(totalPayAmountRMB) }}
                  <span :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#d97706', fontWeight: 600, marginLeft: '4px' }">
                    (差额: ¥{{ formatDecimal(invoiceDiffAmount) }})
                  </span>
                </span>
                <a-button size="small" style="font-size: 11px; height: 22px; padding: 0 6px;" @click="showInputInvoicePicker = true">
                  进项池
                </a-button>
                <a-button size="small" type="primary" ghost style="font-size: 11px; height: 22px; padding: 0 6px;" @click="handleAddInvoiceRow">
                  + 录发票
                </a-button>
              </template>
            </div>
          </div>

          <div class="pa-dock-body">
            <div v-if="formState.invoiceProcess === 2" style="padding: 24px 16px; text-align: center; color: #166534; background: #f0fdf4; border-radius: 4px;">
              <iconify-icon icon="ant-design:safety-certificate-outlined" style="font-size: 20px;"></iconify-icon>
              <div style="font-weight: 600; margin-top: 4px;">已选择「不开票」结算模式</div>
              <div style="font-size: 11px; color: #15803d; margin-top: 2px;">港口规费或豁免发票业务，审核后可直接打款</div>
            </div>

            <table v-else class="pa-inv-table">
              <thead>
                <tr>
                  <th style="width: 30px; text-align: center;">序</th>
                  <th style="width: 150px;">发票号</th>
                  <th style="width: 95px;">开票日期</th>
                  <th style="width: 160px;">销售方抬头</th>
                  <th style="width: 95px; text-align: right;">发票金额</th>
                  <th>发票附件 / OCR</th>
                  <th style="width: 40px; text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, idx) in formState.invoiceRows" :key="row.rowKey || idx">
                  <td style="text-align: center;" class="tabular-nums">{{ idx + 1 }}</td>
                  <td>
                    <a-input v-model:value="row.invoiceNo" size="small" placeholder="发票代码号" @change="handleInvoiceFieldChange(row)"></a-input>
                  </td>
                  <td>
                    <a-date-picker v-model:value="row.invoiceDate" size="small" value-format="YYYY-MM-DD" style="width: 100%;" placeholder="开票日" @change="markMainFormDirty"></a-date-picker>
                  </td>
                  <td>
                    <a-input v-model:value="row.sellerName" size="small" placeholder="销售方" @change="markMainFormDirty"></a-input>
                  </td>
                  <td style="text-align: right;">
                    <a-input-number v-model:value="row.invoiceAmount" size="small" :precision="2" style="width: 100%; text-align: right;" placeholder="0.00" @change="markMainFormDirty"></a-input-number>
                  </td>
                  <td>
                    <div style="display: flex; align-items: center; justify-content: space-between; gap: 4px;">
                      <template v-if="row.attachment">
                        <span style="font-size: 11px; color: #2563eb; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 80px;" :title="row.attachment.name">
                          {{ row.attachment.name }}
                        </span>
                        <a-button type="link" size="small" style="padding: 0; font-size: 11px;" @click="previewAttachment(row.attachment)">预览</a-button>
                      </template>
                      <template v-else>
                        <a-upload :show-upload-list="false" :before-upload="(file) => handleUploadInvoiceFile(row, file)">
                          <a-button size="small" style="font-size: 10px; height: 20px; padding: 0 4px;">上传件</a-button>
                        </a-upload>
                      </template>
                      <a-tag v-if="row.ocrStatus === 'filled'" color="success" style="font-size: 9px; line-height: 14px; margin: 0; padding: 0 3px;">已识别</a-tag>
                    </div>
                  </td>
                  <td style="text-align: center;">
                    <a-button type="link" danger size="small" style="padding: 0 2px;" @click="handleDeleteInvoiceRow(idx)">
                      <iconify-icon icon="ant-design:delete-outlined"></iconify-icon>
                    </a-button>
                  </td>
                </tr>
                <tr v-if="formState.invoiceRows.length === 0">
                  <td colspan="7" style="text-align: center; color: #94a3b8; padding: 20px;">
                    暂无发票明细。点击右上角「+ 录发票」录入
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="pa-dock-footer">
            <span>发票勾稽状态: <strong :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#d97706' }">{{ invoiceDiffAmount === 0 ? '✓ 票费已平' : ('待补 ¥' + formatDecimal(invoiceDiffAmount)) }}</strong></span>
            <span>发票共 {{ formState.invoiceRows.length }} 张</span>
          </div>
        </div>

        <!-- 右翼：审批流程跟踪与单据档案 (50% 宽 · 对称统一) -->
        <div class="pa-dock-card">
          <div class="pa-dock-header">
            <div style="display: flex; align-items: center; gap: 8px;">
              <a-radio-group v-model:value="activeRightTab" size="small" option-type="button" button-style="solid">
                <a-radio-button value="timeline">审批流转跟踪</a-radio-button>
                <a-radio-button value="attachments">单据档案 ({{ applicationAttachmentGroups.reduce((acc, g) => acc + g.items.length, 0) }})</a-radio-button>
              </a-radio-group>
            </div>

            <div>
              <span class="pa-status-tag" :class="'pa-status-' + formState.status" style="font-size: 10px;">
                {{ currentStatusMeta.stampText }}
              </span>
            </div>
          </div>

          <div class="pa-dock-body">
            <!-- 标签页 1：审批流转跟踪 -->
            <div v-if="activeRightTab === 'timeline'">
              <div
                v-for="node in workflowNodes"
                :key="node.nodeName"
                class="pa-step-card"
                :class="{ 'pa-step-reject': node.status === 'rejected', 'pa-step-pass': node.status === 'passed' }"
              >
                <div style="display: flex; align-items: center; justify-content: space-between;">
                  <div style="display: flex; align-items: center; gap: 6px;">
                    <iconify-icon
                      :icon="node.status === 'passed' ? 'ant-design:check-circle-filled' : (node.status === 'rejected' ? 'ant-design:close-circle-filled' : 'ant-design:clock-circle-outlined')"
                      :style="{ color: node.status === 'passed' ? '#16a34a' : (node.status === 'rejected' ? '#dc2626' : '#94a3b8'), fontSize: '13px' }"
                    ></iconify-icon>
                    <strong style="color: #0f172a;">{{ node.nodeName }}</strong>
                    <span style="color: #64748b; font-size: 10px;">({{ node.operatorName }})</span>
                  </div>
                  <span
                    :style="{
                      fontSize: '10px',
                      padding: '1px 5px',
                      borderRadius: '2px',
                      background: node.status === 'passed' ? '#dcfce7' : (node.status === 'rejected' ? '#fee2e2' : '#f1f5f9'),
                      color: node.status === 'passed' ? '#15803d' : (node.status === 'rejected' ? '#b91c1c' : '#64748b'),
                      fontWeight: 600
                    }"
                  >
                    {{ node.statusText || (node.status === 'passed' ? '已通过' : (node.status === 'rejected' ? '已驳回' : '待处理')) }}
                  </span>
                </div>

                <div v-if="node.comment" style="margin-top: 3px; font-size: 11px;" :style="{ color: node.status === 'rejected' ? '#991b1b' : '#334155' }">
                  <span v-if="node.status === 'rejected'" style="font-weight: 600;">驳回原因: </span>
                  <span v-else style="color: #64748b;">意见: </span>
                  {{ node.comment }}
                </div>

                <div style="margin-top: 2px; color: #94a3b8; font-size: 10px; display: flex; justify-content: space-between;">
                  <span>时间: {{ node.operateTime }}</span>
                  <span v-if="node.signature" style="color: #0f172a; font-weight: 500;">
                    <iconify-icon icon="ant-design:safety-outlined" style="color: #d97706;"></iconify-icon> 电子签名: {{ node.signature }}
                  </span>
                </div>
              </div>
            </div>

            <!-- 标签页 2：单据档案 -->
            <div v-else>
              <div v-for="grp in applicationAttachmentGroups" :key="grp.groupName" style="margin-bottom: 6px;">
                <div style="font-weight: 600; color: #475569; font-size: 10px; margin-bottom: 2px;">{{ grp.groupName }} ({{ grp.items.length }})</div>
                <div
                  v-for="att in grp.items"
                  :key="att.name"
                  style="display: flex; align-items: center; justify-content: space-between; padding: 3px 6px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 3px; margin-bottom: 2px;"
                >
                  <div style="display: flex; align-items: center; gap: 6px; overflow: hidden;">
                    <iconify-icon icon="ant-design:file-pdf-outlined" style="color: #dc2626; font-size: 13px;"></iconify-icon>
                    <span style="font-size: 11px; color: #0f172a; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" :title="att.name">
                      {{ att.name }}
                    </span>
                    <span style="font-size: 10px; color: #94a3b8;">({{ att.sizeText || '1.2 MB' }})</span>
                  </div>
                  <div style="display: flex; align-items: center; gap: 4px;">
                    <a-button type="link" size="small" style="font-size: 11px; padding: 0;" @click="previewAttachment(att)">预览</a-button>
                    <a-button type="link" size="small" danger style="font-size: 11px; padding: 0;" @click="removeApplicationAttachment(att)">删</a-button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="pa-dock-footer">
            <span>最后流转: {{ (workflowNodes[workflowNodes.length - 1] || {}).operateTime || '2026-10-30 11:45:00' }}</span>
            <span>流程节点: {{ workflowNodes.length }} 步</span>
          </div>
        </div>
      </div>

    </div>

""" + modals_block + script_block

with open('pages/payment-application-edit.html', 'w', encoding='utf-8') as f:
    f.write(clean_masterpiece)

print("Clean Masterpiece written successfully.")
