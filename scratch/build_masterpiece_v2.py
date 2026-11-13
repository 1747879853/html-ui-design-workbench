# coding: utf-8
import re

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_script = text.find('<script>')
script_block = text[idx_script:]

idx_drawers = text.find('<!-- ====================================================================\n             弹窗 1：添加费用抽屉')
modals_block = text[idx_drawers:idx_script]

masterpiece_v2 = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>付费申请编辑详情 - 费用管理 (PaymentApplicationForm · 金融对账主凭证工作台)</title>

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
       企业级金融主凭证对账工作台 · 深度规范重构 V2：
       1. 【重点第一视角】：驳回原因置顶高亮横幅，申请净额大字看板，核心单号/提单/风控加粗标出，拒绝平铺纯字段罗列；
       2. 【严密结构对齐】：主单底账 4 列独立单元卡，统一 76px 高度、统一 3 层基线（Title / 核心值 / 关联控制），Col1 我方、Col2 对方，逻辑绝对统一；
       3. 【高屏费用主舞台】：费用明细起始于 Y≈145px，采用 6 大业务聚类列（单号/航线/客户/风控闸口/申请额），重点一目了然；
       4. 【底部高度通透咬合】：发票中心 (58%) 与审批附件卡 (42%) 统一 250px 高度，双方均具备 Header / Body / Footer 结构，彻底根除左短右长、半截空洞！
       ========================================================================== */

    [v-cloak] {
      display: none !important;
    }

    body {
      background-color: #f1f5f9;
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

    /* 1. 顶部场景沙盘栏 (开发调试用) */
    .wb-scenario-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 6px;
      background: #0f172a;
      color: #f8fafc;
      border-radius: 4px;
      padding: 3px 10px;
      border-left: 3px solid #38bdf8;
      flex-shrink: 0;
    }

    .wb-scenario-left,
    .wb-scenario-right {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }

    .wb-scenario-title {
      font-size: 11px;
      font-weight: 600;
      color: #38bdf8;
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
      background: rgba(56, 189, 248, 0.15);
      color: #fff;
    }

    .wb-scenario-pill.active {
      background: #2563eb;
      color: #ffffff;
      border-color: #60a5fa;
      font-weight: 600;
    }

    /* 2. 状态决策横幅 (驳回/待审批/补票置顶预警 · 彻底解决看不出重点！) */
    .pa-status-callout {
      padding: 5px 12px;
      border-radius: 5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      font-size: 11px;
      flex-shrink: 0;
    }

    .callout-rejected {
      background: #fef2f2;
      border: 1px solid #fecaca;
      color: #991b1b;
    }

    .callout-pending {
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1e40af;
    }

    .callout-supplement {
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      color: #166534;
    }

    /* 3. 结构化主单金融底账头 (高度锁定 106px · 4 列严密对齐 · 拒绝高低错乱) */
    .pa-master-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02);
      flex-shrink: 0;
      overflow: hidden;
    }

    .pa-action-toolbar {
      padding: 5px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      border-bottom: 1px solid #f1f5f9;
      background: #ffffff;
    }

    .pa-doc-code {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 14px;
      font-weight: 700;
      color: #0f172a;
      letter-spacing: -0.2px;
    }

    .pa-status-badge {
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

    /* 4 列严密结构网格 - 统一严格对齐基线 */
    .pa-ledger-grid {
      display: grid;
      grid-template-columns: minmax(300px, 1.25fr) minmax(350px, 1.45fr) minmax(300px, 1.3fr) 250px;
      gap: 10px;
      padding: 6px 12px;
      background: #f8fafc;
    }

    .pa-ledger-cell {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 5px 8px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 74px;
      box-sizing: border-box;
    }

    .pa-cell-title-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
      color: #64748b;
      line-height: 1.2;
      font-weight: 500;
    }

    .pa-cell-row {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 11px;
      height: 24px;
      min-height: 24px;
    }

    .pa-cell-label {
      color: #64748b;
      white-space: nowrap;
      width: 52px;
      flex-shrink: 0;
      font-size: 11px;
    }

    .pa-vendor-tag {
      background: #0f172a;
      color: #ffffff;
      padding: 1px 5px;
      border-radius: 3px;
      font-weight: 600;
      font-size: 10px;
      flex-shrink: 0;
    }

    .pa-bank-pill {
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 3px;
      padding: 1px 6px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-weight: 500;
      color: #1e293b;
      width: 100%;
      height: 24px;
      box-sizing: border-box;
      justify-content: space-between;
    }

    .pa-net-val {
      font-size: 19px;
      font-weight: 800;
      color: #0f172a;
      font-family: ui-monospace, monospace;
      line-height: 1;
    }

    /* 4. 中部业务费用明细主舞台 (高屏呈现 · 100% 满宽 · 重点突出) */
    .pa-fee-stage {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02);
      flex: 1 1 auto;
      min-height: 260px;
      overflow: hidden;
    }

    .pa-stage-header {
      padding: 6px 12px;
      background: #ffffff;
      border-bottom: 1px solid #f1f5f9;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      flex-shrink: 0;
    }

    .pa-stage-title {
      font-size: 13px;
      font-weight: 600;
      color: #0f172a;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .pa-stage-title::before {
      content: "";
      width: 3px;
      height: 12px;
      background: #2563eb;
      border-radius: 2px;
    }

    .pa-table-scroll-area {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      position: relative;
    }

    .pa-main-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
      table-layout: fixed;
    }

    .pa-main-table th {
      position: sticky;
      top: 0;
      z-index: 5;
      background: #f8fafc;
      color: #475569;
      font-weight: 600;
      padding: 6px 8px;
      border-bottom: 1px solid #cbd5e1;
      border-right: 1px solid #f1f5f9;
      text-align: left;
      white-space: nowrap;
    }

    .pa-group-row td {
      padding: 6px 8px;
      border-bottom: 1px solid #e2e8f0;
      border-right: 1px solid #f8fafc;
      background: #ffffff;
      vertical-align: middle;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .pa-group-row:hover td {
      background: #f8fafc;
    }

    .pa-group-row.is-expanded td {
      background: #f0f7ff;
      border-bottom-color: #bfdbfe;
    }

    /* 货代业务暗号强化 */
    .pa-order-mbl-box {
      display: flex;
      flex-direction: column;
      gap: 2px;
      font-family: ui-monospace, monospace;
    }

    .pa-link-code {
      color: #2563eb;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
    }
    .pa-link-code:hover {
      text-decoration: underline;
    }

    .pa-copy-btn {
      color: #94a3b8;
      cursor: pointer;
      font-size: 12px;
      transition: color 0.15s;
    }
    .pa-copy-btn:hover {
      color: #2563eb;
    }

    .pa-route-capsule {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      background: #e0f2fe;
      color: #0369a1;
      padding: 1px 6px;
      border-radius: 3px;
      font-weight: 600;
      font-size: 11px;
    }

    /* 内层费用子表 */
    .pa-child-box {
      background: #f8fafc;
      padding: 6px 12px 6px 36px;
      border-bottom: 2px solid #cbd5e1;
      position: relative;
    }

    .pa-child-box::before {
      content: "";
      position: absolute;
      left: 18px;
      top: 0;
      bottom: 10px;
      width: 2px;
      border-left: 2px dashed #93c5fd;
    }

    .pa-child-box::after {
      content: "";
      position: absolute;
      left: 18px;
      top: 14px;
      width: 14px;
      height: 2px;
      border-top: 2px dashed #93c5fd;
    }

    .pa-child-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      overflow: hidden;
      table-layout: fixed;
    }

    .pa-child-table th {
      background: #eff6ff;
      color: #1e3a8a;
      font-weight: 600;
      padding: 5px 8px;
      border-bottom: 1px solid #bfdbfe;
      border-right: 1px solid #dbeafe;
      white-space: nowrap;
      text-align: left;
    }

    .pa-child-table td {
      padding: 5px 8px;
      border-bottom: 1px solid #f1f5f9;
      border-right: 1px solid #f1f5f9;
      vertical-align: middle;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
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

    .pa-currency-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 30px;
      padding: 0 4px;
      border-radius: 2px;
      font-weight: 700;
      font-size: 10px;
      font-family: ui-monospace, monospace;
    }

    .pa-currency-RMB { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
    .pa-currency-USD { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
    .pa-currency-EUR { background: #f5f3ff; color: #7c3aed; border: 1px solid #ddd6fe; }

    .pa-fee-footer {
      padding: 4px 12px;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      font-size: 11px;
    }

    /* 5. 底部对账协同区 (左发票 58% / 右审批与附件 42% · 高度严格统合 250px) */
    .pa-bottom-grid {
      display: grid;
      grid-template-columns: minmax(0, 58%) minmax(0, 42%);
      gap: 8px;
      flex: 0 0 250px;
      height: 250px;
      box-sizing: border-box;
      overflow: hidden;
    }

    .pa-deck-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02);
      height: 100%;
      overflow: hidden;
      box-sizing: border-box;
    }

    .pa-deck-header {
      padding: 5px 10px;
      background: #f8fafc;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      flex-shrink: 0;
      height: 34px;
      box-sizing: border-box;
    }

    .pa-deck-body {
      flex: 1;
      overflow-y: auto;
      padding: 4px 8px;
    }

    .pa-deck-footer {
      padding: 4px 10px;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
      color: #64748b;
      flex-shrink: 0;
      height: 28px;
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
      border-bottom: 1px solid #cbd5e1;
      text-align: left;
      white-space: nowrap;
    }

    .pa-inv-table td {
      padding: 3px 6px;
      border-bottom: 1px solid #f1f5f9;
      vertical-align: middle;
      white-space: nowrap;
    }

    .pa-inv-row-error td {
      background: #fff1f2 !important;
    }

    /* 审批时间轴 */
    .pa-timeline-box {
      padding: 6px 12px 6px 8px;
    }

    .pa-node-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 5px 8px;
      margin-bottom: 6px;
      font-size: 11px;
    }

    .pa-node-card.is-reject {
      background: #fef2f2;
      border-color: #fecaca;
    }

    .pa-node-card.is-pass {
      background: #f0fdf4;
      border-color: #bbf7d0;
    }

    .pa-seal-badge {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-size: 10px;
      padding: 1px 5px;
      border-radius: 3px;
      background: #fef3c7;
      color: #92400e;
      border: 1px solid #fde68a;
      font-weight: 600;
    }

    .pa-quiet-no-inv {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 24px 16px;
      background: #f0fdf4;
      border: 1px dashed #86efac;
      border-radius: 6px;
      color: #166534;
      font-size: 11px;
      margin: 12px auto;
      max-width: 90%;
    }
  </style>
