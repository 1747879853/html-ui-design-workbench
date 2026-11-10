import os
import json

output_path = os.path.abspath('pages/comprehensive-business-edit.html')

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>综合业务编辑工作台 - 操作管理 (#178 左右双轨交互与右侧Tab融合优化)</title>

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
       综合业务编辑工作台 (#178 左右双轨 + 右侧Tab融合 + 业务航向动线亮点)
       设计基准：1920×1080 视口，左侧业务档案持续常驻，右侧工作区Tab随心切换
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

    /* 顶部原型审查沙盘控制器 (深色石板高对比沙盘条，与真实业务顶栏形成清晰视觉分层) */
    .scenario-toolbar {
      background: #0f172a;
      color: #cbd5e1;
      padding: 5px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #1e293b;
      border-left: 4px solid #0284c7;
      font-size: 12px;
      z-index: 100;
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
      background: rgba(2, 132, 199, 0.2);
      color: #38bdf8;
      font-weight: 600;
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 4px;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .scenario-toolbar .ant-radio-button-wrapper {
      background: #1e293b !important;
      border-color: #334155 !important;
      color: #cbd5e1 !important;
      font-size: 11px !important;
      height: 22px !important;
      line-height: 20px !important;
      padding: 0 8px !important;
    }
    .scenario-toolbar .ant-radio-button-wrapper:hover {
      color: #38bdf8 !important;
    }
    .scenario-toolbar .ant-radio-button-wrapper-checked {
      background: #0284c7 !important;
      border-color: #0284c7 !important;
      color: #ffffff !important;
      font-weight: 600 !important;
      box-shadow: none !important;
    }
    .scenario-toolbar .ant-radio-button-wrapper::before {
      background-color: #334155 !important;
    }
    .scenario-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* 顶层认票身份与状态驾驶舱 (Ticket Identity Cockpit Header) */
    .wb-header {
      background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
      padding: 6px 16px;
      border-bottom: 1px solid #dbe2ea;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }
    .wb-header-left {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }
    .cockpit-avatar {
      width: 34px;
      height: 34px;
      border-radius: 6px;
      background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
      border: 1px solid #bfdbfe;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #1d4ed8;
      font-size: 18px;
      flex-shrink: 0;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8);
    }
    .cockpit-identity-stack {
      display: flex;
      flex-direction: column;
      gap: 2px;
      min-width: 0;
    }
    .cockpit-row-primary {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .wb-job-no {
      font-size: 15px;
      font-weight: 800;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", Roboto, monospace;
      letter-spacing: 0.3px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .status-glow-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 11px;
      font-weight: 600;
      padding: 1px 8px;
      border-radius: 10px;
      line-height: 18px;
    }
    .status-glow-pill.is-editable {
      background: #ecfdf5;
      color: #059669;
      border: 1px solid #a7f3d0;
    }
    .status-glow-pill.is-locked {
      background: #fef2f2;
      color: #dc2626;
      border: 1px solid #fecaca;
    }
    .bl-identity-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      padding: 1px 7px;
      font-size: 11px;
      color: #334155;
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", monospace;
    }
    .bl-identity-badge strong {
      color: #0f172a;
      font-weight: 700;
    }
    .cockpit-row-secondary {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 11px;
      color: #64748b;
      flex-wrap: wrap;
    }
    .meta-crumb-item {
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .meta-crumb-item strong {
      color: #1e293b;
      font-weight: 600;
    }
    .meta-crumb-sep {
      color: #cbd5e1;
      font-size: 10px;
    }
    .dirty-pill {
      background: #fffbeb;
      border: 1px solid #fde68a;
      color: #d97706;
      font-size: 11px;
      padding: 0 7px;
      height: 19px;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-weight: 600;
    }
    .wb-header-right {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }

    /* ==========================================================================
       页面主体双轨视口 (左常驻业务底账 + 右侧多Tab工作区)
       ========================================================================== */
    .dual-rail-workbench {
      flex: 1;
      display: flex;
      overflow: hidden;
      padding: 6px;
      gap: 6px;
      box-sizing: border-box;
      background: #e6eaf0;
      height: calc(100vh - 84px);
    }

    /* ==========================================================================
       左轨：420px 独立常驻业务底账舱 (Smart Business Master Dossier Cockpit)
       ========================================================================== */
    .left-business-panel {
      width: 420px;
      flex-shrink: 0;
      background: #f3f5f8;
      border-radius: 6px;
      border: 1px solid #cfd6e0;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .panel-header-bar {
      height: 38px;
      padding: 0 12px;
      background: #ffffff;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .panel-title-wrap {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .panel-title {
      font-size: 13px;
      font-weight: 700;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .panel-actions {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* 吸顶分舱导航与齐套度指示条 (Dossier Quick Anchor & Telemetry Bar) */
    .dossier-nav-strip {
      height: 28px;
      padding: 0 10px;
      background: #f8fafc;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .dossier-nav-pills {
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .dossier-nav-pill {
      font-size: 11px;
      color: #475569;
      padding: 1px 5px;
      border-radius: 3px;
      cursor: pointer;
      transition: all 0.15s;
      font-weight: 500;
      display: inline-flex;
      align-items: center;
      gap: 2px;
      user-select: none;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .dossier-nav-pill:hover {
      background: #e2e8f0;
      color: #0f172a;
    }
    .dossier-nav-pill.is-active {
      background: #eff6ff;
      color: #1d4ed8;
      font-weight: 600;
      border: 1px solid #bfdbfe;
    }
    .dossier-completeness {
      font-size: 10px;
      color: #059669;
      background: #ecfdf5;
      border: 1px solid #a7f3d0;
      border-radius: 10px;
      padding: 0 6px;
      line-height: 16px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 3px;
      white-space: nowrap;
      flex-shrink: 0;
    }

    /* 左侧档案模块化画布滚动体 */
    .business-form-scroll {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 8px 8px 18px 8px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .business-form-scroll::-webkit-scrollbar {
      width: 4px;
    }
    .business-form-scroll::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 2px;
    }

    /* 独立业务档案分舱卡片 (Modular Dossier Sub-Card) */
    .dossier-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 9px 11px 11px 11px;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02);
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .dossier-card:hover {
      border-color: #cbd5e1;
    }
    .dossier-card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
      padding-bottom: 5px;
      border-bottom: 1px solid #f1f5f9;
    }
    .dossier-card-title {
      font-size: 12px;
      font-weight: 700;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .sec-idx-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 18px;
      height: 16px;
      border-radius: 3px;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1d4ed8;
      font-size: 10px;
      font-weight: 800;
      font-family: monospace;
    }
    .dossier-card-extra {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      color: #64748b;
    }
    .card-action-link {
      font-size: 11px;
      color: #1677ff;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-weight: 500;
      padding: 1px 5px;
      border-radius: 3px;
      background: #f0f7ff;
      border: 1px solid #bae0ff;
      transition: all 0.15s;
    }
    .card-action-link:hover {
      background: #e0f2fe;
      border-color: #7dd3fc;
      color: #0284c7;
    }

    /* 🌟 创新 1: 三格高密度财务与单据底账条 (3-Cell Ledger Meta Strip) */
    .ledger-meta-strip {
      grid-column: span 2;
      display: grid;
      grid-template-columns: 1.25fr 0.85fr 0.95fr;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      margin-bottom: 2px;
      overflow: hidden;
    }
    .ledger-cell {
      padding: 5px 8px;
      display: flex;
      flex-direction: column;
      gap: 2px;
      border-right: 1px solid #e2e8f0;
      min-width: 0;
    }
    .ledger-cell:last-child {
      border-right: none;
    }
    .ledger-cell-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 10px;
      color: #64748b;
      line-height: 14px;
    }
    .ledger-cell-val {
      font-size: 12px;
      font-weight: 700;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", monospace;
      display: flex;
      align-items: center;
      justify-content: space-between;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
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
      color: #4b5563;
      display: flex;
      align-items: center;
      justify-content: space-between;
      line-height: 16px;
      margin-bottom: 1px;
      white-space: nowrap;
    }
    .biz-label-title {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-weight: 600;
      color: #334155;
    }
    .biz-label-title.is-required::before {
      content: '*';
      color: #ff4d4f;
      font-weight: bold;
      font-size: 12px;
      line-height: 1;
    }
    .biz-label-hint {
      font-size: 10px;
      color: #94a3b8;
      font-weight: normal;
    }
    .customer-credit-pill {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      background: #fff7ed;
      border: 1px solid #fed7aa;
      color: #c2410c;
      font-size: 10px;
      font-weight: 600;
      padding: 0 5px;
      height: 16px;
      line-height: 14px;
      border-radius: 3px;
    }

    /* 🌟 创新 2: 关联主单交互式存根票卡 (Interactive Master Order Ticket Stub) */
    .master-ticket-stub {
      background: linear-gradient(180deg, #f0f7ff 0%, #f8fafc 100%);
      border: 1px solid #93c5fd;
      border-radius: 5px;
      overflow: hidden;
    }
    .stub-main-row {
      padding: 5px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      border-bottom: 1px dashed #bfdbfe;
    }
    .stub-type-badge {
      background: #1d4ed8;
      color: #ffffff;
      font-size: 10px;
      font-weight: 600;
      padding: 1px 5px;
      border-radius: 3px;
      flex-shrink: 0;
    }
    .stub-order-no {
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", monospace;
      font-weight: 700;
      color: #1e3a8a;
      font-size: 12px;
    }
    .stub-sync-bar {
      padding: 4px 8px;
      background: rgba(255, 255, 255, 0.75);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      font-size: 10px;
      color: #475569;
    }
    .stub-sync-btn {
      font-size: 10px;
      color: #0284c7;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 3px;
      padding: 1px 6px;
      border-radius: 3px;
      background: #e0f2fe;
      border: 1px solid #7dd3fc;
      transition: all 0.15s;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .stub-sync-btn:hover {
      background: #0284c7;
      color: #ffffff;
      border-color: #0284c7;
    }

    .master-unlink-icon {
      color: #94a3b8;
      cursor: pointer;
      font-size: 12px;
      padding: 2px 4px;
      border-radius: 2px;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
    }
    .master-unlink-icon:hover {
      color: #ef4444;
      background: rgba(239, 68, 68, 0.08);
    }
    .role-remove-icon {
      color: #94a3b8;
      cursor: pointer;
      font-size: 11px;
      padding: 0 2px;
      line-height: 1;
      display: inline-flex;
      align-items: center;
      transition: color 0.2s;
    }
    .role-remove-icon:hover {
      color: #ef4444;
    }
    .order-pager-wrap {
      display: inline-flex;
      align-items: center;
      gap: 2px;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      padding: 1px 3px;
    }
    .order-pager-num {
      font-size: 11px;
      font-weight: 700;
      color: #334155;
      padding: 0 6px;
      font-family: monospace;
    }

    /* 🌟 创新 3: 团队协作胶囊矩阵 (In-Place Collaborative Team Capsule Matrix) */
    .team-matrix-box {
      grid-column: span 2;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 6px 8px;
      margin-top: 2px;
    }
    .team-matrix-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 5px;
      font-size: 11px;
      color: #475569;
    }
    .quick-role-chips {
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .quick-role-chip {
      font-size: 10px;
      color: #475569;
      background: #ffffff;
      border: 1px dashed #cbd5e1;
      padding: 0 5px;
      height: 18px;
      line-height: 16px;
      border-radius: 3px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .quick-role-chip:hover {
      color: #1677ff;
      border-color: #1677ff;
      background: #eff6ff;
    }
    .team-capsule-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 6px;
    }
    .role-capsule-item {
      display: flex;
      align-items: center;
      background: #ffffff;
      border: 1px solid #dbe2ea;
      border-radius: 4px;
      padding: 1px 4px 1px 6px;
      height: 26px;
      gap: 4px;
      min-width: 0;
    }
    .role-badge-tag {
      font-size: 10px;
      font-weight: 600;
      color: #0369a1;
      background: #e0f2fe;
      padding: 1px 4px;
      border-radius: 2px;
      flex-shrink: 0;
    }
    .role-capsule-item .ant-select {
      flex: 1;
      min-width: 0;
    }
    .role-capsule-item .ant-select-selector {
      border: none !important;
      box-shadow: none !important;
      background: transparent !important;
      padding: 0 2px !important;
      font-size: 11px !important;
    }

    /* 🌟 创新 4: 融合式登机牌航线与起目港直选器 (Fused Boarding-Pass Route & Port Selector) */
    .boarding-route-selector {
      grid-column: span 2;
      background: linear-gradient(135deg, #f0fdfa 0%, #f0f9ff 100%);
      border: 1px solid #99f6e4;
      border-radius: 5px;
      padding: 7px 9px 8px 9px;
      margin-bottom: 2px;
    }
    .boarding-top-visual {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      margin-bottom: 6px;
    }
    .route-port-col {
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }
    .route-port-col.is-pod {
      align-items: flex-end;
      text-align: right;
    }
    .port-role-lbl {
      font-size: 9px;
      font-weight: 700;
      color: #0d9488;
      letter-spacing: 0.4px;
      text-transform: uppercase;
    }
    .port-code-big {
      font-size: 15px;
      font-weight: 800;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", monospace;
      line-height: 1.15;
    }
    .port-cn-sub {
      font-size: 10px;
      color: #475569;
      font-weight: 500;
    }
    .route-spine-center {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-width: 0;
      padding: 0 4px;
    }
    .spine-vessel-pill {
      font-size: 10px;
      color: #0369a1;
      font-weight: 600;
      background: #ffffff;
      border: 1px solid #7dd3fc;
      padding: 1px 7px;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      white-space: nowrap;
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      box-shadow: 0 1px 2px rgba(2, 132, 199, 0.08);
    }
    .spine-track-line {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      margin: 3px 0;
    }
    .spine-track-line::before {
      content: '';
      position: absolute;
      left: 0;
      right: 6px;
      top: 50%;
      height: 1.5px;
      background: #2dd4bf;
    }
    .spine-track-line::after {
      content: '';
      position: absolute;
      right: 0;
      top: 50%;
      transform: translateY(-50%);
      border-top: 3.5px solid transparent;
      border-bottom: 3.5px solid transparent;
      border-left: 6px solid #0d9488;
    }
    .port-swap-btn {
      position: relative;
      z-index: 2;
      background: #ffffff;
      border: 1px solid #5eead4;
      color: #0f766e;
      font-size: 10px;
      padding: 0 6px;
      height: 16px;
      line-height: 14px;
      border-radius: 8px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 2px;
      font-weight: 600;
      transition: all 0.15s;
    }
    .port-swap-btn:hover {
      background: #0d9488;
      color: #ffffff;
      border-color: #0d9488;
    }
    .boarding-port-selects {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
      padding-top: 5px;
      border-top: 1px dashed #99f6e4;
    }

    /* 🌟 创新 5: 计费重(RT)智能试算条与快捷备注标签 (Chargeable Ton RT & Quick Remark Chips) */
    .cargo-rt-telemetry {
      grid-column: span 2;
      background: linear-gradient(90deg, #f8fafc 0%, #eff6ff 100%);
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      padding: 5px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 2px;
      font-size: 11px;
    }
    .rt-main-metric {
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .rt-val-strong {
      font-size: 13px;
      font-weight: 800;
      color: #1d4ed8;
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", monospace;
    }
    .cargo-type-badge {
      font-size: 10px;
      font-weight: 600;
      padding: 1px 6px;
      border-radius: 3px;
      background: #dbeafe;
      color: #1e40af;
    }
    .quick-remark-bar {
      display: flex;
      align-items: center;
      gap: 4px;
      flex-wrap: wrap;
      margin-top: 4px;
    }
    .remark-phrase-chip {
      font-size: 10px;
      color: #475569;
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      border-radius: 3px;
      padding: 1px 6px;
      cursor: pointer;
      transition: all 0.15s;
      user-select: none;
    }
    .remark-phrase-chip:hover {
      background: #eff6ff;
      color: #1677ff;
      border-color: #93c5fd;
    }

    /* ==========================================================================
       右轨：右侧多Tab综合工作台 (Right Workbench Workspace with Integrated Tabs)
       ========================================================================== */
    .right-workbench-panel {
      flex: 1;
      background: #ffffff;
      border-radius: 4px;
      border: 1px solid #d9d9d9;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      min-width: 0;
    }

    /* 右侧工作台融合顶部导航条 (Unified Tab Header) */
    .right-wb-header {
      height: 38px;
      padding: 0 12px;
      background: #ffffff;
      border-bottom: 1px solid #e8e8e8;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .right-wb-header .ant-tabs-nav {
      margin-bottom: 0 !important;
    }
    .right-wb-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* 合并查看·只读模式提示横幅 */
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

    /* 费用 Tab 视图容器 */
    .fee-view-container {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
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
       TAB 2: 更改单页签样式 (在右轨内呈现，与左轨业务保持上下文)
       ========================================================================== */
    .change-order-view {
      flex: 1;
      background: #f1f5f9;
      padding: 12px;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      gap: 10px;
    }
    .co-prerequisite-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 32px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 14px;
      max-width: 680px;
      margin: 36px auto;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .co-delta-strip {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 12px;
    }
    .co-delta-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 8px 12px;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .co-delta-lbl {
      font-size: 11px;
      color: #64748b;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .co-delta-val {
      font-size: 14px;
      font-weight: 800;
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", monospace;
      color: #0f172a;
    }

    /* ==========================================================================
       TAB 3: 附件凭证与单证齐套工作台 (Attachment & Voucher Cockpit)
       ========================================================================== */
    .attachment-view {
      flex: 1;
      background: #eef2f6;
      padding: 10px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      gap: 8px;
    }
    .attachment-card {
      background: #ffffff;
      border: 1px solid #dbe2ea;
      border-radius: 6px;
      padding: 12px;
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    /* 顶部 5 大单证分类齐套核对卡 (Document Category Checklist Grid) */
    .att-category-grid {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 8px;
      flex-shrink: 0;
    }
    .att-cat-card {
      background: #ffffff;
      border: 1px solid #dbe2ea;
      border-radius: 5px;
      padding: 7px 10px;
      cursor: pointer;
      transition: all 0.15s;
      display: flex;
      flex-direction: column;
      gap: 4px;
      position: relative;
      user-select: none;
    }
    .att-cat-card:hover {
      border-color: #93c5fd;
      background: #f8fafc;
    }
    .att-cat-card.is-active {
      background: linear-gradient(180deg, #eff6ff 0%, #ffffff 100%);
      border-color: #1677ff;
      box-shadow: 0 0 0 1px rgba(22, 119, 255, 0.15);
    }
    .att-cat-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 4px;
    }
    .att-cat-name {
      font-size: 12px;
      font-weight: 700;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .att-req-tag {
      font-size: 9px;
      font-weight: 700;
      padding: 0 4px;
      border-radius: 2px;
      line-height: 15px;
      flex-shrink: 0;
    }
    .att-req-tag.is-must {
      background: #fef2f2;
      color: #dc2626;
      border: 1px solid #fecaca;
    }
    .att-req-tag.is-opt {
      background: #f1f5f9;
      color: #64748b;
      border: 1px solid #e2e8f0;
    }
    .att-cat-bottom {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 10px;
      color: #64748b;
    }
    .att-status-pill {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-weight: 600;
      font-size: 10px;
    }
    .att-status-pill.is-done {
      color: #059669;
    }
    .att-status-pill.is-pending {
      color: #d97706;
    }

    /* 主体左右分栏：左侧列表与拖拽上传 (58%) + 右侧同屏单证预览与智能核对 (42%) */
    .att-split-body {
      flex: 1;
      display: flex;
      gap: 8px;
      overflow: hidden;
      min-height: 0;
    }
    .att-left-list-pane {
      width: 58%;
      background: #ffffff;
      border: 1px solid #dbe2ea;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .att-right-preview-pane {
      width: 42%;
      background: #ffffff;
      border: 1px solid #dbe2ea;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    /* 紧凑型拖拽快传条 (Compact Drag-and-Drop Upload Bar) */
    .att-upload-dropbar {
      margin: 8px 10px 6px 10px;
      padding: 7px 12px;
      background: linear-gradient(90deg, #f8fafc 0%, #f0f7ff 100%);
      border: 1px dashed #93c5fd;
      border-radius: 5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      flex-shrink: 0;
      transition: all 0.15s;
    }
    .att-upload-dropbar:hover {
      border-color: #1677ff;
      background: #eff6ff;
    }
    .dropbar-left {
      display: flex;
      align-items: center;
      gap: 8px;
      min-width: 0;
    }
    .dropbar-icon {
      width: 28px;
      height: 28px;
      border-radius: 5px;
      background: #dbeafe;
      color: #1d4ed8;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      flex-shrink: 0;
    }
    .dropbar-text-main {
      font-size: 11px;
      font-weight: 600;
      color: #1e293b;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .dropbar-text-sub {
      font-size: 10px;
      color: #64748b;
    }
    .dropbar-actions {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-shrink: 0;
    }

    /* 原生高密度凭证表格 (Native High-Density Voucher Table) */
    .att-table-wrap {
      flex: 1;
      overflow-y: auto;
      padding: 0 10px;
    }
    .att-native-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
    }
    .att-native-table th {
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      border-bottom: 1px solid #e2e8f0;
      color: #475569;
      font-weight: 600;
      text-align: left;
      padding: 6px 8px;
      position: sticky;
      top: 0;
      z-index: 2;
      white-space: nowrap;
    }
    .att-native-table td {
      padding: 7px 8px;
      border-bottom: 1px solid #f1f5f9;
      color: #1e293b;
      vertical-align: middle;
    }
    .att-row-item {
      cursor: pointer;
      transition: background 0.12s;
    }
    .att-row-item:hover {
      background: #f8fafc;
    }
    .att-row-item.is-selected {
      background: #eff6ff !important;
    }
    .att-row-item.is-selected td:first-child {
      border-left: 3px solid #1677ff;
    }
    .file-ext-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 26px;
      height: 22px;
      border-radius: 3px;
      font-size: 9px;
      font-weight: 800;
      font-family: monospace;
      flex-shrink: 0;
    }
    .file-ext-badge.is-pdf {
      background: #fef2f2;
      color: #dc2626;
      border: 1px solid #fecaca;
    }
    .file-ext-badge.is-img {
      background: #eff6ff;
      color: #2563eb;
      border: 1px solid #bfdbfe;
    }
    .ocr-match-pill {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-size: 10px;
      color: #059669;
      background: #ecfdf5;
      border: 1px solid #a7f3d0;
      padding: 1px 6px;
      border-radius: 3px;
      font-weight: 500;
      white-space: nowrap;
    }
    .att-list-footer {
      height: 30px;
      padding: 0 12px;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 10px;
      color: #64748b;
      flex-shrink: 0;
    }

    /* 右侧同屏单证预览器与智能比对台 (In-Place Voucher Preview & Cross-Check Inspector) */
    .inspector-header {
      height: 34px;
      padding: 0 10px;
      background: #f8fafc;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .inspector-paper-scroll {
      flex: 1;
      background: #334155;
      padding: 12px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      gap: 10px;
    }
    .ocr-verify-card {
      width: 100%;
      max-width: 480px;
      background: #1e293b;
      border: 1px solid #475569;
      border-radius: 5px;
      padding: 9px 12px;
      color: #e2e8f0;
      font-size: 11px;
      box-shadow: 0 2px 8px rgba(15, 23, 42, 0.25);
    }
    .ocr-verify-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 6px 8px;
      margin-top: 7px;
    }
    .ocr-field-row {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid #334155;
      border-radius: 3px;
      padding: 4px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      font-size: 10px;
      white-space: nowrap;
    }
    .voucher-sheet {
      width: 100%;
      max-width: 480px;
      background: #ffffff;
      border-radius: 4px;
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.35);
      padding: 12px 14px 14px 14px;
      font-size: 10px;
      color: #1e293b;
      position: relative;
      border: 1px solid #cbd5e1;
    }
    .voucher-stamp {
      position: absolute;
      right: 16px;
      bottom: 12px;
      border: 1.5px solid #dc2626;
      color: #dc2626;
      font-size: 10px;
      font-weight: 800;
      padding: 1px 7px;
      border-radius: 3px;
      transform: rotate(-6deg);
      background: rgba(254, 242, 242, 0.94);
      letter-spacing: 0.5px;
      pointer-events: none;
    }
    .voucher-grid-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 6px;
    }
    .voucher-grid-table td, .voucher-grid-table th {
      border: 1px solid #cbd5e1;
      padding: 3px 6px;
      font-size: 10px;
    }
    .voucher-grid-lbl {
      color: #64748b;
      font-size: 9px;
      display: block;
    }
    .voucher-grid-val {
      font-weight: 700;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", monospace;
    }
    .inspector-crosscheck-footer {
      padding: 6px 10px;
      background: #f0fdf4;
      border-top: 1px solid #bbf7d0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      font-size: 10px;
      color: #166534;
      flex-shrink: 0;
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
      <a-button size="small" type="primary" ghost class="floating-spec-btn" style="position: static; box-shadow: none; height: 22px; font-size: 11px; padding: 0 8px; border-color: #38bdf8; color: #38bdf8;" @click="showSpecDrawer = true">
        <iconify-icon icon="ant-design:book-outlined"></iconify-icon> 设计交接规范
      </a-button>
    </div>
  </div>

  <!-- ========================================================================
       2. 顶层认票身份与状态驾驶舱 (Ticket Identity Cockpit Header)
       ======================================================================== -->
  <div class="wb-header">
    <div class="wb-header-left">
      <div class="cockpit-avatar" title="海运综合业务单据">
        <iconify-icon icon="ant-design:container-outlined"></iconify-icon>
      </div>

      <div class="cockpit-identity-stack">
        <!-- 第一层：核心单号 + 状态呼吸灯 + 提单主号 + 分区脏状态胶囊 -->
        <div class="cockpit-row-primary">
          <div class="wb-job-no">
            <span>{{ ticketData.jobNo }}</span>
            <a-button type="text" size="small" style="padding: 0 3px; height: 20px; color: #64748b;" @click="copyText(ticketData.jobNo)" title="复制委托编号">
              <iconify-icon icon="ant-design:copy-outlined"></iconify-icon>
            </a-button>
          </div>

          <span v-if="ticketData.isLocked" class="status-glow-pill is-locked">
            <iconify-icon icon="ant-design:lock-filled"></iconify-icon> 本票已锁账
          </span>
          <span v-else class="status-glow-pill is-editable">
            <span style="width: 6px; height: 6px; border-radius: 50%; background: #10b981; display: inline-block;"></span>
            正常可编辑
          </span>

          <div class="bl-identity-badge">
            <span>MBL:</span>
            <strong>{{ form.blNo || '-' }}</strong>
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

        <!-- 第二层：高密度客户、组织、责任人与账期面包屑 -->
        <div class="cockpit-row-secondary">
          <span class="meta-crumb-item">
            委托客户: <strong>{{ ticketData.customerName }}</strong>
          </span>
          <span class="meta-crumb-sep">|</span>
          <span class="meta-crumb-item">
            直属组织: <strong>{{ ticketData.salesOrgName }}</strong>
          </span>
          <span class="meta-crumb-sep">|</span>
          <span class="meta-crumb-item">
            销售/操作: <strong>{{ form.salesPerson }} / {{ form.operator || '-' }}</strong>
          </span>
          <span class="meta-crumb-sep">|</span>
          <span class="meta-crumb-item">
            会计月份: <strong style="color: #1d4ed8;">{{ form.accountingPeriod }}</strong> (应结 {{ form.settlementDate }})
          </span>
        </div>
      </div>
    </div>

    <div class="wb-header-right">
      <!-- 翻票控制器 (带当前序号指示，杜绝歧义) -->
      <div class="order-pager-wrap">
        <a-button size="small" :disabled="orderIndex <= 0" @click="handlePrevOrder" title="上一票">
          <iconify-icon icon="ant-design:left-outlined"></iconify-icon> 上一票
        </a-button>
        <span class="order-pager-num">{{ orderIndex + 1 }} / {{ totalOrders }}</span>
        <a-button size="small" :disabled="orderIndex >= totalOrders - 1" @click="handleNextOrder" title="下一票">
          下一票 <iconify-icon icon="ant-design:right-outlined"></iconify-icon>
        </a-button>
      </div>

      <!-- 独立业务动作 -->
      <a-button size="small" @click="openCopyModal" title="复制本票业务与费用">
        <iconify-icon icon="ant-design:copy-outlined"></iconify-icon> 复制业务
      </a-button>
      <a-tooltip title="重新读取本票最新数据">
        <a-button size="small" @click="reloadTicket">
          <iconify-icon icon="ant-design:reload-outlined"></iconify-icon>
        </a-button>
      </a-tooltip>
    </div>
  </div>

  <!-- ========================================================================
       3. 页面主体双轨视口：左侧业务信息永久常驻，右侧工作区随Tab切换！
       ======================================================================== -->
  <div class="dual-rail-workbench">

    <!-- ====================================================================
         左轨：420px 独立常驻业务底账舱 (Smart Business Master Dossier Cockpit)
         ==================================================================== -->
    <div class="left-business-panel">
      <!-- 1. 面板主顶栏：标题 + 一键带入主单 + 独立保存业务 -->
      <div class="panel-header-bar">
        <div class="panel-title-wrap">
          <div class="panel-title">
            <iconify-icon icon="ant-design:profile-outlined" style="color: #1677ff; font-size: 15px;"></iconify-icon>
            <span>业务基础档案</span>
            <a-tag color="blue" :bordered="false" style="font-size: 10px; line-height: 18px; padding: 0 5px; margin: 0;">综合业务</a-tag>
            <span v-if="dirtyStates.basic" style="color: #d97706; font-size: 11px; font-weight: 700;">(未存*)</span>
          </div>
        </div>
        <div class="panel-actions">
          <a-tooltip title="从已关联主单一键带入提单号、船名航次与起目港">
            <a-button 
              size="small" 
              :disabled="ticketData.isLocked || !form.relatedMasterOrder"
              style="height: 25px; padding: 0 7px; font-size: 11px;"
              @click="syncFromMasterOrder">
              <iconify-icon icon="ant-design:thunderbolt-outlined" style="color: #0284c7;"></iconify-icon> 主单带入
            </a-button>
          </a-tooltip>

          <!-- 业务信息独立保存按钮 (明确只存业务) -->
          <a-button 
            type="primary" 
            size="small" 
            :loading="isSavingBasic" 
            :disabled="ticketData.isLocked"
            style="height: 25px; padding: 0 10px; font-size: 12px; font-weight: 600;"
            @click="saveBasicInfo">
            <iconify-icon icon="ant-design:save-outlined"></iconify-icon> 保存业务
          </a-button>
        </div>
      </div>

      <!-- 2. 吸顶分舱快捷锚点与字段齐套度指示条 -->
      <div class="dossier-nav-strip">
        <div class="dossier-nav-pills">
          <span 
            class="dossier-nav-pill" 
            :class="{ 'is-active': activeDossierSec === 'sec1' }" 
            @click="scrollToDossierSec('dossier-sec-1', 'sec1')">
            01 归属主单
          </span>
          <span 
            class="dossier-nav-pill" 
            :class="{ 'is-active': activeDossierSec === 'sec2' }" 
            @click="scrollToDossierSec('dossier-sec-2', 'sec2')">
            02 客户团队
          </span>
          <span 
            class="dossier-nav-pill" 
            :class="{ 'is-active': activeDossierSec === 'sec3' }" 
            @click="scrollToDossierSec('dossier-sec-3', 'sec3')">
            03 航程船期
          </span>
          <span 
            class="dossier-nav-pill" 
            :class="{ 'is-active': activeDossierSec === 'sec4' }" 
            @click="scrollToDossierSec('dossier-sec-4', 'sec4')">
            04 货量计费
          </span>
        </div>
        <span class="dossier-completeness">
          <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 齐套 17/17
        </span>
      </div>

      <!-- 3. 模块化分舱滚动体 (4张高内聚交互子卡片，告别平铺表单堆砌) -->
      <div class="business-form-scroll">

        <!-- ================================================================
             分舱卡 01: 单据归属与主单联动 (Identification, Period & Master Order)
             ================================================================ -->
        <div id="dossier-sec-1" class="dossier-card">
          <div class="dossier-card-header">
            <div class="dossier-card-title">
              <span class="sec-idx-badge">01</span>
              <span>单据归属与主单联动</span>
            </div>
            <div class="dossier-card-extra">
              <span>组织隔离与账期</span>
            </div>
          </div>

          <div class="biz-form-grid">
            <!-- 🌟 创新 1: 三格高密度只读底账条 (凝练委托编号、会计月份、应结日期，消灭灰框堆叠) -->
            <div class="ledger-meta-strip">
              <!-- 格 1: 委托编号 + 重生成 -->
              <div class="ledger-cell">
                <div class="ledger-cell-top">
                  <span>委托编号</span>
                  <a-popconfirm 
                    title="重新生成委托编号将直接向服务器申请新号并落库，是否确认？" 
                    ok-text="确认重生成" 
                    cancel-text="取消" 
                    :disabled="ticketData.isLocked"
                    @confirm="regenerateJobNo">
                    <a-button type="link" size="small" style="padding: 0; height: 14px; line-height: 14px; font-size: 10px;" :disabled="ticketData.isLocked">
                      重生成
                    </a-button>
                  </a-popconfirm>
                </div>
                <div class="ledger-cell-val">
                  <span>{{ form.jobNo }}</span>
                  <iconify-icon icon="ant-design:lock-outlined" style="color: #94a3b8; font-size: 11px;"></iconify-icon>
                </div>
              </div>

              <!-- 格 2: 会计月份 (只读联动) -->
              <div class="ledger-cell">
                <div class="ledger-cell-top">
                  <span>会计月份</span>
                  <a-tooltip title="后端根据业务日期决定的会计期间，只读">
                    <iconify-icon icon="ant-design:question-circle-outlined" style="color: #94a3b8; font-size: 10px;"></iconify-icon>
                  </a-tooltip>
                </div>
                <div class="ledger-cell-val" style="color: #1d4ed8;">
                  <span>{{ form.accountingPeriod }}</span>
                  <span style="font-size: 9px; font-weight: 500; color: #64748b;">当前期</span>
                </div>
              </div>

              <!-- 格 3: 应结日期 (随客户账期试算) -->
              <div class="ledger-cell">
                <div class="ledger-cell-top">
                  <span>应结日期</span>
                  <span style="color: #c2410c; font-weight: 600;">30天</span>
                </div>
                <div class="ledger-cell-val" style="color: #b45309;">
                  <span>{{ form.settlementDate }}</span>
                </div>
              </div>
            </div>

            <!-- 提单号 (BL No.) - 全宽重点突出 -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label">
                <span class="biz-label-title">提单号 (BL No.)</span>
                <span class="biz-label-hint">外部主运单识别号 · 自动大写</span>
              </div>
              <a-input 
                v-model:value="form.blNo" 
                size="small"
                placeholder="请输入提单号 (英文自动大写)" 
                :maxlength="64"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"
                @input="e => form.blNo = e.target.value.toUpperCase()">
                <template #prefix>
                  <span style="font-size: 10px; font-weight: 700; color: #0284c7; background: #e0f2fe; padding: 0 4px; border-radius: 2px;">MBL</span>
                </template>
                <template #suffix>
                  <iconify-icon icon="ant-design:copy-outlined" style="cursor: pointer; color: #9ca3af;" title="复制提单号" @click="copyText(form.blNo)"></iconify-icon>
                </template>
              </a-input>
            </div>

            <!-- 所属公司 (销售直属组织) - 全宽 -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label">
                <span class="biz-label-title is-required">所属公司 (销售直属组织)</span>
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

            <!-- 🌟 创新 2: 关联主单交互式存根票卡 (支持一键同步主单船期与港口) -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label">
                <span class="biz-label-title">关联主单 (海出/海进/件杂货)</span>
                <span class="biz-label-hint">同公司校验 · 最多1票</span>
              </div>
              <div v-if="form.relatedMasterOrder" class="master-ticket-stub">
                <div class="stub-main-row">
                  <div style="display: flex; align-items: center; gap: 6px; min-width: 0; overflow: hidden;">
                    <span class="stub-type-badge">{{ form.relatedMasterOrder.type }}</span>
                    <span class="stub-order-no">{{ form.relatedMasterOrder.no }}</span>
                    <span style="color: #475569; font-size: 11px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                      ({{ form.relatedMasterOrder.customer }})
                    </span>
                  </div>
                  <div style="display: flex; align-items: center; gap: 4px; flex-shrink: 0;">
                    <a-button type="link" size="small" style="padding: 0 2px; height: 18px; font-size: 10px;" :disabled="ticketData.isLocked" @click="openMasterOrderModal">
                      切换
                    </a-button>
                    <span class="master-unlink-icon" @click="unlinkMasterOrder" title="解除关联主单">
                      <iconify-icon icon="ant-design:close-outlined"></iconify-icon>
                    </span>
                  </div>
                </div>
                <div class="stub-sync-bar">
                  <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    <iconify-icon icon="ant-design:compass-outlined" style="color: #0284c7;"></iconify-icon>
                    主单舱单: MSK · COSCO PRIDE / 024E (CNTAO→USLAX)
                  </span>
                  <span class="stub-sync-btn" @click="syncFromMasterOrder" title="将主单的船名、航次、起目港与提单号一键同步到当前票">
                    <iconify-icon icon="ant-design:retweet-outlined"></iconify-icon>
                    {{ masterSynced ? '✓ 已同步舱单' : '同步船期/港口' }}
                  </span>
                </div>
              </div>
              <div v-else>
                <a-button type="dashed" size="small" block :disabled="ticketData.isLocked" @click="openMasterOrderModal">
                  <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 关联海运主单 / 件杂货单
                </a-button>
              </div>
            </div>
          </div>
        </div>

        <!-- ================================================================
             分舱卡 02: 客户资信与协作团队 (Customer Credit & In-Place Team Matrix)
             ================================================================ -->
        <div id="dossier-sec-2" class="dossier-card">
          <div class="dossier-card-header">
            <div class="dossier-card-title">
              <span class="sec-idx-badge">02</span>
              <span>客户委托与协作团队</span>
            </div>
            <div class="dossier-card-extra">
              <span class="card-action-link" @click="syncCustomerToReceivables" title="将当前委托客户一键设为右侧所有应收明细的结算对象">
                <iconify-icon icon="ant-design:user-switch-outlined"></iconify-icon> 设为应收结算方
              </span>
            </div>
          </div>

          <div class="biz-form-grid">
            <!-- 委托单位 - 全宽 -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label">
                <span class="biz-label-title is-required">委托单位 (客户)</span>
                <span class="customer-credit-pill">
                  <iconify-icon icon="ant-design:safety-certificate-outlined"></iconify-icon>
                  信用 AAA · 协议账期 30天
                </span>
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

            <!-- 单位联系人 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span class="biz-label-title">单位联系人</span>
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

            <!-- 客户本票应收实时对账微卡 - 半宽 (1列，与联系人水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span class="biz-label-title">客户本票应收</span>
                <span class="biz-label-hint">实时联动</span>
              </div>
              <div style="height: 24px; padding: 0 8px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; display: flex; align-items: center; justify-content: space-between; font-size: 11px;">
                <span style="color: #166534; font-weight: 700; font-family: monospace;">RMB {{ receivableTotalRmb }}</span>
                <span style="font-size: 10px; color: #15803d;">额度充足</span>
              </div>
            </div>

            <!-- 销售负责人 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span class="biz-label-title is-required">销售负责人</span>
              </div>
              <a-select 
                v-model:value="form.salesPerson" 
                size="small"
                :options="salesPersonOptions" 
                :disabled="ticketData.isLocked"
                @change="handleSalesChange">
              </a-select>
            </div>

            <!-- 操作人员 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span class="biz-label-title">操作人员</span>
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

            <!-- 🌟 创新 3: 团队协作胶囊矩阵 (支持行内直接切换人员 + 一键快捷点选增补岗位) -->
            <div class="team-matrix-box">
              <div class="team-matrix-header">
                <span style="font-weight: 600; color: #334155;">
                  <iconify-icon icon="ant-design:team-outlined" style="color: #0284c7;"></iconify-icon>
                  协同干系人 ({{ form.additionalRoles.length }})
                </span>
                <div class="quick-role-chips" v-if="!ticketData.isLocked">
                  <span class="quick-role-chip" @click="quickAddRole('商务', '张小妹')" title="一键追加商务岗">+商务</span>
                  <span class="quick-role-chip" @click="quickAddRole('报关', '孙报关')" title="一键追加报关岗">+报关</span>
                  <span class="quick-role-chip" @click="openAddStakeholderModal" style="color: #1677ff; border-color: #93c5fd;">+更多岗位</span>
                </div>
              </div>

              <div class="team-capsule-grid">
                <div v-for="(item, idx) in form.additionalRoles" :key="idx" class="role-capsule-item">
                  <span class="role-badge-tag">{{ item.roleName }}</span>
                  <a-select 
                    v-model:value="item.staffName" 
                    size="small"
                    :options="staffOptions" 
                    :disabled="ticketData.isLocked"
                    @change="markDirty('basic')">
                  </a-select>
                  <span v-if="!ticketData.isLocked" class="role-remove-icon" @click="removeRole(idx)" title="移除此协同岗位">
                    <iconify-icon icon="ant-design:close-outlined"></iconify-icon>
                  </span>
                </div>

                <!-- 奇数岗位时自动补齐网格虚线槽，保持 2 列严格对称 -->
                <div 
                  v-if="form.additionalRoles.length % 2 !== 0 && !ticketData.isLocked" 
                  class="role-capsule-item" 
                  style="border-style: dashed; justify-content: center; color: #64748b; cursor: pointer; background: transparent;"
                  @click="openAddStakeholderModal">
                  <iconify-icon icon="ant-design:plus-outlined" style="font-size: 10px;"></iconify-icon>
                  <span style="font-size: 10px;">追加协同岗</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ================================================================
             分舱卡 03: 交互式登机牌航线与船期 (Fused Boarding-Pass Route & Vessel)
             ================================================================ -->
        <div id="dossier-sec-3" class="dossier-card">
          <div class="dossier-card-header">
            <div class="dossier-card-title">
              <span class="sec-idx-badge">03</span>
              <span>航程与船期路径</span>
            </div>
            <div class="dossier-card-extra">
              <span style="color: #0d9488; font-weight: 600;">海运干线 · 直达</span>
            </div>
          </div>

          <div class="biz-form-grid">
            <!-- 🌟 创新 4: 融合式登机牌起目港直选器 (消灭静态卡片与下方下拉框的信息重复，兼具视觉与一键互换交互！) -->
            <div class="boarding-route-selector">
              <div class="boarding-top-visual">
                <div class="route-port-col">
                  <span class="port-role-lbl">POL · 起运港</span>
                  <span class="port-code-big">{{ form.pol || '---' }}</span>
                  <span class="port-cn-sub">{{ getPortCnName(form.pol) }}</span>
                </div>

                <div class="route-spine-center">
                  <div class="spine-vessel-pill">
                    <iconify-icon icon="ant-design:compass-outlined" style="color: #0284c7;"></iconify-icon>
                    <span>{{ form.carrier || '-' }} · {{ form.vesselName || '-' }} / {{ form.voyage || '-' }}</span>
                  </div>
                  <div class="spine-track-line">
                    <button type="button" class="port-swap-btn" :disabled="ticketData.isLocked" @click="swapPorts" title="一键互换起运港与目的港">
                      <iconify-icon icon="ant-design:swap-outlined"></iconify-icon> 互换港口
                    </button>
                  </div>
                </div>

                <div class="route-port-col is-pod">
                  <span class="port-role-lbl">POD · 目的港</span>
                  <span class="port-code-big">{{ form.pod || '---' }}</span>
                  <span class="port-cn-sub">{{ getPortCnName(form.pod) }}</span>
                </div>
              </div>

              <!-- 登机牌内嵌起运港/目的港选择器 (50/50 严格对齐) -->
              <div class="boarding-port-selects">
                <a-select 
                  v-model:value="form.pol" 
                  size="small"
                  show-search 
                  :options="portOptions" 
                  placeholder="选择起运港 (POL)"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')">
                </a-select>
                <a-select 
                  v-model:value="form.pod" 
                  size="small"
                  show-search 
                  :options="portOptions" 
                  placeholder="选择目的港 (POD)"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')">
                </a-select>
              </div>
            </div>

            <!-- 船公司 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span class="biz-label-title">船公司 (Carrier)</span>
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
                <span class="biz-label-title">业务日期</span>
                <span class="biz-label-hint">联动会计期</span>
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
                <span class="biz-label-title">船名 (Vessel)</span>
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
                <span class="biz-label-title">航次 (Voyage)</span>
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
          </div>
        </div>

        <!-- ================================================================
             分舱卡 04: 货量计费吨 (RT) 联动与快捷备注 (Cargo RT & Quick Remarks)
             ================================================================ -->
        <div id="dossier-sec-4" class="dossier-card">
          <div class="dossier-card-header">
            <div class="dossier-card-title">
              <span class="sec-idx-badge">04</span>
              <span>货物规格与计费联动</span>
            </div>
            <div class="dossier-card-extra">
              <span class="card-action-link" @click="syncCargoToFees" title="将当前计费重(RT)或件数一键带入右侧费用表的数量列">
                <iconify-icon icon="ant-design:calculator-outlined"></iconify-icon> 同步件重尺至费用
              </span>
            </div>
          </div>

          <div class="biz-form-grid">
            <!-- 🌟 创新 5: 实时计费重 (Chargeable RT) 与轻泡比智能试算条 (不重复下方输入框数字，提供真正增量货代计算！) -->
            <div class="cargo-rt-telemetry">
              <div class="rt-main-metric">
                <span style="color: #475569;">计费重:</span>
                <span class="rt-val-strong">{{ chargeableTons }} RT</span>
                <span class="cargo-type-badge">{{ cargoTypeLabel }}</span>
              </div>
              <div style="color: #64748b; font-size: 10px;">
                泡重比 <strong>{{ cargoRatioText }}</strong> · 均重 <strong>{{ avgPieceWeight }}</strong> kg/件
              </div>
            </div>

            <!-- 品名 - 全宽 (商品档案多选) -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label">
                <span class="biz-label-title">品名 (Commodities)</span>
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
                <span class="biz-label-title">件数 (Pieces)</span>
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
                <span class="biz-label-title">包装 (Package)</span>
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
                <span class="biz-label-title">毛重 (Weight)</span>
                <span class="biz-label-hint">KGS</span>
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
                <span class="biz-label-title">尺码 (Volume)</span>
                <span class="biz-label-hint">4位小数</span>
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

            <!-- 业务备注 + 货代常用快捷词条一键点选 -->
            <div class="biz-form-item grid-col-2" style="margin-top: 2px;">
              <div class="biz-form-label">
                <span class="biz-label-title">业务备注 (最多1024字符)</span>
                <span class="biz-label-hint">点击下方词条可快捷追加</span>
              </div>
              <a-textarea 
                v-model:value="form.remark" 
                size="small"
                :rows="2" 
                :maxlength="1024" 
                placeholder="录入对外业务备注信息..." 
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-textarea>
              <div class="quick-remark-bar" v-if="!ticketData.isLocked">
                <span class="remark-phrase-chip" @click="appendQuickRemark('美西直达快船')">+ 美西直达快船</span>
                <span class="remark-phrase-chip" @click="appendQuickRemark('电放保函已收')">+ 电放保函已收</span>
                <span class="remark-phrase-chip" @click="appendQuickRemark('申请目的港免堆14天')">+ 免堆14天</span>
                <span class="remark-phrase-chip" @click="appendQuickRemark('内装加固拍照')">+ 内装拍照</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- ====================================================================
         右轨：右侧多Tab综合工作台 (Right Workbench with Integrated Tabs)
         Tab 置于右侧顶栏，左侧业务底账永远常驻！
         ==================================================================== -->
    <div class="right-workbench-panel">

      <!-- 右侧工作台融合顶栏 (3大核心Tab + 业务全局操作) -->
      <div class="right-wb-header">
        <a-tabs v-model:active-key="activeTabKey" @change="(k) => activeTabKey = k" style="margin-bottom: -1px;">
          <a-tab-pane key="fee">
            <template #tab>
              <span>
                <iconify-icon icon="ant-design:transaction-outlined"></iconify-icon>
                应收应付明细
                <a-badge :count="receivableList.length + payableList.length" :overflow-count="99" :number-style="{ backgroundColor: '#1677ff', marginLeft: '6px' }"></a-badge>
              </span>
            </template>
          </a-tab-pane>

          <a-tab-pane key="changeOrder">
            <template #tab>
              <span>
                <iconify-icon icon="ant-design:form-outlined"></iconify-icon>
                更改单调账
                <a-badge v-if="changeOrderList.length > 0" :count="changeOrderList.length" :number-style="{ backgroundColor: '#fa8c16', marginLeft: '6px' }"></a-badge>
              </span>
            </template>
          </a-tab-pane>

          <a-tab-pane key="attachment">
            <template #tab>
              <span>
                <iconify-icon icon="ant-design:paper-clip-outlined"></iconify-icon>
                附件凭证
                <a-badge v-if="attachmentList.length > 0" :count="attachmentList.length" :number-style="{ backgroundColor: '#52c41a', marginLeft: '6px' }"></a-badge>
              </span>
            </template>
          </a-tab-pane>
        </a-tabs>

        <!-- 右侧全局操作区 (费用相关仅在 fee 页签生效) -->
        <div class="right-wb-actions">
          <template v-if="activeTabKey === 'fee'">
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
            <a-badge status="success" text="利润正常 (预警线 > 0.00)"></a-badge>

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

            <!-- 整票提交按钮 -->
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
          </template>

          <template v-else-if="activeTabKey === 'changeOrder'">
            <span style="font-size: 11px; color: #64748b;">基准原票费用锁定状态: </span>
            <a-tag :color="ticketData.isOriginalFeeLocked ? 'green' : 'orange'">
              {{ ticketData.isOriginalFeeLocked ? '原费用已锁定' : '原费用未锁定' }}
            </a-tag>
          </template>

          <template v-else-if="activeTabKey === 'attachment'">
            <span class="status-glow-pill is-editable" style="font-size: 10px;">
              <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 必传单证齐套 3/3
            </span>
            <a-radio-group v-model:value="attachmentScenario" size="small">
              <a-radio-button value="configured">单证工作台 (有配置)</a-radio-button>
              <a-radio-button value="empty_no_config">无类型配置空态 (图05)</a-radio-button>
            </a-radio-group>
            <a-button size="small" :disabled="ticketData.isLocked" @click="openAddOtherAttachmentType">
              <iconify-icon icon="ant-design:AppstoreAddOutlined"></iconify-icon> 添加其他类型
            </a-button>
            <a-button size="small" @click="downloadAllAttachments">
              <iconify-icon icon="ant-design:CloudDownloadOutlined"></iconify-icon> 打包下载 ({{ attachmentList.length }})
            </a-button>
          </template>
        </div>
      </div>

      <!-- 合并查看·只读模式提示横幅 (若激活) -->
      <div v-if="isMergeChangeOrder && activeTabKey === 'fee'" class="merge-readonly-banner">
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

      <!-- ==================================================================
           TAB 1 内容: 应收应付双轨费用工作台
           ================================================================== -->
      <div v-show="activeTabKey === 'fee'" class="fee-view-container">
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

                <a-tooltip title="将勾选的应收明细（或全部应收）一键镜像生成为应付成本草稿">
                  <a-button 
                    size="small" 
                    :disabled="ticketData.isLocked || isMergeChangeOrder || receivableList.length === 0"
                    @click="copySelectedRecToPay">
                    <iconify-icon icon="ant-design:SwapRightOutlined"></iconify-icon> 镜像转应付
                  </a-button>
                </a-tooltip>

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

                <!-- 应收费用独立保存按钮 -->
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

                <!-- 应付费用独立保存按钮 -->
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

        <!-- 固定吸底财务合计栏 -->
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

          <!-- 右侧：本位币折合统计与利润率 -->
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

      <!-- ==================================================================
           TAB 2 内容: 更改单调账工作台 (右侧切换，左侧业务底账持续常驻！)
           ================================================================== -->
      <div v-show="activeTabKey === 'changeOrder'" class="change-order-view">

        <!-- 分支 1: 原票费用未锁定拦截态 (图04) -->
        <div v-if="!ticketData.isOriginalFeeLocked" class="co-prerequisite-card">
          <iconify-icon icon="ant-design:exclamation-circle-filled" style="font-size: 48px; color: #faad14;"></iconify-icon>
          <div style="font-size: 16px; font-weight: 600; color: #111827;">
            主单费用未锁定，不能添加更改单
          </div>
          <div style="font-size: 13px; color: #4b5563; max-width: 520px; line-height: 1.6;">
            更改单是针对<strong>已完成费用锁账的业务</strong>进行后续费用追溯、补充调账的正式单据。<br>
            当前主单费用尚未执行锁费，如需调整或录入费用，请直接在「应收应付明细」中增删改。若原票已完成核算，请先执行原票费用锁账。
          </div>

          <div style="display: flex; gap: 12px; margin-top: 10px;">
            <a-button type="primary" @click="activeTabKey = 'fee'">
              <iconify-icon icon="ant-design:arrow-left-outlined"></iconify-icon> 前往「应收应付明细」直接调整
            </a-button>
            <a-button @click="mockLockOriginalFee">
              <iconify-icon icon="ant-design:lock-outlined"></iconify-icon> 原型模拟：立即锁账原费用
            </a-button>
          </div>
        </div>

        <!-- 分支 2: 原票费用已锁定，正常更改单列表与调账前后财务对比 -->
        <div v-else style="background: #ffffff; border-radius: 6px; border: 1px solid #dbe2ea; padding: 14px; flex: 1; display: flex; flex-direction: column;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #f1f5f9;">
            <div>
              <div style="font-size: 14px; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 8px;">
                <span>更改单调账工作台 (Change Orders)</span>
                <a-tag color="green" style="font-size: 10px; margin: 0;">原票费用已锁账封存</a-tag>
              </div>
              <div style="font-size: 11px; color: #64748b; margin-top: 2px;">
                支持针对已锁账原票发起应收/应付调增与调减，审批生效后可勾选「合并更改单」透视全貌
              </div>
            </div>

            <div style="display: flex; gap: 8px;">
              <a-button type="primary" size="small" @click="addMockChangeOrder">
                <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 新建更改单
              </a-button>
              <a-button size="small" @click="mockUnlockOriginalFee">
                恢复未锁拦截态 (图04)
              </a-button>
            </div>
          </div>

          <!-- 原票 vs 更改单调账后财务对比条 -->
          <div class="co-delta-strip">
            <div class="co-delta-card">
              <div class="co-delta-lbl">
                <span>原票封存基准 (锁账)</span>
                <iconify-icon icon="ant-design:lock-outlined" style="color: #64748b;"></iconify-icon>
              </div>
              <div class="co-delta-val">收 17.80 / 付 7.80</div>
              <div style="font-size: 10px; color: #64748b;">原票毛利: RMB 10.00</div>
            </div>
            <div class="co-delta-card" style="background: #fffbeb; border-color: #fde68a;">
              <div class="co-delta-lbl">
                <span style="color: #b45309;">更改单累计调增 (应收)</span>
                <span style="color: #d97706; font-weight: 700;">{{ changeOrderList.length }} 份更改单</span>
              </div>
              <div class="co-delta-val" style="color: #d97706;">+ RMB 500.00</div>
              <div style="font-size: 10px; color: #b45309;">卸货港堆存天数补充调账</div>
            </div>
            <div class="co-delta-card">
              <div class="co-delta-lbl">
                <span>更改单累计调增 (应付)</span>
                <span>无变动</span>
              </div>
              <div class="co-delta-val">RMB 0.00</div>
              <div style="font-size: 10px; color: #64748b;">应付成本未发生追加</div>
            </div>
            <div class="co-delta-card" style="background: #f0fdf4; border-color: #bbf7d0;">
              <div class="co-delta-lbl">
                <span style="color: #166534;">合并调账后最新总毛利</span>
                <span style="color: #15803d; font-weight: 700;">↑ +5000%</span>
              </div>
              <div class="co-delta-val" style="color: #15803d;">RMB 510.00</div>
              <div style="font-size: 10px; color: #166534;">合并应收 517.80 / 应付 7.80</div>
            </div>
          </div>

          <!-- 原生高密度更改单表格 (确保所有状态标签与操作按钮 100% 渲染) -->
          <div style="flex: 1; overflow-y: auto;">
            <table class="att-native-table">
              <thead>
                <tr>
                  <th style="width: 40px; text-align: center;">#</th>
                  <th style="width: 140px;">更改单号</th>
                  <th style="width: 130px;">申请时间</th>
                  <th style="width: 90px;">申请人</th>
                  <th style="width: 110px; text-align: right;">应收调增/减</th>
                  <th style="width: 110px; text-align: right;">应付调增/减</th>
                  <th style="width: 110px; text-align: right;">毛利影响</th>
                  <th style="width: 90px; text-align: center;">审核状态</th>
                  <th>调账原因与科目说明</th>
                  <th style="width: 160px; text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(co, idx) in changeOrderList" :key="co.id" class="att-row-item">
                  <td style="text-align: center; color: #94a3b8;">{{ idx + 1 }}</td>
                  <td>
                    <strong style="font-family: monospace; color: #1d4ed8;">{{ co.changeNo }}</strong>
                  </td>
                  <td style="color: #64748b; font-family: monospace;">{{ co.createTime }}</td>
                  <td>{{ co.applicant }}</td>
                  <td style="text-align: right; font-weight: 700; color: #d97706; font-family: monospace;">{{ co.recDiff }}</td>
                  <td style="text-align: right; font-family: monospace; color: #64748b;">{{ co.payDiff }}</td>
                  <td style="text-align: right; font-weight: 700; color: #16a34a; font-family: monospace;">{{ co.profitDiff }}</td>
                  <td style="text-align: center;">
                    <a-tag :color="co.status === '已生效' ? 'green' : 'orange'" style="font-size: 10px; margin: 0;">
                      {{ co.status }}
                    </a-tag>
                  </td>
                  <td style="color: #334155;">{{ co.reason }}</td>
                  <td style="text-align: center;">
                    <a-button type="link" size="small" style="padding: 0 4px; font-size: 11px;" @click="enterMergeModeAndSwitchFee">
                      合并透视
                    </a-button>
                    <a-button type="link" size="small" style="padding: 0 4px; font-size: 11px;" @click="antd.message.info('已打开更改单 ' + co.changeNo + ' 调账明细抽屉')">
                      查看明细
                    </a-button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- ==================================================================
           TAB 3 内容: 附件凭证与单证齐套工作台 (右侧切换，左侧业务底账持续常驻！)
           ================================================================== -->
      <div v-show="activeTabKey === 'attachment'" class="attachment-view">

        <!-- 分支 1: 暂无附件类型配置空态 (100% 还原图05 + 4种空态诊断说明) -->
        <div v-if="attachmentScenario === 'empty_no_config'" class="attachment-card" style="align-items: center; justify-content: center; text-align: center;">
          <a-empty description="暂无附件类型配置">
            <template #image>
              <iconify-icon icon="ant-design:inbox-outlined" style="font-size: 56px; color: #94a3b8;"></iconify-icon>
            </template>
            <div style="color: #64748b; font-size: 12px; max-width: 520px; margin: 0 auto 14px auto; line-height: 1.6;">
              当前业务类型尚未在系统基础档案中预设标准附件分类（非系统故障或无权限）。您可以点击下方<strong>「添加其他类型」</strong>临时扩展分类上传，或切换至已配置单证工作台预览。
            </div>
            <a-space size="middle">
              <a-button type="primary" @click="openAddOtherAttachmentType">
                <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 添加其他类型
              </a-button>
              <a-button @click="attachmentScenario = 'configured'">
                <iconify-icon icon="ant-design:eye-outlined"></iconify-icon> 切换为标准单证齐套工作台
              </a-button>
            </a-space>
          </a-empty>

          <!-- 4类空态与权限边界清晰说明卡 (对齐交接文档第7节优化建议) -->
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; width: 100%; max-width: 820px; margin-top: 28px; text-align: left;">
            <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 5px; padding: 8px 10px;">
              <div style="font-size: 11px; font-weight: 700; color: #0284c7; margin-bottom: 3px;">● 状态 A：未配置类型 (当前)</div>
              <div style="font-size: 10px; color: #64748b;">后台未预设分类字典，允许通过「添加其他类型」补充自定义单证类别。</div>
            </div>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px;">
              <div style="font-size: 11px; font-weight: 700; color: #334155; margin-bottom: 3px;">○ 状态 B：已配置但暂未上传</div>
              <div style="font-size: 10px; color: #64748b;">展示必传/选传单证清单槽位（如提单、报关单），引导拖拽对号上传。</div>
            </div>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px;">
              <div style="font-size: 11px; font-weight: 700; color: #334155; margin-bottom: 3px;">○ 状态 C：锁账受限只读态</div>
              <div style="font-size: 10px; color: #64748b;">单据锁账后禁止删除已归档凭证，仅锁账白名单分类允许补充上传。</div>
            </div>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px;">
              <div style="font-size: 11px; font-weight: 700; color: #334155; margin-bottom: 3px;">○ 状态 D：请求异常可重试</div>
              <div style="font-size: 10px; color: #64748b;">网络失败时独立局部重试，绝不与「无类型配置」混淆且不丢失左栏草稿。</div>
            </div>
          </div>
        </div>

        <!-- 分支 2: 标准单证齐套与同屏预览工作台 (5大单证分类卡 + 左表拖拽快传 + 右侧同屏预览与OCR比对) -->
        <template v-else>
          <!-- 1. 顶部 5 大单证分类齐套核对矩阵 -->
          <div class="att-category-grid">
            <div 
              class="att-cat-card" 
              :class="{ 'is-active': attachmentCategoryFilter === 'all' }"
              @click="selectAttachmentCategory('all')">
              <div class="att-cat-top">
                <span class="att-cat-name">
                  <iconify-icon icon="ant-design:folder-open-outlined" style="color: #1677ff;"></iconify-icon>
                  全部单证凭证
                </span>
                <span class="att-req-tag is-opt">总览</span>
              </div>
              <div class="att-cat-bottom">
                <span class="att-status-pill is-done">已传 {{ attachmentList.length }} 份</span>
                <span>共 4.35 MB</span>
              </div>
            </div>

            <div 
              class="att-cat-card" 
              :class="{ 'is-active': attachmentCategoryFilter === 'bl' }"
              @click="selectAttachmentCategory('bl')">
              <div class="att-cat-top">
                <span class="att-cat-name">
                  <iconify-icon icon="ant-design:container-outlined" style="color: #0284c7;"></iconify-icon>
                  提单/运单 (MBL)
                </span>
                <span class="att-req-tag is-must">必传*</span>
              </div>
              <div class="att-cat-bottom">
                <span class="att-status-pill is-done">
                  <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 已齐备 ({{ getCategoryCount('bl') }})
                </span>
                <span>正本扫描</span>
              </div>
            </div>

            <div 
              class="att-cat-card" 
              :class="{ 'is-active': attachmentCategoryFilter === 'customs' }"
              @click="selectAttachmentCategory('customs')">
              <div class="att-cat-top">
                <span class="att-cat-name">
                  <iconify-icon icon="ant-design:audit-outlined" style="color: #0d9488;"></iconify-icon>
                  报关/放行凭证
                </span>
                <span class="att-req-tag is-must">必传*</span>
              </div>
              <div class="att-cat-bottom">
                <span class="att-status-pill is-done">
                  <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 已齐备 ({{ getCategoryCount('customs') }})
                </span>
                <span>海关放行</span>
              </div>
            </div>

            <div 
              class="att-cat-card" 
              :class="{ 'is-active': attachmentCategoryFilter === 'invoice' }"
              @click="selectAttachmentCategory('invoice')">
              <div class="att-cat-top">
                <span class="att-cat-name">
                  <iconify-icon icon="ant-design:account-book-outlined" style="color: #d97706;"></iconify-icon>
                  应收应付发票/账单
                </span>
                <span class="att-req-tag is-must">必传*</span>
              </div>
              <div class="att-cat-bottom">
                <span class="att-status-pill is-done">
                  <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 已齐备 ({{ getCategoryCount('invoice') }})
                </span>
                <span>匹配应付THC</span>
              </div>
            </div>

            <div 
              class="att-cat-card" 
              :class="{ 'is-active': attachmentCategoryFilter === 'other' }"
              @click="selectAttachmentCategory('other')">
              <div class="att-cat-top">
                <span class="att-cat-name">
                  <iconify-icon icon="ant-design:file-add-outlined" style="color: #7c3aed;"></iconify-icon>
                  保函/装箱单/其他
                </span>
                <span class="att-req-tag is-opt">选传</span>
              </div>
              <div class="att-cat-bottom">
                <span v-if="getCategoryCount('other') > 0" class="att-status-pill is-done">
                  <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 已上传 ({{ getCategoryCount('other') }})
                </span>
                <span v-else class="att-status-pill is-pending">
                  <iconify-icon icon="ant-design:clock-circle-outlined"></iconify-icon> 待补充 (0)
                </span>
                <span style="color: #1677ff;" @click.stop="mockQuickUploadTelex">+快传保函</span>
              </div>
            </div>
          </div>

          <!-- 2. 下方双栏工作区：左栏拖拽上传与结构化清单 (58%) + 右栏足不出户同屏单证预览与智能核对 (42%) -->
          <div class="att-split-body">

            <!-- 左栏：快传区 + 高密度原生单证表格 -->
            <div class="att-left-list-pane">
              <!-- 紧凑拖拽上传栏 -->
              <div class="att-upload-dropbar">
                <div class="dropbar-left">
                  <div class="dropbar-icon">
                    <iconify-icon icon="ant-design:cloud-upload-outlined"></iconify-icon>
                  </div>
                  <div style="min-width: 0;">
                    <div class="dropbar-text-main">
                      拖拽 PDF / JPG / PNG / Excel 单证至此，或选择归属分类上传
                    </div>
                    <div class="dropbar-text-sub">
                      单文件上限 10MB · 支持提单、报关单、增值税发票自动识别比对
                    </div>
                  </div>
                </div>

                <div class="dropbar-actions">
                  <a-select v-model:value="uploadTargetCategory" size="small" style="width: 112px;" :disabled="ticketData.isLocked">
                    <a-select-option value="bl">提单/运单</a-select-option>
                    <a-select-option value="customs">报关/放行单</a-select-option>
                    <a-select-option value="invoice">费用发票</a-select-option>
                    <a-select-option value="other">保函/其他</a-select-option>
                  </a-select>

                  <a-upload :show-upload-list="false" :before-upload="handleFileUpload">
                    <a-button type="primary" size="small" :disabled="ticketData.isLocked">
                      <iconify-icon icon="ant-design:upload-outlined"></iconify-icon> 上传凭证
                    </a-button>
                  </a-upload>

                  <a-tooltip title="一键模拟上传一份「电放保函_青岛万达.pdf」并实时预览">
                    <a-button size="small" :disabled="ticketData.isLocked" @click="mockQuickUploadTelex">
                      <iconify-icon icon="ant-design:thunderbolt-outlined" style="color: #0284c7;"></iconify-icon> 模拟传保函
                    </a-button>
                  </a-tooltip>
                </div>
              </div>

              <!-- 高密度原生单证列表 (点击任意行即可在右侧同屏预览！) -->
              <div class="att-table-wrap">
                <table class="att-native-table">
                  <thead>
                    <tr>
                      <th style="width: 28px; text-align: center;">#</th>
                      <th>凭证文件名称 (点击行同屏预览)</th>
                      <th style="width: 78px;">所属分类</th>
                      <th style="width: 162px;">左栏/费用联动核对</th>
                      <th style="width: 62px; text-align: right;">大小</th>
                      <th style="width: 108px;">上传人 / 时间</th>
                      <th style="width: 116px; text-align: center;">操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr 
                      v-for="(att, idx) in filteredAttachments" 
                      :key="att.id" 
                      class="att-row-item"
                      :class="{ 'is-selected': activePreviewAtt && activePreviewAtt.id === att.id }"
                      @click="selectPreviewAttachment(att)">
                      <td style="text-align: center; color: #94a3b8;">{{ idx + 1 }}</td>
                      <td>
                        <div style="display: flex; align-items: center; gap: 7px;">
                          <span class="file-ext-badge" :class="att.fileName.endsWith('.pdf') ? 'is-pdf' : 'is-img'">
                            {{ att.fileName.endsWith('.pdf') ? 'PDF' : 'JPG' }}
                          </span>
                          <div style="min-width: 0; flex: 1;">
                            <div style="font-weight: 600; color: #0f172a; display: flex; align-items: center; gap: 5px; white-space: nowrap;">
                              <span style="overflow: hidden; text-overflow: ellipsis;">{{ att.fileName }}</span>
                              <span v-if="activePreviewAtt && activePreviewAtt.id === att.id" style="font-size: 9px; background: #dbeafe; color: #1d4ed8; padding: 0 5px; line-height: 16px; border-radius: 2px; font-weight: 700; white-space: nowrap; flex-shrink: 0;">
                                预览中
                              </span>
                            </div>
                            <div style="font-size: 10px; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                              {{ att.docNoText || '单证编号: TEST-GH178-20261109' }}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td>
                        <a-tag :color="getCategoryTagColor(att.fileType)" style="font-size: 10px; margin: 0;">
                          {{ getCategoryLabel(att.fileType) }}
                        </a-tag>
                      </td>
                      <td>
                        <span class="ocr-match-pill">
                          <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon>
                          {{ att.verifyNote || '与左侧档案一致' }}
                        </span>
                      </td>
                      <td style="text-align: right; font-family: monospace; color: #475569;">{{ att.fileSize }}</td>
                      <td>
                        <div style="font-size: 11px; color: #334155;">{{ att.uploader }}</div>
                        <div style="font-size: 10px; color: #94a3b8; font-family: monospace;">{{ att.uploadTime }}</div>
                      </td>
                      <td style="text-align: center; white-space: nowrap;" @click.stop>
                        <a-button type="link" size="small" style="padding: 0 4px; font-size: 11px;" @click="selectPreviewAttachment(att)">
                          预览
                        </a-button>
                        <a-button type="link" size="small" style="padding: 0 4px; font-size: 11px;" @click="downloadAttachment(att)">
                          下载
                        </a-button>
                        <a-popconfirm title="确认从本票单据中删除此附件凭证？" @confirm="deleteAttachment(att.id)">
                          <a-button type="link" size="small" danger style="padding: 0 4px; font-size: 11px;" :disabled="ticketData.isLocked">
                            删除
                          </a-button>
                        </a-popconfirm>
                      </td>
                    </tr>

                    <!-- 当选定分类下无文件时的引导空态 -->
                    <tr v-if="filteredAttachments.length === 0">
                      <td colspan="7" style="text-align: center; padding: 36px 16px; color: #64748b;">
                        <iconify-icon icon="ant-design:folder-open-outlined" style="font-size: 28px; color: #cbd5e1; display: block; margin: 0 auto 6px auto;"></iconify-icon>
                        <div style="font-size: 12px; font-weight: 600; color: #334155;">当前「{{ getCategoryLabel(attachmentCategoryFilter) }}」分类下暂无文件</div>
                        <div style="font-size: 11px; color: #94a3b8; margin: 4px 0 10px 0;">可点击上方上传按钮或点击下方快捷按钮生成测试凭证</div>
                        <a-button type="dashed" size="small" :disabled="ticketData.isLocked" @click="mockQuickUploadTelex">
                          <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 立即补充上传「电放保函」样本
                        </a-button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- 底部权限与归档规则说明条 -->
              <div class="att-list-footer">
                <span>
                  <iconify-icon icon="ant-design:safety-certificate-outlined" style="color: #059669;"></iconify-icon>
                  归档规则：同公司数据隔离校验 · 锁账后受白名单保护
                </span>
                <span>当前展示 {{ filteredAttachments.length }} / {{ attachmentList.length }} 份凭证</span>
              </div>
            </div>

            <!-- 右栏：足不出户同屏单证预览与智能比对台 (In-Place Live Document Inspector) -->
            <div class="att-right-preview-pane">
              <div class="inspector-header">
                <div style="display: flex; align-items: center; gap: 6px; min-width: 0;">
                  <iconify-icon icon="ant-design:file-search-outlined" style="color: #1677ff; font-size: 14px;"></iconify-icon>
                  <strong style="font-size: 11px; color: #0f172a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    同屏凭证预览: {{ activePreviewAtt ? activePreviewAtt.fileName : '请选择左侧凭证' }}
                  </strong>
                </div>
                <div style="display: flex; align-items: center; gap: 4px; flex-shrink: 0;">
                  <a-tag color="blue" style="font-size: 10px; margin: 0;">100% 适宽</a-tag>
                  <a-button v-if="activePreviewAtt" type="text" size="small" style="padding: 0 4px; height: 22px; font-size: 11px;" @click="downloadAttachment(activePreviewAtt)">
                    <iconify-icon icon="ant-design:download-outlined"></iconify-icon> 原件
                  </a-button>
                </div>
              </div>

              <!-- 仿真单证票面预览画布 (随所选提单/报关单/发票动态切换票面！) -->
              <div class="inspector-paper-scroll">
                <!-- 预览模板 1: 海运提单 (BL) -->
                <div v-if="activePreviewAtt && activePreviewAtt.fileType === 'bl'" class="voucher-sheet">
                  <div class="voucher-stamp">ORIGINAL · 正本已核</div>
                  <div style="border-bottom: 2px solid #0f172a; padding-bottom: 5px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: flex-end;">
                    <div>
                      <div style="font-size: 13px; font-weight: 800; letter-spacing: 0.5px; color: #0f172a;">MAERSK LINE · BILL OF LADING</div>
                      <div style="font-size: 9px; color: #64748b;">COMBINED TRANSPORT OR PORT TO PORT SHIPMENT</div>
                    </div>
                    <div style="text-align: right;">
                      <span style="font-size: 9px; color: #64748b;">B/L NO.</span>
                      <div style="font-size: 11px; font-weight: 800; color: #1d4ed8; font-family: monospace;">{{ form.blNo }}</div>
                    </div>
                  </div>

                  <table class="voucher-grid-table">
                    <tr>
                      <td colspan="2">
                        <span class="voucher-grid-lbl">SHIPPER (托运人/委托单位)</span>
                        <span class="voucher-grid-val">{{ ticketData.customerName }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">OCEAN VESSEL (船名)</span>
                        <span class="voucher-grid-val">{{ form.vesselName }}</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">VOYAGE NO. (航次)</span>
                        <span class="voucher-grid-val">{{ form.voyage }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">PORT OF LOADING (起运港)</span>
                        <span class="voucher-grid-val">{{ form.pol }} ({{ getPortCnName(form.pol) }})</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">PORT OF DISCHARGE (目的港)</span>
                        <span class="voucher-grid-val">{{ form.pod }} ({{ getPortCnName(form.pod) }})</span>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="2">
                        <span class="voucher-grid-lbl">PARTICULARS FURNISHED BY SHIPPER (件数 · 毛重 · 体积 · 品名)</span>
                        <div style="display: flex; justify-content: space-between; margin-top: 2px; font-weight: 700; color: #0f172a; font-family: monospace;">
                          <span>{{ form.pieces }} {{ form.packageType }}</span>
                          <span>G.W.: {{ form.weight }} KGS</span>
                          <span>MEAS.: {{ form.volume }} CBM</span>
                        </div>
                        <div style="color: #475569; margin-top: 2px;">DESCRIPTION: {{ form.commodities.join(' / ') }} · FREIGHT PREPAID</div>
                      </td>
                    </tr>
                  </table>
                </div>

                <!-- 预览模板 2: 出口报关单 (Customs) -->
                <div v-else-if="activePreviewAtt && activePreviewAtt.fileType === 'customs'" class="voucher-sheet">
                  <div class="voucher-stamp" style="border-color: #059669; color: #059669; background: rgba(236, 253, 245, 0.9);">海关已放行 · 查验通过</div>
                  <div style="text-align: center; border-bottom: 1.5px solid #0f172a; padding-bottom: 5px; margin-bottom: 6px;">
                    <div style="font-size: 12px; font-weight: 800; color: #0f172a;">中华人民共和国海关出口货物报关单</div>
                    <div style="font-size: 9px; color: #475569; font-family: monospace; margin-top: 2px;">预录入编号: 425820260001892041 · 申报口岸: 青岛大港海关 (4258)</div>
                  </div>

                  <table class="voucher-grid-table">
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">境内发货人</span>
                        <span class="voucher-grid-val">{{ ticketData.customerName }}</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">出境关别 / 申报日期</span>
                        <span class="voucher-grid-val">青岛海关 · {{ form.bizDate }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">运输工具名称及航次号</span>
                        <span class="voucher-grid-val">{{ form.vesselName }} / {{ form.voyage }}</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">提运单号 (B/L No.)</span>
                        <span class="voucher-grid-val">{{ form.blNo }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">贸易国 / 运抵国(地区)</span>
                        <span class="voucher-grid-val">美国 (USLAX 洛杉矶)</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">件数 / 包装种类 / 毛重</span>
                        <span class="voucher-grid-val">{{ form.pieces }} {{ form.packageType }} · {{ form.weight }} KG</span>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="2">
                        <span class="voucher-grid-lbl">商品名称及规格型号 (HS编码核对)</span>
                        <span class="voucher-grid-val">01. 8708999990 {{ form.commodities.join(' / ') }} · 监管方式: 一般贸易</span>
                      </td>
                    </tr>
                  </table>
                </div>

                <!-- 预览模板 3: 增值税专用发票 (Invoice) -->
                <div v-else-if="activePreviewAtt && activePreviewAtt.fileType === 'invoice'" class="voucher-sheet" style="border-color: #fda4af;">
                  <div class="voucher-stamp">真伪查验通过 · 匹配应付</div>
                  <div style="text-align: center; border-bottom: 1.5px double #be123c; padding-bottom: 4px; margin-bottom: 6px;">
                    <div style="font-size: 12px; font-weight: 800; color: #9f1239; letter-spacing: 1px;">山东增值税专用发票 (电子发票)</div>
                    <div style="font-size: 9px; color: #64748b; font-family: monospace;">发票号码: No.263702000001928371 · 开票日期: 2026-11-09</div>
                  </div>

                  <table class="voucher-grid-table">
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">购买方名称</span>
                        <span class="voucher-grid-val">青岛佳越国际物流有限公司</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">销售方名称 (应付结算对象)</span>
                        <span class="voucher-grid-val">青岛中远海运集装箱运输有限公司</span>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="2">
                        <span class="voucher-grid-lbl">项目名称 / 规格型号 / 数量 / 单价</span>
                        <div style="display: flex; justify-content: space-between; font-weight: 700; color: #0f172a; margin-top: 2px;">
                          <span>*港口码头服务* 码头操作费 (THC)</span>
                          <span style="font-family: monospace;">1 票 × ¥7.36</span>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">不含税金额 / 税率 / 税额</span>
                        <span class="voucher-grid-val">¥7.36 · 税率 6% · 税额 ¥0.44</span>
                      </td>
                      <td style="background: #fff1f2;">
                        <span class="voucher-grid-lbl" style="color: #be123c;">价税合计 (小写)</span>
                        <span class="voucher-grid-val" style="color: #be123c; font-size: 12px;">RMB 7.80</span>
                      </td>
                    </tr>
                  </table>
                </div>

                <!-- 预览模板 4: 其他保函/通用单证 -->
                <div v-else class="voucher-sheet">
                  <div class="voucher-stamp" style="border-color: #2563eb; color: #2563eb; background: rgba(239, 246, 255, 0.9);">保函已归档</div>
                  <div style="text-align: center; border-bottom: 1.5px solid #0f172a; padding-bottom: 5px; margin-bottom: 6px;">
                    <div style="font-size: 12px; font-weight: 800; color: #0f172a;">海运出口货物电放保函 (TELEX RELEASE LOI)</div>
                    <div style="font-size: 9px; color: #64748b;">致：青岛佳越国际物流有限公司 / 承运船东 {{ form.carrier }}</div>
                  </div>
                  <table class="voucher-grid-table">
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">对应提单号 (B/L No.)</span>
                        <span class="voucher-grid-val">{{ form.blNo }}</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">船名 / 航次</span>
                        <span class="voucher-grid-val">{{ form.vesselName }} / {{ form.voyage }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="2">
                        <span class="voucher-grid-lbl">保函声明内容</span>
                        <div style="color: #334155; line-height: 1.4;">
                          兹有我司（{{ ticketData.customerName }}）出运至 {{ form.pod }} 货物共 {{ form.pieces }} {{ form.packageType }}，因贸易交单需要申请安排电放放货，一切法律责任由我司承担。
                        </div>
                      </td>
                    </tr>
                  </table>
                </div>

                <!-- 票面关键字段智能提取与底账比对矩阵 (消除下方暗色空白，提供直观字段核对价值) -->
                <div class="ocr-verify-card" v-if="activePreviewAtt">
                  <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #334155; padding-bottom: 4px;">
                    <span style="font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 4px;">
                      <iconify-icon icon="ant-design:scan-outlined"></iconify-icon>
                      票面关键字段提取 vs 当前工作台底账比对
                    </span>
                    <span style="color: #4ade80; font-weight: 600;">✓ 4/4 字段完全一致</span>
                  </div>
                  <div class="ocr-verify-grid" v-if="activePreviewAtt.fileType !== 'invoice'">
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">提单号:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #f8fafc;">{{ form.blNo }}</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">船名/航次:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #f8fafc;">{{ form.vesselName }}/{{ form.voyage }}</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">起运/目的港:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #f8fafc;">{{ form.pol }}→{{ form.pod }}</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">件毛体:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #f8fafc;">{{ form.pieces }}件/{{ form.volume }}CBM</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                  </div>
                  <div class="ocr-verify-grid" v-else>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">匹配费用项:</span>
                      <span style="font-weight: 600; color: #f8fafc;">码头操作费 (THC)</span>
                      <span style="color: #4ade80;">✓应付表</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">销方结算对象:</span>
                      <span style="font-weight: 600; color: #f8fafc;">青岛中远海运</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">发票价税合计:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #fbbf24;">RMB 7.80</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">税率 / 不含税:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #f8fafc;">6% / RMB 7.36</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 底部智能比对与一键同步栏 -->
              <div class="inspector-crosscheck-footer">
                <div style="display: flex; align-items: center; gap: 5px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">
                  <iconify-icon icon="ant-design:check-circle-filled" style="color: #16a34a; font-size: 13px;"></iconify-icon>
                  <span>
                    <strong>智能比对通过：</strong>单证提单号、船名航次、件毛体与左栏底账 100% 吻合
                  </span>
                </div>
                <a-button 
                  type="primary" 
                  size="small" 
                  style="height: 22px; font-size: 10px; padding: 0 8px; background: #16a34a; border-color: #16a34a; flex-shrink: 0;"
                  :disabled="ticketData.isLocked"
                  @click="syncVoucherToWorkbench(activePreviewAtt)">
                  <iconify-icon icon="ant-design:retweet-outlined"></iconify-icon> 提取单证数据至左栏
                </a-button>
              </div>
            </div>

          </div>
        </template>

      </div>

    </div>

  </div>

  <!-- ========================================================================
       4. 弹窗与抽屉矩阵 (关联主单、复制业务、整票提交确认、干系人追加、设计规范)
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
      💡 提示：同公司与数据权限校验；综合业务每票最多关联 1 票主单，确认后点击「保存业务」生效。
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
        show-icon></a-alert>

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

  <!-- 抽屉: 设计交接与交互规范核对抽屉 -->
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

  <!-- 规范按钮已融合至顶部沙盘栏右侧 (.floating-spec-btn)，零遮挡底栏操作 -->

</div>

<script>
  const { createApp, ref, reactive, computed, watch, onMounted, onUnmounted } = Vue;

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

      // 左侧业务档案创新交互状态与货量计费重(RT)实时联动计算
      const activeDossierSec = ref('sec1');
      const masterSynced = ref(false);

      const scrollToDossierSec = (secId, secKey) => {
        activeDossierSec.value = secKey;
        const el = document.getElementById(secId);
        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      };

      const getPortCnName = (code) => {
        const map = {
          CNTAO: '青岛港',
          CNSHA: '上海港',
          USLAX: '洛杉矶港',
          USLGB: '长滩港'
        };
        return map[code] || code || '未指定港口';
      };

      const swapPorts = () => {
        if (ticketData.isLocked) return;
        const tmp = form.pol;
        form.pol = form.pod;
        form.pod = tmp;
        markDirty('basic');
        antd.message.success(`已互换起运港与目的港：${form.pol} ⇄ ${form.pod}`);
      };

      const chargeableTons = computed(() => {
        const wTon = (Number(form.weight) || 0) / 1000;
        const vol = Number(form.volume) || 0;
        return Math.max(wTon, vol).toFixed(2);
      });

      const cargoRatioText = computed(() => {
        const wTon = (Number(form.weight) || 0) / 1000;
        const vol = Number(form.volume) || 0;
        if (wTon <= 0 || vol <= 0) return '1:1.0';
        return '1:' + (vol / wTon).toFixed(1);
      });

      const cargoTypeLabel = computed(() => {
        const wTon = (Number(form.weight) || 0) / 1000;
        const vol = Number(form.volume) || 0;
        if (vol > wTon * 1.1) return '轻泡货 · 按体积计费';
        if (wTon > vol * 1.1) return '重货 · 按毛重计费';
        return '平货 · 标准计费';
      });

      const avgPieceWeight = computed(() => {
        const pcs = Number(form.pieces) || 0;
        const w = Number(form.weight) || 0;
        if (pcs <= 0) return '0.0';
        return (w / pcs).toFixed(1);
      });

      const syncFromMasterOrder = () => {
        if (ticketData.isLocked || !form.relatedMasterOrder) return;
        form.carrier = 'MSK';
        form.vesselName = 'COSCO PRIDE';
        form.voyage = '024E';
        form.pol = 'CNTAO';
        form.pod = 'USLAX';
        if (!form.blNo) {
          form.blNo = 'TEST-GH178-20261109';
        }
        masterSynced.value = true;
        markDirty('basic');
        antd.message.success(`已从关联主单 ${form.relatedMasterOrder.no} 同步船名航次、起目港与提单信息！`);
      };

      const syncCustomerToReceivables = () => {
        if (ticketData.isLocked || isMergeChangeOrder.value) return;
        const custObj = customerOptions.find(c => c.value === form.customerId);
        const custName = custObj ? custObj.label : ticketData.customerName;
        ticketData.customerName = custName;
        receivableList.value.forEach(r => {
          r.settlementTarget = custName;
        });
        dirtyStates.rec = true;
        dirtyStates.recCount = Math.max(1, dirtyStates.recCount);
        antd.message.success(`已将「${custName}」同步设为右侧 ${receivableList.value.length} 笔应收明细的结算对象！`);
      };

      const quickAddRole = (roleName, defaultStaff) => {
        if (ticketData.isLocked) return;
        const exists = form.additionalRoles.some(r => r.roleName === roleName);
        if (exists) {
          antd.message.info(`「${roleName}」岗位已存在，可直接下拉切换人员。`);
          return;
        }
        form.additionalRoles.push({ roleName, staffName: defaultStaff });
        markDirty('basic');
        antd.message.success(`已快捷追加协同岗位：${roleName} (${defaultStaff})`);
      };

      const syncCargoToFees = () => {
        if (ticketData.isLocked || isMergeChangeOrder.value) return;
        const rtVal = parseFloat(chargeableTons.value) || 1;
        receivableList.value.forEach(row => {
          if (row.unit === 'CBM' || row.unit === 'RT' || row.feeName.includes('海运')) {
            row.unit = 'RT';
            row.quantity = rtVal;
            recalcRow(row, 'rec');
          }
        });
        antd.message.success(`已将货量计费重 (${rtVal} RT) 联动同步至右侧海运费用明细！`);
      };

      const appendQuickRemark = (phrase) => {
        if (ticketData.isLocked) return;
        if (!form.remark) {
          form.remark = phrase + '。';
        } else if (!form.remark.includes(phrase)) {
          form.remark = form.remark.replace(/[。；\\s]*$/, '') + '；' + phrase + '。';
        }
        markDirty('basic');
        antd.message.success(`已追加快捷业务备注：「${phrase}」`);
      };

      const copySelectedRecToPay = () => {
        if (ticketData.isLocked || isMergeChangeOrder.value) return;
        const sourceRows = selectedRecKeys.value.length > 0
          ? receivableList.value.filter(r => selectedRecKeys.value.includes(r.id))
          : receivableList.value;
        sourceRows.forEach((src, i) => {
          payableList.value.unshift({
            id: 'pay-mirror-' + Date.now() + '-' + i,
            feeName: src.feeName,
            category: src.category,
            settlementTarget: '青岛中远海运集装箱运输有限公司',
            currency: src.currency,
            exchangeRate: src.exchangeRate,
            unit: src.unit,
            unitPrice: parseFloat((src.unitPrice * 0.8).toFixed(2)),
            quantity: src.quantity,
            amount: parseFloat((src.unitPrice * 0.8 * src.quantity).toFixed(2)),
            taxRate: src.taxRate,
            taxExcludedAmount: parseFloat(((src.unitPrice * 0.8 * src.quantity) / (1 + src.taxRate / 100)).toFixed(2)),
            status: '录入中',
            source: '原票',
            isDraft: true
          });
          dirtyStates.payCount++;
        });
        dirtyStates.pay = true;
        antd.message.success(`已将 ${sourceRows.length} 笔应收费用镜像生成为应付成本草稿！`);
      };

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

      // 附件凭证模型 (默认 configured，沙盘第 6 项切换为 empty_no_config 还原图05)
      const attachmentScenario = ref('configured'); // 'configured' | 'empty_no_config'
      const attachmentCategoryFilter = ref('all');
      const uploadTargetCategory = ref('bl');
      const attachmentList = ref([
        {
          id: 'att-1',
          fileName: '提单正本扫描件_TEST-GH178.pdf',
          fileType: 'bl',
          fileSize: '2.4 MB',
          uploader: '李操作',
          uploadTime: '2026-11-09 11:20',
          docNoText: 'MBL: TEST-GH178-20261109 · 500 CTNS',
          verifyNote: '提单号/件重尺与左栏一致'
        },
        {
          id: 'att-2',
          fileName: '出口报关预录单_CNTAO.pdf',
          fileType: 'customs',
          fileSize: '1.1 MB',
          uploader: '孙报关',
          uploadTime: '2026-11-09 13:45',
          docNoText: '报关单: 42582026000189 · 青岛海关',
          verifyNote: '船名航次/起目港核对一致'
        },
        {
          id: 'att-3',
          fileName: '码头THC增值税发票.jpg',
          fileType: 'invoice',
          fileSize: '850 KB',
          uploader: '王经理',
          uploadTime: '2026-11-09 15:10',
          docNoText: '专票: No.26370200 · 税率6%',
          verifyNote: '匹配应付 THC ¥7.80'
        }
      ]);
      const activePreviewAtt = ref(attachmentList.value[0]);

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
          antd.message.success(`已关联主单 ${form.relatedMasterOrder.no}，请点击「保存业务」生效。`);
        } else {
          antd.message.warning('请选择需要关联的主单记录。');
        }
      };
      const unlinkMasterOrder = () => {
        form.relatedMasterOrder = null;
        markDirty('basic');
        antd.message.warning('已解除主单关联，请点击「保存业务」生效。');
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

      const getCategoryCount = (cat) => {
        return attachmentList.value.filter(a => a.fileType === cat).length;
      };
      const getCategoryLabel = (cat) => {
        const map = { all: '全部单证', bl: '提单/运单', customs: '报关凭证', invoice: '费用发票', other: '保函/其他' };
        return map[cat] || '其他单证';
      };
      const getCategoryTagColor = (cat) => {
        const map = { bl: 'blue', customs: 'cyan', invoice: 'orange', other: 'purple' };
        return map[cat] || 'default';
      };
      const selectAttachmentCategory = (cat) => {
        attachmentCategoryFilter.value = cat;
        const list = cat === 'all' ? attachmentList.value : attachmentList.value.filter(a => a.fileType === cat);
        if (list.length > 0) {
          activePreviewAtt.value = list[0];
        }
      };
      const selectPreviewAttachment = (att) => {
        activePreviewAtt.value = att;
      };
      const mockQuickUploadTelex = () => {
        if (ticketData.isLocked) return;
        const newAtt = {
          id: 'att-' + Date.now(),
          fileName: '电放保函_青岛万达_盖章版.pdf',
          fileType: 'other',
          fileSize: '620 KB',
          uploader: '李操作',
          uploadTime: window.dayjs().format('YYYY-MM-DD HH:mm'),
          docNoText: '电放保函 · ' + form.blNo,
          verifyNote: '客户签章与委托单位一致'
        };
        attachmentList.value.push(newAtt);
        activePreviewAtt.value = newAtt;
        if (!form.remark.includes('电放保函已收')) {
          appendQuickRemark('电放保函已收');
        } else {
          antd.message.success('已上传「电放保函_青岛万达_盖章版.pdf」并自动打开右侧同屏预览！');
        }
      };
      const syncVoucherToWorkbench = (att) => {
        if (!att || ticketData.isLocked) return;
        if (att.fileType === 'bl' || att.fileType === 'customs') {
          form.blNo = 'TEST-GH178-20261109';
          form.vesselName = 'COSCO PRIDE';
          form.voyage = '024E';
          form.pieces = 500;
          form.weight = 2500.00;
          form.volume = 15.5000;
          markDirty('basic');
          antd.message.success(`已将「${att.fileName}」票面提单号、船名航次与件毛体数据同步回填至左侧业务档案！`);
        } else if (att.fileType === 'invoice') {
          antd.message.success('发票金额 RMB 7.80 已与应付明细「码头操作费 (THC)」核对一致！');
        } else {
          appendQuickRemark('电放保函已核对归档');
        }
      };
      const downloadAllAttachments = () => {
        antd.message.success(`已打包下载本票全部 ${attachmentList.value.length} 份单证凭证 (TEST130-0022_单证包.zip)！`);
      };
      const addMockChangeOrder = () => {
        const newCo = {
          id: 'co-' + Date.now(),
          changeNo: 'CO-202611-00' + (changeOrderList.value.length + 1),
          createTime: window.dayjs().format('YYYY-MM-DD HH:mm'),
          applicant: form.salesPerson || '王经理',
          recDiff: '+200.00',
          payDiff: '+120.00',
          profitDiff: '+80.00',
          status: '待审批',
          reason: '目的港查验掏箱费补充调账'
        };
        changeOrderList.value.unshift(newCo);
        antd.message.success(`已新建更改单 ${newCo.changeNo}！`);
      };
      const enterMergeModeAndSwitchFee = () => {
        activeTabKey.value = 'fee';
        enterMergeMode();
      };
      const openAddOtherAttachmentType = () => {
        attachmentScenario.value = 'configured';
        attachmentCategoryFilter.value = 'other';
        antd.message.success('已启用「保函/装箱单/其他」扩展单证分类，可直接上传凭证！');
      };
      const handleFileUpload = (file) => {
        if (file.size > 10 * 1024 * 1024) {
          antd.message.error('单文件大小超过 10MB 限制！');
          return false;
        }
        const newAtt = {
          id: 'att-' + Date.now(),
          fileName: file.name,
          fileType: uploadTargetCategory.value || 'other',
          fileSize: (file.size / 1024).toFixed(1) + ' KB',
          uploader: '李操作',
          uploadTime: window.dayjs().format('YYYY-MM-DD HH:mm'),
          docNoText: '新上传单证 · ' + form.jobNo,
          verifyNote: '已通过同公司权限校验'
        };
        attachmentList.value.push(newAtt);
        activePreviewAtt.value = newAtt;
        antd.message.success(`文件 ${file.name} 上传成功并已在右侧打开预览！`);
        return false;
      };
      const previewAttachment = (att) => {
        activePreviewAtt.value = att;
        antd.message.info(`已在右侧预览窗切换显示: ${att.fileName}`);
      };
      const downloadAttachment = (att) => {
        antd.message.success(`已开始下载原件: ${att.fileName}`);
      };
      const deleteAttachment = (id) => {
        attachmentList.value = attachmentList.value.filter(a => a.id !== id);
        if (activePreviewAtt.value && activePreviewAtt.value.id === id) {
          activePreviewAtt.value = attachmentList.value[0] || null;
        }
        antd.message.success('附件凭证已移除。');
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
      const applyScenario = (sc) => {
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
          attachmentScenario.value = 'configured';
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

      const handleScenarioChange = (e) => {
        const sc = (e && e.target) ? e.target.value : (typeof e === 'string' ? e : currentScenario.value);
        applyScenario(sc);
      };

      watch(currentScenario, (newSc) => {
        applyScenario(newSc);
      });

      if (typeof window !== 'undefined') {
        window.__workbench = {
          activeTabKey,
          currentScenario,
          applyScenario,
          ticketData
        };
      }

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
        activeDossierSec,
        masterSynced,
        scrollToDossierSec,
        getPortCnName,
        swapPorts,
        chargeableTons,
        cargoRatioText,
        cargoTypeLabel,
        avgPieceWeight,
        syncFromMasterOrder,
        syncCustomerToReceivables,
        quickAddRole,
        syncCargoToFees,
        appendQuickRemark,
        copySelectedRecToPay,
        changeOrderList,
        changeOrderColumns,
        attachmentScenario,
        attachmentCategoryFilter,
        uploadTargetCategory,
        attachmentList,
        activePreviewAtt,
        attachmentColumns,
        filteredAttachments,
        getCategoryCount,
        getCategoryLabel,
        getCategoryTagColor,
        selectAttachmentCategory,
        selectPreviewAttachment,
        mockQuickUploadTelex,
        syncVoucherToWorkbench,
        downloadAllAttachments,
        addMockChangeOrder,
        enterMergeModeAndSwitchFee,
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

print("Generated HTML successfully with Right Tabs and Highlights at:", output_path)
