import os
import json

output_path = os.path.abspath('pages/comprehensive-business-edit.html')

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>综合业务编辑工作台 - 操作管理 (#178 左右同屏精简与费用合一交付)</title>

  <!-- 核心样式：Ant Design Vue 4 重置样式与通用规范 -->
  <link rel="stylesheet" href="../assets/vendor/reset.css">
  <link rel="stylesheet" href="../assets/css/common.css">

  <!-- 本地极速资源：零外网依赖、离线秒开 -->
  <script src="../assets/vendor/dayjs-bundle.min.js"></script>
  <script src="../assets/vendor/vue.global.prod.js"></script>
  <script src="../assets/vendor/antd.min.js"></script>
  <script src="../assets/vendor/iconify-icon.min.js"></script>
  <script src="../assets/js/common.js"></script>

  <style>
    /* ==========================================================================
       综合业务编辑工作台 (#178 左右同屏高密度规范)
       设计基准：1920×1080 视口，去除卡片嵌套黑框，深度还原真实货代生产系统
       3大页签：应收应付 (左业务410px + 右费用双轨)、更改单、附件
       ========================================================================== */

    html, body {
      height: 100%;
      margin: 0;
      padding: 0;
      background-color: #f0f2f5;
      color: #1f2329;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
      font-size: 12px;
      overflow: hidden;
    }

    #app {
      height: 100%;
      display: flex;
      flex-direction: column;
    }

    /* 顶部原型审查沙盘控制器 (浅色优雅风格，杜绝漆黑黑客控制台) */
    .scenario-toolbar {
      background: #ffffff;
      color: #4b5563;
      padding: 5px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #e5e7eb;
      font-size: 12px;
      z-index: 100;
      box-shadow: 0 1px 2px rgba(0,0,0,0.02);
      flex-shrink: 0;
    }
    .scenario-left {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .scenario-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: #eff6ff;
      color: #1d4ed8;
      font-weight: 600;
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 4px;
      border: 1px solid #dbeafe;
    }
    .scenario-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* 顶层认票身份与状态条 (Ticket Identity Header) */
    .wb-header {
      background: #ffffff;
      padding: 6px 16px;
      border-bottom: 1px solid #e8e8e8;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .wb-header-left {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .wb-job-no {
      font-size: 15px;
      font-weight: 700;
      color: #111827;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .ticket-chip {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      color: #4b5563;
      background: #f3f4f6;
      padding: 1px 8px;
      border-radius: 3px;
      border: 1px solid #e5e7eb;
    }
    .ticket-chip strong {
      color: #111827;
    }
    .dirty-pill {
      background: #fffbe6;
      border: 1px solid #ffe58f;
      color: #d46b08;
      font-size: 11px;
      padding: 1px 6px;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-weight: 500;
    }
    .wb-header-right {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* 三大功能页签导航条 */
    .wb-nav-tabs-bar {
      background: #ffffff;
      padding: 0 16px;
      border-bottom: 1px solid #d9d9d9;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .wb-nav-tabs-bar .ant-tabs-nav {
      margin-bottom: 0 !important;
    }

    /* 页面主体视口 */
    .wb-view-container {
      flex: 1;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      position: relative;
    }

    /* ==========================================================================
       TAB 1: 应收应付双轨工作台布局 (#178 左右同屏)
       左侧业务信息固定约410px，右侧费用上下双表 + 分隔条 + 底部固定合计
       ========================================================================== */
    .dual-rail-workbench {
      flex: 1;
      display: flex;
      overflow: hidden;
      padding: 6px;
      gap: 6px;
      box-sizing: border-box;
      background: #eaedf1;
    }

        /* ==========================================================================
       左侧业务信息面板 (410px 严格对齐网格、单画布无框套框、高清晰层级)
       ========================================================================== */
    .left-business-panel {
      width: 410px;
      flex-shrink: 0;
      background: #ffffff;
      border-radius: 4px;
      border: 1px solid #d9d9d9;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transition: width 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .left-business-panel.is-collapsed {
      width: 44px;
      cursor: pointer;
      background: #fafafa;
    }
    .panel-header-bar {
      height: 38px;
      padding: 0 12px;
      background: #fafafa;
      border-bottom: 1px solid #e8e8e8;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .panel-title-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .panel-title {
      font-size: 13px;
      font-weight: 700;
      color: #111827;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .panel-actions {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .panel-collapsed-strip {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 14px 0;
      background: #fafafa;
    }
    .collapsed-vertical-text {
      writing-mode: vertical-lr;
      letter-spacing: 4px;
      font-weight: 600;
      color: #374151;
      font-size: 13px;
    }

    /* 左侧表单滚动体：纯净单画布，去除嵌套卡片与杂乱边框 */
    .business-form-scroll {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 10px 14px 16px 14px;
    }
    .business-form-scroll::-webkit-scrollbar {
      width: 4px;
    }
    .business-form-scroll::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 2px;
    }

    /* 区段分割标题 (Section Divider) */
    .form-section-divider {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin: 14px 0 8px 0;
      padding-bottom: 4px;
      border-bottom: 1px solid #f0f0f0;
    }
    .form-section-divider:first-child {
      margin-top: 0;
    }
    .form-section-title {
      font-size: 12px;
      font-weight: 700;
      color: #1f2937;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .form-section-title::before {
      content: '';
      display: inline-block;
      width: 3px;
      height: 12px;
      background: #1677ff;
      border-radius: 1.5px;
    }
    .form-section-sub {
      font-size: 11px;
      color: #9ca3af;
      font-weight: normal;
    }

    /* 严谨 2 列表单网格 (Strict 2-Column Grid) */
    .biz-form-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 7px 10px;
    }
    .grid-col-1 {
      grid-column: span 1;
    }
    .grid-col-2 {
      grid-column: span 2;
    }

    /* 表单项单元 (Form Item) */
    .biz-form-item {
      display: flex;
      flex-direction: column;
      gap: 3px;
      min-width: 0;
    }
    .biz-form-label {
      font-size: 11px;
      font-weight: 500;
      color: #4b5563;
      display: flex;
      align-items: center;
      justify-content: space-between;
      line-height: 1.3;
      white-space: nowrap;
    }
    .biz-form-label.required::before {
      content: '*';
      color: #ff4d4f;
      margin-right: 3px;
      font-weight: bold;
    }
    .biz-label-hint {
      font-size: 10px;
      color: #9ca3af;
      font-weight: normal;
    }

    /* 等宽等高只读展示框 */
    .readonly-box {
      height: 24px;
      line-height: 22px;
      padding: 0 7px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 2px;
      font-size: 11px;
      color: #1e293b;
      font-family: -apple-system, BlinkMacSystemFont, monospace;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: space-between;
      overflow: hidden;
      white-space: nowrap;
    }

    /* 主单关联紧凑卡片 */
    .linked-master-box {
      background: #f0f7ff;
      border: 1px solid #bae0ff;
      border-radius: 3px;
      padding: 4px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
    }

    /* 追加干系人岗位紧凑表格 */
    .stakeholder-grid-row {
      display: grid;
      grid-template-columns: 50px 1fr 24px;
      gap: 6px;
      align-items: center;
      margin-top: 5px;
    }
    .stakeholder-tag-lbl {
      font-size: 11px;
      color: #4b5563;
      text-align: right;
      font-weight: 500;
    }

    /* ==========================================================================
       右侧费用工作区 (Fee Workspace)
       ========================================================================== */
    .right-fee-panel {
      flex: 1;
      background: #ffffff;
      border-radius: 4px;
      border: 1px solid #d9d9d9;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      min-width: 0;
    }

    /* 费用全局工具栏 */
    .fee-global-toolbar {
      height: 36px;
      padding: 0 10px;
      background: #fafafa;
      border-bottom: 1px solid #e8e8e8;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .fee-toolbar-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .fee-toolbar-right {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* 合并查看·只读模式提示条 */
    .merge-readonly-banner {
      background: #fff7e6;
      border-bottom: 1px solid #ffd591;
      color: #d46b08;
      padding: 4px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      flex-shrink: 0;
    }
    .merge-banner-text {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* 上下费用双表容器 */
    .fee-tables-container {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
    }

    /* 单张费用表卡片 */
    .fee-table-block {
      display: flex;
      flex-direction: column;
      overflow: hidden;
      min-height: 120px;
    }
    .fee-table-header {
      height: 32px;
      padding: 0 10px;
      background: #f8fafc;
      border-bottom: 1px solid #e5e7eb;
      border-top: 1px solid #e5e7eb;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .fee-table-title {
      font-size: 12px;
      font-weight: 600;
      color: #1e293b;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .fee-table-actions {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* 可拖拽高度分隔条 */
    .fee-splitter-bar {
      height: 6px;
      background: #e2e8f0;
      border-top: 1px solid #cbd5e1;
      border-bottom: 1px solid #cbd5e1;
      cursor: row-resize;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      user-select: none;
      flex-shrink: 0;
      transition: background 0.2s;
    }
    .fee-splitter-bar:hover, .fee-splitter-bar.is-dragging {
      background: #1677ff;
    }
    .splitter-handle {
      width: 32px;
      height: 3px;
      background: #94a3b8;
      border-radius: 2px;
    }
    .fee-splitter-bar:hover .splitter-handle {
      background: #ffffff;
    }
    .splitter-quick-btns {
      position: absolute;
      right: 12px;
      top: -9px;
      display: flex;
      gap: 4px;
      background: #ffffff;
      padding: 0 4px;
      border-radius: 3px;
      border: 1px solid #cbd5e1;
      font-size: 10px;
      z-index: 10;
    }
    .splitter-quick-btn {
      background: transparent;
      border: none;
      color: #64748b;
      cursor: pointer;
      padding: 0 3px;
      font-size: 10px;
    }
    .splitter-quick-btn:hover {
      color: #1677ff;
      font-weight: 600;
    }

    /* 表格体滚动 */
    .fee-table-scroll {
      flex: 1;
      overflow: auto;
    }
    .fee-table-scroll::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .fee-table-scroll::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 3px;
    }

    /* 表格内高密度行内编辑控件 */
    .cell-input-clean {
      width: 100%;
      height: 24px;
      padding: 0 4px;
      border: 1px solid transparent;
      background: transparent;
      border-radius: 2px;
      font-size: 11px;
      box-sizing: border-box;
      transition: all 0.2s;
    }
    .cell-input-clean:hover {
      border-color: #d9d9d9;
      background: #ffffff;
    }
    .cell-input-clean:focus {
      border-color: #1677ff;
      background: #ffffff;
      outline: none;
      box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1);
    }
    .cell-num-right {
      text-align: right;
      font-variant-numeric: tabular-nums;
    }

    /* 固定吸底利润合计栏 */
    .fixed-fee-summary-bar {
      height: 38px;
      background: #fafafa;
      border-top: 1px solid #d9d9d9;
      padding: 0 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      font-size: 12px;
    }
    .summary-left-currencies {
      display: flex;
      align-items: center;
      gap: 16px;
      color: #4b5563;
    }
    .summary-item {
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .summary-right-totals {
      display: flex;
      align-items: center;
      gap: 20px;
    }
    .profit-val-highlight {
      font-size: 14px;
      font-weight: 700;
      font-variant-numeric: tabular-nums;
    }

    /* ==========================================================================
       TAB 2: 更改单页签样式
       ========================================================================== */
    .change-order-view {
      flex: 1;
      background: #f0f2f5;
      padding: 12px;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      gap: 10px;
    }
    .co-prerequisite-card {
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 6px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 12px;
      max-width: 720px;
      margin: 40px auto;
    }

    /* ==========================================================================
       TAB 3: 附件页签样式
       ========================================================================== */
    .attachment-view {
      flex: 1;
      background: #f0f2f5;
      padding: 12px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      gap: 10px;
    }
    .attachment-card {
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 6px;
      padding: 16px;
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    /* 浮动设计规范抽屉按钮 */
    .floating-spec-btn {
      position: fixed;
      right: 18px;
      bottom: 48px;
      z-index: 1000;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  </style>
</head>
<body>
<div id="app">

  <!-- ========================================================================
       1. 顶部原型审查沙盘控制器 (评审与多状态验证专用)
       ======================================================================== -->
  <div class="scenario-toolbar">
    <div class="scenario-left">
      <div class="scenario-badge">
        <iconify-icon icon="ant-design:experiment-outlined"></iconify-icon>
        原型审查沙盘
      </div>
      <a-radio-group v-model:value="currentScenario" size="small" @change="handleScenarioChange">
        <a-radio-button value="standard">1. 标准待补全 (TEST130-0022)</a-radio-button>
        <a-radio-button value="dirty">2. 分区脏状态 (3大保存独立)</a-radio-button>
        <a-radio-button value="merge">3. 合并更改单 (只读态)</a-radio-button>
        <a-radio-button value="co_blocked">4. 更改单前置拦截 (未锁费用)</a-radio-button>
        <a-radio-button value="co_unlocked">5. 更改单录入 (已锁原费)</a-radio-button>
        <a-radio-button value="attach_empty">6. 附件无类型配置 (空态)</a-radio-button>
        <a-radio-button value="attach_full">7. 附件分类管理 (有文件)</a-radio-button>
        <a-radio-button value="ticket_locked">8. 本票已锁账 (字段屏蔽)</a-radio-button>
      </a-radio-group>
    </div>

    <div class="scenario-right">
      <a-tag v-if="ticketData.isLocked" color="red">
        <iconify-icon icon="ant-design:lock-outlined"></iconify-icon> 本票已锁账
      </a-tag>
      <a-tag v-else color="green">
        <iconify-icon icon="ant-design:unlock-outlined"></iconify-icon> 正常可编辑
      </a-tag>
      <a-button size="small" type="link" @click="showSpecDrawer = true">
        <iconify-icon icon="ant-design:file-text-outlined"></iconify-icon> 规范交接与核对报告
      </a-button>
    </div>
  </div>

  <!-- ========================================================================
       2. 顶层认票身份与状态条 (Persistent Ticket Identity Bar)
       ======================================================================== -->
  <div class="wb-header">
    <div class="wb-header-left">
      <div class="wb-job-no">
        <iconify-icon icon="ant-design:container-outlined" style="color: #1677ff;"></iconify-icon>
        {{ ticketData.jobNo }}
        <a-button type="text" size="small" @click="copyText(ticketData.jobNo)" title="复制委托编号">
          <iconify-icon icon="ant-design:copy-outlined"></iconify-icon>
        </a-button>
      </div>

      <div class="ticket-chip">
        提单号: <strong>{{ ticketData.blNo || '-' }}</strong>
      </div>
      <div class="ticket-chip">
        委托单位: <strong>{{ ticketData.customerName }}</strong>
      </div>
      <div class="ticket-chip">
        组织: <strong>{{ ticketData.salesOrgName }}</strong>
      </div>
      <div class="ticket-chip">
        销售: <strong>{{ ticketData.salesPerson }}</strong>
      </div>
      <div class="ticket-chip">
        会计月份: <strong>{{ ticketData.accountingPeriod }}</strong>
      </div>

      <!-- 分区未保存脏状态胶囊提示 -->
      <span v-if="dirtyStates.basic" class="dirty-pill">
        <iconify-icon icon="ant-design:edit-outlined"></iconify-icon> 业务信息未存*
      </span>
      <span v-if="dirtyStates.rec" class="dirty-pill">
        <iconify-icon icon="ant-design:edit-outlined"></iconify-icon> 应收未存*
      </span>
      <span v-if="dirtyStates.pay" class="dirty-pill">
        <iconify-icon icon="ant-design:edit-outlined"></iconify-icon> 应付未存*
      </span>
    </div>

    <div class="wb-header-right">
      <a-button-group size="small">
        <a-button :disabled="orderIndex <= 0" @click="handlePrevOrder">
          <iconify-icon icon="ant-design:left-outlined"></iconify-icon> 上一票
        </a-button>
        <a-button :disabled="orderIndex >= totalOrders - 1" @click="handleNextOrder">
          下一票 <iconify-icon icon="ant-design:right-outlined"></iconify-icon>
        </a-button>
      </a-button-group>

      <a-dropdown size="small">
        <template #overlay>
          <a-menu>
            <a-menu-item key="copy" @click="openCopyModal">
              <iconify-icon icon="ant-design:copy-outlined"></iconify-icon> 复制本票业务 (带费用选择)
            </a-menu-item>
            <a-menu-item key="refresh" @click="reloadTicket">
              <iconify-icon icon="ant-design:reload-outlined"></iconify-icon> 重新读取本票数据
            </a-menu-item>
          </a-menu>
        </template>
        <a-button size="small">
          更多 <iconify-icon icon="ant-design:down-outlined"></iconify-icon>
        </a-button>
      </a-dropdown>
    </div>
  </div>

  <!-- ========================================================================
       3. 核心三大页签导航条 (应收应付、更改单、附件)
       ======================================================================== -->
  <div class="wb-nav-tabs-bar">
    <a-tabs v-model:activeKey="activeTabKey" style="margin-bottom: -1px;">
      <a-tab-pane key="fee">
        <template #tab>
          <span>
            <iconify-icon icon="ant-design:transaction-outlined"></iconify-icon>
            应收应付
            <a-badge :count="receivableList.length + payableList.length" :overflow-count="99" :number-style="{ backgroundColor: '#1677ff', marginLeft: '6px' }"></a-badge>
          </span>
        </template>
      </a-tab-pane>

      <a-tab-pane key="changeOrder">
        <template #tab>
          <span>
            <iconify-icon icon="ant-design:form-outlined"></iconify-icon>
            更改单
            <a-badge v-if="changeOrderList.length > 0" :count="changeOrderList.length" :number-style="{ backgroundColor: '#fa8c16', marginLeft: '6px' }"></a-badge>
          </span>
        </template>
      </a-tab-pane>

      <a-tab-pane key="attachment">
        <template #tab>
          <span>
            <iconify-icon icon="ant-design:paper-clip-outlined"></iconify-icon>
            附件
            <a-badge v-if="attachmentList.length > 0" :count="attachmentList.length" :number-style="{ backgroundColor: '#52c41a', marginLeft: '6px' }"></a-badge>
          </span>
        </template>
      </a-tab-pane>
    </a-tabs>

    <div style="font-size: 11px; color: #64748b; display: flex; align-items: center; gap: 8px;">
      <span>业务路由: <code>/comprehensive/:id/edit</code></span>
      <a-tag v-if="ticketData.masked" color="orange">敏感字段已脱敏遮罩</a-tag>
    </div>
  </div>

  <!-- ========================================================================
       4. 页面主体视口 (包含3大页签的内容切换)
       ======================================================================== -->
  <div class="wb-view-container">

    <!-- ====================================================================
         TAB 1: 应收应付工作台 (#178 左右同屏双轨模型)
         左栏: 业务信息 (~410px，独立滚动)
         右栏: 费用区 (顶部工具栏 + 上应收 + 拖动条 + 下应付 + 固定合计)
         ==================================================================== -->
    <div v-show="activeTabKey === 'fee'" class="dual-rail-workbench">

      <!-- 左侧业务信息面板 (~410px) -->
      <div class="left-business-panel" :class="{ 'is-collapsed': isLeftCollapsed }">
        <!-- 面板顶栏 (清晰标题 + 独立保存 + 折叠) -->
        <div class="panel-header-bar">
          <div class="panel-title-wrap">
            <div class="panel-title">
              <iconify-icon icon="ant-design:form-outlined" style="color: #1677ff; font-size: 14px;"></iconify-icon>
              <span v-if="!isLeftCollapsed">业务基础信息</span>
              <a-tag v-if="!isLeftCollapsed" color="blue" :bordered="false" style="font-size: 10px; line-height: 18px; padding: 0 4px; margin: 0;">综合业务</a-tag>
              <span v-if="!isLeftCollapsed && dirtyStates.basic" style="color: #fa8c16; font-size: 11px; font-weight: 600;">(未存*)</span>
            </div>
          </div>
          <div class="panel-actions">
            <template v-if="!isLeftCollapsed">
              <!-- 业务信息独立保存按钮 (明确只存业务) -->
              <a-button 
                type="primary" 
                size="small" 
                :loading="isSavingBasic" 
                :disabled="ticketData.isLocked"
                style="height: 26px; padding: 0 10px; font-size: 12px; font-weight: 500;"
                @click="saveBasicInfo">
                <iconify-icon icon="ant-design:save-outlined"></iconify-icon> 保存业务
              </a-button>
              <a-tooltip title="收起左栏，最大化右侧费用表格宽度">
                <a-button type="text" size="small" style="color: #64748b; padding: 0 4px;" @click="isLeftCollapsed = true">
                  <iconify-icon icon="ant-design:menu-fold-outlined"></iconify-icon>
                </a-button>
              </a-tooltip>
            </template>
            <template v-else>
              <a-tooltip title="展开左侧业务信息栏">
                <a-button type="text" size="small" @click="isLeftCollapsed = false">
                  <iconify-icon icon="ant-design:menu-unfold-outlined"></iconify-icon>
                </a-button>
              </a-tooltip>
            </template>
          </div>
        </div>

        <!-- 折叠后的极窄竖向标识条 -->
        <div v-if="isLeftCollapsed" class="panel-collapsed-strip" @click="isLeftCollapsed = false">
          <div class="collapsed-vertical-text">业务信息 · {{ ticketData.jobNo }}</div>
          <a-tooltip title="点击展开">
            <a-button type="link" size="small">
              <iconify-icon icon="ant-design:right-outlined"></iconify-icon>
            </a-button>
          </a-tooltip>
        </div>

        <!-- 展开后的完整业务字段表单 (纯净单画布，严谨网格对齐，清晰层次) -->
        <div v-else class="business-form-scroll">

          <!-- 模块 1: 单据归属与期间 (Identification & Accounting) -->
          <div class="form-section-divider">
            <div class="form-section-title">单据归属与期间</div>
            <span class="form-section-sub">核对识别与组织隔离</span>
          </div>

          <div class="biz-form-grid">
            <!-- 提单号 (BL No.) - 全宽 -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label">
                <span>提单号 (BL No.)</span>
                <span class="biz-label-hint">外部运输号 · 优先展示</span>
              </div>
              <a-input 
                v-model:value="form.blNo" 
                size="small"
                placeholder="请输入提单号 (英文自动大写)" 
                :maxlength="64"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"
                @input="e => form.blNo = e.target.value.toUpperCase()">
                <template #suffix>
                  <iconify-icon icon="ant-design:copy-outlined" style="cursor: pointer; color: #9ca3af;" title="复制提单号" @click="copyText(form.blNo)"></iconify-icon>
                </template>
              </a-input>
            </div>

            <!-- 委托编号 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>委托编号</span>
                <a-popconfirm 
                  title="重新生成委托编号将直接向服务器申请新号并落库，是否确认？" 
                  ok-text="确认重生成" 
                  cancel-text="取消" 
                  :disabled="ticketData.isLocked"
                  @confirm="regenerateJobNo">
                  <a-button type="link" size="small" style="padding: 0; height: auto; font-size: 10px;" :disabled="ticketData.isLocked">
                    重生成
                  </a-button>
                </a-popconfirm>
              </div>
              <div class="readonly-box">
                <span>{{ form.jobNo }}</span>
                <iconify-icon icon="ant-design:lock-outlined" style="color: #94a3b8; font-size: 12px;"></iconify-icon>
              </div>
            </div>

            <!-- 会计月份 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>会计月份</span>
                <a-tooltip title="后端决定的会计月份，只读">
                  <iconify-icon icon="ant-design:question-circle-outlined" style="color: #94a3b8; font-size: 11px;"></iconify-icon>
                </a-tooltip>
              </div>
              <div class="readonly-box" style="color: #1d4ed8;">
                <span>{{ form.accountingPeriod }}</span>
                <iconify-icon icon="ant-design:calendar-outlined" style="color: #94a3b8; font-size: 12px;"></iconify-icon>
              </div>
            </div>

            <!-- 所属公司 (销售直属组织) - 全宽 -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label required">
                <span>所属公司 (销售直属组织)</span>
                <a-tooltip title="当前选择的是销售直属组织路径；切换销售将联动更新组织">
                  <iconify-icon icon="ant-design:info-circle-outlined" style="color: #1677ff; font-size: 11px;"></iconify-icon>
                </a-tooltip>
              </div>
              <a-select 
                v-model:value="form.salesOrgId" 
                size="small"
                :options="salesOrgOptions" 
                placeholder="请选择直属销售组织"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 关联主单 - 全宽 -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label">
                <span>关联主单 (海出/海进/件杂货)</span>
                <span class="biz-label-hint">同公司校验 · 最多1票</span>
              </div>
              <div v-if="form.relatedMasterOrder" class="linked-master-box">
                <span style="color: #1e40af; font-weight: 500;">
                  <iconify-icon icon="ant-design:link-outlined"></iconify-icon>
                  {{ form.relatedMasterOrder.type }} · {{ form.relatedMasterOrder.no }}
                  <span style="color: #4b5563; font-weight: normal; margin-left: 4px;">({{ form.relatedMasterOrder.customer }})</span>
                </span>
                <a-button type="text" size="small" danger style="padding: 0 4px; height: 18px;" @click="unlinkMasterOrder" title="解除关联">
                  <iconify-icon icon="ant-design:close-outlined"></iconify-icon>
                </a-button>
              </div>
              <div v-else>
                <a-button type="dashed" size="small" block :disabled="ticketData.isLocked" @click="openMasterOrderModal">
                  <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 关联海运主单 / 件杂货单
                </a-button>
              </div>
            </div>
          </div>

          <!-- 模块 2: 往来单位与干系人 (Customer & Stakeholders) -->
          <div class="form-section-divider">
            <div class="form-section-title">客户委托与干系人</div>
            <span class="form-section-sub">往来信用与权责分配</span>
          </div>

          <div class="biz-form-grid">
            <!-- 委托单位 - 全宽 (保证长客户名绝不截断) -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label required">
                <span>委托单位 (客户)</span>
                <a-tag color="orange" :bordered="false" style="font-size: 10px; padding: 0 4px; line-height: 16px; margin: 0;">账期: 30天</a-tag>
              </div>
              <a-select 
                v-model:value="form.customerId" 
                size="small"
                show-search 
                :options="customerOptions" 
                placeholder="请选择委托客户"
                :disabled="ticketData.isLocked"
                @change="handleCustomerChange">
              </a-select>
            </div>

            <!-- 联系人 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>单位联系人</span>
              </div>
              <a-select 
                v-model:value="form.contactPerson" 
                size="small"
                allow-clear 
                :options="contactOptions" 
                placeholder="选择联系人"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 应结日期 - 半宽 (1列，与联系人严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>应结日期</span>
                <a-tooltip title="按委托单位账期与业务日期联动试算">
                  <iconify-icon icon="ant-design:clock-circle-outlined" style="color: #9ca3af; font-size: 11px;"></iconify-icon>
                </a-tooltip>
              </div>
              <div class="readonly-box" style="color: #b45309;">
                <span>{{ form.settlementDate }}</span>
                <iconify-icon icon="ant-design:schedule-outlined" style="color: #94a3b8; font-size: 12px;"></iconify-icon>
              </div>
            </div>

            <!-- 销售负责人 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label required">
                <span>销售负责人</span>
              </div>
              <a-select 
                v-model:value="form.salesPerson" 
                size="small"
                :options="salesPersonOptions" 
                :disabled="ticketData.isLocked"
                @change="handleSalesChange">
              </a-select>
            </div>

            <!-- 操作人员 - 半宽 (1列，与销售负责人严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>操作人员</span>
              </div>
              <a-select 
                v-model:value="form.operator" 
                size="small"
                allow-clear 
                :options="operatorOptions" 
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 动态追加岗位 - 全宽容器 -->
            <div v-if="form.additionalRoles.length > 0 || !ticketData.isLocked" class="biz-form-item grid-col-2" style="background: #f9fafb; border: 1px solid #f3f4f6; border-radius: 4px; padding: 6px 8px; margin-top: 2px;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 2px;">
                <span style="font-size: 10px; font-weight: 600; color: #475569;">其他协作干系人:</span>
                <a-button type="link" size="small" style="padding: 0; height: auto; font-size: 10px;" :disabled="ticketData.isLocked" @click="openAddStakeholderModal">
                  + 追加岗位
                </a-button>
              </div>

              <div v-for="(item, idx) in form.additionalRoles" :key="idx" class="stakeholder-grid-row">
                <span class="stakeholder-tag-lbl">{{ item.roleName }}:</span>
                <a-select 
                  v-model:value="item.staffName" 
                  size="small"
                  :options="staffOptions" 
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')">
                </a-select>
                <a-button type="text" size="small" danger style="padding: 0 4px;" :disabled="ticketData.isLocked" @click="removeRole(idx)">
                  <iconify-icon icon="ant-design:close-outlined"></iconify-icon>
                </a-button>
              </div>
            </div>
          </div>

          <!-- 模块 3: 航程与物流路径 (Voyage & Routing) -->
          <div class="form-section-divider">
            <div class="form-section-title">航程与物流路径</div>
            <span class="form-section-sub">船期港口与节点</span>
          </div>

          <div class="biz-form-grid">
            <!-- 船公司 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>船公司 (Carrier)</span>
              </div>
              <a-select 
                v-model:value="form.carrier" 
                size="small"
                allow-clear 
                show-search 
                :options="carrierOptions" 
                placeholder="船公司代码/简称"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 业务发生日 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>业务日期</span>
              </div>
              <a-date-picker 
                v-model:value="form.bizDate" 
                size="small"
                value-format="YYYY-MM-DD" 
                placeholder="业务发生日" 
                style="width: 100%;"
                :disabled="ticketData.isLocked"
                @change="handleBizDateChange">
              </a-date-picker>
            </div>

            <!-- 船名 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>船名 (Vessel)</span>
                <span class="biz-label-hint">限64字</span>
              </div>
              <a-input 
                v-model:value="form.vesselName" 
                size="small"
                placeholder="船名 (Vessel)" 
                :maxlength="64"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-input>
            </div>

            <!-- 航次 - 半宽 (1列，与船名严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>航次 (Voyage)</span>
                <span class="biz-label-hint">限64字</span>
              </div>
              <a-input 
                v-model:value="form.voyage" 
                size="small"
                placeholder="航次 (Voyage)" 
                :maxlength="64"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-input>
            </div>

            <!-- 起运港 (POL) - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>起运港 (POL)</span>
              </div>
              <a-select 
                v-model:value="form.pol" 
                size="small"
                show-search 
                :options="portOptions" 
                placeholder="起运港代码/港口"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 目的港 (POD) - 半宽 (1列，与起运港严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>目的港 (POD)</span>
              </div>
              <a-select 
                v-model:value="form.pod" 
                size="small"
                show-search 
                :options="portOptions" 
                placeholder="目的港代码/港口"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>
          </div>

          <!-- 模块 4: 货物规格与包装 (Cargo & Packaging) -->
          <div class="form-section-divider">
            <div class="form-section-title">货物规格与包装</div>
            <span class="form-section-sub">品名件毛体计量</span>
          </div>

          <div class="biz-form-grid">
            <!-- 品名 - 全宽 (商品档案多选) -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label">
                <span>品名 (Commodities)</span>
                <span class="biz-label-hint">商品档案多选</span>
              </div>
              <a-select 
                v-model:value="form.commodities" 
                size="small"
                mode="multiple" 
                :options="commodityOptions" 
                placeholder="选择关联商品档案"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 件数 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>件数 (Pieces)</span>
              </div>
              <a-input-number 
                v-model:value="form.pieces" 
                size="small"
                :min="0" 
                :precision="0" 
                placeholder="数量" 
                style="width: 100%;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-input-number>
            </div>

            <!-- 包装字典 - 半宽 (1列，与件数严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>包装 (Package)</span>
              </div>
              <a-select 
                v-model:value="form.packageType" 
                size="small"
                :options="packageOptions" 
                placeholder="包装字典" 
                style="width: 100%;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-select>
            </div>

            <!-- 毛重(KGS) - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>毛重 (Weight)</span>
              </div>
              <a-input-number 
                v-model:value="form.weight" 
                size="small"
                :min="0" 
                :precision="2" 
                addon-after="KGS" 
                placeholder="毛重" 
                style="width: 100%;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-input-number>
            </div>

            <!-- 尺码(CBM 体积) - 半宽 (1列，与毛重严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>尺码 (Volume 体积)</span>
                <span class="biz-label-hint">最多4位</span>
              </div>
              <a-input-number 
                v-model:value="form.volume" 
                size="small"
                :min="0" 
                :precision="4" 
                addon-after="CBM" 
                placeholder="体积" 
                style="width: 100%;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-input-number>
            </div>

            <!-- 业务备注 - 全宽 -->
            <div class="biz-form-item grid-col-2" style="margin-top: 2px;">
              <div class="biz-form-label">
                <span>业务备注 (最多1024字符)</span>
              </div>
              <a-textarea 
                v-model:value="form.remark" 
                size="small"
                :rows="2" 
                :maxlength="1024" 
                placeholder="录入对外业务备注信息..." 
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-textarea>
            </div>
          </div>

        </div>
      </div>

      <!-- 右侧费用双轨工作区 (右主操作区) -->
      <div class="right-fee-panel">

        <!-- 费用全局顶层工具栏 (选择汇总、合并更改单、结算申请、整票提交) -->
        <div class="fee-global-toolbar">
          <div class="fee-toolbar-left">
            <a-tag :color="selectedFeeCount > 0 ? 'blue' : 'default'">
              已选 {{ selectedFeeCount }} 项 
              <span v-if="selectedFeeCount > 0">(收 {{ selectedRecKeys.length }} / 付 {{ selectedPayKeys.length }})</span>
            </a-tag>
            <a-button v-if="selectedFeeCount > 0" type="link" size="small" @click="clearFeeSelection">
              清除选择
            </a-button>

            <!-- 合并更改单开关 -->
            <a-checkbox 
              v-model:checked="isMergeChangeOrder" 
              @change="handleToggleMergeChangeOrder">
              <strong>合并更改单</strong>
            </a-checkbox>
            <a-tooltip title="勾选后将自动合并当前票原费用与所有有效更改单调账，进入只读查看全貌模式">
              <iconify-icon icon="ant-design:question-circle-outlined" style="color: #9ca3af;"></iconify-icon>
            </a-tooltip>

            <!-- 利润预警状态标签 -->
            <a-badge status="success" text="利润正常 (预警线 > 0.00)" />
          </div>

          <div class="fee-toolbar-right">
            <!-- 结算申请下拉菜单 (未选择费用时置灰禁用，选择后激活) -->
            <a-dropdown :disabled="selectedFeeCount === 0">
              <template #overlay>
                <a-menu @click="handleSettlementAction">
                  <a-menu-item key="invoice">
                    <iconify-icon icon="ant-design:file-protect-outlined"></iconify-icon> 创建开票申请 (需应收审核通过)
                  </a-menu-item>
                  <a-menu-item key="payment">
                    <iconify-icon icon="ant-design:pay-circle-outlined"></iconify-icon> 创建付费申请 (需应付审核通过)
                  </a-menu-item>
                  <a-menu-divider></a-menu-divider>
                  <a-menu-item key="batch_target">
                    <iconify-icon icon="ant-design:user-switch-outlined"></iconify-icon> 批量修改结算对象
                  </a-menu-item>
                  <a-menu-item key="batch_tax">
                    <iconify-icon icon="ant-design:percentage-outlined"></iconify-icon> 批量修改税率
                  </a-menu-item>
                </a-menu>
              </template>
              <a-button size="small" :disabled="selectedFeeCount === 0">
                结算申请 <iconify-icon icon="ant-design:down-outlined"></iconify-icon>
              </a-button>
            </a-dropdown>

            <!-- 整票提交按钮 (按是否选中调整范围，点击弹出范围确认) -->
            <a-button 
              type="primary" 
              ghost 
              size="small" 
              :disabled="ticketData.isLocked || isMergeChangeOrder"
              @click="openSubmitScopeModal">
              <iconify-icon icon="ant-design:send-outlined"></iconify-icon> 
              {{ selectedFeeCount > 0 ? '提交所选 (' + selectedFeeCount + ')' : '整票提交审核' }}
            </a-button>

            <!-- 更多操作 -->
            <a-dropdown size="small">
              <template #overlay>
                <a-menu>
                  <a-menu-item key="print" :disabled="isMergeChangeOrder" @click="handlePrintStatement">
                    <iconify-icon icon="ant-design:printer-outlined"></iconify-icon> 打印对账单 (合并态禁用)
                  </a-menu-item>
                  <a-menu-item key="export" @click="handleExportFees">
                    <iconify-icon icon="ant-design:file-excel-outlined"></iconify-icon> 导出费用 Excel
                  </a-menu-item>
                  <a-menu-item key="currency" @click="handleCurrencyExchange">
                    <iconify-icon icon="ant-design:swap-outlined"></iconify-icon> 汇率重新折算
                  </a-menu-item>
                </a-menu>
              </template>
              <a-button size="small">
                更多 <iconify-icon icon="ant-design:down-outlined"></iconify-icon>
              </a-button>
            </a-dropdown>
          </div>
        </div>

        <!-- 合并查看·只读模式提示横幅 (若激活) -->
        <div v-if="isMergeChangeOrder" class="merge-readonly-banner">
          <div class="merge-banner-text">
            <iconify-icon icon="ant-design:info-circle-filled" style="font-size: 14px;"></iconify-icon>
            <span>
              当前处于<strong>「合并更改单·只读查看」</strong>模式，已汇总原票与更改单费用。明细表增加「来源」列，费用编辑、保存与提交已锁定只读。
            </span>
          </div>
          <a-button type="link" size="small" style="padding: 0; color: #d46b08; font-weight: 600;" @click="exitMergeMode">
            关闭合并恢复编辑
          </a-button>
        </div>

        <!-- 上下费用双表滚动区域 (含可拖拽分隔条) -->
        <div class="fee-tables-container" ref="feeTablesContainer">

          <!-- 上表：应收费用 (Receivables) -->
          <div class="fee-table-block" :style="{ height: splitRatio + '%' }">
            <div class="fee-table-header">
              <div class="fee-table-title">
                <iconify-icon icon="ant-design:arrow-down-outlined" style="color: #1677ff;"></iconify-icon>
                <span>应收明细 (Receivables)</span>
                <a-badge :count="receivableList.length" :overflow-count="99" :number-style="{ backgroundColor: '#e6f4ff', color: '#1677ff' }"></a-badge>
                <span style="font-weight: 400; color: #64748b; font-size: 11px;">合计: RMB {{ receivableTotalRmb }}</span>
              </div>

              <div class="fee-table-actions">
                <a-button 
                  size="small" 
                  type="dashed" 
                  :disabled="ticketData.isLocked || isMergeChangeOrder"
                  @click="addReceivableRow">
                  <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 新增应收
                </a-button>

                <a-popconfirm 
                  title="确认批量删除已选中的应收费用？已入库费用将调用后端撤销。" 
                  :disabled="selectedRecKeys.length === 0"
                  @confirm="batchDeleteReceivables">
                  <a-button size="small" danger :disabled="selectedRecKeys.length === 0 || ticketData.isLocked || isMergeChangeOrder">
                    <iconify-icon icon="ant-design:delete-outlined"></iconify-icon> 批量删除 ({{ selectedRecKeys.length }})
                  </a-button>
                </a-popconfirm>

                <a-button size="small" :disabled="ticketData.isLocked || isMergeChangeOrder" @click="openAiOcrModal('rec')">
                  <iconify-icon icon="ant-design:scan-outlined"></iconify-icon> AI 识别
                </a-button>

                <!-- 应收费用独立保存按钮 (明确保存边界与未存计数) -->
                <a-button 
                  type="primary" 
                  size="small" 
                  :loading="isSavingRec" 
                  :disabled="ticketData.isLocked || isMergeChangeOrder"
                  @click="saveReceivableFees">
                  <iconify-icon icon="ant-design:save-outlined"></iconify-icon> 
                  保存应收 {{ dirtyStates.recCount > 0 ? '(' + dirtyStates.recCount + '未存*)' : '' }}
                </a-button>
              </div>
            </div>

            <!-- 应收表格 (支持横纵滚动、行内编辑) -->
            <div class="fee-table-scroll">
              <table style="width: 100%; min-width: 1300px; border-collapse: collapse; font-size: 11px;">
                <thead>
                  <tr style="background: #fafafa; border-bottom: 1px solid #e8e8e8; color: #475569; text-align: left; height: 28px;">
                    <th style="width: 36px; text-align: center;">
                      <a-checkbox 
                        :checked="isAllRecSelected" 
                        :indeterminate="isPartRecSelected"
                        @change="toggleSelectAllRec"></a-checkbox>
                    </th>
                    <th style="width: 36px; text-align: center;">#</th>
                    <th v-if="isMergeChangeOrder" style="width: 110px;">来源单据</th>
                    <th style="width: 120px;">费用名称*</th>
                    <th style="width: 90px;">行业类别</th>
                    <th style="width: 160px;">结算对象*</th>
                    <th style="width: 70px;">币别</th>
                    <th style="width: 70px; text-align: right;">汇率</th>
                    <th style="width: 60px;">单位</th>
                    <th style="width: 80px; text-align: right;">含税单价</th>
                    <th style="width: 70px; text-align: right;">数量</th>
                    <th style="width: 90px; text-align: right;">含税金额</th>
                    <th style="width: 70px;">税率%</th>
                    <th style="width: 90px; text-align: right;">不含税金额</th>
                    <th style="width: 80px; text-align: center;">费用状态</th>
                    <th style="width: 80px; text-align: center;">操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="(row, idx) in receivableList" 
                    :key="row.id" 
                    :style="{ background: row.isDraft ? '#fffbe6' : (idx % 2 === 1 ? '#fcfcfc' : '#ffffff'), borderBottom: '1px solid #f0f0f0', height: '32px' }">
                    <td style="text-align: center;">
                      <a-checkbox 
                        :checked="selectedRecKeys.includes(row.id)" 
                        @change="toggleSelectRec(row.id)"></a-checkbox>
                    </td>
                    <td style="text-align: center; color: #94a3b8;">
                      <span v-if="row.isDraft" style="color: #fa8c16; font-weight: 700;">*</span>
                      {{ idx + 1 }}
                    </td>

                    <!-- 合并来源列 -->
                    <td v-if="isMergeChangeOrder">
                      <a-tag :color="row.source === '原票' ? 'blue' : 'orange'" style="font-size: 10px; margin: 0;">
                        {{ row.source }}
                      </a-tag>
                    </td>

                    <!-- 费用名称 (可直接编辑) -->
                    <td>
                      <input 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean" 
                        v-model="row.feeName" 
                        @change="markRecDirty(row)" />
                      <span v-else>{{ row.feeName }}</span>
                    </td>

                    <!-- 行业类别 -->
                    <td>
                      <span style="color: #64748b;">{{ row.category || '海运' }}</span>
                    </td>

                    <!-- 结算对象 -->
                    <td>
                      <input 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean" 
                        v-model="row.settlementTarget" 
                        @change="markRecDirty(row)" />
                      <span v-else>{{ row.settlementTarget }}</span>
                    </td>

                    <!-- 币别 -->
                    <td>
                      <select 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean" 
                        v-model="row.currency" 
                        @change="recalcRow(row, 'rec')">
                        <option value="RMB">RMB</option>
                        <option value="USD">USD</option>
                        <option value="EUR">EUR</option>
                        <option value="HKD">HKD</option>
                      </select>
                      <span v-else><strong>{{ row.currency }}</strong></span>
                    </td>

                    <!-- 汇率 -->
                    <td style="text-align: right;">
                      <input 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean cell-num-right" 
                        type="number" 
                        step="0.0001" 
                        v-model.number="row.exchangeRate" 
                        @change="recalcRow(row, 'rec')" />
                      <span v-else>{{ row.exchangeRate.toFixed(4) }}</span>
                    </td>

                    <!-- 单位 -->
                    <td>
                      <span style="color: #64748b;">{{ row.unit || '票' }}</span>
                    </td>

                    <!-- 含税单价 -->
                    <td style="text-align: right;">
                      <input 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean cell-num-right" 
                        type="number" 
                        step="0.01" 
                        v-model.number="row.unitPrice" 
                        @input="recalcRow(row, 'rec')" />
                      <span v-else>{{ row.unitPrice.toFixed(2) }}</span>
                    </td>

                    <!-- 数量 -->
                    <td style="text-align: right;">
                      <input 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean cell-num-right" 
                        type="number" 
                        step="1" 
                        v-model.number="row.quantity" 
                        @input="recalcRow(row, 'rec')" />
                      <span v-else>{{ row.quantity }}</span>
                    </td>

                    <!-- 含税金额 -->
                    <td style="text-align: right; font-weight: 600; color: #111827;">
                      {{ row.amount.toFixed(2) }}
                    </td>

                    <!-- 税率% -->
                    <td>
                      <select 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean" 
                        v-model.number="row.taxRate" 
                        @change="recalcRow(row, 'rec')">
                        <option :value="0">0%</option>
                        <option :value="6">6%</option>
                        <option :value="9">9%</option>
                        <option :value="13">13%</option>
                      </select>
                      <span v-else>{{ row.taxRate }}%</span>
                    </td>

                    <!-- 不含税金额 -->
                    <td style="text-align: right; color: #64748b;">
                      {{ row.taxExcludedAmount.toFixed(2) }}
                    </td>

                    <!-- 费用状态 -->
                    <td style="text-align: center;">
                      <a-tag :color="getStatusTagColor(row.status)" style="font-size: 10px; margin: 0;">
                        {{ row.status }}
                      </a-tag>
                    </td>

                    <!-- 行操作 -->
                    <td style="text-align: center;">
                      <template v-if="row.isDraft">
                        <a-button type="link" size="small" danger style="padding: 0; font-size: 11px;" @click="removeDraftRow('rec', row.id)">
                          移除草稿
                        </a-button>
                      </template>
                      <template v-else-if="!isMergeChangeOrder && !ticketData.isLocked">
                        <a-dropdown size="small">
                          <a-button type="text" size="small" style="padding: 0 4px;">···</a-button>
                          <template #overlay>
                            <a-menu>
                              <a-menu-item key="apply_edit" @click="applyFeeChange(row)">
                                申请修改
                              </a-menu-item>
                              <a-menu-item key="apply_del" danger @click="applyFeeDelete(row)">
                                申请删除
                              </a-menu-item>
                            </a-menu>
                          </template>
                        </a-dropdown>
                      </template>
                      <template v-else>
                        <span style="color: #cbd5e1;">-</span>
                      </template>
                    </td>
                  </tr>

                  <!-- 空态提示 -->
                  <tr v-if="receivableList.length === 0">
                    <td :colspan="isMergeChangeOrder ? 16 : 15" style="text-align: center; padding: 24px 0; color: #94a3b8;">
                      暂无应收费用记录，可点击上方「新增应收」添加
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- 高度可拖拽分隔条 (Splitter Bar) -->
          <div 
            class="fee-splitter-bar" 
            :class="{ 'is-dragging': isDraggingSplitter }"
            @mousedown="startDragSplitter">
            <div class="splitter-handle"></div>
            <div class="splitter-quick-btns">
              <button class="splitter-quick-btn" title="5:5 均分" @click.stop="splitRatio = 50">5:5</button>
              <button class="splitter-quick-btn" title="7:3 重应收" @click.stop="splitRatio = 70">7:3</button>
              <button class="splitter-quick-btn" title="3:7 重应付" @click.stop="splitRatio = 30">3:7</button>
            </div>
          </div>

          <!-- 下表：应付费用 (Payables) -->
          <div class="fee-table-block" :style="{ height: (100 - splitRatio) + '%' }">
            <div class="fee-table-header">
              <div class="fee-table-title">
                <iconify-icon icon="ant-design:arrow-up-outlined" style="color: #fa8c16;"></iconify-icon>
                <span>应付明细 (Payables)</span>
                <a-badge :count="payableList.length" :overflow-count="99" :number-style="{ backgroundColor: '#fff7e6', color: '#fa8c16' }"></a-badge>
                <span style="font-weight: 400; color: #64748b; font-size: 11px;">合计: RMB {{ payableTotalRmb }}</span>
              </div>

              <div class="fee-table-actions">
                <a-button 
                  size="small" 
                  type="dashed" 
                  :disabled="ticketData.isLocked || isMergeChangeOrder"
                  @click="addPayableRow">
                  <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 新增应付
                </a-button>

                <a-popconfirm 
                  title="确认批量删除已选中的应付费用？已入库费用将调用后端撤销。" 
                  :disabled="selectedPayKeys.length === 0"
                  @confirm="batchDeletePayables">
                  <a-button size="small" danger :disabled="selectedPayKeys.length === 0 || ticketData.isLocked || isMergeChangeOrder">
                    <iconify-icon icon="ant-design:delete-outlined"></iconify-icon> 批量删除 ({{ selectedPayKeys.length }})
                  </a-button>
                </a-popconfirm>

                <a-button size="small" :disabled="ticketData.isLocked || isMergeChangeOrder" @click="openAiOcrModal('pay')">
                  <iconify-icon icon="ant-design:scan-outlined"></iconify-icon> AI 识别
                </a-button>

                <!-- 应付费用独立保存按钮 (明确保存边界与未存计数) -->
                <a-button 
                  type="primary" 
                  size="small" 
                  :loading="isSavingPay" 
                  :disabled="ticketData.isLocked || isMergeChangeOrder"
                  @click="savePayableFees">
                  <iconify-icon icon="ant-design:save-outlined"></iconify-icon> 
                  保存应付 {{ dirtyStates.payCount > 0 ? '(' + dirtyStates.payCount + '未存*)' : '' }}
                </a-button>
              </div>
            </div>

            <!-- 应付表格 (支持横纵滚动、行内编辑) -->
            <div class="fee-table-scroll">
              <table style="width: 100%; min-width: 1300px; border-collapse: collapse; font-size: 11px;">
                <thead>
                  <tr style="background: #fafafa; border-bottom: 1px solid #e8e8e8; color: #475569; text-align: left; height: 28px;">
                    <th style="width: 36px; text-align: center;">
                      <a-checkbox 
                        :checked="isAllPaySelected" 
                        :indeterminate="isPartPaySelected"
                        @change="toggleSelectAllPay"></a-checkbox>
                    </th>
                    <th style="width: 36px; text-align: center;">#</th>
                    <th v-if="isMergeChangeOrder" style="width: 110px;">来源单据</th>
                    <th style="width: 120px;">费用名称*</th>
                    <th style="width: 90px;">行业类别</th>
                    <th style="width: 160px;">结算对象*</th>
                    <th style="width: 70px;">币别</th>
                    <th style="width: 70px; text-align: right;">汇率</th>
                    <th style="width: 60px;">单位</th>
                    <th style="width: 80px; text-align: right;">含税单价</th>
                    <th style="width: 70px; text-align: right;">数量</th>
                    <th style="width: 90px; text-align: right;">含税金额</th>
                    <th style="width: 70px;">税率%</th>
                    <th style="width: 90px; text-align: right;">不含税金额</th>
                    <th style="width: 80px; text-align: center;">费用状态</th>
                    <th style="width: 80px; text-align: center;">操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="(row, idx) in payableList" 
                    :key="row.id" 
                    :style="{ background: row.isDraft ? '#fffbe6' : (idx % 2 === 1 ? '#fcfcfc' : '#ffffff'), borderBottom: '1px solid #f0f0f0', height: '32px' }">
                    <td style="text-align: center;">
                      <a-checkbox 
                        :checked="selectedPayKeys.includes(row.id)" 
                        @change="toggleSelectPay(row.id)"></a-checkbox>
                    </td>
                    <td style="text-align: center; color: #94a3b8;">
                      <span v-if="row.isDraft" style="color: #fa8c16; font-weight: 700;">*</span>
                      {{ idx + 1 }}
                    </td>

                    <!-- 合并来源列 -->
                    <td v-if="isMergeChangeOrder">
                      <a-tag :color="row.source === '原票' ? 'blue' : 'orange'" style="font-size: 10px; margin: 0;">
                        {{ row.source }}
                      </a-tag>
                    </td>

                    <!-- 费用名称 -->
                    <td>
                      <input 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean" 
                        v-model="row.feeName" 
                        @change="markPayDirty(row)" />
                      <span v-else>{{ row.feeName }}</span>
                    </td>

                    <!-- 行业类别 -->
                    <td>
                      <span style="color: #64748b;">{{ row.category || '海运' }}</span>
                    </td>

                    <!-- 结算对象 -->
                    <td>
                      <input 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean" 
                        v-model="row.settlementTarget" 
                        @change="markPayDirty(row)" />
                      <span v-else>{{ row.settlementTarget }}</span>
                    </td>

                    <!-- 币别 -->
                    <td>
                      <select 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean" 
                        v-model="row.currency" 
                        @change="recalcRow(row, 'pay')">
                        <option value="RMB">RMB</option>
                        <option value="USD">USD</option>
                        <option value="EUR">EUR</option>
                        <option value="HKD">HKD</option>
                      </select>
                      <span v-else><strong>{{ row.currency }}</strong></span>
                    </td>

                    <!-- 汇率 -->
                    <td style="text-align: right;">
                      <input 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean cell-num-right" 
                        type="number" 
                        step="0.0001" 
                        v-model.number="row.exchangeRate" 
                        @change="recalcRow(row, 'pay')" />
                      <span v-else>{{ row.exchangeRate.toFixed(4) }}</span>
                    </td>

                    <!-- 单位 -->
                    <td>
                      <span style="color: #64748b;">{{ row.unit || '票' }}</span>
                    </td>

                    <!-- 含税单价 -->
                    <td style="text-align: right;">
                      <input 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean cell-num-right" 
                        type="number" 
                        step="0.01" 
                        v-model.number="row.unitPrice" 
                        @input="recalcRow(row, 'pay')" />
                      <span v-else>{{ row.unitPrice.toFixed(2) }}</span>
                    </td>

                    <!-- 数量 -->
                    <td style="text-align: right;">
                      <input 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean cell-num-right" 
                        type="number" 
                        step="1" 
                        v-model.number="row.quantity" 
                        @input="recalcRow(row, 'pay')" />
                      <span v-else>{{ row.quantity }}</span>
                    </td>

                    <!-- 含税金额 -->
                    <td style="text-align: right; font-weight: 600; color: #111827;">
                      {{ row.amount.toFixed(2) }}
                    </td>

                    <!-- 税率% -->
                    <td>
                      <select 
                        v-if="!isMergeChangeOrder && !ticketData.isLocked" 
                        class="cell-input-clean" 
                        v-model.number="row.taxRate" 
                        @change="recalcRow(row, 'pay')">
                        <option :value="0">0%</option>
                        <option :value="6">6%</option>
                        <option :value="9">9%</option>
                        <option :value="13">13%</option>
                      </select>
                      <span v-else>{{ row.taxRate }}%</span>
                    </td>

                    <!-- 不含税金额 -->
                    <td style="text-align: right; color: #64748b;">
                      {{ row.taxExcludedAmount.toFixed(2) }}
                    </td>

                    <!-- 费用状态 -->
                    <td style="text-align: center;">
                      <a-tag :color="getStatusTagColor(row.status)" style="font-size: 10px; margin: 0;">
                        {{ row.status }}
                      </a-tag>
                    </td>

                    <!-- 行操作 -->
                    <td style="text-align: center;">
                      <template v-if="row.isDraft">
                        <a-button type="link" size="small" danger style="padding: 0; font-size: 11px;" @click="removeDraftRow('pay', row.id)">
                          移除草稿
                        </a-button>
                      </template>
                      <template v-else-if="!isMergeChangeOrder && !ticketData.isLocked">
                        <a-dropdown size="small">
                          <a-button type="text" size="small" style="padding: 0 4px;">···</a-button>
                          <template #overlay>
                            <a-menu>
                              <a-menu-item key="apply_edit" @click="applyFeeChange(row)">
                                申请修改
                              </a-menu-item>
                              <a-menu-item key="apply_del" danger @click="applyFeeDelete(row)">
                                申请删除
                              </a-menu-item>
                            </a-menu>
                          </template>
                        </a-dropdown>
                      </template>
                      <template v-else>
                        <span style="color: #cbd5e1;">-</span>
                      </template>
                    </td>
                  </tr>

                  <!-- 空态提示 -->
                  <tr v-if="payableList.length === 0">
                    <td :colspan="isMergeChangeOrder ? 16 : 15" style="text-align: center; padding: 24px 0; color: #94a3b8;">
                      暂无应付费用记录，可点击上方「新增应付」添加
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>

        <!-- 固定吸底财务合计栏 (分币别收付/利润、本位币合计利润与利润率) -->
        <div class="fixed-fee-summary-bar">
          <!-- 左侧：分币别原币收付统计 -->
          <div class="summary-left-currencies">
            <div class="summary-item">
              <span style="color: #64748b;">应收原币:</span>
              <strong>RMB {{ receivableTotalRmb }}</strong>
            </div>
            <div class="summary-item">
              <span style="color: #64748b;">应付原币:</span>
              <strong>RMB {{ payableTotalRmb }}</strong>
            </div>
            <div class="summary-item">
              <span style="color: #64748b;">原币差额:</span>
              <strong style="color: #1677ff;">RMB {{ netProfitRmb }}</strong>
            </div>
          </div>

          <!-- 右侧：本位币折合统计与利润率 (实测样本：收17.80、付7.80、毛利10.00、利润率128.2%) -->
          <div class="summary-right-totals">
            <div class="summary-item">
              <span>应收折合:</span>
              <strong>RMB {{ receivableTotalRmb }}</strong>
            </div>
            <div class="summary-item">
              <span>应付折合:</span>
              <strong>RMB {{ payableTotalRmb }}</strong>
            </div>
            <div class="summary-item">
              <span>毛利润 (折合):</span>
              <span class="profit-val-highlight" :style="{ color: netProfitNumber >= 0 ? '#52c41a' : '#ff4d4f' }">
                RMB {{ netProfitRmb }}
              </span>
            </div>
            <div class="summary-item">
              <span>利润率:</span>
              <span class="profit-val-highlight" style="color: #1677ff;">
                {{ profitMarginText }}
              </span>
              <a-tooltip title="利润率计算公式：毛利润 / 应付折合 (10.00 / 7.80 = 128.2%)，与当前系统生产口径100%一致">
                <iconify-icon icon="ant-design:question-circle-outlined" style="color: #9ca3af; font-size: 11px;"></iconify-icon>
              </a-tooltip>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- ====================================================================
         TAB 2: 更改单页签
         分状态演示：未锁定原费用拦截态 (截图04) vs 已锁原费录入态
         ==================================================================== -->
    <div v-show="activeTabKey === 'changeOrder'" class="change-order-view">

      <!-- 分支 1: 原票费用未锁定拦截态 (100% 还原系统截图 04) -->
      <div v-if="!ticketData.isOriginalFeeLocked" class="co-prerequisite-card">
        <iconify-icon icon="ant-design:exclamation-circle-filled" style="font-size: 48px; color: #faad14;"></iconify-icon>
        <div style="font-size: 16px; font-weight: 600; color: #111827;">
          主单费用未锁定，不能添加更改单
        </div>
        <div style="font-size: 13px; color: #4b5563; max-width: 540px; line-height: 1.6;">
          更改单是针对<strong>已完成费用锁账的业务</strong>进行后续费用追溯、补充调账的正式单据。<br>
          当前主单费用尚未执行锁费，如需调整或录入费用，请直接在「应收应付」页签内增删改。若原票已完成核算，请先执行原票费用锁账。
        </div>

        <div style="display: flex; gap: 12px; margin-top: 12px;">
          <a-button type="primary" @click="activeTabKey = 'fee'">
            <iconify-icon icon="ant-design:arrow-left-outlined"></iconify-icon> 前往「应收应付」直接调整
          </a-button>
          <a-button @click="mockLockOriginalFee">
            <iconify-icon icon="ant-design:lock-outlined"></iconify-icon> 原型模拟：立即锁账原费用
          </a-button>
        </div>
      </div>

      <!-- 分支 2: 原票费用已锁定，正常更改单列表与调账录入 -->
      <div v-else style="background: #ffffff; border-radius: 6px; border: 1px solid #e5e7eb; padding: 16px; flex: 1; display: flex; flex-direction: column;">
        <!-- 更改单顶栏 -->
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; padding-bottom: 12px; border-bottom: 1px solid #f0f0f0;">
          <div>
            <div style="font-size: 14px; font-weight: 600; color: #111827;">
              更改单管理 (Change Orders)
            </div>
            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">
              基准原票费用已封存锁定：应收 RMB 17.80 / 应付 RMB 7.80 / 毛利 RMB 10.00
            </div>
          </div>

          <div style="display: flex; gap: 8px;">
            <a-button type="primary" size="small" @click="openCreateChangeOrderModal">
              <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 新建更改单
            </a-button>
            <a-button size="small" @click="mockUnlockOriginalFee">
              恢复未锁拦截态
            </a-button>
          </div>
        </div>

        <!-- 更改单列表表格 -->
        <a-table 
          size="small" 
          :data-source="changeOrderList" 
          :columns="changeOrderColumns" 
          :pagination="false" 
          row-key="id">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'status'">
              <a-tag :color="record.status === '已生效' ? 'green' : 'orange'">
                {{ record.status }}
              </a-tag>
            </template>
            <template v-if="column.key === 'action'">
              <a-space size="small">
                <a-button type="link" size="small" @click="viewChangeOrderDetail(record)">查看调账</a-button>
                <a-button type="link" size="small" v-if="record.status !== '已生效'">提交审批</a-button>
              </a-space>
            </template>
          </template>
        </a-table>
      </div>

    </div>

    <!-- ====================================================================
         TAB 3: 附件页签
         分状态演示：暂无附件类型配置空态 (截图05) vs 标准附件分类管理
         ==================================================================== -->
    <div v-show="activeTabKey === 'attachment'" class="attachment-view">

      <!-- 分支 1: 暂无附件类型配置 (100% 还原系统截图 05) -->
      <div v-if="attachmentScenario === 'empty_no_config'" class="attachment-card" style="align-items: center; justify-content: center; text-align: center;">
        <a-empty description="暂无附件类型配置">
          <template #image>
            <iconify-icon icon="ant-design:inbox-outlined" style="font-size: 64px; color: #cbd5e1;"></iconify-icon>
          </template>
          <div style="color: #64748b; font-size: 12px; margin-bottom: 16px;">
            当前业务类型尚未在系统档案中配置预设附件分类，您可以点击下方按钮添加自定义分类或上传临时文件。
          </div>
          <a-space>
            <a-button type="primary" @click="openAddOtherAttachmentType">
              <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 添加其他类型
            </a-button>
            <a-button @click="attachmentScenario = 'configured'">
              切换为标准分类演示
            </a-button>
          </a-space>
        </a-empty>
      </div>

      <!-- 分支 2: 标准附件分类管理态 -->
      <div v-else class="attachment-card">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #f0f0f0;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 13px; font-weight: 600;">附件清单 (Attachments)</span>
            <a-radio-group v-model:value="attachmentCategoryFilter" size="small">
              <a-radio-button value="all">全部 ({{ attachmentList.length }})</a-radio-button>
              <a-radio-button value="bl">提单/运单 (1)</a-radio-button>
              <a-radio-button value="customs">报关单 (1)</a-radio-button>
              <a-radio-button value="invoice">费用发票 (1)</a-radio-button>
            </a-radio-group>
          </div>

          <a-space>
            <a-upload :show-upload-list="false" :before-upload="handleFileUpload">
              <a-button type="primary" size="small" :disabled="ticketData.isLocked">
                <iconify-icon icon="ant-design:upload-outlined"></iconify-icon> 上传附件 (限10MB)
              </a-button>
            </a-upload>
            <a-button size="small" @click="attachmentScenario = 'empty_no_config'">
              切换为无配置空态
            </a-button>
          </a-space>
        </div>

        <a-table 
          size="small" 
          :data-source="filteredAttachments" 
          :columns="attachmentColumns" 
          :pagination="false" 
          row-key="id">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'fileName'">
              <span style="display: flex; align-items: center; gap: 6px;">
                <iconify-icon :icon="getFileIcon(record.fileName)" style="font-size: 16px; color: #1677ff;"></iconify-icon>
                <strong>{{ record.fileName }}</strong>
              </span>
            </template>
            <template v-if="column.key === 'action'">
              <a-space size="small">
                <a-button type="link" size="small" @click="previewAttachment(record)">预览</a-button>
                <a-button type="link" size="small" @click="downloadAttachment(record)">下载</a-button>
                <a-popconfirm title="确认删除此附件记录？" @confirm="deleteAttachment(record.id)">
                  <a-button type="link" size="small" danger :disabled="ticketData.isLocked">删除</a-button>
                </a-popconfirm>
              </a-space>
            </template>
          </template>
        </a-table>
      </div>

    </div>

  </div>

  <!-- ========================================================================
       5. 弹窗与抽屉矩阵 (关联主单、复制业务、整票提交确认、干系人追加、设计规范)
       ======================================================================== -->

  <!-- 弹窗 1: 关联主单选择弹窗 -->
  <a-modal 
    v-model:open="showMasterOrderModal" 
    title="关联海运主单 / 件杂货单" 
    width="780px" 
    @ok="confirmLinkMasterOrder">
    <div style="margin-bottom: 12px; display: flex; gap: 8px;">
      <a-input 
        v-model:value="masterOrderSearchKey" 
        size="small" 
        placeholder="搜索编号 / 主单号 / 客户名称..." 
        style="width: 280px;"></a-input>
      <a-select v-model:value="masterOrderTypeFilter" size="small" style="width: 120px;">
        <option value="all">全部类型</option>
        <option value="海运出口">海运出口</option>
        <option value="海运进口">海运进口</option>
        <option value="件杂货">件杂货</option>
      </a-select>
    </div>

    <a-table 
      size="small" 
      :data-source="masterOrderCandidates" 
      :columns="masterOrderColumns" 
      :pagination="{ pageSize: 5 }" 
      row-key="id"
      :row-selection="{ type: 'radio', selectedRowKeys: selectedMasterOrderKey, onChange: (keys, rows) => { selectedMasterOrderKey = keys; tempSelectedMasterOrder = rows[0]; } }">
    </a-table>

    <div style="margin-top: 10px; font-size: 11px; color: #64748b;">
      💡 提示：同公司与数据权限校验；综合业务每票最多关联 1 票主单，确认后点击「保存业务信息」生效。
    </div>
  </a-modal>

  <!-- 弹窗 2: 复制本票业务弹窗 -->
  <a-modal 
    v-model:open="showCopyModal" 
    title="复制本票业务 (创建新综合业务票)" 
    width="520px" 
    @ok="confirmCopyOrder">
    <div style="display: flex; flex-direction: column; gap: 12px; padding: 6px 0;">
      <div style="font-size: 13px; color: #111827;">
        您即将以 <strong>{{ ticketData.jobNo }}</strong> 为模板创建一票新的综合业务单据：
      </div>
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 10px;">
        <div style="margin-bottom: 6px;">
          <a-checkbox v-model:checked="copyOptions.copyBasic" disabled>
            复制基础业务信息 (客户、组织、港口、品名等)
          </a-checkbox>
        </div>
        <div style="margin-bottom: 6px;">
          <a-checkbox v-model:checked="copyOptions.copyReceivables">
            同时复制应收费用明细 ({{ receivableList.length }} 笔)
          </a-checkbox>
        </div>
        <div style="margin-bottom: 6px;">
          <a-checkbox v-model:checked="copyOptions.copyPayables">
            同时复制应付费用明细 ({{ payableList.length }} 笔)
          </a-checkbox>
        </div>
        <div>
          <a-checkbox v-model:checked="copyOptions.clearBlNo">
            自动清空提单号 (避免新票提单号冲突)
          </a-checkbox>
        </div>
      </div>
      <div style="font-size: 11px; color: #94a3b8;">
        • 复制生成的新单据将自动分配全新委托编号，原单锁账与审批状态不继承。
      </div>
    </div>
  </a-modal>

  <!-- 弹窗 3: 整票提交确认弹窗 (明确提交范围) -->
  <a-modal 
    v-model:open="showSubmitScopeModal" 
    title="提交费用审核确认" 
    width="560px" 
    @ok="confirmFeeSubmit">
    <div style="display: flex; flex-direction: column; gap: 12px;">
      <a-alert 
        :message="selectedFeeCount > 0 ? '已勾选局部费用提交模式' : '整票全额提交审核模式'" 
        :description="selectedFeeCount > 0 ? '当前共勾选 ' + selectedFeeCount + ' 笔费用明细，本次仅将所选费用提交至审核中心，未勾选费用将保留在草稿状态。' : '当前未勾选特定费用，系统将为本票所有处于录入中的费用 (共 ' + (receivableList.length + payableList.length) + ' 笔) 执行批量提交审核。'" 
        type="info" 
        show-icon />

      <div style="background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 4px; padding: 12px; font-size: 12px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <span style="color: #64748b;">提交应收额:</span>
          <strong>RMB {{ receivableTotalRmb }}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <span style="color: #64748b;">提交应付额:</span>
          <strong>RMB {{ payableTotalRmb }}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding-top: 6px; border-top: 1px solid #e5e7eb;">
          <span style="color: #64748b;">预估毛利润:</span>
          <strong style="color: #52c41a;">RMB {{ netProfitRmb }} (利润率 {{ profitMarginText }})</strong>
        </div>
      </div>

      <div style="font-size: 11px; color: #94a3b8;">
        • 提示：提交审核后，对应费用行状态将变更为「待审核」，在审核通过前不可再次直接修改。
      </div>
    </div>
  </a-modal>

  <!-- 弹窗 4: 追加干系人岗位弹窗 -->
  <a-modal 
    v-model:open="showAddStakeholderModal" 
    title="追加干系人岗位" 
    width="420px" 
    @ok="confirmAddStakeholder">
    <div style="display: flex; flex-direction: column; gap: 10px;">
      <div>
        <label style="font-size: 12px; color: #374151;">岗位角色:</label>
        <a-select v-model:value="newStakeholder.roleName" size="small" style="width: 100%; margin-top: 4px;">
          <option value="客服">客服 (Customer Service)</option>
          <option value="单证">单证 (Documentation)</option>
          <option value="调度">调度 (Dispatcher)</option>
          <option value="报关员">报关员 (Customs Broker)</option>
        </a-select>
      </div>

      <div>
        <label style="font-size: 12px; color: #374151;">人员姓名:</label>
        <a-select v-model:value="newStakeholder.staffName" size="small" :options="staffOptions" style="width: 100%; margin-top: 4px;">
        </a-select>
      </div>
    </div>
  </a-modal>

  <!-- 抽屉: 设计交接与交互规范核对抽屉 (100% 对应交接文档各章节) -->
  <a-drawer 
    v-model:open="showSpecDrawer" 
    title="综合业务编辑工作台 · 交互规范与交接核对报告" 
    width="680px" 
    placement="right">
    <div style="font-size: 12px; line-height: 1.6; color: #334155;">
      <a-alert message="100% 对齐《综合业务编辑页 UI／交互设计交接》规范标准" type="success" show-icon style="margin-bottom: 16px;"></a-alert>

      <h4 style="font-size: 14px; font-weight: 700; color: #0f172a; margin: 14px 0 8px 0; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px;">
        一、必须保留的 8 大业务规则核对
      </h4>
      <ol style="padding-left: 20px; margin: 0;">
        <li><strong>保留委托单位与全量必填字段</strong>：委托单位必填、所属公司（销售直属组织）必填、销售必填；完整保留船名航次组合、件毛体单位。</li>
        <li><strong>单号与归属边界清晰</strong>：关联主单最多 1 票，支持海出/海进/件杂货类型过滤与同公司数据隔离校验。</li>
        <li><strong>严守财务语义</strong>：会计日期展示为月份 (2026-11，只读)；应结日期联动试算；尺码明确为体积 (CBM)；利润率计算严谨对齐生产公式 (10.00 / 7.80 = 128.2%)。</li>
        <li><strong>3 大独立保存域</strong>：页面彻底分离「保存业务信息」「保存应收」「保存应付」，杜绝破坏事务的一键合并保存。</li>
        <li><strong>字段屏蔽与锁账白名单</strong>：支持查看脱敏遮罩与锁账限制。</li>
        <li><strong>合并更改单只读闭环</strong>：勾选「合并更改单」后两表重载并展示「来源」列，费用区全部只读，提供退出合并恢复编辑入口。</li>
        <li><strong>整票提交与结算菜单精准联动</strong>：无选中费用时结算菜单各项禁用；整票提交根据是否有勾选自动切换提交范围并弹窗确认。</li>
        <li><strong>高密度行内编辑与人体工学</strong>：支持单价/数量/币别/汇率实时联动运算，上下表具备拖动调节分隔条，吸底常驻财务合计。</li>
      </ol>

      <h4 style="font-size: 14px; font-weight: 700; color: #0f172a; margin: 18px 0 8px 0; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px;">
        二、8 大沙盘测试场景说明
      </h4>
      <p style="color: #64748b;">
        您可以通过页面顶部的「原型审查沙盘」一键切换评审以下状态：
      </p>
      <ul style="padding-left: 20px;">
        <li><code>1. 标准待补全</code>：还原观察样本 TEST130-0022，收17.80、付7.80、毛利10.00、利润率128.2%。</li>
        <li><code>2. 分区脏状态</code>：展示左侧业务改动、右侧应收新草稿行，顶端与按钮分别显示未存气泡与防丢保护。</li>
        <li><code>3. 合并更改单</code>：展示两表只读警示条与来源列。</li>
        <li><code>4. 更改单未锁拦截</code>：还原截图 04，主单费用未锁定前置告警与引导。</li>
        <li><code>5. 更改单录入</code>：原费用锁定后的更改单列表与调账明细。</li>
        <li><code>6. 附件无类型配置</code>：还原截图 05 空态。</li>
        <li><code>7. 附件分类管理</code>：多分类切换、上传与删除确认。</li>
        <li><code>8. 本票已锁账</code>：全单锁账提示与敏感字段星号遮罩。</li>
      </ul>
    </div>
  </a-drawer>

  <!-- 浮动查看规范按钮 -->
  <a-button type="primary" shape="round" class="floating-spec-btn" @click="showSpecDrawer = true">
    <iconify-icon icon="ant-design:book-outlined"></iconify-icon> 设计交接规范
  </a-button>

</div>

<script>
  const { createApp, ref, reactive, computed, onMounted, onUnmounted } = Vue;

  const app = createApp({
    setup() {
      // 场景沙盘
      const currentScenario = ref('standard');
      const activeTabKey = ref('fee');
      const isLeftCollapsed = ref(false);
      const isMergeChangeOrder = ref(false);
      const showSpecDrawer = ref(false);

      // 保存与加载状态 (3大独立保存域)
      const isSavingBasic = ref(false);
      const isSavingRec = ref(false);
      const isSavingPay = ref(false);

      // 分割条比例 (默认 50%)
      const splitRatio = ref(50);
      const isDraggingSplitter = ref(false);

      // 票据与业务主模型 (对齐实测样本 TEST130-0022)
      const ticketData = reactive({
        jobNo: 'TEST130-0022',
        blNo: 'TEST-GH178-20261109',
        customerName: '青岛万达进出口贸易有限公司',
        salesOrgName: '青岛佳越国际物流 / 市场部',
        salesPerson: '王经理',
        accountingPeriod: '2026-11',
        settlementDate: '2026-12-15',
        isLocked: false,
        isOriginalFeeLocked: false,
        masked: false
      });

      // 翻票序号模拟
      const orderIndex = ref(0);
      const totalOrders = 5;

      // 脏状态追踪
      const dirtyStates = reactive({
        basic: false,
        rec: false,
        recCount: 0,
        pay: false,
        payCount: 0
      });

      // 左侧业务表单数据模型
      const form = reactive({
        jobNo: 'TEST130-0022',
        blNo: 'TEST-GH178-20261109',
        accountingPeriod: '2026-11',
        settlementDate: '2026-12-15',
        salesOrgId: 'org-market',
        customerId: 'cust-wanda',
        contactPerson: '张建国',
        carrier: 'MSK',
        vesselName: 'COSCO PRIDE',
        voyage: '024E',
        bizDate: '2026-11-09',
        pol: 'CNTAO',
        pod: 'USLAX',
        commodities: ['汽车配件', '电子元器件'],
        pieces: 500,
        packageType: 'CTNS',
        weight: 2500.00,
        volume: 15.5000,
        remark: '客户指定走美西直达快船，请及时跟踪提单放行。',
        salesPerson: '王经理',
        operator: '李操作',
        relatedMasterOrder: {
          id: 'mo-1',
          type: '海运出口',
          no: 'EXP202610-008',
          customer: '海尔智家股份有限公司'
        },
        additionalRoles: [
          { roleName: '客服', staffName: '张小妹' },
          { roleName: '单证', staffName: '赵大姐' }
        ]
      });

      // 字典选项
      const salesOrgOptions = [
        { label: '青岛佳越国际物流 / 市场部', value: 'org-market' },
        { label: '青岛佳越国际物流 / 海外拓展部', value: 'org-overseas' },
        { label: '上海佳越国际物流 / 华东业务部', value: 'org-east' }
      ];

      const customerOptions = [
        { label: '青岛万达进出口贸易有限公司', value: 'cust-wanda' },
        { label: '海尔智家进出口供应链有限公司', value: 'cust-haier' },
        { label: '山东重工国际物流有限公司', value: 'cust-sdzg' }
      ];

      const contactOptions = ref([
        { label: '张建国 (13800138000)', value: '张建国' },
        { label: '刘财务 (0532-88889999)', value: '刘财务' }
      ]);

      const carrierOptions = [
        { label: 'MSK / 马士基航运', value: 'MSK' },
        { label: 'COSCO / 中远海运', value: 'COSCO' },
        { label: 'CMA / 达飞轮船', value: 'CMA' },
        { label: 'ONE / 海洋网联', value: 'ONE' }
      ];

      const portOptions = [
        { label: 'CNTAO - 青岛港 (QINGDAO)', value: 'CNTAO' },
        { label: 'CNSHA - 上海港 (SHANGHAI)', value: 'CNSHA' },
        { label: 'USLAX - 洛杉矶港 (LOS ANGELES)', value: 'USLAX' },
        { label: 'USLGB - 长滩港 (LONG BEACH)', value: 'USLGB' }
      ];

      const commodityOptions = [
        { label: '汽车配件 (Auto Parts)', value: '汽车配件' },
        { label: '电子元器件 (Electronics)', value: '电子元器件' },
        { label: '机械设备 (Machinery)', value: '机械设备' },
        { label: '橡胶轮胎 (Tires)', value: '橡胶轮胎' }
      ];

      const packageOptions = [
        { label: 'CTNS / 纸箱', value: 'CTNS' },
        { label: 'PLTS / 托盘', value: 'PLTS' },
        { label: 'WOODEN / 木箱', value: 'WOODEN' },
        { label: 'BAGS / 袋装', value: 'BAGS' }
      ];

      const salesPersonOptions = [
        { label: '王经理 (市场一部)', value: '王经理' },
        { label: '陈总监 (大客户组)', value: '陈总监' }
      ];

      const operatorOptions = [
        { label: '李操作 (登录人)', value: '李操作' },
        { label: '孙操作 (交接备份)', value: '孙操作' }
      ];

      const staffOptions = [
        { label: '张小妹 (客服部)', value: '张小妹' },
        { label: '赵大姐 (单证部)', value: '赵大姐' },
        { label: '钱调度 (调度部)', value: '钱调度' },
        { label: '孙报关 (通关行)', value: '孙报关' }
      ];

      // 应收费用列表 (对齐实测样本：收 RMB 17.80)
      const receivableList = ref([
        {
          id: 'rec-1',
          feeName: '海运订舱费',
          category: '海运',
          settlementTarget: '青岛万达进出口贸易有限公司',
          currency: 'RMB',
          exchangeRate: 1.0000,
          unit: '票',
          unitPrice: 10.00,
          quantity: 1,
          amount: 10.00,
          taxRate: 6,
          taxExcludedAmount: 9.43,
          status: '录入中',
          source: '原票',
          isDraft: false
        },
        {
          id: 'rec-2',
          feeName: '港杂操作费',
          category: '港口',
          settlementTarget: '青岛万达进出口贸易有限公司',
          currency: 'RMB',
          exchangeRate: 1.0000,
          unit: '票',
          unitPrice: 7.80,
          quantity: 1,
          amount: 7.80,
          taxRate: 6,
          taxExcludedAmount: 7.36,
          status: '录入中',
          source: '原票',
          isDraft: false
        }
      ]);

      // 应付费用列表 (对齐实测样本：付 RMB 7.80)
      const payableList = ref([
        {
          id: 'pay-1',
          feeName: '码头操作费 (THC)',
          category: '码头',
          settlementTarget: '青岛中远海运集装箱运输有限公司',
          currency: 'RMB',
          exchangeRate: 1.0000,
          unit: '票',
          unitPrice: 7.80,
          quantity: 1,
          amount: 7.80,
          taxRate: 6,
          taxExcludedAmount: 7.36,
          status: '录入中',
          source: '原票',
          isDraft: false
        }
      ]);

      // 多选状态
      const selectedRecKeys = ref([]);
      const selectedPayKeys = ref([]);

      const selectedFeeCount = computed(() => {
        return selectedRecKeys.value.length + selectedPayKeys.value.length;
      });

      const isAllRecSelected = computed(() => {
        return receivableList.value.length > 0 && selectedRecKeys.value.length === receivableList.value.length;
      });
      const isPartRecSelected = computed(() => {
        return selectedRecKeys.value.length > 0 && selectedRecKeys.value.length < receivableList.value.length;
      });

      const isAllPaySelected = computed(() => {
        return payableList.value.length > 0 && selectedPayKeys.value.length === payableList.value.length;
      });
      const isPartPaySelected = computed(() => {
        return selectedPayKeys.value.length > 0 && selectedPayKeys.value.length < payableList.value.length;
      });

      // 财务统计计算
      const receivableTotalRmb = computed(() => {
        const sum = receivableList.value.reduce((acc, cur) => acc + (cur.amount * cur.exchangeRate), 0);
        return sum.toFixed(2);
      });

      const payableTotalRmb = computed(() => {
        const sum = payableList.value.reduce((acc, cur) => acc + (cur.amount * cur.exchangeRate), 0);
        return sum.toFixed(2);
      });

      const netProfitNumber = computed(() => {
        return parseFloat(receivableTotalRmb.value) - parseFloat(payableTotalRmb.value);
      });

      const netProfitRmb = computed(() => {
        return netProfitNumber.value.toFixed(2);
      });

      const profitMarginText = computed(() => {
        const pay = parseFloat(payableTotalRmb.value);
        if (pay === 0) return '100.0%';
        const ratio = (netProfitNumber.value / pay) * 100;
        return ratio.toFixed(1) + '%';
      });

      // 更改单模型
      const changeOrderList = ref([
        {
          id: 'co-1',
          changeNo: 'CO-202611-001',
          createTime: '2026-11-09 14:30',
          applicant: '王销售',
          recDiff: '+500.00',
          payDiff: '0.00',
          profitDiff: '+500.00',
          status: '已生效',
          reason: '客户变更卸货港堆存天数补充调账'
        }
      ]);

      const changeOrderColumns = [
        { title: '更改单号', dataIndex: 'changeNo', key: 'changeNo' },
        { title: '申请时间', dataIndex: 'createTime', key: 'createTime' },
        { title: '申请人', dataIndex: 'applicant', key: 'applicant' },
        { title: '应收调增', dataIndex: 'recDiff', key: 'recDiff' },
        { title: '应付调增', dataIndex: 'payDiff', key: 'payDiff' },
        { title: '毛利影响', dataIndex: 'profitDiff', key: 'profitDiff' },
        { title: '审核状态', dataIndex: 'status', key: 'status' },
        { title: '调账说明', dataIndex: 'reason', key: 'reason' },
        { title: '操作', key: 'action', width: 140, align: 'center' }
      ];

      // 附件模型
      const attachmentScenario = ref('empty_no_config'); // 'empty_no_config' | 'configured'
      const attachmentCategoryFilter = ref('all');
      const attachmentList = ref([
        { id: 'att-1', fileName: '提单正本扫描件_TEST-GH178.pdf', fileType: 'bl', fileSize: '2.4 MB', uploader: '李操作', uploadTime: '2026-11-09 11:20' },
        { id: 'att-2', fileName: '出口报关预录单_CNTAO.pdf', fileType: 'customs', fileSize: '1.1 MB', uploader: '孙报关', uploadTime: '2026-11-09 13:45' },
        { id: 'att-3', fileName: '码头THC增值税发票.jpg', fileType: 'invoice', fileSize: '850 KB', uploader: '王经理', uploadTime: '2026-11-09 15:10' }
      ]);

      const attachmentColumns = [
        { title: '文件名称', dataIndex: 'fileName', key: 'fileName' },
        { title: '文件大小', dataIndex: 'fileSize', key: 'fileSize', width: 100 },
        { title: '上传人', dataIndex: 'uploader', key: 'uploader', width: 100 },
        { title: '上传时间', dataIndex: 'uploadTime', key: 'uploadTime', width: 160 },
        { title: '操作', key: 'action', width: 150, align: 'center' }
      ];

      const filteredAttachments = computed(() => {
        if (attachmentCategoryFilter.value === 'all') return attachmentList.value;
        return attachmentList.value.filter(item => item.fileType === attachmentCategoryFilter.value);
      });

      // 弹窗状态
      const showMasterOrderModal = ref(false);
      const masterOrderSearchKey = ref('');
      const masterOrderTypeFilter = ref('all');
      const selectedMasterOrderKey = ref([]);
      const tempSelectedMasterOrder = ref(null);

      const masterOrderCandidates = [
        { id: 'mo-1', type: '海运出口', no: 'EXP202610-008', customer: '海尔智家股份有限公司', pol: '青岛', pod: '洛杉矶' },
        { id: 'mo-2', type: '海运进口', no: 'IMP202610-015', customer: '万达贸易', pol: '釜山', pod: '青岛' },
        { id: 'mo-3', type: '件杂货', no: 'BB202611-002', customer: '山东重工', pol: '青岛', pod: '休斯顿' }
      ];

      const masterOrderColumns = [
        { title: '业务类型', dataIndex: 'type', key: 'type', width: 90 },
        { title: '主单号/业务号', dataIndex: 'no', key: 'no' },
        { title: '客户名称', dataIndex: 'customer', key: 'customer' },
        { title: '起运港', dataIndex: 'pol', key: 'pol', width: 80 },
        { title: '目的港', dataIndex: 'pod', key: 'pod', width: 80 }
      ];

      const showCopyModal = ref(false);
      const copyOptions = reactive({
        copyBasic: true,
        copyReceivables: true,
        copyPayables: true,
        clearBlNo: true
      });

      const showSubmitScopeModal = ref(false);
      const showAddStakeholderModal = ref(false);
      const newStakeholder = reactive({
        roleName: '客服',
        staffName: '张小妹'
      });

      // 辅助方法
      const copyText = (txt) => {
        if (!txt) return;
        navigator.clipboard ? navigator.clipboard.writeText(txt) : null;
        antd.message.success(`已复制: ${txt}`);
      };

      const getStatusTagColor = (st) => {
        if (st === '录入中') return 'default';
        if (st === '待审核') return 'processing';
        if (st === '已审核') return 'success';
        if (st === '已开票' || st === '已结算') return 'purple';
        return 'default';
      };

      const getFileIcon = (name) => {
        if (name.endsWith('.pdf')) return 'ant-design:file-pdf-outlined';
        if (name.endsWith('.jpg') || name.endsWith('.png')) return 'ant-design:file-image-outlined';
        return 'ant-design:file-outlined';
      };

      const markDirty = (type) => {
        if (type === 'basic') dirtyStates.basic = true;
      };

      const markRecDirty = (row) => {
        dirtyStates.rec = true;
        dirtyStates.recCount = receivableList.value.filter(r => r.isDraft).length || 1;
      };

      const markPayDirty = (row) => {
        dirtyStates.pay = true;
        dirtyStates.payCount = payableList.value.filter(r => r.isDraft).length || 1;
      };

      const recalcRow = (row, type) => {
        row.amount = parseFloat((row.unitPrice * row.quantity).toFixed(2));
        const taxRateDecimal = row.taxRate / 100;
        row.taxExcludedAmount = parseFloat((row.amount / (1 + taxRateDecimal)).toFixed(2));
        if (type === 'rec') markRecDirty(row);
        else markPayDirty(row);
      };

      // 联动事件
      const handleCustomerChange = (val) => {
        markDirty('basic');
        if (val === 'cust-wanda') {
          contactOptions.value = [
            { label: '张建国 (13800138000)', value: '张建国' },
            { label: '刘财务 (0532-88889999)', value: '刘财务' }
          ];
          form.contactPerson = '张建国';
          form.settlementDate = '2026-12-15';
        } else if (val === 'cust-haier') {
          contactOptions.value = [
            { label: '王主管 (13900139000)', value: '王主管' }
          ];
          form.contactPerson = '王主管';
          form.settlementDate = '2026-12-30';
        }
        antd.message.info('已联动更新单位联系人与应结日期。');
      };

      const handleSalesChange = (val) => {
        markDirty('basic');
        antd.message.info('切换销售人员，已核验直属组织候选范围。');
      };

      const handleBizDateChange = (date) => {
        markDirty('basic');
        if (date) {
          form.accountingPeriod = date.substring(0, 7);
          antd.message.info(`业务日期更新，联动重算会计月份: ${form.accountingPeriod}`);
        }
      };

      // 独立保存方法 1: 保存业务信息
      const saveBasicInfo = () => {
        isSavingBasic.value = true;
        setTimeout(() => {
          isSavingBasic.value = false;
          dirtyStates.basic = false;
          ticketData.blNo = form.blNo;
          antd.message.success('业务信息已成功保存落库！(不影响费用表)');
        }, 500);
      };

      // 独立保存方法 2: 保存应收费用
      const saveReceivableFees = () => {
        isSavingRec.value = true;
        setTimeout(() => {
          isSavingRec.value = false;
          dirtyStates.rec = false;
          dirtyStates.recCount = 0;
          receivableList.value.forEach(r => r.isDraft = false);
          antd.message.success('应收费用已成功保存落库！');
        }, 500);
      };

      // 独立保存方法 3: 保存应付费用
      const savePayableFees = () => {
        isSavingPay.value = true;
        setTimeout(() => {
          isSavingPay.value = false;
          dirtyStates.pay = false;
          dirtyStates.payCount = 0;
          payableList.value.forEach(r => r.isDraft = false);
          antd.message.success('应付费用已成功保存落库！');
        }, 500);
      };

      // 重新生成委托编号 (直接落库)
      const regenerateJobNo = () => {
        ticketData.jobNo = 'TEST130-' + Math.floor(1000 + Math.random() * 9000);
        form.jobNo = ticketData.jobNo;
        antd.message.success(`已生成新编号 ${ticketData.jobNo} 并即时落库！`);
      };

      // 费用多选处理
      const toggleSelectRec = (id) => {
        const idx = selectedRecKeys.value.indexOf(id);
        if (idx > -1) selectedRecKeys.value.splice(idx, 1);
        else selectedRecKeys.value.push(id);
      };

      const toggleSelectAllRec = (e) => {
        if (e.target.checked) {
          selectedRecKeys.value = receivableList.value.map(r => r.id);
        } else {
          selectedRecKeys.value = [];
        }
      };

      const toggleSelectPay = (id) => {
        const idx = selectedPayKeys.value.indexOf(id);
        if (idx > -1) selectedPayKeys.value.splice(idx, 1);
        else selectedPayKeys.value.push(id);
      };

      const toggleSelectAllPay = (e) => {
        if (e.target.checked) {
          selectedPayKeys.value = payableList.value.map(r => r.id);
        } else {
          selectedPayKeys.value = [];
        }
      };

      const clearFeeSelection = () => {
        selectedRecKeys.value = [];
        selectedPayKeys.value = [];
      };

      // 新增草稿行
      const addReceivableRow = () => {
        const newId = 'rec-draft-' + Date.now();
        receivableList.value.unshift({
          id: newId,
          feeName: '海运代理操作费',
          category: '海运',
          settlementTarget: form.customerId === 'cust-wanda' ? '青岛万达进出口贸易有限公司' : '海尔智家',
          currency: 'RMB',
          exchangeRate: 1.0000,
          unit: '票',
          unitPrice: 100.00,
          quantity: 1,
          amount: 100.00,
          taxRate: 6,
          taxExcludedAmount: 94.34,
          status: '录入中',
          source: '原票',
          isDraft: true
        });
        dirtyStates.rec = true;
        dirtyStates.recCount++;
        antd.message.warning('已在应收列表顶部插入本地草稿行，请点击「保存应收」生效。');
      };

      const addPayableRow = () => {
        const newId = 'pay-draft-' + Date.now();
        payableList.value.unshift({
          id: newId,
          feeName: '堆场装箱费',
          category: '堆场',
          settlementTarget: '青岛港大港分公司',
          currency: 'RMB',
          exchangeRate: 1.0000,
          unit: '柜',
          unitPrice: 80.00,
          quantity: 1,
          amount: 80.00,
          taxRate: 6,
          taxExcludedAmount: 75.47,
          status: '录入中',
          source: '原票',
          isDraft: true
        });
        dirtyStates.pay = true;
        dirtyStates.payCount++;
        antd.message.warning('已在应付列表顶部插入本地草稿行，请点击「保存应付」生效。');
      };

      const removeDraftRow = (type, id) => {
        if (type === 'rec') {
          receivableList.value = receivableList.value.filter(r => r.id !== id);
          dirtyStates.recCount = Math.max(0, dirtyStates.recCount - 1);
          if (dirtyStates.recCount === 0) dirtyStates.rec = false;
        } else {
          payableList.value = payableList.value.filter(r => r.id !== id);
          dirtyStates.payCount = Math.max(0, dirtyStates.payCount - 1);
          if (dirtyStates.payCount === 0) dirtyStates.pay = false;
        }
        antd.message.info('已移除本地草稿行。');
      };

      const batchDeleteReceivables = () => {
        receivableList.value = receivableList.value.filter(r => !selectedRecKeys.value.includes(r.id));
        selectedRecKeys.value = [];
        antd.message.success('已完成所选应收费用删除。');
      };

      const batchDeletePayables = () => {
        payableList.value = payableList.value.filter(r => !selectedPayKeys.value.includes(r.id));
        selectedPayKeys.value = [];
        antd.message.success('已完成所选应付费用的批量删除。');
      };

      // 合并更改单开关处理
      const handleToggleMergeChangeOrder = (e) => {
        if (isMergeChangeOrder.value) {
          // 检查是否有未保存草稿
          if (dirtyStates.rec || dirtyStates.pay) {
            antd.Modal.confirm({
              title: '存在未保存的费用草稿',
              content: '切换到「合并更改单·只读模式」将重新载入服务端数据，未保存的草稿将被放弃，是否继续？',
              okText: '放弃草稿并合并查看',
              cancelText: '取消',
              onOk() {
                enterMergeMode();
              },
              onCancel() {
                isMergeChangeOrder.value = false;
              }
            });
          } else {
            enterMergeMode();
          }
        } else {
          exitMergeMode();
        }
      };

      const enterMergeMode = () => {
        isMergeChangeOrder.value = true;
        clearFeeSelection();
        // 注入一条更改单来源费用展示
        if (!receivableList.value.some(r => r.source.includes('更改单'))) {
          receivableList.value.push({
            id: 'rec-co-merge-1',
            feeName: '堆存调整费 (更改单补录)',
            category: '堆存',
            settlementTarget: '青岛万达进出口贸易有限公司',
            currency: 'RMB',
            exchangeRate: 1.0000,
            unit: '票',
            unitPrice: 500.00,
            quantity: 1,
            amount: 500.00,
            taxRate: 6,
            taxExcludedAmount: 471.70,
            status: '已审核',
            source: '更改单 CO-202611-001',
            isDraft: false
          });
        }
        antd.message.info('已载入合并更改单视图，费用区进入只读模式。');
      };

      const exitMergeMode = () => {
        isMergeChangeOrder.value = false;
        receivableList.value = receivableList.value.filter(r => !r.source.includes('更改单'));
        antd.message.info('已退出合并模式，恢复原票编辑状态。');
      };

      // 拖拽高度调节分隔条
      const startDragSplitter = (e) => {
        isDraggingSplitter.value = true;
        const container = document.querySelector('.fee-tables-container');
        if (!container) return;
        const containerRect = container.getBoundingClientRect();

        const onMouseMove = (moveEvent) => {
          if (!isDraggingSplitter.value) return;
          const offsetY = moveEvent.clientY - containerRect.top;
          let percent = (offsetY / containerRect.height) * 100;
          if (percent < 20) percent = 20;
          if (percent > 80) percent = 80;
          splitRatio.value = Math.round(percent);
        };

        const onMouseUp = () => {
          isDraggingSplitter.value = false;
          window.removeEventListener('mousemove', onMouseMove);
          window.removeEventListener('mouseup', onMouseUp);
        };

        window.addEventListener('mousemove', onMouseMove);
        window.addEventListener('mouseup', onMouseUp);
      };

      // 更改单前置锁账模拟
      const mockLockOriginalFee = () => {
        ticketData.isOriginalFeeLocked = true;
        antd.message.success('【原型模拟】已成功将原票费用执行财务锁账！更改单新建入口已解锁。');
      };

      const mockUnlockOriginalFee = () => {
        ticketData.isOriginalFeeLocked = false;
        antd.message.info('已恢复为原票费用未锁定状态。');
      };

      // 弹窗相关触发
      const openMasterOrderModal = () => {
        showMasterOrderModal.value = true;
      };
      const confirmLinkMasterOrder = () => {
        if (tempSelectedMasterOrder.value) {
          form.relatedMasterOrder = { ...tempSelectedMasterOrder.value };
          markDirty('basic');
          showMasterOrderModal.value = false;
          antd.message.success(`已关联主单 ${form.relatedMasterOrder.no}，请点击「保存业务信息」生效。`);
        } else {
          antd.message.warning('请选择需要关联的主单记录。');
        }
      };
      const unlinkMasterOrder = () => {
        form.relatedMasterOrder = null;
        markDirty('basic');
        antd.message.warning('已解除主单关联，请点击「保存业务信息」生效。');
      };

      const openCopyModal = () => {
        showCopyModal.value = true;
      };
      const confirmCopyOrder = () => {
        showCopyModal.value = false;
        antd.message.success('已依据所选配置克隆并创建新业务单据！');
      };

      const openSubmitScopeModal = () => {
        showSubmitScopeModal.value = true;
      };
      const confirmFeeSubmit = () => {
        showSubmitScopeModal.value = false;
        receivableList.value.forEach(r => r.status = '待审核');
        payableList.value.forEach(p => p.status = '待审核');
        clearFeeSelection();
        antd.message.success('已成功提交费用至审核中心！状态已更新为「待审核」。');
      };

      const openAddStakeholderModal = () => {
        showAddStakeholderModal.value = true;
      };
      const confirmAddStakeholder = () => {
        form.additionalRoles.push({ ...newStakeholder });
        markDirty('basic');
        showAddStakeholderModal.value = false;
        antd.message.success(`已追加岗位 ${newStakeholder.roleName}: ${newStakeholder.staffName}`);
      };
      const removeRole = (idx) => {
        form.additionalRoles.splice(idx, 1);
        markDirty('basic');
      };

      const handleSettlementAction = ({ key }) => {
        if (key === 'invoice') antd.message.info('正在为所选应收明细跳转开票申请流程...');
        else if (key === 'payment') antd.message.info('正在为所选应付明细跳转付款申请流程...');
        else if (key === 'batch_target') antd.message.info('打开批量修改结算对象弹窗...');
        else if (key === 'batch_tax') antd.message.info('打开批量修改税率弹窗...');
      };

      const openAiOcrModal = (side) => {
        antd.message.info(`已开启 ${side === 'rec' ? '应收' : '应付'} AI 智能凭证识别导入通道。`);
      };

      const handlePrintStatement = () => {
        antd.message.success('正在生成对账单 PDF 并调起打印...');
      };
      const handleExportFees = () => {
        antd.message.success('已导出本票应收应付明细 Excel 报表。');
      };
      const handleCurrencyExchange = () => {
        antd.message.info('已获取总账最新外币牌价并完成折合试算。');
      };

      const openAddOtherAttachmentType = () => {
        antd.message.info('已调起自定义附件类型字典扩展窗口。');
      };
      const handleFileUpload = (file) => {
        if (file.size > 10 * 1024 * 1024) {
          antd.message.error('单文件大小超过 10MB 限制！');
          return false;
        }
        attachmentList.value.push({
          id: 'att-' + Date.now(),
          fileName: file.name,
          fileType: 'other',
          fileSize: (file.size / 1024).toFixed(1) + ' KB',
          uploader: '李操作',
          uploadTime: window.dayjs().format('YYYY-MM-DD HH:mm')
        });
        antd.message.success(`文件 ${file.name} 上传成功！`);
        return false;
      };
      const previewAttachment = (att) => {
        antd.message.info(`正在调起附件安全预览: ${att.fileName}`);
      };
      const downloadAttachment = (att) => {
        antd.message.success(`已开始下载: ${att.fileName}`);
      };
      const deleteAttachment = (id) => {
        attachmentList.value = attachmentList.value.filter(a => a.id !== id);
        antd.message.success('附件已删除。');
      };

      const handlePrevOrder = () => {
        orderIndex.value = Math.max(0, orderIndex.value - 1);
        antd.message.info(`已切换至上一票综合业务 (序号 ${orderIndex.value + 1}/${totalOrders})`);
      };
      const handleNextOrder = () => {
        orderIndex.value = Math.min(totalOrders - 1, orderIndex.value + 1);
        antd.message.info(`已切换至下一票综合业务 (序号 ${orderIndex.value + 1}/${totalOrders})`);
      };
      const reloadTicket = () => {
        antd.message.success('已重新从服务器获取本票最新数据。');
      };

      // 沙盘场景切换器
      const handleScenarioChange = (e) => {
        const sc = e.target.value;
        if (sc === 'standard') {
          activeTabKey.value = 'fee';
          ticketData.isLocked = false;
          ticketData.isOriginalFeeLocked = false;
          ticketData.masked = false;
          isMergeChangeOrder.value = false;
          dirtyStates.basic = false;
          dirtyStates.rec = false;
          dirtyStates.recCount = 0;
          dirtyStates.pay = false;
          dirtyStates.payCount = 0;
          attachmentScenario.value = 'empty_no_config';
          antd.message.success('已切换至「1. 标准待补全态 (TEST130-0022)」');
        } else if (sc === 'dirty') {
          activeTabKey.value = 'fee';
          dirtyStates.basic = true;
          addReceivableRow();
          antd.message.warning('已激活「2. 分区脏状态」：左侧业务修改未存，右侧有应收草稿。');
        } else if (sc === 'merge') {
          activeTabKey.value = 'fee';
          enterMergeMode();
        } else if (sc === 'co_blocked') {
          activeTabKey.value = 'changeOrder';
          ticketData.isOriginalFeeLocked = false;
          antd.message.info('已切换至「4. 更改单未锁拦截态」，还原图04提示。');
        } else if (sc === 'co_unlocked') {
          activeTabKey.value = 'changeOrder';
          ticketData.isOriginalFeeLocked = true;
          antd.message.success('已切换至「5. 更改单录入态」：原票费用已锁账。');
        } else if (sc === 'attach_empty') {
          activeTabKey.value = 'attachment';
          attachmentScenario.value = 'empty_no_config';
          antd.message.info('已切换至「6. 附件无类型配置空态」，还原图05。');
        } else if (sc === 'attach_full') {
          activeTabKey.value = 'attachment';
          attachmentScenario.value = 'configured';
          antd.message.success('已切换至「7. 附件分类管理态」。');
        } else if (sc === 'ticket_locked') {
          activeTabKey.value = 'fee';
          ticketData.isLocked = true;
          ticketData.masked = true;
          antd.message.error('已切换至「8. 本票已锁账态」：只读且字段脱敏。');
        }
      };

      return {
        currentScenario,
        activeTabKey,
        isLeftCollapsed,
        isMergeChangeOrder,
        showSpecDrawer,
        isSavingBasic,
        isSavingRec,
        isSavingPay,
        splitRatio,
        isDraggingSplitter,
        ticketData,
        orderIndex,
        totalOrders,
        dirtyStates,
        form,
        salesOrgOptions,
        customerOptions,
        contactOptions,
        carrierOptions,
        portOptions,
        commodityOptions,
        packageOptions,
        salesPersonOptions,
        operatorOptions,
        staffOptions,
        receivableList,
        payableList,
        selectedRecKeys,
        selectedPayKeys,
        selectedFeeCount,
        isAllRecSelected,
        isPartRecSelected,
        isAllPaySelected,
        isPartPaySelected,
        receivableTotalRmb,
        payableTotalRmb,
        netProfitNumber,
        netProfitRmb,
        profitMarginText,
        changeOrderList,
        changeOrderColumns,
        attachmentScenario,
        attachmentCategoryFilter,
        attachmentList,
        attachmentColumns,
        filteredAttachments,
        showMasterOrderModal,
        masterOrderSearchKey,
        masterOrderTypeFilter,
        selectedMasterOrderKey,
        tempSelectedMasterOrder,
        masterOrderCandidates,
        masterOrderColumns,
        showCopyModal,
        copyOptions,
        showSubmitScopeModal,
        showAddStakeholderModal,
        newStakeholder,
        copyText,
        getStatusTagColor,
        getFileIcon,
        markDirty,
        markRecDirty,
        markPayDirty,
        recalcRow,
        handleCustomerChange,
        handleSalesChange,
        handleBizDateChange,
        saveBasicInfo,
        saveReceivableFees,
        savePayableFees,
        regenerateJobNo,
        toggleSelectRec,
        toggleSelectAllRec,
        toggleSelectPay,
        toggleSelectAllPay,
        clearFeeSelection,
        addReceivableRow,
        addPayableRow,
        removeDraftRow,
        batchDeleteReceivables,
        batchDeletePayables,
        handleToggleMergeChangeOrder,
        enterMergeMode,
        exitMergeMode,
        startDragSplitter,
        mockLockOriginalFee,
        mockUnlockOriginalFee,
        openMasterOrderModal,
        confirmLinkMasterOrder,
        unlinkMasterOrder,
        openCopyModal,
        confirmCopyOrder,
        openSubmitScopeModal,
        confirmFeeSubmit,
        openAddStakeholderModal,
        confirmAddStakeholder,
        removeRole,
        handleSettlementAction,
        openAiOcrModal,
        handlePrintStatement,
        handleExportFees,
        handleCurrencyExchange,
        openAddOtherAttachmentType,
        handleFileUpload,
        previewAttachment,
        downloadAttachment,
        deleteAttachment,
        handlePrevOrder,
        handleNextOrder,
        reloadTicket,
        handleScenarioChange
      };
    }
  });

  app.use(antd);
  app.mount('#app');
</script>
</body>
</html>
'''

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated HTML successfully at:", output_path)