</head>
<body>
  <div id="app" v-cloak>
    <div class="pa-workbench">

      <!-- ====================================================================
           1. 顶部场景沙盘栏 (开发验收与极端场景快速切换)
           ==================================================================== -->
      <div class="wb-scenario-bar">
        <div class="wb-scenario-left">
          <span class="wb-scenario-title">
            <iconify-icon icon="ant-design:experiment-outlined"></iconify-icon>
            业务场景沙盘:
          </span>
          <div
            v-for="s in presetScenarios"
            :key="s.id"
            class="wb-scenario-pill"
            :class="{ active: currentScenarioId === s.id }"
            @click="switchScenario(s.id)"
          >
            <span>{{ s.label }}</span>
            <span style="opacity: 0.6; font-size: 9px; font-family: monospace;">[{{ s.docCode }}]</span>
          </div>
        </div>

        <div class="wb-scenario-right">
          <a-switch
            v-model:checked="simulateSendFailure"
            size="small"
            checked-children="送审失败"
            un-checked-children="模拟送审失败恢复"
          ></a-switch>
          <a-button size="small" type="primary" ghost style="font-size: 10px; height: 20px; padding: 0 6px;" @click="showFieldFixModal = true">
            演示异常定位
          </a-button>
          <a-button size="small" type="primary" style="font-size: 10px; height: 20px; padding: 0 6px;" @click="showHandoffDocModal = true">
            交接说明 (5项)
          </a-button>
        </div>
      </div>

      <!-- ====================================================================
           2. 状态决策横幅 (重点置顶第一视角 · 告别纯字段罗列无重点！)
           ==================================================================== -->
      <!-- S3 已驳回：置顶强视觉警示横幅 -->
      <div v-if="formState.status === 2" class="pa-status-callout callout-rejected">
        <div style="display: flex; align-items: center; gap: 8px;">
          <iconify-icon icon="ant-design:close-circle-filled" style="color: #dc2626; font-size: 14px; flex-shrink: 0;"></iconify-icon>
          <strong style="color: #991b1b; white-space: nowrap;">审批已驳回 ({{ auditTimeline[1]?.operator || '张财务' }} · {{ auditTimeline[1]?.time || '2026-10-30 11:45' }})：</strong>
          <span style="color: #b91c1c;">{{ auditTimeline[1]?.comment || 'GH137测试结束：恢复原专用申请至驳回状态，请补充水单盖章件后重提。' }}</span>
        </div>
        <a-tag color="error" style="font-size: 10px; line-height: 18px; margin: 0; flex-shrink: 0;">需修改后重新送审</a-tag>
      </div>

      <!-- S4 待审核：柔和提示横幅 -->
      <div v-else-if="formState.status === 1" class="pa-status-callout callout-pending">
        <div style="display: flex; align-items: center; gap: 8px;">
          <iconify-icon icon="ant-design:clock-circle-filled" style="color: #2563eb; font-size: 14px; flex-shrink: 0;"></iconify-icon>
          <strong style="color: #1e40af;">当前状态：财务初审中</strong>
          <span style="color: #1d4ed8;">特批垫资流程已推送至财务负责人，单据字段已被财务工作流锁定保护，如需改单请先撤回。</span>
        </div>
        <a-button size="small" danger ghost style="font-size: 10px; height: 20px; padding: 0 6px;" @click="handleWithdrawAudit">
          撤回申请
        </a-button>
      </div>

      <!-- S5 部分结算补票横幅 -->
      <div v-else-if="formState.status === 4 && invoiceDiffAmount > 0" class="pa-status-callout callout-supplement">
        <div style="display: flex; align-items: center; gap: 8px;">
          <iconify-icon icon="ant-design:info-circle-filled" style="color: #16a34a; font-size: 14px; flex-shrink: 0;"></iconify-icon>
          <strong style="color: #166534;">后补发票通道激活：</strong>
          <span style="color: #15803d;">首笔出款已结算完成，当前待补发票差额 <strong>¥{{ formatDecimal(invoiceDiffAmount) }}</strong>，请录入发票后重新归档。</span>
        </div>
        <a-button size="small" type="primary" style="font-size: 10px; height: 20px; padding: 0 6px;" @click="handleAddInvoiceRow">
          立即补票
        </a-button>
      </div>

      <!-- ====================================================================
           3. 结构化主单金融底账头 (统一 76px 高度 · 严密 3 层基线对齐)
           ==================================================================== -->
      <div class="pa-master-card">
        <!-- 顶部动作与单号工具条 -->
        <div class="pa-action-toolbar">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="color: #64748b;">申请单号:</span>
            <span class="pa-doc-code">{{ formState.docCode }}</span>
            <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-btn" @click="copyText(formState.docCode, '申请单号')"></iconify-icon>

            <!-- 状态胶囊 -->
            <span class="pa-status-badge" :class="'pa-status-' + formState.status">
              <iconify-icon :icon="getStatusIcon(formState.status)"></iconify-icon>
              {{ formState.statusName }}
            </span>

            <span style="color: #cbd5e1;">|</span>
            <span style="color: #64748b;">申请人:</span>
            <strong style="color: #334155;">{{ formState.applicantName }}</strong>

            <template v-if="formState.submitTime">
              <span style="color: #64748b; margin-left: 4px;">提交:</span>
              <span class="tabular-nums" style="color: #475569;">{{ formState.submitTime }}</span>
            </template>
            <template v-if="formState.auditTime">
              <span style="color: #64748b; margin-left: 4px;">审核:</span>
              <span class="tabular-nums" style="color: #475569;">{{ formState.auditTime }}</span>
            </template>

            <!-- 协同联动指示器 -->
            <a-tooltip title="主表所属公司变更已自动联动发票销售方与对方账户">
              <a-tag color="success" style="font-size: 10px; line-height: 18px; margin: 0; padding: 0 5px; cursor: help;">
                <iconify-icon icon="ant-design:check-circle-outlined" style="margin-right: 2px;"></iconify-icon>
                主表与发票已同步
              </a-tag>
            </a-tooltip>
          </div>

          <!-- 右侧动作按钮组 (纯白背景 + 规范间距) -->
          <div style="display: flex; align-items: center; gap: 6px;">
            <a-button size="small" style="font-size: 11px;" @click="handleCreateBlank">
              <template #icon><iconify-icon icon="ant-design:plus-outlined"></iconify-icon></template>
              新建空白
            </a-button>

            <a-button size="small" style="font-size: 11px;" :disabled="!isMainFormEditable" @click="handleSaveDraft">
              <template #icon><iconify-icon icon="ant-design:save-outlined"></iconify-icon></template>
              保存草稿
            </a-button>

            <a-button size="small" type="primary" style="font-size: 11px;" :disabled="!canSubmit" @click="handleSubmitAudit">
              <template #icon><iconify-icon icon="ant-design:send-outlined"></iconify-icon></template>
              {{ formState.status === 2 ? '重新送审' : '提交送审' }}
            </a-button>

            <a-dropdown>
              <template #overlay>
                <a-menu @click="handleExportAction">
                  <a-menu-item key="excel">导出 Excel 对账凭证</a-menu-item>
                  <a-menu-item key="pdf">导出 PDF 付款凭证单</a-menu-item>
                  <a-menu-item key="zip">打包下载发票与水单</a-menu-item>
                </a-menu>
              </template>
              <a-button size="small" style="font-size: 11px;">
                导出 <iconify-icon icon="ant-design:down-outlined" style="font-size: 9px;"></iconify-icon>
              </a-button>
            </a-dropdown>

            <a-button size="small" style="font-size: 11px;" @click="handlePrintDoc">
              <template #icon><iconify-icon icon="ant-design:printer-outlined"></iconify-icon></template>
              打印
            </a-button>
          </div>
        </div>

        <!-- 4 列严密结构网格：Col1 我方付款主体 / Col2 对方收款单位 / Col3 支付时效 / Col4 申请净额 -->
        <div class="pa-ledger-grid">
          <!-- 单元卡 1：付款主体 (我司出款抬头与账户) -->
          <div class="pa-ledger-cell">
            <div class="pa-cell-title-row">
              <span style="font-weight: 600; color: #1e293b;">付款主体 (我司出款)</span>
              <span style="font-size: 10px; color: #94a3b8;">出款责任方</span>
            </div>
            <div class="pa-cell-row">
              <span class="pa-cell-label">所属公司:</span>
              <a-select
                v-model:value="formState.companyId"
                size="small"
                style="flex: 1; min-width: 0;"
                :disabled="!isMainFormEditable"
                :options="companyOptions"
                @change="handleCompanyChange"
              ></a-select>
            </div>
            <div class="pa-cell-row">
              <span class="pa-cell-label">出款账户:</span>
              <div class="pa-bank-pill" :title="myCompanyBank.bankName + ' · ' + myCompanyBank.accountNo">
                <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: flex; align-items: center; gap: 4px;">
                  <iconify-icon icon="ant-design:bank-outlined" style="color: #2563eb;"></iconify-icon>
                  <strong style="color: #1e293b; font-size: 11px;">{{ myCompanyBank.shortName }}</strong>
                  <span class="tabular-nums" style="font-family: monospace; color: #64748b; font-size: 10px;">{{ myCompanyBank.accountNo }}</span>
                </div>
                <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-btn" @click="copyText(myCompanyBank.accountNo, '我司付款账号')"></iconify-icon>
              </div>
            </div>
          </div>

          <!-- 单元卡 2：收款对象 (往来结算单位与账户) -->
          <div class="pa-ledger-cell">
            <div class="pa-cell-title-row">
              <span style="font-weight: 600; color: #1e293b;">收款对象 (往来单位)</span>
              <a-tag v-if="orderFeeGroups.length > 0" color="blue" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">
                <iconify-icon icon="ant-design:lock-outlined" style="margin-right: 2px;"></iconify-icon>结算已锁定
              </a-tag>
              <a-tag v-else color="warning" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">无费用·可换</a-tag>
            </div>
            <div class="pa-cell-row">
              <span class="pa-cell-label">往来单位:</span>
              <div style="flex: 1; min-width: 0; display: flex; align-items: center; gap: 4px; overflow: hidden;" :title="formState.settlementName">
                <span class="pa-vendor-tag">{{ formState.settlementShortName || '海丰船代' }}</span>
                <strong style="font-size: 11px; color: #0f172a; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                  {{ formState.settlementName }}
                </strong>
              </div>
            </div>
            <div class="pa-cell-row">
              <span class="pa-cell-label">对方账户:</span>
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

          <!-- 单元卡 3：付款排期与时效附言 -->
          <div class="pa-ledger-cell">
            <div class="pa-cell-title-row">
              <span style="font-weight: 600; color: #1e293b;">付款排期与时效附言</span>
              <span style="font-size: 10px; color: #94a3b8;">最晚出款 ~ 预计回款</span>
            </div>
            <div class="pa-cell-row">
              <span class="pa-cell-label">付款排期:</span>
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
            <div class="pa-cell-row">
              <span class="pa-cell-label">汇款附言:</span>
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

          <!-- 单元卡 4：申请结算净额大字牌 -->
          <div class="pa-ledger-cell" style="background: #faf5ff; border-color: #e9d5ff;">
            <div class="pa-cell-title-row">
              <span style="color: #7e22ce; font-weight: 600;">本次申请净额 (付 - 收)</span>
              <a-tag :color="formState.isCurrencyFixed ? 'purple' : 'blue'" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">
                {{ formState.isCurrencyFixed ? ('固定 · ' + formState.currencyCode) : '按原票币' }}
              </a-tag>
            </div>
            <div class="pa-cell-row" style="justify-content: space-between;">
              <span class="pa-cell-label" style="color: #7e22ce;">结算净额:</span>
              <div style="display: flex; align-items: baseline; gap: 4px;">
                <span class="pa-currency-badge" :class="'pa-currency-' + primaryCurrencyCode">{{ primaryCurrencyCode }}</span>
                <span class="pa-net-val" style="color: #6b21a8;">{{ formatMoney(currencySummaryList[0]?.netAmount || 0, primaryCurrencyCode) }}</span>
              </div>
            </div>
            <div class="pa-cell-row" style="justify-content: space-between; font-size: 10px;">
              <span v-if="!formState.isReceiveAllSettled" style="color: #ea580c; font-weight: 600;">
                ⚠️ 垫资: {{ unSettledReceiveSummaryText }}
              </span>
              <span v-else style="color: #16a34a; font-weight: 500;">
                ✓ 关联合同已结清
              </span>
              <span :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#ea580c', fontWeight: 600 }">
                {{ formState.invoiceProcess === 2 ? '免开票' : (invoiceDiffAmount === 0 ? '票费已平' : '待补票差') }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- ====================================================================
           4. 业务费用明细主舞台 (高屏呈现 · 100% 满宽 · 6大业务聚类重点突出)
           ==================================================================== -->
      <div class="pa-fee-stage">
        <div class="pa-stage-header">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span class="pa-stage-title">业务费用明细</span>
            <span style="font-size: 11px; color: #64748b;">
              共 <strong>{{ orderFeeGroups.length }}</strong> 票业务 · <strong>{{ totalFeeCount }}</strong> 笔费用
            </span>
            <a-tag color="blue" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">
              ⚡ 增删费用实时生效
            </a-tag>
          </div>

          <!-- 右侧紧凑工具与搜索 -->
          <div style="display: flex; align-items: center; gap: 6px;">
            <a-input
              v-model:value="feeFilters.orderNo"
              size="small"
              placeholder="快速筛选委托号/提单号/费用名..."
              style="width: 220px;"
              allow-clear
            >
              <template #prefix><iconify-icon icon="ant-design:search-outlined" style="color: #94a3b8;"></iconify-icon></template>
            </a-input>

            <a-button size="small" type="primary" style="font-size: 11px;" :disabled="!isMainFormEditable" @click="handleOpenAddFeeDrawer">
              <template #icon><iconify-icon icon="ant-design:plus-outlined"></iconify-icon></template>
              添加费用
            </a-button>

            <a-popconfirm
              title="确认解除选中费用的关联？"
              description="仅从本单移除，原订单费用不受影响。"
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

        <!-- 100% 满宽表格区 (重点聚类列结构 · 彻底消除纯字段罗列) -->
        <div class="pa-table-scroll-area">
          <table class="pa-main-table">
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
                <th style="width: 22px;"></th>
                <th style="width: 32px; text-align: center;">序</th>
                <th style="width: 175px;">业务单号 (委托号 / 提单号)</th>
                <th style="width: 190px;">航线船期 (目的港 / 船司 / 箱量)</th>
                <th style="width: 230px;">往来对象 (委托客户 / 结算单位)</th>
                <th style="width: 230px;">审核闸口与垫资风控 (核心决策点)</th>
                <th style="width: 140px; text-align: right;">本单申请净合计</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(group, gIdx) in filteredOrderFeeGroups" :key="group.groupId || gIdx">
                <!-- 主单业务行 (聚类后极度清晰，业务重点一目了然) -->
                <tr class="pa-group-row" :class="{ 'is-expanded': group.isExpanded }">
                  <td style="text-align: center;">
                    <a-checkbox
                      :checked="isGroupAllSelected(group)"
                      :indeterminate="isGroupPartiallySelected(group)"
                      :disabled="!isMainFormEditable"
                      @change="(e) => handleSelectGroupFees(group, e.target.checked)"
                    ></a-checkbox>
                  </td>
                  <td style="text-align: center; cursor: pointer;" @click="group.isExpanded = !group.isExpanded">
                    <iconify-icon :icon="group.isExpanded ? 'ant-design:down-outlined' : 'ant-design:right-outlined'" style="font-size: 10px; color: #64748b;"></iconify-icon>
                  </td>
                  <td style="text-align: center;" class="tabular-nums">{{ gIdx + 1 }}</td>

                  <!-- 聚类列 1：业务单号 (委托编号 + 主提单号) -->
                  <td>
                    <div class="pa-order-mbl-box">
                      <div style="display: flex; align-items: center; gap: 4px;">
                        <span style="color: #64748b; font-size: 10px;">委托:</span>
                        <a class="pa-link-code" @click="handlePenetrateOrder(group.commissionNum)">{{ group.commissionNum }}</a>
                        <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-btn" @click="copyText(group.commissionNum, '委托编号')"></iconify-icon>
                      </div>
                      <div style="display: flex; align-items: center; gap: 4px;">
                        <span style="color: #64748b; font-size: 10px;">提单:</span>
                        <strong style="color: #0f172a; font-size: 11px;">{{ group.mblNum || '-' }}</strong>
                        <iconify-icon v-if="group.mblNum" icon="ant-design:copy-outlined" class="pa-copy-btn" @click="copyText(group.mblNum, '主提单号')"></iconify-icon>
                      </div>
                    </div>
                  </td>

                  <!-- 聚类列 2：航线与船期 -->
                  <td>
                    <div style="display: flex; flex-direction: column; gap: 2px;">
                      <div style="display: flex; align-items: center; gap: 4px;">
                        <span class="pa-route-capsule">{{ group.podName || '-' }}</span>
                        <span style="color: #0f172a; font-weight: 600;">{{ group.carrierName || '-' }}</span>
                        <span style="color: #64748b; font-size: 10px;">{{ group.totalCtn || '-' }}</span>
                      </div>
                      <div style="color: #64748b; font-size: 10px;">
                        <span>ETD: {{ group.etd || '-' }}</span>
                        <span style="margin-left: 6px;">会计: {{ group.accountDate || '-' }}</span>
                      </div>
                    </div>
                  </td>

                  <!-- 聚类列 3：往来客户与结算单位 -->
                  <td>
                    <div style="display: flex; flex-direction: column; gap: 2px; max-width: 220px;">
                      <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" :title="group.clientName">
                        <span style="color: #64748b; font-size: 10px;">客户:</span>
                        <strong style="color: #0f172a; margin-left: 2px;">{{ group.clientName || '-' }}</strong>
                      </div>
                      <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #64748b; font-size: 10px;" :title="group.settlementName">
                        <span>结算: {{ group.settlementName || '-' }}</span>
                        <span v-if="group.salesmanName" style="margin-left: 4px;">({{ group.salesmanName }})</span>
                      </div>
                    </div>
                  </td>

                  <!-- 聚类列 4：审核闸口与垫资风控 (核心业务焦点) -->
                  <td>
                    <div style="display: flex; flex-direction: column; gap: 3px;">
                      <div style="display: flex; align-items: center; gap: 4px;">
                        <a-tag :color="getFeeAuditColor(group.receiveFeeStatus)" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">
                          应收: {{ group.receiveFeeStatus || '已审核' }}
                        </a-tag>
                        <a-tag :color="getFeeAuditColor(group.payFeeStatus)" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">
                          应付: {{ group.payFeeStatus || '已审核' }}
                        </a-tag>
                        <a-tag :color="getSettlementStatusColor(group.recSettlementStatus)" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">
                          {{ group.recSettlementStatus || '结算完毕' }}
                        </a-tag>
                      </div>

                      <!-- 核心风控判定：未结垫资风险预警 -->
                      <div>
                        <template v-if="group.unSettledReceiveList && group.unSettledReceiveList.some(r => r.amount > 0)">
                          <span
                            v-for="unRec in group.unSettledReceiveList.filter(r => r.amount > 0)"
                            :key="unRec.currency"
                            style="color: #c2410c; font-weight: 700; background: #fff7ed; border: 1px solid #fed7aa; padding: 1px 5px; border-radius: 3px; font-size: 10px; display: inline-flex; align-items: center; gap: 2px;"
                          >
                            ⚠️ 垫资未结: {{ unRec.currency }} {{ formatDecimal(unRec.amount) }}
                          </span>
                        </template>
                        <span v-else style="color: #16a34a; font-size: 10px; font-weight: 600; display: inline-flex; align-items: center; gap: 2px;">
                          <iconify-icon icon="ant-design:check-circle-filled" style="color: #16a34a;"></iconify-icon>
                          客户应收已结清 (无垫资风险)
                        </span>
                      </div>
                    </div>
                  </td>

                  <!-- 聚类列 5：申请合计 -->
                  <td style="text-align: right;">
                    <div v-for="(sumAmt, cCode) in group.groupCurrencySum" :key="cCode" style="font-size: 13px; font-weight: 800; color: #0f172a;" class="tabular-nums">
                      {{ cCode }} {{ formatDecimal(sumAmt) }}
                    </div>
                  </td>
                </tr>

                <!-- 嵌套子明细：费用子项 -->
                <tr v-if="group.isExpanded">
                  <td colspan="8" style="padding: 0;">
                    <div class="pa-child-box">
                      <table class="pa-child-table">
                        <thead>
                          <tr>
                            <th style="width: 28px; text-align: center;"></th>
                            <th style="width: 32px; text-align: center;">序</th>
                            <th style="width: 45px; text-align: center;">收付</th>
                            <th style="width: 140px;">费用名称</th>
                            <th style="width: 60px;">币别</th>
                            <th style="width: 105px; text-align: right;">原金额</th>
                            <th style="width: 85px; text-align: right;">原始汇率</th>
                            <th style="width: 105px; text-align: right;">已核销金额</th>
                            <th style="width: 105px; text-align: right;">可申请余额</th>
                            <th v-if="formState.isCurrencyFixed" style="width: 105px; text-align: right;">申请汇率</th>
                            <th v-if="formState.isCurrencyFixed" style="width: 115px; text-align: right;">折币 ({{ formState.currencyCode }})</th>
                            <th style="width: 125px; text-align: right; background: #e0f2fe; color: #0369a1;">本次申请金额</th>
                            <th>费用备注</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="(fee, fIdx) in group.filteredFees"
                            :key="fee.id"
                            :id="'fee-row-' + fee.id"
                            :class="{ 'is-highlighted-fee': fee.isHighlighted }"
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
                            <td><strong style="color: #0f172a; font-size: 12px;">{{ fee.feeCodeName }}</strong></td>
                            <td><span class="pa-currency-badge" :class="'pa-currency-' + fee.currencyCode">{{ fee.currencyCode }}</span></td>
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
                            <td style="text-align: right;">
                              <span class="tabular-nums" style="font-size: 13px; font-weight: 800; color: #1d4ed8;">
                                {{ formatMoney(fee.appliedAmount, fee.currencyCode) }}
                              </span>
                            </td>
                            <td style="color: #64748b;">{{ fee.itemRemark || '-' }}</td>
                          </tr>
                          <tr v-if="group.filteredFees.length === 0">
                            <td :colspan="formState.isCurrencyFixed ? 13 : 11" style="text-align: center; color: #94a3b8; padding: 10px;">
                              筛选条件未命中此票业务下的费用
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </td>
                </tr>
              </template>

              <tr v-if="filteredOrderFeeGroups.length === 0">
                <td colspan="8" style="text-align: center; color: #94a3b8; padding: 32px;">
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
           5. 底部对账协同区 (左发票 58% / 右审批与附件 42% · 高度严格统合 250px)
           ==================================================================== -->
      <div class="pa-bottom-grid">
        <!-- 左卡：发票核对中心 (带专属 Header / Body / Footer，结构饱满通透) -->
        <div class="pa-deck-card">
          <div class="pa-deck-header">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-weight: 600; color: #0f172a; display: inline-flex; align-items: center; gap: 4px;">
                <iconify-icon icon="ant-design:file-protect-outlined" style="color: #2563eb;"></iconify-icon>
                发票核对中心 ({{ formState.invoiceRows.length }})
              </span>

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
              <template v-if="formState.invoiceProcess === 2">
                <a-tag color="success" style="font-size: 10px; line-height: 16px; margin: 0;">
                  ✓ 免开票业务 · 已合规豁免
                </a-tag>
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

              <a-button size="small" style="font-size: 11px; height: 22px; padding: 0 6px;" :disabled="formState.invoiceProcess === 2" @click="showInputInvoicePicker = true">
                从进项池选
              </a-button>
              <a-button size="small" type="primary" ghost style="font-size: 11px; height: 22px; padding: 0 6px;" :disabled="formState.invoiceProcess === 2" @click="handleAddInvoiceRow">
                + 录发票
              </a-button>
            </div>
          </div>

          <div class="pa-deck-body">
            <!-- 不开票提示条 -->
            <div v-if="formState.invoiceProcess === 2" class="pa-quiet-no-inv">
              <iconify-icon icon="ant-design:safety-certificate-filled" style="color: #16a34a; font-size: 18px; flex-shrink: 0;"></iconify-icon>
              <div style="flex: 1;">
                <strong style="color: #166534;">当前业务适用「不开票」付款通道：</strong>
                <div style="color: #15803d; margin-top: 2px;">
                  根据企业财务结算制度，本单属于港口规费或免税业务，系统在送审及审批全流程已自动豁免发票差额拦截，审核通过后可直接安排打款。
                </div>
              </div>
              <a-button type="link" size="small" style="font-size: 11px; padding: 0;" @click="formState.invoiceProcess = 1; markMainFormDirty();">
                需要补发票？切换为「先票后付」
              </a-button>
            </div>

            <!-- 正常发票表格 -->
            <table v-else class="pa-inv-table">
              <thead>
                <tr>
                  <th style="width: 30px; text-align: center;">序</th>
                  <th style="width: 160px;"><span style="color: #ef4444;">*</span>发票号</th>
                  <th style="width: 105px;">开票日期</th>
                  <th style="width: 200px;">销售方抬头</th>
                  <th style="width: 105px; text-align: right;">发票金额 (元)</th>
                  <th style="width: 160px;">发票附件 / OCR状态</th>
                  <th style="width: 45px; text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(row, idx) in formState.invoiceRows"
                  :key="row.rowKey || idx"
                  :id="'invoice-row-' + idx"
                  :class="{ 'pa-inv-row-error': row.hasError }"
                >
                  <td style="text-align: center;" class="tabular-nums">{{ idx + 1 }}</td>
                  <td>
                    <a-input
                      v-model:value="row.invoiceNo"
                      size="small"
                      placeholder="发票代码号"
                      :status="row.hasError ? 'error' : ''"
                      @change="handleInvoiceFieldChange(row)"
                    ></a-input>
                    <div v-if="row.errorMsg" style="color: #ef4444; font-size: 10px; margin-top: 1px;">
                      {{ row.errorMsg }}
                    </div>
                  </td>
                  <td>
                    <a-date-picker
                      v-model:value="row.invoiceDate"
                      size="small"
                      value-format="YYYY-MM-DD"
                      style="width: 100%;"
                      placeholder="开票日"
                      @change="markMainFormDirty"
                    ></a-date-picker>
                  </td>
                  <td>
                    <a-input
                      v-model:value="row.sellerName"
                      size="small"
                      placeholder="销售方企业名称"
                      @change="markMainFormDirty"
                    ></a-input>
                  </td>
                  <td style="text-align: right;">
                    <a-input-number
                      v-model:value="row.invoiceAmount"
                      size="small"
                      :precision="2"
                      style="width: 100%; text-align: right;"
                      placeholder="0.00"
                      @change="markMainFormDirty"
                    ></a-input-number>
                  </td>
                  <td>
                    <div style="display: flex; align-items: center; justify-content: space-between; gap: 4px;">
                      <template v-if="row.attachment">
                        <span style="font-size: 11px; color: #2563eb; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 85px;" :title="row.attachment.name">
                          {{ row.attachment.name }}
                        </span>
                        <a-space size="small">
                          <a-button type="link" size="small" style="padding: 0; font-size: 11px;" @click="previewAttachment(row.attachment)">预览</a-button>
                          <a-button type="link" size="small" danger style="padding: 0; font-size: 11px;" @click="removeInvoiceAttachment(row)">删</a-button>
                        </a-space>
                      </template>
                      <template v-else>
                        <a-upload :show-upload-list="false" :before-upload="(file) => handleUploadInvoiceFile(row, file)">
                          <a-button size="small" style="font-size: 10px; height: 20px; padding: 0 4px;">上传件</a-button>
                        </a-upload>
                      </template>

                      <a-tag v-if="row.ocrStatus === 'recognizing'" color="processing" style="font-size: 9px; line-height: 14px; margin: 0; padding: 0 3px;">识别中</a-tag>
                      <a-tag v-else-if="row.ocrStatus === 'filled'" color="success" style="font-size: 9px; line-height: 14px; margin: 0; padding: 0 3px;">已提取</a-tag>
                    </div>
                  </td>
                  <td style="text-align: center;">
                    <a-popconfirm title="确认删除发票？" ok-text="删" cancel-text="取消" @confirm="handleDeleteInvoiceRow(idx)">
                      <a-button type="link" danger size="small" style="padding: 0 2px;">
                        <iconify-icon icon="ant-design:delete-outlined"></iconify-icon>
                      </a-button>
                    </a-popconfirm>
                  </td>
                </tr>
                <tr v-if="formState.invoiceRows.length === 0">
                  <td colspan="7" style="text-align: center; color: #94a3b8; padding: 24px;">
                    暂无发票明细。点击右上角「+ 录发票」或「从进项池选」
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 左卡专属底栏：发票核验与勾稽统计 -->
          <div class="pa-deck-footer">
            <span v-if="formState.invoiceProcess === 2">
              勾稽策略：<strong style="color: #16a34a;">已豁免发票审核</strong> (港杂/规费业务直接出款)
            </span>
            <span v-else>
              发票汇总：共 <strong>{{ formState.invoiceRows.length }}</strong> 张发票 · 已录金额 <strong>¥{{ formatDecimal(totalInvoiceAmount) }}</strong> · 差额状态:
              <strong :style="{ color: invoiceDiffAmount === 0 ? '#16a34a' : '#ea580c' }">
                {{ invoiceDiffAmount === 0 ? '✓ 票费已平' : ('待补 ¥' + formatDecimal(invoiceDiffAmount)) }}
              </strong>
            </span>
            <span style="font-size: 10px; color: #94a3b8;">支持专用发票与通行费发票 OCR 自动校验</span>
          </div>
        </div>

        <!-- 右卡：审批流转跟踪与单据档案 (带专属 Header / Body / Footer，左右无缝咬合) -->
        <div class="pa-deck-card">
          <div class="pa-deck-header">
            <div style="display: flex; align-items: center; gap: 8px;">
              <a-radio-group v-model:value="activeRightTab" size="small" option-type="button" button-style="solid">
                <a-radio-button value="timeline">
                  <iconify-icon icon="ant-design:history-outlined" style="margin-right: 3px;"></iconify-icon>
                  审批流程跟踪
                </a-radio-button>
                <a-radio-button value="attachments">
                  <iconify-icon icon="ant-design:paper-clip-outlined" style="margin-right: 3px;"></iconify-icon>
                  单据档案 ({{ docAttachmentList.length }})
                </a-radio-button>
              </a-radio-group>
            </div>

            <div style="display: flex; align-items: center; gap: 4px;">
              <span class="pa-status-badge" :class="'pa-status-' + formState.status" style="font-size: 10px;">
                {{ formState.statusName }}
              </span>
            </div>
          </div>

          <div class="pa-deck-body">
            <!-- 标签页 1：审批流转跟踪 -->
            <div v-if="activeRightTab === 'timeline'" class="pa-timeline-box">
              <div
                v-for="node in auditTimeline"
                :key="node.nodeId"
                class="pa-node-card"
                :class="{ 'is-reject': node.status === 'rejected', 'is-pass': node.status === 'passed' }"
              >
                <div style="display: flex; align-items: center; justify-content: space-between;">
                  <div style="display: flex; align-items: center; gap: 6px;">
                    <iconify-icon
                      :icon="node.status === 'passed' ? 'ant-design:check-circle-filled' : (node.status === 'rejected' ? 'ant-design:close-circle-filled' : 'ant-design:clock-circle-outlined')"
                      :style="{ color: node.status === 'passed' ? '#16a34a' : (node.status === 'rejected' ? '#dc2626' : '#94a3b8'), fontSize: '14px' }"
                    ></iconify-icon>
                    <strong style="color: #0f172a;">{{ node.nodeName }}</strong>
                  </div>
                  <span
                    :style="{
                      fontSize: '10px',
                      padding: '1px 5px',
                      borderRadius: '3px',
                      background: node.status === 'passed' ? '#dcfce7' : (node.status === 'rejected' ? '#fee2e2' : '#f1f5f9'),
                      color: node.status === 'passed' ? '#15803d' : (node.status === 'rejected' ? '#b91c1c' : '#64748b'),
                      fontWeight: 600
                    }"
                  >
                    {{ node.status === 'passed' ? '已提交' : (node.status === 'rejected' ? '已驳回' : '未到达') }}
                  </span>
                </div>

                <div style="margin-top: 3px; color: #64748b; font-size: 10px; display: flex; align-items: center; justify-content: space-between;">
                  <span>处理人: {{ node.operator }}</span>
                  <span class="tabular-nums">{{ node.time }}</span>
                </div>

                <div v-if="node.comment" style="margin-top: 4px; padding: 3px 6px; border-radius: 3px; font-size: 11px;" :style="{ background: node.status === 'rejected' ? '#fee2e2' : '#ffffff', color: node.status === 'rejected' ? '#991b1b' : '#334155' }">
                  <strong v-if="node.status === 'rejected'">驳回原因: </strong>
                  <span v-else>意见: </span>
                  {{ node.comment }}
                </div>

                <div v-if="node.hasSignature" style="margin-top: 4px; display: flex; justify-content: flex-end;">
                  <span class="pa-seal-badge">
                    <iconify-icon icon="ant-design:safety-outlined"></iconify-icon>
                    电子签名: {{ node.operator }}
                  </span>
                </div>
              </div>
            </div>

            <!-- 标签页 2：单据档案与附件池 -->
            <div v-else style="padding: 4px 6px;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #64748b; font-size: 11px;">单据归档清单 (支持发票扫描件、水单、货权凭证)</span>
                <a-upload :show-upload-list="false" :before-upload="handleUploadDocAttachment">
                  <a-button size="small" type="primary" ghost style="font-size: 10px; height: 20px; padding: 0 6px;">
                    + 上传单据附件
                  </a-button>
                </a-upload>
              </div>

              <div
                v-for="att in docAttachmentList"
                :key="att.id"
                style="display: flex; align-items: center; justify-content: space-between; padding: 4px 6px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; margin-bottom: 4px;"
              >
                <div style="display: flex; align-items: center; gap: 6px; overflow: hidden;">
                  <iconify-icon icon="ant-design:file-pdf-outlined" style="color: #dc2626; font-size: 14px; flex-shrink: 0;"></iconify-icon>
                  <span style="font-size: 11px; color: #0f172a; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" :title="att.name">
                    {{ att.name }}
                  </span>
                  <span style="font-size: 10px; color: #94a3b8; font-family: monospace;">({{ att.size }})</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                  <a-button type="link" size="small" style="font-size: 11px; padding: 0;" @click="previewAttachment(att)">预览</a-button>
                  <a-button type="link" size="small" style="font-size: 11px; padding: 0;" @click="downloadAttachment(att)">下载</a-button>
                  <a-button type="link" size="small" danger style="font-size: 11px; padding: 0;" @click="removeDocAttachment(att.id)">删</a-button>
                </div>
              </div>

              <div v-if="docAttachmentList.length === 0" style="text-align: center; color: #94a3b8; padding: 20px;">
                暂无归档附件
              </div>
            </div>
          </div>

          <!-- 右卡专属底栏：审批流转与审计引擎 -->
          <div class="pa-deck-footer">
            <span>流程引擎：企业财务资金审批流标准版 (双签核)</span>
            <span style="font-size: 10px; color: #94a3b8;">
              最后流转: {{ auditTimeline[auditTimeline.length - 1]?.time || '2026-10-30 11:45:00' }}
            </span>
          </div>
        </div>
      </div>

    </div>

""" + modals_block + script_block

with open('pages/payment-application-edit.html', 'w', encoding='utf-8') as f:
    f.write(masterpiece_v2)

print("Masterpiece V2 updated successfully.")
