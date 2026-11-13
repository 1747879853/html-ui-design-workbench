import re

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_script = text.find('<script>')
script_block = text[idx_script:]

idx_drawers = text.find('<!-- ====================================================================\n             弹窗 1：添加费用抽屉')
modals_block = text[idx_drawers:idx_script]

flawless_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>付费申请编辑详情 - 费用管理 (PaymentApplicationForm · 高屏聚焦高密度金融工作台)</title>

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
       付费申请编辑详情 · 高屏聚焦与细节极致调优
       设计准则：
       1. 消除一切拥挤胶带与盒中盒，建立从容、严密对齐的 4 列结构化底账头；
       2. 核心业务费用明细在 Y≈140px 高屏位置舒展呈现 (100% 满宽，0 横向滚动条)；
       3. 底部发票与审批左右明确分工，开票方式与对账差额丝滑联动；
       4. 严禁任何伪需求遥测卡片，回归最纯正、安静的金融中后台气质。
       ========================================================================== */

    [v-cloak] {
      display: none !important;
    }

    body {
      background-color: #f1f4f8;
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

    /* 2. 结构化主单金融底账头 (高密度 · 严密网格对齐 · 拒绝胶带拥挤) */
    .pa-master-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02);
      flex-shrink: 0;
      overflow: hidden;
    }

    .pa-card-action-bar {
      padding: 5px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      border-bottom: 1px solid #f1f5f9;
      background: #ffffff;
    }

    .pa-action-left {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
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

    .pa-save-indicator {
      font-size: 11px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 1px 6px;
      border-radius: 3px;
    }

    .pa-save-indicator.is-dirty {
      background: #fffbeb;
      color: #b45309;
      border: 1px solid #fde68a;
    }

    .pa-save-indicator.is-clean {
      background: #f0fdf4;
      color: #15803d;
      border: 1px solid #bbf7d0;
    }

    /* 4 列严密对齐金融底账网格 */
    .pa-ledger-grid {
      display: grid;
      grid-template-columns: minmax(280px, 1.2fr) minmax(360px, 1.5fr) minmax(280px, 1.2fr) 240px;
      gap: 12px;
      padding: 6px 12px;
      background: #f8fafc;
      align-items: center;
    }

    .pa-ledger-col {
      display: flex;
      flex-direction: column;
      gap: 4px;
      min-width: 0;
    }

    .pa-ledger-col-title {
      font-size: 11px;
      color: #64748b;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .pa-vendor-row {
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
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

    .pa-bank-route-card {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      padding: 3px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      font-size: 11px;
    }

    .pa-net-val {
      font-size: 18px;
      font-weight: 700;
      color: #0f172a;
      font-family: ui-monospace, monospace;
      line-height: 1;
    }

    /* 3. 中部业务费用明细主舞台 (高屏呈现 · 100% 满宽 · 0 横向滚动条) */
    .pa-fee-stage {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02);
      flex: 1 1 auto;
      min-height: 360px;
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
      padding: 5px 6px;
      border-bottom: 1px solid #cbd5e1;
      border-right: 1px solid #f1f5f9;
      text-align: left;
      white-space: nowrap;
    }

    .pa-group-row td {
      padding: 6px 6px;
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
      padding: 4px 6px;
      border-bottom: 1px solid #bfdbfe;
      border-right: 1px solid #dbeafe;
      white-space: nowrap;
      text-align: left;
    }

    .pa-child-table td {
      padding: 4px 6px;
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
      height: 16px;
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

    /* 4. 底部对账协同区 (左发票 58% / 右审批与附件 42%) */
    .pa-bottom-grid {
      display: grid;
      grid-template-columns: minmax(0, 58%) minmax(0, 42%);
      gap: 8px;
      flex: 0 0 250px;
      height: 250px;
      overflow: hidden;
    }

    .pa-deck-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02);
      overflow: hidden;
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
    }

    .pa-deck-body {
      flex: 1;
      overflow-y: auto;
      padding: 4px 8px;
    }

    /* 发票表格 */
    .pa-inv-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
    }

    .pa-inv-table th {
      position: sticky;
      top: 0;
      z-index: 3;
      background: #f8fafc;
      color: #475569;
      font-weight: 600;
      padding: 4px 6px;
      border-bottom: 1px solid #e2e8f0;
      border-right: 1px solid #f1f5f9;
      text-align: left;
      white-space: nowrap;
    }

    .pa-inv-table td {
      padding: 3px 6px;
      border-bottom: 1px solid #f1f5f9;
      border-right: 1px solid #f8fafc;
      vertical-align: middle;
      white-space: nowrap;
    }

    .pa-quiet-no-inv {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 16px;
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      border-radius: 5px;
      color: #15803d;
      font-size: 11px;
      margin: 12px 6px;
    }

    .pa-copy-btn {
      cursor: pointer;
      color: #94a3b8;
      font-size: 11px;
      margin-left: 3px;
    }

    .pa-copy-btn:hover {
      color: #2563eb;
    }

    .pa-link-code {
      color: #2563eb;
      font-weight: 600;
      cursor: pointer;
      font-family: ui-monospace, monospace;
    }

    .pa-link-code:hover {
      text-decoration: underline;
    }

    .pa-audit-stamp {
      font-size: 10px;
      font-weight: 700;
      padding: 1px 6px;
      border-radius: 3px;
      text-transform: uppercase;
    }

    .stamp-status-0 { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
    .stamp-status-1 { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }
    .stamp-status-2 { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
    .stamp-status-3 { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
    .stamp-status-4 { background: #ecfeff; color: #0e7490; border: 1px solid #a5f3fc; }
    .stamp-status-5 { background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; }
  </style>
</head>
<body>
  <div id="app" v-cloak>
    <a-config-provider :theme="antdTheme">
      <div class="pa-workbench">

        <!-- ====================================================================
             1. 顶部场景沙盘栏 (开发调试用)
             ==================================================================== -->
        <div class="wb-scenario-bar">
          <div class="wb-scenario-left">
            <span class="wb-scenario-title">
              <iconify-icon icon="ant-design:experiment-outlined"></iconify-icon>
              业务场景沙盘:
            </span>
            <div
              v-for="s in scenarioList"
              :key="s.key"
              class="wb-scenario-pill"
              :class="{ active: currentScenarioKey === s.key }"
              @click="switchScenario(s.key)"
            >
              <span>{{ s.label }}</span>
              <span style="opacity: 0.6; font-size: 10px;">[{{ s.docNo }}]</span>
            </div>
          </div>

          <div class="wb-scenario-right">
            <a-tooltip title="模拟点击「提交送审」时：第1步保存(EditAsync)成功，但第2步送审(SubmitAsync)超时的半成功恢复提示">
              <a-checkbox v-model:checked="simulateSubmitStepFail" style="color: #cbd5e1; font-size: 11px;">
                模拟送审失败恢复
              </a-checkbox>
            </a-tooltip>

            <a-button size="small" type="dashed" ghost style="font-size: 11px; height: 20px; padding: 0 6px;" @click="triggerValidationLocateDemo">
              演示异常定位
            </a-button>

            <a-button size="small" type="primary" style="font-size: 11px; height: 20px; padding: 0 8px; background: #0284c7;" @click="showHandoffDrawer = true">
              交接说明 (5项)
            </a-button>
          </div>
        </div>

        <!-- ====================================================================
             2. 结构化主单金融底账头 (高度控制在 105px · 4 列严密对齐 · 拒绝单行拥挤)
             ==================================================================== -->
        <div class="pa-master-card">
          <!-- 上行：单据全局动作条 -->
          <div class="pa-card-action-bar">
            <div class="pa-action-left">
              <span style="font-size: 11px; color: #64748b;">单据:</span>
              <span class="pa-doc-code">{{ formState.applicationNo }}</span>
              <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-btn" @click="copyText(formState.applicationNo, '申请单号')"></iconify-icon>

              <span class="pa-status-badge" :class="'pa-status-' + formState.status">
                <iconify-icon :icon="currentStatusMeta.icon"></iconify-icon>
                <span>{{ currentStatusMeta.stampText }}</span>
              </span>

              <span style="color: #cbd5e1;">|</span>

              <span style="color: #64748b; font-size: 11px;">申请人: <strong style="color: #1e293b;">{{ formState.creatorUserName }}</strong></span>
              <span v-if="formState.submitTime" style="color: #64748b; font-size: 11px;">提交: <strong class="tabular-nums" style="color: #1e293b;">{{ formState.submitTime }}</strong></span>
              <span v-if="formState.auditTime" style="color: #64748b; font-size: 11px;">审核: <strong class="tabular-nums" style="color: #1e293b;">{{ formState.auditTime }}</strong></span>

              <span class="pa-save-indicator" :class="isMainFormDirty ? 'is-dirty' : 'is-clean'">
                <template v-if="isMainFormEditable">
                  <iconify-icon :icon="isMainFormDirty ? 'ant-design:exclamation-circle-filled' : 'ant-design:check-circle-filled'"></iconify-icon>
                  <span>{{ isMainFormDirty ? '主表有未保存改动' : '主表与发票已同步' }}</span>
                </template>
                <template v-else>
                  <iconify-icon icon="ant-design:lock-filled"></iconify-icon>
                  <span>单据已锁定 (审核流归档)</span>
                </template>
              </span>
            </div>

            <!-- 右侧动作按钮组 -->
            <div style="display: flex; align-items: center; gap: 6px;">
              <a-popconfirm
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
              </a-popconfirm>

              <template v-if="isMainFormEditable">
                <a-button size="small" :loading="saving" @click="handleSaveMainForm(false)">
                  <template #icon><iconify-icon icon="ant-design:save-outlined"></iconify-icon></template>
                  保存
                </a-button>

                <a-button size="small" type="primary" :loading="submitting" :disabled="workflowSyncing" @click="handleSubmitApplication">
                  <template #icon><iconify-icon icon="ant-design:send-outlined"></iconify-icon></template>
                  {{ workflowSyncing ? '同步中...' : '提交送审' }}
                </a-button>
              </template>

              <template v-else>
                <a-button size="small" type="primary" ghost @click="handleSaveInvoiceSupplementOnly">
                  <template #icon><iconify-icon icon="ant-design:file-protect-outlined"></iconify-icon></template>
                  保存发票与补件 (EditInvoice)
                </a-button>
              </template>

              <template v-if="formState.status === 1">
                <a-popconfirm title="确认撤销提交？" ok-text="确认撤回" cancel-text="取消" @confirm="handleUnSubmitApplication">
                  <a-button size="small" danger :loading="unsubmitting">撤销提交</a-button>
                </a-popconfirm>
              </template>

              <a-dropdown>
                <a-button size="small">
                  <iconify-icon icon="ant-design:download-outlined"></iconify-icon>
                  导出
                  <iconify-icon icon="ant-design:down-outlined" style="font-size: 10px; margin-left: 2px;"></iconify-icon>
                </a-button>
                <template #overlay>
                  <a-menu @click="handleExportMenuClick">
                    <a-menu-item key="detail">导出费用明细</a-menu-item>
                    <a-menu-item key="summary">按汇总导出</a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>

              <a-button size="small" @click="handlePrintPreview">
                <template #icon><iconify-icon icon="ant-design:printer-outlined"></iconify-icon></template>
                打印
              </a-button>
            </div>
          </div>

          <!-- 下行：严密对齐的 4 列金融底账网格 -->
          <div class="pa-ledger-grid">
            <!-- 第 1 列：结算单位 & 所属公司 -->
            <div class="pa-ledger-col">
              <div class="pa-ledger-col-title">
                <span>往来结算对象</span>
                <a-tag v-if="orderFeeGroups.length > 0" color="blue" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">
                  <iconify-icon icon="ant-design:lock-outlined"></iconify-icon> 结算已锁定
                </a-tag>
                <a-tag v-else color="warning" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">无费用·可换</a-tag>
              </div>
              <div class="pa-vendor-row" :title="formState.settlementName">
                <span class="pa-vendor-tag">{{ formState.settlementShortName || '荣易达天津' }}</span>
                <strong style="font-size: 12px; color: #0f172a; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                  {{ formState.settlementName }}
                </strong>
              </div>
              <div style="display: flex; align-items: center; gap: 4px; font-size: 11px; color: #64748b;">
                <span style="white-space: nowrap;">所属公司:</span>
                <a-select
                  v-model:value="formState.companyId"
                  size="small"
                  style="flex: 1; min-width: 0;"
                  :disabled="!isMainFormEditable"
                  :options="companyOptions"
                  @change="handleCompanyChange"
                ></a-select>
              </div>
            </div>

            <!-- 第 2 列：资金出入银行账户 (流向对账) -->
            <div class="pa-ledger-col">
              <div class="pa-ledger-col-title">
                <span>出入资金账户 (我司出款 ──▶ 对方收款)</span>
                <span style="font-size: 10px; color: #94a3b8;">结算档案直连</span>
              </div>
              <div class="pa-bank-route-card" :title="myCompanyBank.bankName + ' · ' + myCompanyBank.accountNo">
                <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: flex; align-items: center; gap: 4px;">
                  <iconify-icon icon="ant-design:bank-outlined" style="color: #2563eb;"></iconify-icon>
                  <strong style="color: #1e293b;">{{ myCompanyBank.shortName }}</strong>
                  <span class="tabular-nums" style="font-family: monospace; color: #64748b;">{{ myCompanyBank.accountNo }}</span>
                </div>
                <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-btn" @click="copyText(myCompanyBank.accountNo, '我司付款账号')"></iconify-icon>
              </div>
              <div style="display: flex; align-items: center; gap: 4px;">
                <a-select
                  v-model:value="formState.bankAccountMap[primaryCurrencyCode]"
                  size="small"
                  style="flex: 1; min-width: 0;"
                  :disabled="!isMainFormEditable"
                  :options="getPayeeBankOptions(primaryCurrencyCode)"
                  @change="markMainFormDirty"
                ></a-select>
                <iconify-icon v-if="getSelectedPayeeBank(primaryCurrencyCode)" icon="ant-design:copy-outlined" class="pa-copy-btn" @click="copyText(getSelectedPayeeBank(primaryCurrencyCode).accountNo, '对方收款账号')"></iconify-icon>
              </div>
            </div>

            <!-- 第 3 列：付款时效与汇款附言 -->
            <div class="pa-ledger-col">
              <div class="pa-ledger-col-title">
                <span>付款时效与支付附言</span>
                <span style="font-size: 10px; color: #94a3b8;">最晚出款 ~ 预计回款</span>
              </div>
              <div style="display: flex; align-items: center; gap: 4px;">
                <a-date-picker
                  v-model:value="formState.latestPaymentDate"
                  size="small"
                  value-format="YYYY-MM-DD"
                  style="flex: 1; min-width: 0;"
                  placeholder="最晚付款日"
                  :disabled="!isMainFormEditable"
                  @change="markMainFormDirty"
                ></a-date-picker>
                <span style="color: #cbd5e1;">至</span>
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
              <a-input
                v-model:value="formState.paymentDemand"
                size="small"
                :title="formState.paymentDemand"
                placeholder="汇款附言/支付要求 (限1024字)..."
                :disabled="!isMainFormEditable"
                allow-clear
                @change="markMainFormDirty"
              ></a-input>
            </div>

            <!-- 第 4 列：申请净额牌 -->
            <div class="pa-ledger-col" style="border-left: 1px solid #edf2f7; padding-left: 10px;">
              <div class="pa-ledger-col-title">
                <span>本次申请净额 (付 - 收)</span>
                <a-tag :color="formState.isCurrencyFixed ? 'purple' : 'blue'" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">
                  {{ formState.isCurrencyFixed ? ('固定 · ' + formState.currencyCode) : '按原票币' }}
                </a-tag>
              </div>
              <div style="display: flex; align-items: baseline; gap: 4px;">
                <span class="pa-currency-badge" :class="'pa-currency-' + primaryCurrencyCode">{{ primaryCurrencyCode }}</span>
                <span class="pa-net-val">{{ formatMoney(currencySummaryList[0]?.netAmount || 0, primaryCurrencyCode) }}</span>
              </div>
              <div style="font-size: 10px;">
                <span v-if="!formState.isReceiveAllSettled" style="color: #ea580c; font-weight: 600;">
                  ⚠️ 垫资未结: {{ unSettledReceiveSummaryText }}
                </span>
                <span v-else style="color: #16a34a;">
                  ✓ 关联合同已结清 (无垫资敞口)
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 异常提示条 -->
        <a-alert
          v-if="partialSubmitFailedBanner"
          type="warning"
          show-icon
          closable
          @close="partialSubmitFailedBanner = false"
          style="padding: 3px 10px; border-radius: 4px; flex-shrink: 0;"
        >
          <template #message>
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 11px;">
              <span><strong>保存成功但送审超时</strong>：{{ partialSubmitFailedReason }}。表单数据已安全落库。</span>
              <a-button size="small" type="primary" style="height: 20px; font-size: 11px;" @click="retrySubmitOnly">仅重试送审</a-button>
            </div>
          </template>
        </a-alert>

        <!-- ====================================================================
             3. 业务费用明细主舞台 (高屏呈现 · 100% 满宽 · 0 横向滚动条)
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

          <!-- 100% 满宽表格区 (0 横向滚动条) -->
          <div class="pa-table-scroll-area">
            <table class="pa-main-table">
              <thead>
                <tr>
                  <th style="width: 30px; text-align: center;">
                    <a-checkbox
                      :checked="isAllFeesSelected"
                      :indeterminate="isFeesPartiallySelected"
                      :disabled="!isMainFormEditable"
                      @change="handleSelectAllFees"
                    ></a-checkbox>
                  </th>
                  <th style="width: 22px;"></th>
                  <th style="width: 32px; text-align: center;">序</th>
                  <th style="width: 80px;">开船日</th>
                  <th style="width: 80px;">会计日</th>
                  <th style="width: 140px;">委托编号</th>
                  <th style="width: 125px;">主提单号</th>
                  <th style="width: 160px;">委托单位</th>
                  <th style="width: 160px;">结算单位</th>
                  <th style="width: 70px; text-align: center;">应收审核</th>
                  <th style="width: 70px; text-align: center;">应付审核</th>
                  <th style="width: 90px;">目的港</th>
                  <th style="width: 65px;">箱量</th>
                  <th style="width: 70px;">销售</th>
                  <th style="width: 70px;">船司</th>
                  <th style="width: 75px; text-align: center;">应收结算</th>
                  <th style="width: 130px; text-align: right;">应收未结金额</th>
                  <th style="width: 120px; text-align: right;">申请合计</th>
                </tr>
              </thead>
              <tbody>
                <template v-for="(group, gIdx) in filteredOrderFeeGroups" :key="group.groupId || gIdx">
                  <!-- 主单业务行 -->
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
                    <td class="tabular-nums">{{ group.etd || '-' }}</td>
                    <td class="tabular-nums">{{ group.accountDate || '-' }}</td>
                    <td>
                      <a class="pa-link-code" @click="handlePenetrateOrder(group.commissionNum)">{{ group.commissionNum }}</a>
                      <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-btn" @click="copyText(group.commissionNum, '委托编号')"></iconify-icon>
                    </td>
                    <td>
                      <span class="tabular-nums" style="font-family: monospace;">{{ group.mblNum || '-' }}</span>
                      <iconify-icon v-if="group.mblNum" icon="ant-design:copy-outlined" class="pa-copy-btn" @click="copyText(group.mblNum, '主提单号')"></iconify-icon>
                    </td>
                    <td>
                      <span :title="group.clientName" style="display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ group.clientName || '-' }}</span>
                    </td>
                    <td>
                      <span :title="group.settlementName" style="display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ group.settlementName || '-' }}</span>
                    </td>
                    <td style="text-align: center;">
                      <a-tag :color="getFeeAuditColor(group.receiveFeeStatus)" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">{{ group.receiveFeeStatus || '未审' }}</a-tag>
                    </td>
                    <td style="text-align: center;">
                      <a-tag :color="getFeeAuditColor(group.payFeeStatus)" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">{{ group.payFeeStatus || '未审' }}</a-tag>
                    </td>
                    <td>{{ group.podName || '-' }}</td>
                    <td>{{ group.totalCtn || '-' }}</td>
                    <td>{{ group.salesmanName || '-' }}</td>
                    <td>{{ group.carrierName || '-' }}</td>
                    <td style="text-align: center;">
                      <a-tag :color="getSettlementStatusColor(group.recSettlementStatus)" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">
                        {{ group.recSettlementStatus || '未结' }}
                      </a-tag>
                    </td>
                    <!-- 应收未结 -->
                    <td style="text-align: right;">
                      <div v-for="unRec in group.unSettledReceiveList" :key="unRec.currency" style="font-size: 11px;" :style="{ color: unRec.amount > 0 ? '#ea580c' : '#64748b' }">
                        <span class="tabular-nums font-semibold">{{ unRec.currency }} {{ formatDecimal(unRec.amount) }}</span>
                      </div>
                      <div v-if="!group.unSettledReceiveList || group.unSettledReceiveList.length === 0" style="color: #16a34a; font-size: 11px;">
                        已结清
                      </div>
                    </td>
                    <!-- 申请合计 -->
                    <td style="text-align: right;">
                      <div v-for="(sumAmt, cCode) in group.groupCurrencySum" :key="cCode" style="font-size: 11px; font-weight: 700; color: #0f172a;" class="tabular-nums">
                        {{ cCode }} {{ formatDecimal(sumAmt) }}
                      </div>
                    </td>
                  </tr>

                  <!-- 嵌套子明细 -->
                  <tr v-if="group.isExpanded">
                    <td colspan="18" style="padding: 0;">
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
                              <th style="width: 120px; text-align: right;">本次申请金额</th>
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
                              <td><strong style="color: #0f172a;">{{ fee.feeCodeName }}</strong></td>
                              <td><span class="pa-currency-badge" :class="'pa-currency-' + fee.currencyCode">{{ fee.currencyCode }}</span></td>
                              <td style="text-align: right;" class="tabular-nums">{{ formatMoney(fee.amount, fee.currencyCode) }}</td>
                              <td style="text-align: right;" class="tabular-nums">{{ Number(fee.exchangeRate || 1).toFixed(4) }}</td>
                              <td style="text-align: right; color: #64748b;" class="tabular-nums">{{ formatMoney(fee.settledAmount, fee.currencyCode) }}</td>
                              <td style="text-align: right; font-weight: 600; color: #2563eb;" class="tabular-nums">{{ formatMoney(fee.unRqstPaymentAmount, fee.currencyCode) }}</td>
                              <td v-if="formState.isCurrencyFixed" style="text-align: right;" class="tabular-nums">
                                <span v-if="fee.currencyCode === formState.currencyCode">1.000000</span>
                                <span v-else style="color: #7c3aed; font-weight: 600;">{{ Number(fee.rate || 0.15).toFixed(6) }}</span>
                              </td>
                              <td v-if="formState.isCurrencyFixed" style="text-align: right; color: #7c3aed; font-weight: 600;" class="tabular-nums">
                                {{ formatMoney(fee.appliedAmountConverted, formState.currencyCode) }}
                              </td>
                              <td style="text-align: right;">
                                <span class="tabular-nums" style="font-size: 12px; font-weight: 700; color: #0f172a;">
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
                  <td colspan="18" style="text-align: center; color: #94a3b8; padding: 32px;">
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
                <span style="color: #64748b;">{{ cur.currencyCode }} 申请净额:</span>
                <strong class="tabular-nums" style="font-size: 13px; color: #0f172a; margin-left: 3px;">
                  {{ formatMoney(cur.netAmount, cur.currencyCode) }}
                </strong>
              </div>

              <div v-if="formState.isCurrencyFixed" style="border-left: 1px solid #cbd5e1; padding-left: 10px;">
                <span style="color: #7c3aed;">固定币总计 ({{ formState.currencyCode }}):</span>
                <strong class="tabular-nums" style="font-size: 14px; color: #7c3aed; margin-left: 3px;">
                  {{ formatMoney(fixedCurrencyGrandTotal, formState.currencyCode) }}
                </strong>
              </div>
            </div>
          </div>
        </div>

        <!-- ====================================================================
             4. 底部对账协同区 (左发票 58% / 右审批与附件 42%)
             ==================================================================== -->
        <div class="pa-bottom-grid">
          <!-- 左卡：发票核对中心 -->
          <div class="pa-deck-card">
            <div class="pa-deck-header">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-weight: 600; color: #0f172a; display: inline-flex; align-items: center; gap: 4px;">
                  <iconify-icon icon="ant-design:file-protect-outlined" style="color: #2563eb;"></iconify-icon>
                  发票核对 ({{ formState.invoiceRows.length }})
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
                  <span style="font-size: 11px; color: #15803d; font-weight: 500;">
                    <iconify-icon icon="ant-design:check-circle-filled" style="margin-right: 3px;"></iconify-icon>
                    免开票业务 · 已合规豁免
                  </span>
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
          </div>

          <!-- 右卡：审批流程与附件档案 (双 Tab 切换) -->
          <div class="pa-deck-card">
            <div class="pa-deck-header">
              <a-radio-group v-model:value="activeDeckTab" size="small" button-style="solid">
                <a-radio-button value="workflow">
                  <iconify-icon icon="ant-design:history-outlined" style="margin-right: 3px;"></iconify-icon>
                  审批流程跟踪
                </a-radio-button>
                <a-radio-button value="attachment">
                  <iconify-icon icon="ant-design:paper-clip-outlined" style="margin-right: 3px;"></iconify-icon>
                  单据附件 ({{ applicationAttachmentGroups.reduce((c, g) => c + g.items.length, 0) + settlementAttachments.length }})
                </a-radio-button>
              </a-radio-group>

              <span class="pa-audit-stamp" :class="'stamp-status-' + formState.status">
                {{ currentStatusMeta.stampText }}
              </span>
            </div>

            <div class="pa-deck-body">
              <!-- Tab 1: 审批流程 -->
              <div v-if="activeDeckTab === 'workflow'" style="display: flex; flex-direction: column; gap: 6px;">
                <div
                  v-for="(node, nIdx) in workflowNodes"
                  :key="nIdx"
                  style="border: 1px solid #e2e8f0; border-radius: 4px; padding: 6px 10px; background: #f8fafc;"
                  :style="{ borderColor: node.status === 'rejected' ? '#fecaca' : (node.status === 'passed' ? '#bbf7d0' : '#e2e8f0') }"
                >
                  <div style="display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-weight: 600; color: #0f172a; font-size: 11px;">
                      <iconify-icon :icon="getNodeIcon(node.status)" :style="{ color: getNodeColor(node.status) }"></iconify-icon>
                      {{ node.nodeName }}
                    </span>
                    <a-tag :color="getNodeTagColor(node.status)" style="font-size: 10px; line-height: 16px; margin: 0; padding: 0 4px;">{{ node.statusText }}</a-tag>
                  </div>
                  <div style="font-size: 10px; color: #64748b; margin-top: 3px; display: flex; justify-content: space-between;">
                    <span>处理人: {{ node.operatorName || '系统分配' }}</span>
                    <span v-if="node.operateTime" class="tabular-nums">{{ node.operateTime }}</span>
                  </div>
                  <div v-if="node.comment || (nIdx === 0 && formState.status === 0)" style="margin-top: 4px; padding: 3px 6px; border-radius: 3px; font-size: 10px;" :style="{ background: node.status === 'rejected' ? '#fee2e2' : '#f1f5f9', color: node.status === 'rejected' ? '#991b1b' : '#334155' }">
                    <strong>{{ node.status === 'rejected' ? '驳回原因: ' : '意见: ' }}</strong>
                    <span>{{ (nIdx === 0 && formState.status === 0) ? draftNodeComment : node.comment }}</span>
                  </div>
                  <div v-if="node.signature" style="margin-top: 4px; text-align: right;">
                    <span style="display: inline-block; border: 1px dashed #94a3b8; padding: 1px 6px; font-size: 9px; color: #475569; border-radius: 2px;">
                      ✍️ 电子签名: {{ node.signature }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Tab 2: 附件档案 -->
              <div v-if="activeDeckTab === 'attachment'">
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px;">
                  <template v-for="grp in applicationAttachmentGroups" :key="grp.title">
                    <div v-for="att in grp.items" :key="att.id" style="border: 1px solid #e2e8f0; border-radius: 4px; padding: 5px 8px; background: #f8fafc; display: flex; align-items: center; justify-content: space-between;">
                      <div style="display: flex; align-items: center; gap: 6px; overflow: hidden;">
                        <iconify-icon icon="ant-design:file-pdf-outlined" style="color: #ef4444; font-size: 15px; flex-shrink: 0;"></iconify-icon>
                        <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                          <div style="font-weight: 600; font-size: 11px; color: #0f172a;" :title="att.name">{{ att.name }}</div>
                          <div style="font-size: 9px; color: #94a3b8;">{{ grp.title }} · {{ att.size }}</div>
                        </div>
                      </div>
                      <a-button type="link" size="small" style="font-size: 11px; padding: 0;" @click="previewAttachment(att)">预览</a-button>
                    </div>
                  </template>
                  <div v-if="applicationAttachmentGroups.reduce((c, g) => c + g.items.length, 0) === 0" style="grid-column: 1 / -1; text-align: center; color: #94a3b8; padding: 20px;">
                    暂无附件档案
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

""" + modals_block + script_block

with open('pages/payment-application-edit.html', 'w', encoding='utf-8') as f:
    f.write(flawless_html)

print("Overwrote pages/payment-application-edit.html with flawless architecture!")
