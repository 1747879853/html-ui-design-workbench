import os

html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>综合业务编辑工作台 - 操作管理 (高保真交互与UI优化)</title>

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
       综合业务编辑工作台 (Comprehensive Business Workbench) · 极致纯净优雅规范
       设计基准：1920×1080 视口，去除卡片嵌套黑框，深度还原真实货代生产系统
       ========================================================================== */

    body {
      background-color: #f5f7fa;
      color: #1f2329;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
      margin: 0;
      padding: 0;
      font-size: 13px;
    }

    .wb-wrapper {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* 顶部原型审查沙盘控制器 (浅色优雅风格，杜绝漆黑黑客控制台) */
    .scenario-toolbar {
      background: #ffffff;
      color: #4b5563;
      padding: 6px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #e5e7eb;
      font-size: 12px;
      z-index: 100;
      box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .scenario-left {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .scenario-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #eff6ff;
      color: #1d4ed8;
      font-weight: 600;
      font-size: 12px;
      padding: 3px 10px;
      border-radius: 4px;
      border: 1px solid #dbeafe;
    }
    .scenario-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    /* 主工作台顶部导航栏 (White Minimalist Workbench Header) */
    .wb-header {
      background: #ffffff;
      padding: 10px 24px;
      border-bottom: 1px solid #e5e7eb;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .wb-header-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .wb-job-no {
      font-size: 17px;
      font-weight: 700;
      color: #111827;
      letter-spacing: -0.01em;
    }
    .wb-job-sub {
      color: #6b7280;
      font-size: 13px;
    }
    .dirty-pill {
      background: #fffbeb;
      border: 1px solid #fde68a;
      color: #b45309;
      font-size: 12px;
      padding: 2px 8px;
      border-radius: 12px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      animation: pulse-dirty 2s infinite ease-in-out;
    }
    @keyframes pulse-dirty {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.7; }
    }
    .wb-header-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* 浅蓝核心信息条 (100% 高保真还原系统截图 01) */
    .banner-strip {
      background: #e6f4ff;
      border: 1px solid #bae0ff;
      border-radius: 4px;
      margin: 12px 20px 0 20px;
      padding: 8px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
      font-size: 13px;
    }
    .banner-items {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
      color: #1f2937;
    }
    .banner-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .banner-label {
      color: #4b5563;
      font-weight: 400;
    }
    .banner-val {
      font-weight: 600;
      color: #111827;
    }

    /* 主体内容区域 */
    .wb-main-content {
      padding: 12px 20px 24px 20px;
      flex: 1;
    }

    /* 主卡片：纯白画布，扁平清爽，无多重卡片嵌套框 */
    .pure-card {
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 6px;
      padding: 18px 24px 24px 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }

    /* 优雅区段标题 */
    .section-title-line {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin: 20px 0 14px 0;
      padding-bottom: 8px;
      border-bottom: 1px solid #f3f4f6;
    }
    .section-title-line:first-child {
      margin-top: 0;
    }
    .section-title-text {
      font-size: 14px;
      font-weight: 600;
      color: #111827;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .section-title-text::before {
      content: '';
      display: inline-block;
      width: 3px;
      height: 14px;
      background: #1677ff;
      border-radius: 2px;
    }

    /* 表单紧凑对齐 */
    .field-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px 20px;
      margin-bottom: 14px;
    }
    .field-col-1 { grid-column: span 1; }
    .field-col-2 { grid-column: span 2; }
    .field-col-3 { grid-column: span 3; }
    .field-col-4 { grid-column: span 4; }

    .form-item-clean {
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .form-item-clean label {
      font-size: 12px;
      font-weight: 500;
      color: #4b5563;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .form-item-clean label.required::before {
      content: '*';
      color: #ef4444;
      font-size: 13px;
    }

    /* 收发通收起/展开按钮条 */
    .shoufadivider {
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      margin: 18px 0 16px 0;
    }
    .shoufadivider::before {
      content: '';
      position: absolute;
      left: 0;
      right: 0;
      top: 50%;
      height: 1px;
      background: #e5e7eb;
    }
    .shoufatoggle-btn {
      position: relative;
      z-index: 1;
      background: #ffffff;
      border: 1px solid #d1d5db;
      padding: 3px 14px;
      border-radius: 14px;
      font-size: 12px;
      color: #1677ff;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .shoufatoggle-btn:hover {
      background: #f0f7ff;
      border-color: #93c5fd;
    }

    /* 收发通三列容器 */
    .shoufa-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      background: #f9fafb;
      padding: 14px 16px;
      border-radius: 6px;
      border: 1px solid #f3f4f6;
      margin-bottom: 16px;
    }

    /* 船期里程碑横向容器 */
    .milestone-container {
      display: flex;
      align-items: center;
      background: #f9fafb;
      border: 1px solid #e5e7eb;
      border-radius: 6px;
      padding: 12px 18px;
      gap: 12px;
      margin-bottom: 16px;
    }
    .milestone-step {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .milestone-arrow {
      color: #9ca3af;
      font-size: 16px;
      display: flex;
      align-items: center;
    }

    /* 港口横向容器 */
    .ports-container {
      display: grid;
      grid-template-columns: 1fr auto 1fr 1fr;
      gap: 16px;
      align-items: flex-end;
      background: #f9fafb;
      border: 1px solid #e5e7eb;
      border-radius: 6px;
      padding: 12px 18px;
      margin-bottom: 16px;
    }

    /* 基础信息左右两栏布局 */
    .basic-layout {
      display: flex;
      gap: 24px;
      align-items: flex-start;
    }
    .basic-left {
      flex: 1;
      min-width: 0;
    }
    .basic-right {
      width: 250px;
      flex-shrink: 0;
      border-left: 1px solid #f3f4f6;
      padding-left: 20px;
    }

    /* 干系人角色列表 (克制扁平，绝无浮夸卡片) */
    .stakeholder-item {
      margin-bottom: 12px;
    }

    /* 费用页专属布局 */
    .fee-layout {
      display: flex;
      gap: 18px;
      align-items: flex-start;
    }
    .fee-anchor-sidebar {
      width: 210px;
      flex-shrink: 0;
      background: #fafafa;
      border: 1px solid #e5e7eb;
      border-radius: 6px;
      padding: 14px 16px;
      font-size: 12px;
    }
    .fee-anchor-title {
      font-weight: 600;
      color: #111827;
      margin-bottom: 12px;
      font-size: 13px;
      border-bottom: 1px solid #e5e7eb;
      padding-bottom: 6px;
    }
    .fee-anchor-row {
      margin-bottom: 8px;
      line-height: 1.5;
    }
    .fee-anchor-label {
      color: #6b7280;
    }
    .fee-anchor-val {
      font-weight: 500;
      color: #111827;
      word-break: break-all;
    }

    .fee-main-area {
      flex: 1;
      min-width: 0;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    /* 费用底部汇总条 (高保真还原图 03：浅灰清爽条，杜绝大黑条) */
    .fee-profit-strip {
      background: #fafafa;
      border: 1px solid #e5e7eb;
      border-radius: 4px;
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 13px;
    }
    .fee-profit-stats {
      display: flex;
      align-items: center;
      gap: 24px;
    }
    .fee-profit-num {
      font-weight: 700;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
    }
    .profit-positive {
      color: #059669;
    }
    .profit-negative {
      color: #dc2626;
    }

    /* 更改单与附件提示横幅 */
    .co-warning-box {
      background: #fffbe6;
      border: 1px solid #ffe58f;
      border-radius: 6px;
      padding: 14px 18px;
      display: flex;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 16px;
    }
  </style>
</head>
<body>
<div id="app" v-cloak>
  <div class="wb-wrapper">

    <!-- 顶部原型审查沙盘控制器 (浅色优雅风格，杜绝漆黑黑客控制台) -->
    <div class="scenario-toolbar">
      <div class="scenario-left">
        <span class="scenario-badge">
          <iconify-icon icon="ant-design:experiment-outlined"></iconify-icon>
          综合业务工作台 · 原型审查沙盘
        </span>
        <span style="color: #9ca3af;">|</span>
        <span style="color: #6b7280; font-weight: 500;">模拟场景：</span>
        <a-radio-group v-model:value="selectedScenario" size="small" @change="switchScenario">
          <a-radio-button value="standard">1. 标准待补全 (TEST130-0003)</a-radio-button>
          <a-radio-button value="empty">2. 空白新业务</a-radio-button>
          <a-radio-button value="locked">3. 财务锁账/只读</a-radio-button>
          <a-radio-button value="co_blocked">4. 更改单未锁费用拦截</a-radio-button>
          <a-radio-button value="attach_empty">5. 附件未配置类型</a-radio-button>
        </a-radio-group>
      </div>

      <div class="scenario-right">
        <a-switch v-model:checked="isEmbeddedMode" size="small"></a-switch>
        <span style="font-size: 12px; color: #4b5563;">内嵌主单模式</span>
        <a-divider type="vertical"></a-divider>
        <a-button size="small" @click="resetCurrentData">
          <iconify-icon icon="ant-design:redo-outlined"></iconify-icon> 重置当前数据
        </a-button>
      </div>
    </div>

    <!-- 主工作台顶部导航栏 (White Minimalist Workbench Header) -->
    <div class="wb-header">
      <div class="wb-header-left">
        <a-tag color="blue" style="font-weight: 600; font-size: 12px;">综合业务</a-tag>
        <span class="wb-job-no">{{ currentData.jobNo }}</span>
        <span class="wb-job-sub">{{ currentData.vesselVoyage }} · {{ currentData.customerName }}</span>
        
        <span v-if="currentData.isLocked" class="ant-tag ant-tag-warning">
          <iconify-icon icon="ant-design:lock-outlined"></iconify-icon> 费用已锁账 (只读)
        </span>
        <span v-else class="ant-tag ant-tag-success">
          <iconify-icon icon="ant-design:check-circle-outlined"></iconify-icon> 正常作业中
        </span>

        <span v-if="isDirty" class="dirty-pill">
          <iconify-icon icon="ant-design:edit-outlined"></iconify-icon>
          有未保存草稿
        </span>
      </div>

      <div class="wb-header-right">
        <!-- 翻票操作 (内嵌模式下隐藏) -->
        <a-button-group v-if="!isEmbeddedMode" size="small">
          <a-button :disabled="orderIndex <= 0" @click="handlePrevOrder">
            <iconify-icon icon="ant-design:left-outlined"></iconify-icon> 上一票
          </a-button>
          <a-button :disabled="orderIndex >= totalOrders - 1" @click="handleNextOrder">
            下一票 <iconify-icon icon="ant-design:right-outlined"></iconify-icon>
          </a-button>
        </a-button-group>

        <!-- 更多菜单：复制 / 刷新 -->
        <a-dropdown>
          <template #overlay>
            <a-menu>
              <a-menu-item key="copy" @click="openCopyModal">
                <iconify-icon icon="ant-design:copy-outlined"></iconify-icon> 复制本票业务 (带费用选择)
              </a-menu-item>
              <a-menu-item key="reload" @click="reloadOrder">
                <iconify-icon icon="ant-design:reload-outlined"></iconify-icon> 重新读取
              </a-menu-item>
            </a-menu>
          </template>
          <a-button size="small">
            更多 <iconify-icon icon="ant-design:down-outlined"></iconify-icon>
          </a-button>
        </a-dropdown>

        <!-- 保存基础信息按钮 (独立保存单元) -->
        <a-button 
          v-if="activeTabKey === 'basic'"
          type="primary" 
          size="small"
          :loading="isSaving" 
          :disabled="currentData.isLocked"
          @click="saveBasicInfo">
          <iconify-icon icon="ant-design:save-outlined"></iconify-icon> 保存基础信息
        </a-button>

        <!-- 保存费用按钮 -->
        <a-button 
          v-if="activeTabKey === 'fee'"
          type="primary" 
          size="small"
          :loading="isSaving" 
          :disabled="currentData.isLocked || isFeeMergeReadonly"
          @click="saveFeeInfo">
          <iconify-icon icon="ant-design:save-outlined"></iconify-icon> 保存本票费用
        </a-button>
      </div>
    </div>

    <!-- 四大核心功能页签 -->
    <div style="background: #ffffff; padding: 0 20px; border-bottom: 1px solid #e5e7eb;">
      <a-tabs v-model:activeKey="activeTabKey" style="margin-bottom: -1px;">
        <a-tab-pane key="basic" tab="基础信息"></a-tab-pane>
        <a-tab-pane key="fee">
          <template #tab>
            <span>应收应付 <a-badge :count="receivableList.length + payableList.length" :overflow-count="99" :number-style="{ backgroundColor: '#1677ff' }"></a-badge></span>
          </template>
        </a-tab-pane>
        <a-tab-pane key="changeOrder" tab="更改单"></a-tab-pane>
        <a-tab-pane key="attachment">
          <template #tab>
            <span>附件 <a-badge :count="attachmentCount" :overflow-count="99" :number-style="{ backgroundColor: '#52c41a' }"></a-badge></span>
          </template>
        </a-tab-pane>
      </a-tabs>
    </div>

    <!-- 浅蓝核心信息条 (100% 高保真还原系统截图 01) -->
    <div class="banner-strip">
      <div class="banner-items">
        <div class="banner-item">
          <span class="banner-label">委托编号:</span>
          <span class="banner-val">{{ currentData.jobNo }}</span>
          <a-button 
            type="link" 
            size="small" 
            style="padding: 0 4px; font-size: 12px;"
            :disabled="currentData.isLocked"
            @click="regenerateJobNo">
            重新生成
          </a-button>
        </div>

        <div class="banner-item">
          <span class="banner-label">会计期间:</span>
          <span class="banner-val">{{ currentData.accountingPeriod }}</span>
        </div>

        <div class="banner-item">
          <span class="banner-label">应结日期:</span>
          <span class="banner-val">{{ currentData.settlementDate }}</span>
        </div>

        <div class="banner-item">
          <span class="banner-label">归属组织:</span>
          <span class="banner-val">{{ currentData.salesOrgName }}</span>
        </div>

        <div class="banner-item">
          <span class="banner-label">业务来源:</span>
          <span class="banner-val">{{ currentData.businessSource }}</span>
        </div>
      </div>

      <div class="banner-item">
        <span class="banner-label">关联主单:</span>
        <div v-if="currentData.relatedMasterOrder">
          <a-tag color="blue" closable @close="unlinkMasterOrder" style="cursor: pointer;">
            <iconify-icon icon="ant-design:link-outlined"></iconify-icon>
            {{ currentData.relatedMasterOrder.type }} / {{ currentData.relatedMasterOrder.no }} ({{ currentData.relatedMasterOrder.customer }})
          </a-tag>
        </div>
        <div v-else>
          <a-button type="dashed" size="small" style="font-size: 12px;" @click="openRelatedOrderModal">
            <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 关联海运主单
          </a-button>
        </div>
      </div>
    </div>

    <!-- 主体内容区域 -->
    <div class="wb-main-content">

      <!-- ========================================== -->
      <!-- 页签 1: 基础信息 (Basic Information)        -->
      <!-- ========================================== -->
      <div v-show="activeTabKey === 'basic'" class="pure-card">
        <div class="basic-layout">
          
          <!-- 左侧主体表单 (80%) -->
          <div class="basic-left">

            <!-- 区段 1: 业务主体与核心单证 (4列网格) -->
            <div class="section-title-line">
              <div class="section-title-text">业务主体与往来单证</div>
              <div style="font-size: 12px; color: #9ca3af;">* 标记为核心必填项</div>
            </div>

            <div class="field-row">
              <div class="form-item-clean field-col-1">
                <label class="required">委托单位 (客户)</label>
                <a-select 
                  v-model:value="currentData.customerId" 
                  show-search 
                  placeholder="选择往来客户"
                  :disabled="currentData.isLocked"
                  @change="handleCustomerChange">
                  <a-select-option value="CUST001">CUST001 - 宁波万达进出口有限公司</a-select-option>
                  <a-select-option value="CUST002">CUST002 - 浙江吉利汽车零部件制造</a-select-option>
                  <a-select-option value="CUST003">CUST003 - 义乌华贸供应链管理</a-select-option>
                </a-select>
              </div>

              <div class="form-item-clean field-col-1">
                <label>客户联系人</label>
                <a-select 
                  v-model:value="currentData.contactPerson" 
                  placeholder="选择联系人"
                  :disabled="currentData.isLocked">
                  <a-select-option value="张经理">张经理 (13800138000)</a-select-option>
                  <a-select-option value="王业务">王业务 (13900139000)</a-select-option>
                  <a-select-option value="李跟单">李跟单 (13700137000)</a-select-option>
                </a-select>
              </div>

              <div class="form-item-clean field-col-1">
                <label>业务编号</label>
                <a-input v-model:value="currentData.businessNo" placeholder="外部业务单号" :disabled="currentData.isLocked"></a-input>
              </div>

              <div class="form-item-clean field-col-1">
                <label>合同号</label>
                <a-input v-model:value="currentData.contractNo" placeholder="业务合同协议号" :disabled="currentData.isLocked"></a-input>
              </div>
            </div>

            <div class="field-row">
              <div class="form-item-clean field-col-1">
                <label>船公司 (Carrier)</label>
                <a-select v-model:value="currentData.carrier" placeholder="选择船公司" :disabled="currentData.isLocked">
                  <a-select-option value="SITC">SITC - 海丰国际</a-select-option>
                  <a-select-option value="COSCO">COSCO - 中远海运</a-select-option>
                  <a-select-option value="MSK">MSK - 马士基航运</a-select-option>
                  <a-select-option value="EMC">EMC - 长荣海运</a-select-option>
                </a-select>
              </div>

              <div class="form-item-clean field-col-1">
                <label>船名 (Vessel)</label>
                <a-input v-model:value="currentData.vessel" placeholder="英文船名" :disabled="currentData.isLocked"></a-input>
              </div>

              <div class="form-item-clean field-col-1">
                <label>航次 (Voyage)</label>
                <a-input v-model:value="currentData.voyage" placeholder="航次编号" :disabled="currentData.isLocked" @change="markDirty"></a-input>
              </div>

              <div class="form-item-clean field-col-1">
                <label>承运车队</label>
                <a-input v-model:value="currentData.truckingCompany" placeholder="公路车队/集卡运输商" :disabled="currentData.isLocked"></a-input>
              </div>
            </div>

            <div class="field-row">
              <div class="form-item-clean field-col-1">
                <label>主提单号 (MBL No.)</label>
                <a-input v-model:value="currentData.mblNo" placeholder="海运主提单号" :disabled="currentData.isLocked"></a-input>
              </div>

              <div class="form-item-clean field-col-1">
                <label>订舱编号 (Booking No.)</label>
                <a-input v-model:value="currentData.bookingNo" placeholder="订舱SO编号" :disabled="currentData.isLocked"></a-input>
              </div>

              <div class="form-item-clean field-col-1">
                <label>报关发票号</label>
                <a-input v-model:value="currentData.customsInvoiceNo" placeholder="报关发票号" :disabled="currentData.isLocked"></a-input>
              </div>

              <div class="form-item-clean field-col-1">
                <label>货物属性</label>
                <a-radio-group v-model:value="currentData.cargoType" :disabled="currentData.isLocked">
                  <a-radio value="NORMAL">普通货</a-radio>
                  <a-radio value="DG">危险品</a-radio>
                  <a-radio value="RF">冷藏箱</a-radio>
                </a-radio-group>
              </div>
            </div>

            <div class="field-row">
              <div class="form-item-clean field-col-1">
                <label>运输条款</label>
                <a-select v-model:value="currentData.trafficTerms" placeholder="运输条款" :disabled="currentData.isLocked">
                  <a-select-option value="CY-CY">CY-CY (场到场)</a-select-option>
                  <a-select-option value="CY-DOOR">CY-DOOR (场到门)</a-select-option>
                  <a-select-option value="DOOR-CY">DOOR-CY (门到场)</a-select-option>
                  <a-select-option value="DOOR-DOOR">DOOR-DOOR (门到门)</a-select-option>
                </a-select>
              </div>

              <div class="form-item-clean field-col-1">
                <label>贸易条款</label>
                <a-select v-model:value="currentData.tradeTerms" placeholder="贸易条款" :disabled="currentData.isLocked">
                  <a-select-option value="FOB">FOB - 装运港船上交货</a-select-option>
                  <a-select-option value="CIF">CIF - 成本保险加运费</a-select-option>
                  <a-select-option value="CFR">CFR - 成本加运费</a-select-option>
                  <a-select-option value="EXW">EXW - 工厂交货</a-select-option>
                  <a-select-option value="DAP">DAP - 目的地交货</a-select-option>
                </a-select>
              </div>

              <div class="form-item-clean field-col-1">
                <label>付费方式</label>
                <a-select v-model:value="currentData.paymentTerm" placeholder="付费方式" :disabled="currentData.isLocked">
                  <a-select-option value="PP">预付 (Freight Prepaid)</a-select-option>
                  <a-select-option value="CC">到付 (Freight Collect)</a-select-option>
                </a-select>
              </div>

              <div class="form-item-clean field-col-1">
                <label>付费地点</label>
                <a-input v-model:value="currentData.paymentPlace" placeholder="如 NINGBO / TOKYO" :disabled="currentData.isLocked"></a-input>
              </div>
            </div>

            <div class="field-row">
              <div class="form-item-clean field-col-1">
                <label>保险公司</label>
                <a-select v-model:value="currentData.insuranceCompany" placeholder="选择保险公司" :disabled="currentData.isLocked" allow-clear>
                  <a-select-option value="PICC">中国人民财产保险 (PICC)</a-select-option>
                  <a-select-option value="PINGAN">中国平安财产保险</a-select-option>
                  <a-select-option value="CPIC">中国太平洋财产保险</a-select-option>
                </a-select>
              </div>

              <div class="form-item-clean field-col-1">
                <label>报关行</label>
                <a-select v-model:value="currentData.customsBroker" placeholder="选择合作报关行" :disabled="currentData.isLocked" allow-clear>
                  <a-select-option value="DASHUN">宁波达顺报关服务有限公司</a-select-option>
                  <a-select-option value="XINTONG">宁波信通进出口代理报关</a-select-option>
                </a-select>
              </div>

              <div class="form-item-clean field-col-1">
                <label>装卸仓库</label>
                <a-select v-model:value="currentData.warehouse" placeholder="选择作业仓库" :disabled="currentData.isLocked" allow-clear>
                  <a-select-option value="WH01">佳越北仑保税1号仓</a-select-option>
                  <a-select-option value="WH02">大榭集装箱中转堆场</a-select-option>
                </a-select>
              </div>

              <div class="form-item-clean field-col-1">
                <label>内部参考号</label>
                <a-input v-model:value="currentData.internalRefNo" placeholder="企业内部分组编号" :disabled="currentData.isLocked"></a-input>
              </div>
            </div>

            <!-- 区段 2: 收发通 (折叠展开条，高保真还原图 01 与图 02) -->
            <div class="shoufadivider">
              <button type="button" class="shoufatoggle-btn" @click="isShouFaExpanded = !isShouFaExpanded">
                <span>收发通 (发货人 / 收货人 / 通知人)</span>
                <iconify-icon :icon="isShouFaExpanded ? 'ant-design:up-outlined' : 'ant-design:down-outlined'"></iconify-icon>
              </button>
            </div>

            <div v-show="isShouFaExpanded" class="shoufa-grid">
              <!-- 发货人 Shipper -->
              <div class="form-item-clean">
                <label>发货人 (Shipper)</label>
                <a-select v-model:value="currentData.shipperId" placeholder="选择往来单位快速填入" :disabled="currentData.isLocked" allow-clear>
                  <a-select-option value="SH01">NINGBO WANDA EXPORT CO., LTD.</a-select-option>
                  <a-select-option value="SH02">ZHEJIANG AUTO PARTS INDUSTRY</a-select-option>
                </a-select>
                <a-textarea 
                  v-model:value="currentData.shipperText" 
                  :rows="4" 
                  placeholder="英文名称、详细地址、城市、国别、联系电话/税号" 
                  :maxlength="1024"
                  :disabled="currentData.isLocked">
                </a-textarea>
              </div>

              <!-- 收货人 Consignee -->
              <div class="form-item-clean">
                <label>收货人 (Consignee)</label>
                <a-select v-model:value="currentData.consigneeId" placeholder="选择往来单位快速填入" :disabled="currentData.isLocked" allow-clear>
                  <a-select-option value="TO_ORDER">TO ORDER</a-select-option>
                  <a-select-option value="CN01">PACIFIC LOGISTICS (JAPAN) CO., LTD.</a-select-option>
                </a-select>
                <a-textarea 
                  v-model:value="currentData.consigneeText" 
                  :rows="4" 
                  placeholder="TO ORDER 或英文名称、地址、电话、税号" 
                  :maxlength="1024"
                  :disabled="currentData.isLocked">
                </a-textarea>
              </div>

              <!-- 通知人 Notify Party -->
              <div class="form-item-clean">
                <label>通知人 (Notify Party)</label>
                <a-select v-model:value="currentData.notifyPartyId" placeholder="选择往来单位快速填入" :disabled="currentData.isLocked" allow-clear>
                  <a-select-option value="SAME_AS">SAME AS CONSIGNEE</a-select-option>
                  <a-select-option value="NP01">EASTERN TRADING NOTIFY AGENCY</a-select-option>
                </a-select>
                <a-textarea 
                  v-model:value="currentData.notifyPartyText" 
                  :rows="4" 
                  placeholder="SAME AS CONSIGNEE 或通知人详细英文联系方式" 
                  :maxlength="1024"
                  :disabled="currentData.isLocked">
                </a-textarea>
              </div>
            </div>

            <!-- 区段 3: 船期里程碑与航线港口 (流程化横向呈现) -->
            <div class="section-title-line">
              <div class="section-title-text">船期里程碑与港口</div>
              <div style="font-size: 12px; color: #6b7280;">计划离港 → 实际离港 → 预计到港全周期追踪</div>
            </div>

            <div class="milestone-container">
              <div class="milestone-step">
                <span style="font-size: 12px; color: #6b7280; font-weight: 500;">货好时间 (Ready Date)</span>
                <a-date-picker 
                  v-model:value="currentData.cargoReadyDate" 
                  show-time 
                  placeholder="货好日期时间" 
                  style="width: 100%;" 
                  :disabled="currentData.isLocked">
                </a-date-picker>
              </div>

              <div class="milestone-arrow"><iconify-icon icon="ant-design:arrow-right-outlined"></iconify-icon></div>

              <div class="milestone-step">
                <span style="font-size: 12px; color: #6b7280; font-weight: 500;">计划开船 (ETD)</span>
                <a-date-picker 
                  v-model:value="currentData.etd" 
                  placeholder="计划离港日期" 
                  style="width: 100%;" 
                  :disabled="currentData.isLocked">
                </a-date-picker>
              </div>

              <div class="milestone-arrow"><iconify-icon icon="ant-design:arrow-right-outlined"></iconify-icon></div>

              <div class="milestone-step">
                <span style="font-size: 12px; color: #6b7280; font-weight: 500;">实际开船 (ATD)</span>
                <a-date-picker 
                  v-model:value="currentData.atd" 
                  placeholder="实际出海日期" 
                  style="width: 100%;" 
                  :disabled="currentData.isLocked">
                </a-date-picker>
              </div>

              <div class="milestone-arrow"><iconify-icon icon="ant-design:arrow-right-outlined"></iconify-icon></div>

              <div class="milestone-step">
                <span style="font-size: 12px; color: #6b7280; font-weight: 500;">预计到达 (ETA)</span>
                <a-date-picker 
                  v-model:value="currentData.eta" 
                  placeholder="预计抵港日期" 
                  style="width: 100%;" 
                  :disabled="currentData.isLocked">
                </a-date-picker>
              </div>
            </div>

            <div class="ports-container">
              <div class="form-item-clean">
                <label class="required">起运港 (POL)</label>
                <a-select v-model:value="currentData.polPort" show-search placeholder="选择起运海港" :disabled="currentData.isLocked">
                  <a-select-option value="CNNBG - 宁波 (NINGBO)">CNNBG - 宁波 (NINGBO)</a-select-option>
                  <a-select-option value="CNSHA - 上海 (SHANGHAI)">CNSHA - 上海 (SHANGHAI)</a-select-option>
                  <a-select-option value="CNSZX - 深圳 (SHENZHEN)">CNSZX - 深圳 (SHENZHEN)</a-select-option>
                </a-select>
              </div>

              <div style="padding-bottom: 8px; color: #9ca3af; font-size: 18px;">
                <iconify-icon icon="ant-design:swap-right-outlined"></iconify-icon>
              </div>

              <div class="form-item-clean">
                <label class="required">目的港 (POD)</label>
                <a-select v-model:value="currentData.podPort" show-search placeholder="选择目的海港" :disabled="currentData.isLocked">
                  <a-select-option value="JPTYO - 东京 (TOKYO)">JPTYO - 东京 (TOKYO)</a-select-option>
                  <a-select-option value="JPYOK - 横滨 (YOKOHAMA)">JPYOK - 横滨 (YOKOHAMA)</a-select-option>
                  <a-select-option value="USLAX - 洛杉矶 (LOS ANGELES)">USLAX - 洛杉矶 (LOS ANGELES)</a-select-option>
                </a-select>
              </div>

              <div class="form-item-clean">
                <label>航线与国别说明</label>
                <a-input v-model:value="currentData.routeDescription" placeholder="如 日本关东快线 / JAPAN" :disabled="currentData.isLocked"></a-input>
              </div>
            </div>

            <!-- 区段 4: 货物信息与包装明细 (严禁箱型箱量，保留件毛体与品名唛头) -->
            <div class="section-title-line">
              <div class="section-title-text">货物信息与包装</div>
              <div style="font-size: 12px; color: #6b7280;">注：综合业务无集装箱箱量，按通用件毛体核算</div>
            </div>

            <div class="field-row">
              <div class="form-item-clean field-col-2">
                <label>品名 (Commodity)</label>
                <a-input v-model:value="currentData.commodityName" placeholder="中文或英文标准品名" :disabled="currentData.isLocked"></a-input>
              </div>

              <div class="form-item-clean field-col-2">
                <label>唛头 (Marks & Numbers)</label>
                <a-input v-model:value="currentData.shippingMarks" placeholder="N/M 或具体箱唛编号" :disabled="currentData.isLocked"></a-input>
              </div>
            </div>

            <div class="field-row">
              <div class="form-item-clean field-col-4">
                <label>货物描述 (Goods Description)</label>
                <a-textarea v-model:value="currentData.goodsDescription" :rows="2" placeholder="货物规格、材质或申报描述" :disabled="currentData.isLocked"></a-textarea>
              </div>
            </div>

            <div class="field-row">
              <div class="form-item-clean field-col-1">
                <label class="required">总件数 (Pieces)</label>
                <a-input-number v-model:value="currentData.pieces" :min="0" :precision="0" style="width: 100%;" placeholder="0" :disabled="currentData.isLocked"></a-input-number>
              </div>

              <div class="form-item-clean field-col-1">
                <label>包装类型 (Package)</label>
                <a-select v-model:value="currentData.packageType" placeholder="包装单位" :disabled="currentData.isLocked">
                  <a-select-option value="CTNS">CTNS (纸箱)</a-select-option>
                  <a-select-option value="PLTS">PLTS (托盘)</a-select-option>
                  <a-select-option value="BAGS">BAGS (袋装)</a-select-option>
                  <a-select-option value="WOODEN">WOODEN CASES (木箱)</a-select-option>
                </a-select>
              </div>

              <div class="form-item-clean field-col-1">
                <label class="required">毛重 (Gross Weight KGS)</label>
                <a-input-number v-model:value="currentData.grossWeight" :min="0" :precision="3" style="width: 100%;" placeholder="0.000" :disabled="currentData.isLocked"></a-input-number>
              </div>

              <div class="form-item-clean field-col-1">
                <label class="required">体积 (Volume CBM)</label>
                <a-input-number v-model:value="currentData.volume" :min="0" :precision="3" style="width: 100%;" placeholder="0.000" :disabled="currentData.isLocked"></a-input-number>
              </div>
            </div>

            <!-- 区段 5: 内部/外部双备注 (Tab 隔离) -->
            <div style="margin-top: 18px;">
              <a-tabs size="small" type="card">
                <a-tab-pane key="internal" tab="内部备注 (仅企业可见)">
                  <a-textarea 
                    v-model:value="currentData.internalRemark" 
                    :rows="3" 
                    placeholder="业务风险、操作要点、内部结算注意事项（对外不导出）" 
                    :maxlength="1024"
                    :disabled="currentData.isLocked">
                  </a-textarea>
                </a-tab-pane>
                <a-tab-pane key="external" tab="外部备注 (可对客展现)">
                  <a-textarea 
                    v-model:value="currentData.externalRemark" 
                    :rows="3" 
                    placeholder="提单打印说明、对客交付注意事项" 
                    :maxlength="1024"
                    :disabled="currentData.isLocked">
                  </a-textarea>
                </a-tab-pane>
              </a-tabs>
            </div>

          </div>

          <!-- 右侧业务干系人 (20%, 极简干净，无花哨 AI 警告卡) -->
          <div class="basic-right">
            <div style="font-weight: 600; color: #111827; font-size: 14px; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between;">
              <span>业务责任干系人</span>
              <span style="font-size: 12px; color: #9ca3af; font-weight: normal;">组织归属联动</span>
            </div>

            <div class="stakeholder-item form-item-clean">
              <label class="required">负责销售 (Sales)</label>
              <a-select 
                v-model:value="currentData.salesPersonId" 
                placeholder="选择销售人员"
                :disabled="currentData.isLocked"
                @change="handleSalesChange">
                <a-select-option value="U101">张晓华 (销售一部)</a-select-option>
                <a-select-option value="U102">王大为 (销售二部)</a-select-option>
                <a-select-option value="U103">赵敏 (大客户部)</a-select-option>
              </a-select>
            </div>

            <div class="stakeholder-item form-item-clean">
              <label class="required">直属组织 (Organization)</label>
              <a-select 
                v-model:value="currentData.salesOrgId" 
                placeholder="归属组织"
                :disabled="currentData.isLocked">
                <a-select-option v-for="org in availableOrgs" :key="org.id" :value="org.id">
                  {{ org.name }}
                </a-select-option>
              </a-select>
            </div>

            <a-divider style="margin: 14px 0;"></a-divider>

            <div class="stakeholder-item form-item-clean">
              <label>操作专员 (Operator)</label>
              <a-select v-model:value="currentData.operatorId" placeholder="分派操作" :disabled="currentData.isLocked" allow-clear>
                <a-select-option value="OP01">李操作 (综合业务组)</a-select-option>
                <a-select-option value="OP02">孙海运 (海运部)</a-select-option>
              </a-select>
            </div>

            <div class="stakeholder-item form-item-clean">
              <label>客服专员 (CS)</label>
              <a-select v-model:value="currentData.customerServiceId" placeholder="指定客服" :disabled="currentData.isLocked" allow-clear>
                <a-select-option value="CS01">周客服 (VIP专线)</a-select-option>
                <a-select-option value="CS02">钱助理</a-select-option>
              </a-select>
            </div>

            <div class="stakeholder-item form-item-clean">
              <label>订舱专员 (Booking)</label>
              <a-select v-model:value="currentData.bookingPersonId" placeholder="订舱员" :disabled="currentData.isLocked" allow-clear>
                <a-select-option value="BK01">吴订舱</a-select-option>
              </a-select>
            </div>

            <div class="stakeholder-item form-item-clean">
              <label>财务结算 (Settlement)</label>
              <a-select v-model:value="currentData.financialPersonId" placeholder="财务结算员" :disabled="currentData.isLocked" allow-clear>
                <a-select-option value="FN01">郑财务 (华东组)</a-select-option>
              </a-select>
            </div>

            <!-- 极简权限状态提醒 (纯净文本，绝不使用荧光绿大卡片) -->
            <div style="margin-top: 18px; padding: 10px 12px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 4px; font-size: 11px; color: #6b7280; line-height: 1.5;">
              <div style="font-weight: 600; color: #374151; margin-bottom: 4px;">业务状态与归属规则</div>
              <div>• 销售仅能指定一人，组织由销售直属范围联动</div>
              <div>• 基础信息保存独立生效，不包含费用提交</div>
            </div>

          </div>

        </div>
      </div>

      <!-- ========================================== -->
      <!-- 页签 2: 应收应付 (Receivables & Payables)   -->
      <!-- ========================================== -->
      <div v-show="activeTabKey === 'fee'" class="pure-card">
        <div class="fee-layout">
          
          <!-- 左侧持久身份核对锚点 (210px，满足 P1 认票与无死角核对) -->
          <div class="fee-anchor-sidebar">
            <div class="fee-anchor-title">
              <iconify-icon icon="ant-design:file-protect-outlined"></iconify-icon> 当前业务凭据
            </div>

            <div class="fee-anchor-row">
              <div class="fee-anchor-label">委托编号</div>
              <div class="fee-anchor-val">{{ currentData.jobNo }}</div>
            </div>

            <div class="fee-anchor-row">
              <div class="fee-anchor-label">委托单位 (客户)</div>
              <div class="fee-anchor-val">{{ currentData.customerName }}</div>
            </div>

            <div class="fee-anchor-row">
              <div class="fee-anchor-label">船名 / 航次</div>
              <div class="fee-anchor-val">{{ currentData.vessel }} / {{ currentData.voyage }}</div>
            </div>

            <div class="fee-anchor-row">
              <div class="fee-anchor-label">起运港 → 目的港</div>
              <div class="fee-anchor-val">
                {{ (currentData.polPort || '').split(' - ')[0] }} → {{ (currentData.podPort || '').split(' - ')[0] }}
              </div>
            </div>

            <div class="fee-anchor-row">
              <div class="fee-anchor-label">会计期间</div>
              <div class="fee-anchor-val">{{ currentData.accountingPeriod }}</div>
            </div>

            <div class="fee-anchor-row">
              <div class="fee-anchor-label">关联主单</div>
              <div class="fee-anchor-val" style="color: #1677ff;">
                {{ currentData.relatedMasterOrder ? currentData.relatedMasterOrder.no : '未关联主单' }}
              </div>
            </div>

            <div class="fee-anchor-row" style="margin-top: 14px; border-top: 1px dashed #e5e7eb; padding-top: 10px;">
              <div class="fee-anchor-label">锁定与编辑权限</div>
              <div>
                <a-tag v-if="currentData.isLocked" color="warning">费用已锁账</a-tag>
                <a-tag v-else-if="isFeeMergeReadonly" color="orange">合并更改单·只读</a-tag>
                <a-tag v-else color="green">可自由录入</a-tag>
              </div>
            </div>
          </div>

          <!-- 右侧费用双表与操作区 (满足 100% 18列字段保真) -->
          <div class="fee-main-area">

            <!-- 顶部工具与合并更改单开关条 (高保真还原图 04) -->
            <div style="display: flex; align-items: center; justify-content: space-between; background: #f9fafb; padding: 10px 16px; border-radius: 4px; border: 1px solid #e5e7eb;">
              <div style="display: flex; align-items: center; gap: 14px;">
                <a-checkbox v-model:checked="isFeeMergeReadonly" @change="handleToggleMergeReadonly">
                  <span style="font-weight: 600; color: #111827;">合并更改单 (合并查看·只读)</span>
                </a-checkbox>
                <span v-if="isFeeMergeReadonly" style="color: #b45309; font-size: 12px; background: #fffbeb; padding: 2px 8px; border-radius: 4px; border: 1px solid #fde68a;">
                  <iconify-icon icon="ant-design:info-circle-outlined"></iconify-icon> 当前已包含更改单费用，为防止数据冲突，整页已置为只读
                </span>
              </div>

              <div style="display: flex; align-items: center; gap: 8px;">
                <a-button 
                  type="primary" 
                  size="small" 
                  :disabled="isFeeMergeReadonly || currentData.isLocked"
                  @click="addReceivableRow">
                  <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 新增应收
                </a-button>
                <a-button 
                  type="primary" 
                  ghost
                  size="small" 
                  :disabled="isFeeMergeReadonly || currentData.isLocked"
                  @click="addPayableRow">
                  <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 新增应付
                </a-button>
                <a-button size="small" :disabled="isFeeMergeReadonly || currentData.isLocked">
                  <iconify-icon icon="ant-design:import-outlined"></iconify-icon> 引入标准模板
                </a-button>
                <a-button size="small">
                  <iconify-icon icon="ant-design:scan-outlined"></iconify-icon> AI账单识别
                </a-button>
                <a-button size="small">
                  <iconify-icon icon="ant-design:printer-outlined"></iconify-icon> 打印账单
                </a-button>
              </div>
            </div>

            <!-- 应收费用表 (Receivables 18列) -->
            <div>
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-weight: 600; font-size: 13px; color: #1677ff; display: flex; align-items: center; gap: 6px;">
                  <iconify-icon icon="ant-design:arrow-down-outlined"></iconify-icon> 应收费用列表 (Receivable)
                </span>
                <span style="font-size: 12px; color: #6b7280;">共 {{ receivableList.length }} 笔应收</span>
              </div>

              <a-table 
                :data-source="receivableList" 
                :columns="feeColumns" 
                size="small" 
                :pagination="false" 
                bordered
                :scroll="{ x: 1600 }">
                
                <template #bodyCell="{ column, record, index }">
                  <template v-if="column.key === 'index'">
                    {{ index + 1 }}
                  </template>

                  <template v-else-if="column.key === 'source'">
                    <a-tag :color="record.source === '更改单' ? 'orange' : 'blue'">
                      {{ record.source || '本票原始' }}
                    </a-tag>
                  </template>

                  <template v-else-if="column.key === 'feeItem'">
                    <a-select 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.feeItem" 
                      size="small" 
                      style="width: 100%;">
                      <a-select-option value="拖车费">拖车费 (Trucking Fee)</a-select-option>
                      <a-select-option value="报关代理费">报关代理费 (Customs Fee)</a-select-option>
                      <a-select-option value="仓储服务费">仓储服务费 (Storage Fee)</a-select-option>
                      <a-select-option value="港杂费">港杂费 (Port Surcharge)</a-select-option>
                    </a-select>
                    <span v-else>{{ record.feeItem }}</span>
                  </template>

                  <template v-else-if="column.key === 'settlementUnit'">
                    <a-input 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.settlementUnit" 
                      size="small">
                    </a-input>
                    <span v-else>{{ record.settlementUnit }}</span>
                  </template>

                  <template v-else-if="column.key === 'currency'">
                    <a-select 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.currency" 
                      size="small" 
                      style="width: 80px;">
                      <a-select-option value="CNY">CNY</a-select-option>
                      <a-select-option value="USD">USD</a-select-option>
                    </a-select>
                    <span v-else>{{ record.currency }}</span>
                  </template>

                  <template v-else-if="column.key === 'unitPrice'">
                    <a-input-number 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.unitPrice" 
                      size="small" 
                      :precision="2" 
                      style="width: 90px;"
                      @change="recalcRow(record)">
                    </a-input-number>
                    <span v-else>{{ record.unitPrice ? record.unitPrice.toFixed(2) : '0.00' }}</span>
                  </template>

                  <template v-else-if="column.key === 'quantity'">
                    <a-input-number 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.quantity" 
                      size="small" 
                      :precision="2" 
                      style="width: 70px;"
                      @change="recalcRow(record)">
                    </a-input-number>
                    <span v-else>{{ record.quantity }}</span>
                  </template>

                  <template v-else-if="column.key === 'taxRate'">
                    <a-select 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.taxRate" 
                      size="small" 
                      style="width: 80px;"
                      @change="recalcRow(record)">
                      <a-select-option :value="0">0%</a-select-option>
                      <a-select-option :value="6">6%</a-select-option>
                      <a-select-option :value="9">9%</a-select-option>
                      <a-select-option :value="13">13%</a-select-option>
                    </a-select>
                    <span v-else>{{ record.taxRate }}%</span>
                  </template>

                  <template v-else-if="column.key === 'amountWithTax'">
                    <span style="font-weight: 600; color: #111827;">{{ (record.amountWithTax || 0).toFixed(2) }}</span>
                  </template>

                  <template v-else-if="column.key === 'action'">
                    <a-popconfirm 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked"
                      title="确定删除此条费用吗？" 
                      @confirm="removeReceivableRow(index)">
                      <a-button type="link" danger size="small" style="padding: 0;">删除</a-button>
                    </a-popconfirm>
                    <span v-else style="color: #9ca3af;">--</span>
                  </template>
                </template>
              </a-table>
            </div>

            <!-- 应付费用表 (Payables 18列) -->
            <div>
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-weight: 600; font-size: 13px; color: #ea580c; display: flex; align-items: center; gap: 6px;">
                  <iconify-icon icon="ant-design:arrow-up-outlined"></iconify-icon> 应付费用列表 (Payable)
                </span>
                <span style="font-size: 12px; color: #6b7280;">共 {{ payableList.length }} 笔应付</span>
              </div>

              <a-table 
                :data-source="payableList" 
                :columns="feeColumns" 
                size="small" 
                :pagination="false" 
                bordered
                :scroll="{ x: 1600 }">
                
                <template #bodyCell="{ column, record, index }">
                  <template v-if="column.key === 'index'">
                    {{ index + 1 }}
                  </template>

                  <template v-else-if="column.key === 'source'">
                    <a-tag :color="record.source === '更改单' ? 'orange' : 'blue'">
                      {{ record.source || '本票原始' }}
                    </a-tag>
                  </template>

                  <template v-else-if="column.key === 'feeItem'">
                    <a-select 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.feeItem" 
                      size="small" 
                      style="width: 100%;">
                      <a-select-option value="拖车费">拖车费 (集卡外付)</a-select-option>
                      <a-select-option value="仓储费">仓储理货费</a-select-option>
                      <a-select-option value="报关代理费">报关行代理规费</a-select-option>
                      <a-select-option value="港杂费">码头堆存费</a-select-option>
                    </a-select>
                    <span v-else>{{ record.feeItem }}</span>
                  </template>

                  <template v-else-if="column.key === 'settlementUnit'">
                    <a-input 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.settlementUnit" 
                      size="small">
                    </a-input>
                    <span v-else>{{ record.settlementUnit }}</span>
                  </template>

                  <template v-else-if="column.key === 'currency'">
                    <a-select 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.currency" 
                      size="small" 
                      style="width: 80px;">
                      <a-select-option value="CNY">CNY</a-select-option>
                      <a-select-option value="USD">USD</a-select-option>
                    </a-select>
                    <span v-else>{{ record.currency }}</span>
                  </template>

                  <template v-else-if="column.key === 'unitPrice'">
                    <a-input-number 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.unitPrice" 
                      size="small" 
                      :precision="2" 
                      style="width: 90px;"
                      @change="recalcRow(record)">
                    </a-input-number>
                    <span v-else>{{ record.unitPrice ? record.unitPrice.toFixed(2) : '0.00' }}</span>
                  </template>

                  <template v-else-if="column.key === 'quantity'">
                    <a-input-number 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.quantity" 
                      size="small" 
                      :precision="2" 
                      style="width: 70px;"
                      @change="recalcRow(record)">
                    </a-input-number>
                    <span v-else>{{ record.quantity }}</span>
                  </template>

                  <template v-else-if="column.key === 'taxRate'">
                    <a-select 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked" 
                      v-model:value="record.taxRate" 
                      size="small" 
                      style="width: 80px;"
                      @change="recalcRow(record)">
                      <a-select-option :value="0">0%</a-select-option>
                      <a-select-option :value="6">6%</a-select-option>
                      <a-select-option :value="9">9%</a-select-option>
                    </a-select>
                    <span v-else>{{ record.taxRate }}%</span>
                  </template>

                  <template v-else-if="column.key === 'amountWithTax'">
                    <span style="font-weight: 600; color: #111827;">{{ (record.amountWithTax || 0).toFixed(2) }}</span>
                  </template>

                  <template v-else-if="column.key === 'action'">
                    <a-popconfirm 
                      v-if="!isFeeMergeReadonly && !currentData.isLocked"
                      title="确定删除此条费用吗？" 
                      @confirm="removePayableRow(index)">
                      <a-button type="link" danger size="small" style="padding: 0;">删除</a-button>
                    </a-popconfirm>
                    <span v-else style="color: #9ca3af;">--</span>
                  </template>
                </template>
              </a-table>
            </div>

            <!-- 费用底部汇总条 (高保真还原图 03：浅灰清爽条，杜绝大黑条) -->
            <div class="fee-profit-strip">
              <div class="fee-profit-stats">
                <div>
                  <span style="color: #6b7280;">应收合计:</span>
                  <span class="fee-profit-num" style="color: #1677ff; margin-left: 6px;">{{ totalReceivable.toFixed(2) }} CNY</span>
                </div>

                <div style="color: #d1d5db;">|</div>

                <div>
                  <span style="color: #6b7280;">应付合计:</span>
                  <span class="fee-profit-num" style="color: #ea580c; margin-left: 6px;">{{ totalPayable.toFixed(2) }} CNY</span>
                </div>

                <div style="color: #d1d5db;">|</div>

                <div>
                  <span style="color: #6b7280;">预估利润:</span>
                  <span 
                    class="fee-profit-num" 
                    :class="totalProfit >= 0 ? 'profit-positive' : 'profit-negative'"
                    style="margin-left: 6px;">
                    {{ totalProfit >= 0 ? '+' : '' }}{{ totalProfit.toFixed(2) }} CNY
                  </span>
                </div>

                <div style="color: #d1d5db;">|</div>

                <div>
                  <span style="color: #6b7280;">毛利率:</span>
                  <span class="fee-profit-num" style="margin-left: 6px;">
                    {{ totalReceivable > 0 ? (totalProfit / totalReceivable * 100).toFixed(2) + '%' : '--' }}
                  </span>
                </div>
              </div>

              <div>
                <a-button 
                  type="primary" 
                  size="small" 
                  :loading="isSaving" 
                  :disabled="isFeeMergeReadonly || currentData.isLocked"
                  @click="saveFeeInfo">
                  <iconify-icon icon="ant-design:check-outlined"></iconify-icon> 保存费用修改
                </a-button>
              </div>
            </div>

          </div>

        </div>
      </div>

      <!-- ========================================== -->
      <!-- 页签 3: 更改单 (Change Orders)              -->
      <!-- ========================================== -->
      <div v-show="activeTabKey === 'changeOrder'" class="pure-card">
        
        <!-- 前置条件不足警示 (高保真还原图 05) -->
        <div v-if="!currentData.isFeeLocked" class="co-warning-box">
          <iconify-icon icon="ant-design:warning-filled" style="color: #faad14; font-size: 20px; flex-shrink: 0; margin-top: 2px;"></iconify-icon>
          <div style="flex: 1;">
            <div style="font-weight: 600; color: #111827; font-size: 14px; margin-bottom: 4px;">
              本票原费用未锁定，暂无法发起更改单
            </div>
            <div style="color: #4b5563; font-size: 13px; line-height: 1.5; margin-bottom: 10px;">
              更改单是针对<strong>已完成锁账的业务</strong>进行费用追溯与调整的正式单据。当前票尚未执行费用锁账，您可以直接在「应收应付」页签内增删改费用。若需封存原费用，请联系财务人员执行本票费用锁账。
            </div>
            <div style="display: flex; gap: 10px;">
              <a-button type="primary" size="small" @click="activeTabKey = 'fee'">
                <iconify-icon icon="ant-design:arrow-left-outlined"></iconify-icon> 前往「应收应付」直接调整
              </a-button>
              <a-button size="small" @click="simulateFeeLock">
                <iconify-icon icon="ant-design:lock-outlined"></iconify-icon> 原型模拟：立即锁账原费用
              </a-button>
            </div>
          </div>
        </div>

        <!-- 已满足前置条件 (已锁费用)：可新建或查阅更改单 -->
        <div v-else>
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #f3f4f6;">
            <div style="display: flex; align-items: center; gap: 12px;">
              <span style="font-weight: 600; font-size: 14px; color: #111827;">更改单记录：</span>
              <a-select v-model:value="selectedChangeOrderId" style="width: 260px;" size="small">
                <a-select-option value="CO-202611-001">CO-202611-001 (补录仓储理货费 - 待审批)</a-select-option>
                <a-select-option value="NEW">+ 发起新更改单 (草稿)</a-select-option>
              </a-select>
              <a-tag color="blue">当前状态：待财务审核</a-tag>
            </div>

            <div style="display: flex; align-items: center; gap: 8px;">
              <a-button type="primary" size="small" @click="saveChangeOrderSingleSide">
                <iconify-icon icon="ant-design:save-outlined"></iconify-icon> 仅保存当前侧费用与更改单
              </a-button>
            </div>
          </div>

          <!-- 更改单表单 -->
          <div class="field-row">
            <div class="form-item-clean field-col-2">
              <label class="required">更改原因说明 (必填)</label>
              <a-textarea v-model:value="changeOrderReason" :rows="2" placeholder="详细说明改单原因（如：目的港额外产生堆存规费，客户已邮件确认确认）"></a-textarea>
            </div>

            <div class="form-item-clean field-col-1">
              <label class="required">调整归属期间</label>
              <a-input v-model:value="currentData.accountingPeriod" disabled></a-input>
            </div>

            <div class="form-item-clean field-col-1">
              <label>申请责任人</label>
              <a-input value="李操作 (综合业务组)" disabled></a-input>
            </div>
          </div>

          <!-- 风险与边界提醒条 (防丢草稿重要规则) -->
          <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 4px; padding: 8px 12px; margin-bottom: 14px; font-size: 12px; color: #1e40af; display: flex; align-items: center; gap: 8px;">
            <iconify-icon icon="ant-design:info-circle-filled"></iconify-icon>
            <span><strong>保存边界重要说明：</strong>更改单提交仅保存当前处于活动编辑状态的一侧（应收或应付）。若另一侧有临时草稿，请先切换保存，避免刷新覆盖。</span>
          </div>

          <!-- 更改单费用调整表 -->
          <a-table 
            :data-source="changeOrderFeeList" 
            :columns="feeColumns" 
            size="small" 
            :pagination="false" 
            bordered>
            <template #bodyCell="{ column, record, index }">
              <template v-if="column.key === 'index'">{{ index + 1 }}</template>
              <template v-else-if="column.key === 'source'"><a-tag color="orange">更改单新增</a-tag></template>
              <template v-else-if="column.key === 'action'">
                <a-button type="link" danger size="small" style="padding: 0;">移除</a-button>
              </template>
            </template>
          </a-table>
        </div>

      </div>

      <!-- ========================================== -->
      <!-- 页签 4: 附件管理 (Attachments)              -->
      <!-- ========================================== -->
      <div v-show="activeTabKey === 'attachment'" class="pure-card">
        
        <!-- 空态 A: 暂无附件类型配置 (高保真还原图 06) -->
        <div v-if="attachmentCategories.length === 0" style="text-align: center; padding: 48px 0;">
          <iconify-icon icon="ant-design:folder-open-outlined" style="font-size: 48px; color: #9ca3af; margin-bottom: 12px;"></iconify-icon>
          <div style="font-size: 15px; font-weight: 600; color: #111827; margin-bottom: 6px;">暂无附件类型配置</div>
          <div style="font-size: 13px; color: #6b7280; max-width: 480px; margin: 0 auto 18px auto;">
            当前综合业务尚未配置默认单证类型（如提单、报关单、委托书）。您可以点击下方按钮添加自定义类型。
          </div>
          <a-button type="primary" size="small" @click="openAddAttachTypeModal">
            <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 添加其他类型
          </a-button>
        </div>

        <!-- 状态 B: 已配置附件类型 (高保真还原图 07) -->
        <div v-else>
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #f3f4f6;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-weight: 600; font-size: 14px; color: #111827;">单证附件分类</span>
              <a-tag color="blue">共 {{ attachmentCategories.length }} 种类型</a-tag>
            </div>
            <div>
              <a-button size="small" @click="openAddAttachTypeModal">
                <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 补充附件类型
              </a-button>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 16px;">
            <div v-for="cat in attachmentCategories" :key="cat.id" style="border: 1px solid #e5e7eb; border-radius: 6px; padding: 14px 16px;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600; font-size: 13px; color: #111827; display: flex; align-items: center; gap: 6px;">
                  <iconify-icon icon="ant-design:file-text-outlined" style="color: #1677ff;"></iconify-icon>
                  {{ cat.name }} ({{ cat.files.length }})
                </span>
                <a-upload :show-upload-list="false" :custom-request="handleSimulateUpload(cat)">
                  <a-button size="small">
                    <iconify-icon icon="ant-design:upload-outlined"></iconify-icon> 上传{{ cat.name }}
                  </a-button>
                </a-upload>
              </div>

              <div v-if="cat.files.length === 0" style="padding: 16px 0; text-align: center; color: #9ca3af; font-size: 12px; background: #f9fafb; border-radius: 4px; border: 1px dashed #d1d5db;">
                暂无此分类文件，可将文件直接拖拽至此处
              </div>

              <div v-else style="display: flex; flex-direction: column; gap: 6px;">
                <div v-for="(f, fIdx) in cat.files" :key="fIdx" style="display: flex; align-items: center; justify-content: space-between; background: #f9fafb; padding: 6px 12px; border-radius: 4px; font-size: 12px;">
                  <span style="display: flex; align-items: center; gap: 6px;">
                    <iconify-icon icon="ant-design:paper-clip-outlined" style="color: #6b7280;"></iconify-icon>
                    <strong>{{ f.name }}</strong> ({{ f.size }})
                  </span>
                  <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #9ca3af;">{{ f.uploadTime }} · {{ f.uploader }}</span>
                    <a-button type="link" size="small" style="padding: 0;">预览</a-button>
                    <a-button type="link" size="small" style="padding: 0;">下载</a-button>
                    <a-button type="link" danger size="small" style="padding: 0;" @click="removeFile(cat, fIdx)">移除</a-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- ========================================== -->
    <!-- 弹窗 1: 关联海运主单选择 (Related Order Modal) -->
    <!-- ========================================== -->
    <a-modal 
      v-model:open="isRelatedModalOpen" 
      title="关联海运主单 (最多挂靠一票)" 
      width="780px"
      @ok="confirmRelatedOrder">
      <div style="margin-bottom: 12px; display: flex; gap: 10px;">
        <a-input-search 
          v-model:value="searchMasterKeyword" 
          placeholder="输入海运主单号 / 主提单号 / 客户名称搜索" 
          enter-button 
          style="width: 100%;">
        </a-input-search>
      </div>

      <a-table 
        :data-source="candidateMasterOrders" 
        :columns="masterOrderColumns" 
        size="small" 
        :pagination="false"
        :row-selection="{ type: 'radio', selectedRowKeys: selectedMasterKeys, onChange: onMasterSelectChange }">
      </a-table>

      <div style="margin-top: 12px; font-size: 12px; color: #6b7280; line-height: 1.5;">
        • 关联后仅用于业务组织与上下游穿透查看，综合业务独立核算，财务与费用不与主单合并。<br>
        • 主单仅在初次关联时提供信息参考，后续修改双方不自动同步。
      </div>
    </a-modal>

    <!-- ========================================== -->
    <!-- 弹窗 2: 复制本票业务确认 (高保真还原图 08)   -->
    <!-- ========================================== -->
    <a-modal 
      v-model:open="isCopyModalOpen" 
      title="复制综合业务" 
      width="480px"
      @ok="handleConfirmCopy">
      <div style="margin-bottom: 14px; font-size: 13px; color: #374151;">
        您正在复制业务：<strong>{{ currentData.jobNo }}</strong>
      </div>

      <div style="background: #f9fafb; padding: 12px 14px; border-radius: 4px; border: 1px solid #e5e7eb; margin-bottom: 14px;">
        <div style="font-size: 12px; color: #4b5563; margin-bottom: 6px;">原单凭据核对：</div>
        <div style="font-size: 13px; font-weight: 600; color: #111827;">{{ currentData.customerName }}</div>
        <div style="font-size: 12px; color: #6b7280;">{{ currentData.vesselVoyage }}</div>
      </div>

      <div style="margin-bottom: 14px;">
        <a-checkbox v-model:checked="isCopyFeeChecked">
          <span style="font-weight: 500; color: #111827;">同时复制原票应收应付费用</span>
        </a-checkbox>
        <div style="font-size: 12px; color: #9ca3af; margin-left: 24px; margin-top: 2px;">
          默认不勾选费用；复制只基于服务器已保存数据，不继承关联主单与本地草稿。
        </div>
      </div>
    </a-modal>

    <!-- ========================================== -->
    <!-- 弹窗 3: 补充附件类型 (高保真还原图 07)       -->
    <!-- ========================================== -->
    <a-modal 
      v-model:open="isAttachTypeModalOpen" 
      title="选择或添加附件类型" 
      width="460px"
      @ok="confirmAddAttachType">
      <div style="margin-bottom: 12px;">
        <label style="display: block; font-size: 12px; font-weight: 500; color: #374151; margin-bottom: 6px;">预设单证类型</label>
        <a-select v-model:value="selectedPresetAttachType" style="width: 100%;" placeholder="从标准单证字典选择">
          <a-select-option value="提单文件 (Bill of Lading)">提单文件 (Bill of Lading)</a-select-option>
          <a-select-option value="报关单证 (Customs Declaration)">报关单证 (Customs Declaration)</a-select-option>
          <a-select-option value="费用凭证 (Expense Receipt)">费用凭证 (Expense Receipt)</a-select-option>
          <a-select-option value="客户委托书 (Booking Note)">客户委托书 (Booking Note)</a-select-option>
        </a-select>
      </div>

      <div>
        <label style="display: block; font-size: 12px; font-weight: 500; color: #374151; margin-bottom: 6px;">或输入自定义类型名称</label>
        <a-input v-model:value="customAttachTypeName" placeholder="如：保税仓入库单"></a-input>
      </div>
    </a-modal>

  </div>
</div>

<script>
  const { createApp, ref, reactive, computed } = Vue;

  // 模拟全量测试数据集
  const mockOrders = [
    {
      jobNo: 'TEST130-0003',
      accountingPeriod: '2026-11',
      settlementDate: '2026-11-06',
      salesOrgName: '佳越国际物流有限公司',
      businessSource: '自揽货',
      customerName: '宁波万达进出口有限公司',
      customerId: 'CUST001',
      contactPerson: '张经理',
      businessNo: 'TEST130-0003',
      contractNo: 'HT-202611-09',
      carrier: 'SITC',
      vessel: 'SITC HEFEI',
      voyage: '2412N',
      vesselVoyage: 'SITC HEFEI / 2412N',
      truckingCompany: '宁波港通集卡物流有限公司',
      mblNo: 'SITC2412N001',
      bookingNo: 'BK20261106-01',
      customsInvoiceNo: 'INV-998231',
      cargoType: 'NORMAL',
      trafficTerms: 'CY-CY',
      tradeTerms: 'FOB',
      paymentTerm: 'PP',
      paymentPlace: 'NINGBO',
      insuranceCompany: 'PICC',
      customsBroker: 'DASHUN',
      warehouse: 'WH01',
      internalRefNo: 'REF-NB-2026',
      // 收发通
      shipperId: 'SH01',
      shipperText: 'NINGBO WANDA EXPORT CO., LTD.\\nNO. 88 CENTURY AVENUE, NINGBO, CHINA\\nTEL: +86-574-88889999',
      consigneeId: 'TO_ORDER',
      consigneeText: 'TO ORDER',
      notifyPartyId: 'SAME_AS',
      notifyPartyText: 'SAME AS CONSIGNEE',
      // 船期与港口
      cargoReadyDate: dayjs('2026-11-06 00:00:00'),
      etd: dayjs('2026-11-09'),
      atd: null,
      eta: dayjs('2026-11-18'),
      polPort: 'CNNBG - 宁波 (NINGBO)',
      podPort: 'JPTYO - 东京 (TOKYO)',
      routeDescription: '日本关东直达快线 / JAPAN',
      // 货物
      commodityName: '日用小家电 (Small Home Appliances)',
      shippingMarks: 'N/M',
      goodsDescription: 'ELECTRONIC APPLIANCES WITH BATTERIES (NORMAL CARGO)',
      pieces: 500,
      packageType: 'CTNS',
      grossWeight: 4500.000,
      volume: 18.500,
      internalRemark: '客户要求周五前必须放行，注意集卡排队情况。',
      externalRemark: '请目的港代理凭正本提单换单放货。',
      // 干系人
      salesPersonId: 'U101',
      salesOrgId: 'ORG01',
      operatorId: 'OP01',
      customerServiceId: 'CS01',
      bookingPersonId: 'BK01',
      financialPersonId: 'FN01',
      // 状态
      isLocked: false,
      isFeeLocked: false,
      relatedMasterOrder: null
    },
    {
      jobNo: 'TEST130-0004',
      accountingPeriod: '2026-11',
      settlementDate: '2026-11-10',
      salesOrgName: '佳越国际物流有限公司',
      businessSource: '指定货',
      customerName: '浙江吉利汽车零部件制造',
      customerId: 'CUST002',
      contactPerson: '王业务',
      businessNo: 'GEELY-2026-08',
      contractNo: 'GL-9901',
      carrier: 'COSCO',
      vessel: 'COSCO SHIPPING PLANET',
      voyage: '042W',
      vesselVoyage: 'COSCO SHIPPING PLANET / 042W',
      truckingCompany: '吉利恒顺物流',
      mblNo: 'COSU63281900',
      bookingNo: 'CO-NB-8821',
      customsInvoiceNo: 'INV-GL-1102',
      cargoType: 'NORMAL',
      trafficTerms: 'CY-DOOR',
      tradeTerms: 'CIF',
      paymentTerm: 'PP',
      paymentPlace: 'NINGBO',
      insuranceCompany: 'PINGAN',
      customsBroker: 'XINTONG',
      warehouse: 'WH02',
      internalRefNo: 'REF-GEELY-01',
      shipperId: 'SH02',
      shipperText: 'ZHEJIANG AUTO PARTS INDUSTRY CO., LTD.',
      consigneeId: 'CN01',
      consigneeText: 'PACIFIC LOGISTICS (JAPAN) CO., LTD.\\nTOKYO PORT TERMINAL 3',
      notifyPartyId: 'NP01',
      notifyPartyText: 'EASTERN TRADING NOTIFY AGENCY',
      cargoReadyDate: dayjs('2026-11-08 12:00:00'),
      etd: dayjs('2026-11-12'),
      atd: null,
      eta: dayjs('2026-11-22'),
      polPort: 'CNNBG - 宁波 (NINGBO)',
      podPort: 'JPYOK - 横滨 (YOKOHAMA)',
      routeDescription: '横滨定期班轮',
      commodityName: '汽车冲压钣金件',
      shippingMarks: 'GEELY / TOKYO',
      goodsDescription: 'AUTO PARTS IN PALLETS',
      pieces: 120,
      packageType: 'PLTS',
      grossWeight: 8200.000,
      volume: 32.000,
      internalRemark: '已锁账票据，仅供核账查询。',
      externalRemark: '',
      salesPersonId: 'U102',
      salesOrgId: 'ORG01',
      operatorId: 'OP02',
      customerServiceId: 'CS02',
      bookingPersonId: 'BK01',
      financialPersonId: 'FN01',
      isLocked: true,
      isFeeLocked: true,
      relatedMasterOrder: {
        type: '海出',
        no: 'EXP2026110001',
        customer: '吉利汽车'
      }
    }
  ];

  const app = createApp({
    setup() {
      // 场景沙盘
      const selectedScenario = ref('standard');
      const isEmbeddedMode = ref(false);
      const isDirty = ref(false);
      const isSaving = ref(false);

      // 当前业务数据
      const orderIndex = ref(0);
      const totalOrders = ref(mockOrders.length);
      const currentData = reactive({ ...mockOrders[0] });

      // 当前激活页签
      const activeTabKey = ref('basic');

      // 收发通收起状态 (默认收起，符合高密标准)
      const isShouFaExpanded = ref(false);

      // 组织联动选项
      const availableOrgs = ref([
        { id: 'ORG01', name: '佳越国际物流有限公司' },
        { id: 'ORG02', name: '佳越供应链上海分公司' }
      ]);

      // 费用合并更改单状态
      const isFeeMergeReadonly = ref(false);

      // 应收费用列表
      const receivableList = ref([
        {
          key: 'r1',
          source: '本票原始',
          feeItem: '拖车费',
          settlementUnit: '宁波万达进出口有限公司',
          currency: 'CNY',
          exchangeRate: 1.0000,
          unitPrice: 1800.00,
          quantity: 1,
          taxRate: 6,
          amountWithTax: 1800.00,
          amountWithoutTax: 1698.11,
          taxAmount: 101.89,
          billingStatus: '未开票'
        },
        {
          key: 'r2',
          source: '本票原始',
          feeItem: '报关代理费',
          settlementUnit: '宁波万达进出口有限公司',
          currency: 'CNY',
          exchangeRate: 1.0000,
          unitPrice: 350.00,
          quantity: 1,
          taxRate: 6,
          amountWithTax: 350.00,
          amountWithoutTax: 330.19,
          taxAmount: 19.81,
          billingStatus: '未开票'
        }
      ]);

      // 应付费用列表
      const payableList = ref([
        {
          key: 'p1',
          source: '本票原始',
          feeItem: '拖车费',
          settlementUnit: '宁波港通集卡物流有限公司',
          currency: 'CNY',
          exchangeRate: 1.0000,
          unitPrice: 1500.00,
          quantity: 1,
          taxRate: 9,
          amountWithTax: 1500.00,
          amountWithoutTax: 1376.15,
          taxAmount: 123.85,
          billingStatus: '未开票'
        },
        {
          key: 'p2',
          source: '本票原始',
          feeItem: '报关代理费',
          settlementUnit: '宁波达顺报关服务有限公司',
          currency: 'CNY',
          exchangeRate: 1.0000,
          unitPrice: 200.00,
          quantity: 1,
          taxRate: 6,
          amountWithTax: 200.00,
          amountWithoutTax: 188.68,
          taxAmount: 11.32,
          billingStatus: '未开票'
        }
      ]);

      // 费用表格列配置 (18列标准生产级结构)
      const feeColumns = [
        { title: '#', key: 'index', width: 45, fixed: 'left' },
        { title: '来源', key: 'source', width: 90, fixed: 'left' },
        { title: '费用科目', key: 'feeItem', width: 160 },
        { title: '收付款单位 (结算对象)', key: 'settlementUnit', width: 220 },
        { title: '币别', key: 'currency', width: 90 },
        { title: '单价', key: 'unitPrice', width: 110, align: 'right' },
        { title: '数量', key: 'quantity', width: 90, align: 'right' },
        { title: '税率', key: 'taxRate', width: 90, align: 'right' },
        { title: '含税金额', key: 'amountWithTax', width: 120, align: 'right' },
        { title: '开票状态', key: 'billingStatus', width: 100 },
        { title: '操作', key: 'action', width: 70, fixed: 'right' }
      ];

      // 费用统计汇总
      const totalReceivable = computed(() => {
        return receivableList.value.reduce((acc, cur) => acc + (cur.amountWithTax || 0), 0);
      });
      const totalPayable = computed(() => {
        return payableList.value.reduce((acc, cur) => acc + (cur.amountWithTax || 0), 0);
      });
      const totalProfit = computed(() => {
        return totalReceivable.value - totalPayable.value;
      });

      // 更改单相关数据
      const selectedChangeOrderId = ref('CO-202611-001');
      const changeOrderReason = ref('目的港查验产生额外堆存理货规费，客户已邮件确认补贴');
      const changeOrderFeeList = ref([
        {
          key: 'co1',
          source: '更改单',
          feeItem: '港杂费',
          settlementUnit: '宁波港通集卡物流有限公司',
          currency: 'CNY',
          unitPrice: 400.00,
          quantity: 1,
          taxRate: 6,
          amountWithTax: 400.00,
          billingStatus: '未开票'
        }
      ]);

      // 附件数据
      const attachmentCategories = ref([
        {
          id: 'cat1',
          name: '提单与运输单证',
          files: [
            { name: 'SITC2412N001_Draft_MBL.pdf', size: '248 KB', uploadTime: '2026-11-06 14:20', uploader: '张晓华' }
          ]
        },
        {
          id: 'cat2',
          name: '报关发票与装箱单',
          files: []
        }
      ]);

      const attachmentCount = computed(() => {
        return attachmentCategories.value.reduce((acc, cur) => acc + cur.files.length, 0);
      });

      // 弹窗状态
      const isRelatedModalOpen = ref(false);
      const isCopyModalOpen = ref(false);
      const isCopyFeeChecked = ref(false);
      const isAttachTypeModalOpen = ref(false);
      const selectedPresetAttachType = ref('提单文件 (Bill of Lading)');
      const customAttachTypeName = ref('');

      // 关联主单弹窗数据
      const searchMasterKeyword = ref('');
      const selectedMasterKeys = ref([]);
      const candidateMasterOrders = ref([
        { key: '1', type: '海出', no: 'EXP2026110001', customer: '宁波万达进出口', pol: '宁波', pod: '东京', etd: '2026-11-09' },
        { key: '2', type: '海出', no: 'EXP2026110002', customer: '浙江吉利汽车', pol: '宁波', pod: '横滨', etd: '2026-11-12' },
        { key: '3', type: '海进', no: 'IMP2026110018', customer: '义乌华贸供应链', pol: '汉堡', pod: '宁波', etd: '2026-11-02' }
      ]);
      const masterOrderColumns = [
        { title: '业务类型', dataIndex: 'type', key: 'type', width: 90 },
        { title: '主单编号', dataIndex: 'no', key: 'no', width: 140 },
        { title: '客户单位', dataIndex: 'customer', key: 'customer' },
        { title: '起运/目的港', key: 'route', customRender: ({ record }) => `${record.pol} → ${record.pod}` },
        { title: '离港日期', dataIndex: 'etd', key: 'etd', width: 110 }
      ];

      // 方法定义
      const markDirty = () => {
        isDirty.value = true;
      };

      const handleCustomerChange = (val) => {
        markDirty();
        if (val === 'CUST001') {
          currentData.customerName = '宁波万达进出口有限公司';
          currentData.contactPerson = '张经理';
        } else if (val === 'CUST002') {
          currentData.customerName = '浙江吉利汽车零部件制造';
          currentData.contactPerson = '王业务';
        }
      };

      const handleSalesChange = (val) => {
        markDirty();
        if (val === 'U101') {
          availableOrgs.value = [{ id: 'ORG01', name: '佳越国际物流有限公司' }];
          currentData.salesOrgId = 'ORG01';
          currentData.salesOrgName = '佳越国际物流有限公司';
        } else {
          availableOrgs.value = [
            { id: 'ORG01', name: '佳越国际物流有限公司' },
            { id: 'ORG02', name: '佳越供应链上海分公司' }
          ];
        }
      };

      const regenerateJobNo = () => {
        const rand = Math.floor(1000 + Math.random() * 9000);
        currentData.jobNo = `TEST130-${rand}`;
        antd.message.success(`委托编号已重新生成为 ${currentData.jobNo}`);
      };

      const handlePrevOrder = () => {
        if (orderIndex.value > 0) {
          orderIndex.value--;
          Object.assign(currentData, mockOrders[orderIndex.value]);
          isDirty.value = false;
          antd.message.info(`已切换至业务 ${currentData.jobNo}`);
        }
      };

      const handleNextOrder = () => {
        if (orderIndex.value < totalOrders.value - 1) {
          orderIndex.value++;
          Object.assign(currentData, mockOrders[orderIndex.value]);
          isDirty.value = false;
          antd.message.info(`已切换至业务 ${currentData.jobNo}`);
        }
      };

      const reloadOrder = () => {
        Object.assign(currentData, mockOrders[orderIndex.value]);
        isDirty.value = false;
        antd.message.success('已重新从服务器加载业务数据');
      };

      const saveBasicInfo = () => {
        isSaving.value = true;
        setTimeout(() => {
          isSaving.value = false;
          isDirty.value = false;
          antd.message.success('基础信息已成功保存！');
        }, 600);
      };

      const saveFeeInfo = () => {
        isSaving.value = true;
        setTimeout(() => {
          isSaving.value = false;
          antd.message.success('应收应付费用已成功提交入库！');
        }, 600);
      };

      const handleToggleMergeReadonly = () => {
        if (isFeeMergeReadonly.value) {
          antd.message.warning('合并模式已开启：包含更改单数据，整页费用已置为只读');
        } else {
          antd.message.info('已恢复为本票费用编辑模式');
        }
      };

      const addReceivableRow = () => {
        receivableList.value.push({
          key: `r_${Date.now()}`,
          source: '本票原始',
          feeItem: '拖车费',
          settlementUnit: currentData.customerName || '宁波万达进出口有限公司',
          currency: 'CNY',
          exchangeRate: 1.0,
          unitPrice: 500.0,
          quantity: 1,
          taxRate: 6,
          amountWithTax: 500.0,
          billingStatus: '未开票'
        });
        antd.message.success('已新增一行应收费用');
      };

      const removeReceivableRow = (idx) => {
        receivableList.value.splice(idx, 1);
        antd.message.success('已移除该应收项目');
      };

      const addPayableRow = () => {
        payableList.value.push({
          key: `p_${Date.now()}`,
          source: '本票原始',
          feeItem: '仓储费',
          settlementUnit: '佳越北仑保税1号仓',
          currency: 'CNY',
          exchangeRate: 1.0,
          unitPrice: 300.0,
          quantity: 1,
          taxRate: 6,
          amountWithTax: 300.0,
          billingStatus: '未开票'
        });
        antd.message.success('已新增一行应付费用');
      };

      const removePayableRow = (idx) => {
        payableList.value.splice(idx, 1);
        antd.message.success('已移除该应付项目');
      };

      const recalcRow = (record) => {
        const u = record.unitPrice || 0;
        const q = record.quantity || 0;
        const t = (record.taxRate || 0) / 100;
        record.amountWithTax = u * q;
        record.amountWithoutTax = Number((record.amountWithTax / (1 + t)).toFixed(2));
        record.taxAmount = Number((record.amountWithTax - record.amountWithoutTax).toFixed(2));
      };

      const simulateFeeLock = () => {
        currentData.isFeeLocked = true;
        antd.message.success('模拟成功：本票原费用已进入锁账状态，更改单前置条件已解锁！');
      };

      const saveChangeOrderSingleSide = () => {
        antd.Modal.confirm({
          title: '确认提交更改单当前侧费用',
          content: '根据业务规范，更改单保存仅提交当前编辑侧费用，若另一侧存在临时改动将不会一并提交。确定继续？',
          onOk() {
            antd.message.success('更改单及当前侧费用已成功提交！');
          }
        });
      };

      // 附件操作
      const openAddAttachTypeModal = () => {
        isAttachTypeModalOpen.value = true;
      };

      const confirmAddAttachType = () => {
        const name = customAttachTypeName.value.trim() || selectedPresetAttachType.value;
        attachmentCategories.value.push({
          id: `cat_${Date.now()}`,
          name: name,
          files: []
        });
        customAttachTypeName.value = '';
        isAttachTypeModalOpen.value = false;
        antd.message.success(`已成功添加「${name}」分类`);
      };

      const handleSimulateUpload = (cat) => {
        return (options) => {
          setTimeout(() => {
            cat.files.push({
              name: options.file.name || '业务单据扫描件.pdf',
              size: '320 KB',
              uploadTime: dayjs().format('YYYY-MM-DD HH:mm'),
              uploader: '当前用户'
            });
            options.onSuccess();
            antd.message.success(`文件上传并关联至「${cat.name}」成功`);
          }, 500);
        };
      };

      const removeFile = (cat, idx) => {
        cat.files.splice(idx, 1);
        antd.message.success('已解除该附件关联');
      };

      // 复制业务
      const openCopyModal = () => {
        isCopyFeeChecked.value = false;
        isCopyModalOpen.value = true;
      };

      const handleConfirmCopy = () => {
        isCopyModalOpen.value = false;
        antd.message.loading('正在创建新票据...', 1).then(() => {
          antd.message.success(`已基于 ${currentData.jobNo} 复制生成新综合业务 TEST130-9999`);
        });
      };

      // 关联主单
      const openRelatedOrderModal = () => {
        isRelatedModalOpen.value = true;
      };

      const onMasterSelectChange = (keys) => {
        selectedMasterKeys.value = keys;
      };

      const confirmRelatedOrder = () => {
        if (selectedMasterKeys.value.length === 0) {
          antd.message.warning('请选择需要关联的海运主单');
          return;
        }
        const selected = candidateMasterOrders.value.find(item => item.key === selectedMasterKeys.value[0]);
        if (selected) {
          currentData.relatedMasterOrder = {
            type: selected.type,
            no: selected.no,
            customer: selected.customer
          };
          isRelatedModalOpen.value = false;
          markDirty();
          antd.message.success(`已关联主单：${selected.no}`);
        }
      };

      const unlinkMasterOrder = () => {
        currentData.relatedMasterOrder = null;
        markDirty();
        antd.message.info('已解除海运主单关联');
      };

      // 场景沙盘切换
      const switchScenario = (e) => {
        const sc = e.target.value;
        if (sc === 'standard') {
          Object.assign(currentData, mockOrders[0]);
          currentData.isLocked = false;
          currentData.isFeeLocked = false;
          activeTabKey.value = 'basic';
          attachmentCategories.value = [
            { id: 'c1', name: '提单与运输单证', files: [{ name: 'SITC2412N001_Draft_MBL.pdf', size: '248 KB', uploadTime: '2026-11-06 14:20', uploader: '张晓华' }] },
            { id: 'c2', name: '报关发票与装箱单', files: [] }
          ];
        } else if (sc === 'empty') {
          Object.assign(currentData, {
            jobNo: 'TEST130-0005',
            accountingPeriod: '2026-11',
            settlementDate: '2026-11-07',
            salesOrgName: '佳越国际物流有限公司',
            businessSource: '自揽货',
            customerName: '',
            customerId: undefined,
            contactPerson: undefined,
            businessNo: '',
            contractNo: '',
            carrier: undefined,
            vessel: '',
            voyage: '',
            vesselVoyage: '暂无船舶航次',
            truckingCompany: '',
            mblNo: '',
            bookingNo: '',
            customsInvoiceNo: '',
            cargoType: 'NORMAL',
            trafficTerms: undefined,
            tradeTerms: undefined,
            paymentTerm: undefined,
            paymentPlace: '',
            insuranceCompany: undefined,
            customsBroker: undefined,
            warehouse: undefined,
            internalRefNo: '',
            shipperId: undefined,
            shipperText: '',
            consigneeId: undefined,
            consigneeText: '',
            notifyPartyId: undefined,
            notifyPartyText: '',
            cargoReadyDate: null,
            etd: null,
            atd: null,
            eta: null,
            polPort: undefined,
            podPort: undefined,
            routeDescription: '',
            commodityName: '',
            shippingMarks: '',
            goodsDescription: '',
            pieces: null,
            packageType: undefined,
            grossWeight: null,
            volume: null,
            internalRemark: '',
            externalRemark: '',
            salesPersonId: 'U101',
            salesOrgId: 'ORG01',
            operatorId: undefined,
            customerServiceId: undefined,
            bookingPersonId: undefined,
            financialPersonId: undefined,
            isLocked: false,
            isFeeLocked: false,
            relatedMasterOrder: null
          });
          receivableList.value = [];
          payableList.value = [];
          activeTabKey.value = 'basic';
        } else if (sc === 'locked') {
          Object.assign(currentData, mockOrders[1]);
          activeTabKey.value = 'basic';
        } else if (sc === 'co_blocked') {
          Object.assign(currentData, mockOrders[0]);
          currentData.isFeeLocked = false;
          activeTabKey.value = 'changeOrder';
        } else if (sc === 'attach_empty') {
          Object.assign(currentData, mockOrders[0]);
          attachmentCategories.value = [];
          activeTabKey.value = 'attachment';
        }
      };

      const resetCurrentData = () => {
        Object.assign(currentData, mockOrders[orderIndex.value]);
        isDirty.value = false;
        antd.message.success('测试数据已重置');
      };

      return {
        selectedScenario,
        isEmbeddedMode,
        isDirty,
        isSaving,
        orderIndex,
        totalOrders,
        currentData,
        activeTabKey,
        isShouFaExpanded,
        availableOrgs,
        isFeeMergeReadonly,
        receivableList,
        payableList,
        feeColumns,
        totalReceivable,
        totalPayable,
        totalProfit,
        selectedChangeOrderId,
        changeOrderReason,
        changeOrderFeeList,
        attachmentCategories,
        attachmentCount,
        isRelatedModalOpen,
        isCopyModalOpen,
        isCopyFeeChecked,
        isAttachTypeModalOpen,
        selectedPresetAttachType,
        customAttachTypeName,
        searchMasterKeyword,
        selectedMasterKeys,
        candidateMasterOrders,
        masterOrderColumns,
        markDirty,
        handleCustomerChange,
        handleSalesChange,
        regenerateJobNo,
        handlePrevOrder,
        handleNextOrder,
        reloadOrder,
        saveBasicInfo,
        saveFeeInfo,
        handleToggleMergeReadonly,
        addReceivableRow,
        removeReceivableRow,
        addPayableRow,
        removePayableRow,
        recalcRow,
        simulateFeeLock,
        saveChangeOrderSingleSide,
        openAddAttachTypeModal,
        confirmAddAttachType,
        handleSimulateUpload,
        removeFile,
        openCopyModal,
        handleConfirmCopy,
        openRelatedOrderModal,
        onMasterSelectChange,
        confirmRelatedOrder,
        unlinkMasterOrder,
        switchScenario,
        resetCurrentData
      };
    }
  });

  app.use(antd);
  app.mount('#app');
</script>
</body>
</html>
'''

with open('pages/comprehensive-business-edit.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Comprehensive Business Edit page generated successfully. Size:", len(html_content))
