import os

with open('scratch/build_right_tabbed_workbench.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Replace CSS styles (from /* 顶部原型审查沙盘控制器 to /* 右轨：右侧多Tab综合工作台)
css_start = code.find('    /* 顶部原型审查沙盘控制器 (评审与多状态验证专用) */')
css_end = code.find('    /* ==========================================================================\n       右轨：右侧多Tab综合工作台')

assert css_start != -1 and css_end != -1, f"CSS markers not found: {css_start}, {css_end}"

new_css = '''    /* 顶部原型审查沙盘控制器 (深色石板高对比沙盘条，与真实业务顶栏形成清晰视觉分层) */
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
      padding: 1px 6px;
      border-radius: 3px;
      cursor: pointer;
      transition: all 0.15s;
      font-weight: 500;
      display: inline-flex;
      align-items: center;
      gap: 3px;
      user-select: none;
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
      min-width: 85px;
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

'''

code = code[:css_start] + new_css + code[css_end:]

# 2. Replace Top Header (.wb-header) and Left Business Panel (.left-business-panel)
header_start = code.find('  <!-- ========================================================================\n       2. 顶层认票身份与状态条')
right_panel_start = code.find('    <!-- ====================================================================\n         右轨：右侧多Tab综合工作台')

assert header_start != -1 and right_panel_start != -1, f"Header/Left markers not found: {header_start}, {right_panel_start}"

new_header_and_left = '''  <!-- ========================================================================
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
          <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 档案齐套 17/17
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
                  <span class="port-role-lbl">ORIGIN · 起运港 (POL)</span>
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
                  <span class="port-role-lbl">DEST · 目的港 (POD)</span>
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

'''

code = code[:header_start] + new_header_and_left + code[right_panel_start:]

# 3. Add "[复制至应付]" button in Receivable toolbar
rec_toolbar_target = '''                <a-button 
                  size="small" 
                  type="dashed" 
                  :disabled="ticketData.isLocked || isMergeChangeOrder"
                  @click="addReceivableRow">
                  <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 新增应收
                </a-button>'''

rec_toolbar_replacement = '''                <a-button 
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
                </a-tooltip>'''

assert rec_toolbar_target in code, "rec_toolbar_target not found"
code = code.replace(rec_toolbar_target, rec_toolbar_replacement, 1)

# 4. Inject new reactive state, computed properties, and methods in Vue setup()
setup_inject_target = '''      const netProfitRmb = computed(() => {
        return netProfitNumber.value.toFixed(2);
      });'''

setup_inject_replacement = '''      const netProfitRmb = computed(() => {
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
          CNTAO: '青岛港 (QINGDAO)',
          CNSHA: '上海港 (SHANGHAI)',
          USLAX: '洛杉矶港 (LOS ANGELES)',
          USLGB: '长滩港 (LONG BEACH)'
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
      };'''

assert setup_inject_target in code, "setup_inject_target not found"
code = code.replace(setup_inject_target, setup_inject_replacement, 1)

# 5. Export new properties in return block of setup()
return_target = '''        netProfitRmb,
        profitMarginText,'''

return_replacement = '''        netProfitRmb,
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
        copySelectedRecToPay,'''

assert return_target in code, "return_target not found"
code = code.replace(return_target, return_replacement, 1)

with open('scratch/build_right_tabbed_workbench.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully upgraded scratch/build_right_tabbed_workbench.py!")
