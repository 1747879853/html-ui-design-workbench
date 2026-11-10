# Ant Design Vue 4.0 静态 HTML UI 样式优化工作台 (代替设计稿项目)

> 专为**「以真实可运行的 Ant Design Vue 4.0 静态 HTML 优化 UI，直接替代传统 Figma / 静态设计稿交付」**量身定制的工作台与工程模板。

---

## 一、为什么用静态可运行 HTML 代替设计稿？

1. **零还原成本**：传统设计稿与真实组件库间距、高度、交互经常不一致；本项目交付物采用真实的 Ant Design Vue 4.0 原生组件，前端研发人员直接 `Ctrl+C / Ctrl+V` 即可迁入生产代码。
2. **极速零依赖预览**：全量通过可靠 CDN 加载 Vue 3、Ant Design Vue 4.2+ 与 Iconify 图标，**直接双击任何 HTML 文件即可在浏览器中运行**，无需安装 Node.js 或构建步骤。
3. **100% 业务一致性保障**：严格保留原页面全部字段名称、类型、必填标识、枚举选项、按钮操作与表格列，不漏项，不减配。
4. **真实工业级场景**：内置接近真实大宗贸易与供应链的业务 Mock 数据，覆盖 100 字以上长文本浮窗、空数据态 `-` 兜底以及表格列固定。
5. **1920×1080 CSS 宽屏视口优化**：基准对齐主流桌面分辨率，兼顾呼吸感与首屏数据信息密度。

---

## 二、目录结构

```text
├── index.html                   # 统一设计工作台（支持 1920×1080 等比缩放仿真、页面切换、核对报告对比）
├── package.json                 # 可选本地快捷命令 (npm run dev / npx serve)
├── README.md                    # 本文档
├── assets/
│   ├── css/
│   │   └── common.css           # 通用布局与 Token 规范（标准 8px 栅格、色彩层级、阴影规范）
│   └── js/
│       └── common.js            # Mock 生成器、金额格式化、手机号脱敏与 Dayjs 初始化
├── templates/                   # 核心基础模板库（接收新原页面时直接复制使用）
│   ├── template-table-list.html # 1. 高级查询表格列表页模板（折叠搜索、批量操作、抽屉详情）
│   ├── template-form-layout.html# 2. 复杂分组卡片式表单模板（栅格对齐、必填校验、底部吸底栏）
│   └── template-detail-view.html# 3. 全息业务实体详情页模板（4维大盘指标、多Tab切换、时效流转）
├── pages/                       # 业务落地页面目录
│   ├── comprehensive-business-edit.html # 标杆示范：综合业务编辑工作台 (#178 左右同屏双轨驾驶舱)
│   └── demo-order-management.html # 业务示范：B2B大宗采购与订单履约调度中心 (附带抽屉核对表)
└── docs/                        # SOP 与核对规范
    ├── WORKBENCH_UI_UX_PLAYBOOK.md # 🌟 复杂业务工作台与单据编辑页 UI/交互重构沉淀指南 (核心必读)
    ├── WORKFLOW_GUIDE.md        # 完整优化工作流 SOP
    ├── AUDIT_CHECKLIST_TEMPLATE.md # 字段、按钮、列一致性核对报告模板
    └── VUE_SFC_MIGRATION_GUIDE.md  # 一键迁移至 Vue 3 SFC 开发指南
```

---

## 三、快速开始

### 方式 1：直接浏览器打开（最快、无需任何安装）
直接双击打开项目根目录下的 [index.html](file:///Users/blank/Documents/antigravity/intelligent-hopper/index.html)，即可进入交互式预览工作台。

### 方式 2：启动简易本地服务
如果需要测试静态服务环境，可执行：
```bash
npm run dev
# 或
npx serve . -l 3000
```
然后访问 `http://localhost:3000`。

---

## 四、如何将用户提供的原页面制作成优化 HTML？

1. **新建文件**：在 `pages/` 目录下创建 `your-page-name.html`（可直接从 `templates/` 中复制对应类型的模板）。
2. **要素清点与核对**：根据原页面列出所有字段、按钮与表格列，在 HTML 的 `<a-drawer>` 或独立 Markdown 中附上核对表。
3. **布局优化**：
   - 搜索表单按 1920 视口配置为 4 列网格（`grid-template-columns: repeat(4, 1fr)`）。
   - 表格配置 Y 轴滚动 `scroll: { y: 'calc(100vh - 440px)' }`，锁定表头。
4. **真实 Mock 注入**：调用 `window.MockUtils` 注入真实长文本、空值与状态 Tag。
5. **注册到看板**：在 `index.html` 的 `pageOptions` 中加入新页面，随时向产品或研发演示！
