---
name: enterprise-ui-optimization
description: >-
  Standard operating procedure and design system for optimizing enterprise B2B web applications
  into production-grade, zero-dependency Ant Design Vue 4.x + Vue 3 standalone HTML prototypes.
  Activate when the user asks to optimize, redesign, refactor, or build enterprise management
  pages (forms, tables, detail pages, approval flows, settlement, expense claims, ERP/OA pages),
  eliminate UI fluff, ensure 100% field fidelity, or generate high-density, restrained B2B UI.
---

# Enterprise UI Optimization & High-Density Prototype Skill

This skill defines the complete methodology, design patterns, anti-patterns, and engineering standards for creating production-ready, zero-dependency B2B enterprise prototypes (Ant Design Vue 4.x + Vue 3).

Follow these principles strictly whenever optimizing, refactoring, or building enterprise management interfaces.

---

## 1. Core Principles (企业级中后台核心法则)

### 1.1 "Anti-AI-Fluff" (彻底去 AI 味，严禁伪需求)
- **Do NOT hallucinate features**: Never invent "AI 风控评估" (AI risk control), "智能建议条" (AI recommendations), "风险评分" (risk score), or decorative widgets unless the user explicitly requested them or they exist in the real system.
- **No decorative stripes or gimmicky badges**: Avoid high-saturation colorful vertical bars, gradient borders, glowing drop-shadows, or floating decorative pills.
- **Restraint and Density**: Enterprise users value data density, scanability, and precision over flashy marketing visuals.

### 1.2 "100% Field Fidelity" (业务字段 100% 对齐，零遗漏)
- Always inspect the real codebase or user screenshots for the complete field schema.
- Every business nuance matters:
  - Help texts (e.g., `不选为本位币`, `先选业务类型再搜委托编号/主单号`).
  - Searchable selects (business type dropdown + order search select).
  - Complete sub-object cards (e.g., all 11 invoice fields: 票种、发票代码、发票号码、开票日期、销售方、销方税号、购方税号、价税合计、不含税金额、税额、附件上传).
  - Category-specific sub-forms (traffic, hotel, entertainment, allowance).

### 1.3 "Single Source of Truth for Status" (状态单点呈现，拒绝冗余刷屏)
- If a document is rejected or passed, display the rejection reason / approval remarks **strictly in the audit workflow timeline (审批流程时间轴)**.
- Do NOT repeat the exact same rejection notice in:
  1. Header banner
  2. Main body top warning bar
  3. Timeline tab
  *(Repetitive status warnings scream amateurism and eat up valuable vertical space).*

### 1.4 "Golden Balance: High-Craft Structure + Minimalist Copy" (结构高质感 + 文案极度克制)
- **Richness comes from structural micro-components, NOT wordy helper text**:
  - Use a soft slate canvas (`#f3f5f8`) to frame modular white sub-cards (`#ffffff`), 3-cell readonly ledger strips, interactive master-order ticket stubs, 2-column role capsule matrices, fused boarding-pass port selectors, and dark-slate in-place document previewers.
  - Keep field labels pure and concise (e.g., `所属公司`, `关联主单`, `委托单位`, `船公司`, `船名`, `航次`, `毛重`, `尺码`). **Never clutter labels with right-aligned grey spec hints** (`限64字`, `4位小数`, `同公司校验·最多1票`, `sortNo:90`) or redundant bilingual brackets (`(Carrier)`, `(Vessel)`, `(Receivables)`).
- **Eliminate 100% redundant static graphics above inputs**:
  - Never place a static route card or static cargo summary directly above inputs that repeat the exact same values. Fuse the route graphic with the POL/POD selects into a single **Boarding-Pass Route Selector**, and use the cargo telemetry bar to show **computed incremental metrics** (e.g., `计费重 15.50 RT · 轻泡货 · 泡重比 1:6.2`).
- **Beware of C-end vs B2B domain mismatches**:
  - Do NOT add a Ctrip-style `[⇄ 互换港口]` button in the center of a freight forwarding route line (B2B shipments have a fixed one-way trade direction; use a clean directional arrow `───▶`).
  - Do NOT use `"齐套 17/17"` to count form field completion ("齐套" in freight forwarding means document completeness, and most form fields are optional).
- **Converge controls to the user's mental model layer**:
  - Even if the backend stores `clientVisible` per attachment file, when the user's mental model is "by attachment type" (`按类型维度是否可见`), place the `客户可见` checkbox **strictly on the Attachment Type Card layer**—never repeat switches on every file row, in the upload bar, and in the preview card.
- **Micro-Craft & Toolbar Precision**:
  - **No Double-Border Nesting (Box-in-a-Box)**: Never put bordered `<a-button>` elements inside another bordered wrapper (like `[ < 上一票 | 1 / 5 | 下一票 > ]`). Build a single seamless `28px`-tall segmented pill (`border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden`) with `1px solid #f1f5f9` dividers and pure `#ffffff` button backgrounds (dimming only text/icon to `#cbd5e1` when disabled).
  - **No `01 / 02 / 03` Numbered Boxes**: Use a 4-column recessed **Segmented Control** (`#f1f5f9` track + `#ffffff` active pill) for section quick-jump and **20×20px Semantic Color-Tinted Icon Badges** on card headers.
  - See full reference in [`docs/WORKBENCH_UI_UX_PLAYBOOK.md`](../../../docs/WORKBENCH_UI_UX_PLAYBOOK.md).

---

## 2. Form Grid & Financial Calculation Standard (4列自适应表单网格)

### 2.1 The 4-Column Grid Standard
All standard enterprise dialogs and form boxes must use a strict 4-column CSS grid:
```css
.item-form-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px 12px;
}
```

### 2.2 Mathematical & Currency Grouping (金额/汇率/本位币必须对齐)
Financial calculations follow a strict mathematical relationship:
$$\text{原币金额} \times \text{汇率} = \text{本位币金额}$$

**Layout Rules**:
1. **Never let `汇率` occupy an empty line alone**: Putting `汇率` on its own line with 3 empty columns creates jarring whitespace and forces vertical scrolling.
2. **Align Currency with Rate, Amount with Local Amount**:
   - **Column 3**: `币别` (Row 1) $\rightarrow$ `汇率` (Row 2, 外币时显示)
   - **Column 4**: `申报金额（原币）` (Row 1) $\rightarrow$ `本位币金额（折合RMB）` (Row 2)
   - **Column 1**: `报销类型` (Row 1) $\rightarrow$ `关联客户` (Row 2)
   - **Column 2**: `发生日期` (Row 1) $\rightarrow$ `关联业务` (Row 2)
3. **Adaptive Business Order Span**:
   - **When 本位币 (RMB)**: `汇率` is hidden; `关联业务` automatically spans 2 columns (`col-span-2`), giving the business type select (120px) and order search select ample width.
   - **When 外币 (USD/EUR/HKD)**: `关联业务` contracts to 1 column, and `汇率` neatly appears in Column 3, right next to `本位币金额` in Column 4.
   - Result: Exactly 2 rows, 8 fields, 0 wasted space, 0 empty lines!

### 2.3 Separate General Fields from Category-Specific Details
- **Never sandwich category fields in between general fields**:
  - WRONG: Row 1 Basic $\rightarrow$ Travel Info (出发地/目的地) $\rightarrow$ Row 2 Business (关联客户/业务). *(This causes label/column collision and makes business look like a sub-field of travel)*.
  - RIGHT:
    1. **基础要素区 (Basic Info)**: 报销类型、发生日期、币别、申报金额、关联客户、关联业务、汇率、本位币金额。
    2. **分类专属明细区 (Category Detail Box)**: 独立卡片承载交通/住宿/招待/补贴明细，`出发地`、`目的地`、`交通工具` 各占 1 列整齐排布。
    3. **说明 (Description)**: 紧凑单行输入框，带 `allow-clear`。
    4. **发票清单 (Invoices)**: 交互式发票卡片。

---

## 3. High-Density Table Standard (表格顶部统一集成操作 & 双击穿透沉淀)

### 3.1 Eliminate Row-Level Action Column (彻底删除行级操作列，改为顶部统一操作)
- 在企业级高密度表格中，每行重复渲染 `[查看] | [编辑] | [结转] | [删除]` 不仅浪费 140px~180px 水平横向空间，而且加剧视觉噪音。
- **强制规范**：
  1. **彻底删除表格右侧固定「操作」列**。
  2. **所有业务操作全部上提至表格顶部工具栏（Table Header Toolbar）**：
     - 未选中行时：显示全局操作（如「结转当期」、「刷新」）或置灰单行依赖操作。
     - 选中某行时：顶部工具栏动态激活对应操作（如选中已结转期间时激活「反结转」、「查看结转快照」；选中当期时激活「结转向导」）。
     - 支持批量勾选多行进行批量处理（如批量审批、批量锁账、批量删除）。

### 3.2 Double-Click Row Drill-Down Standard (双击行穿透查看详情 / 抽屉 / 向导)
- 当移除了行级操作列后，高频单行核心操作通过**双击行（onDblclick）**承担：
  ```javascript
  const customRow = (record) => {
    return {
      onClick: () => {
        // 单击：选中当前行，驱动顶部工具栏按钮响应
        selectedRowKeys.value = [record.id];
      },
      onDblclick: () => {
        // 双击：直接穿透打开详情抽屉 / 编辑弹窗 / 业务向导
        if (record.state === 0) {
          openSnapshotDrawer(record); // 如已结转行双击直接看快照
        } else if (record.state === 1) {
          openCloseWizardModal(record); // 如当期行双击直接进入结转向导
        }
      }
    };
  };
  ```
- **用户提示规范**：在表格工具栏左侧或统计区必须给出轻量提示（如 `💡 提示：双击行可直接穿透查看详情`），让企业财务/业务人员秒级建立操作习惯。

### 3.3 Vben Admin Standard List Design (标准 Vben 列表与搜索栏规范)
- 保持与企业通用 Vben Admin 风格完全一致：
  1. **顶部搜索表单区**：独立白色卡片，行内表单网格（关键字、日期区间、下拉字典），右侧对齐 `[重置]`（图标+灰字）与 `[搜索]`（主色蓝钮）。
  2. **表格顶部工具区**：左侧为带有条目计数的轻量线型 Tab（`全部`、`未结转 (N)`、`已结转 (M)`、`审计日志`），右侧为按钮组（主操作蓝钮、次级操作白钮/红边危险钮）+ 表格右端工具图标（列设置、密度、刷新）。
  3. **表格底部分页条**：左侧显示 `共 N 条记录` 与 `20条/页` 下拉选择器，右侧显示简洁翻页器 `|< < 1 > >|`。
  4. **严禁破坏表格既有视觉体系**：保持表头浅底色（`#f8fafc` 或 `#f0f5ff`）、单元格内边距与边框基调，禁止随意修改表格骨架。

---

## 4. Modal & Interaction Ergonomics (弹窗与交互人体工学)

### 4.0 Compact Financial Alerts (财务告警与前置预检紧凑化，拒绝大块占空)
- **Anti-Pattern (严禁反模式)**：
  - 严禁堆叠 5 个大尺寸白底卡片（标题、长篇描述、状态标签纵向占满 400px 高度）。
  - 严禁下方再放一个内容重复的大黄色 Alert 告警框。
- **Standard (正确规范)**：
  - 采用**高密度预检矩阵（2列排布或紧凑清单）**：绿色对勾/红色叉号/橙色叹号 + 检查项名称 + 核心状态统计 pill + 紧凑跳转动作。整体高度压低在 120px~150px 黄金视觉区。
  - 核心指标卡水平单行排布，将「可直接处理 N 笔 / 需顺延 M 笔」提炼为极简状态胶囊标签。

### 4.1 Modals Over Drawers for Data Records
- Complex multi-field data entry should default to a centered `<a-modal>` (width: 880px ~ 920px).
- Bottom actions: Standard right-aligned `[取消]` and `[确定]` (Primary).
- Do NOT use right-hand drawers where buttons float awkwardly in the vertical center.

### 4.2 Compact Inputs vs Oversized Textareas
- Avoid tall multi-row textareas for single-thought fields like `说明` or `备注` inside modals; they create dead space and trigger unnecessary modal scrollbars.
- Use a single-line `<a-input allow-clear maxlength="512" placeholder="..." />`.

### 4.3 Readonly Calculated Numbers Must Look Like Inputs
- When showing calculated or system-derived values (e.g., 本位币金额):
  - Do NOT render them as bare floating text or lonely dashes `-` that look like missing inputs.
  - Render them as `<a-input disabled>` with:
    - `background: #f9fafb; border-color: #d9d9d9;`
    - `color: #111827; font-weight: 600;`
    - `text-align: right; font-variant-numeric: tabular-nums;` (financial standard).

### 4.4 Invoices & Attachments Must Be Fully Editable & Deletable
- **Intake / OCR Invoices**: Must never be locked or rendered as static text. Provide full in-place editing.
- **Collapsible Invoice Cards**:
  - Header: `第 N 张 [手工/进项] [文件名] [编辑票面 / 收起] | [移除]`
  - Body: 11 full invoice fields when expanded, compact 1-line summary when collapsed.
  - Linkage: `[同步至申报金额]` button to quickly copy invoice total into item amount.
- **Attachments List**:
  - Every attachment item must provide both `[预览]` and danger-styled `[删除]`.
  - Deleting an attachment must prompt a Popconfirm ("确认删除该附件文件？").

---

## 5. Technical & Engineering Standard (零依赖单页 HTML 规范)

### 5.1 Architecture
- Generate single-file standalone HTML pages under `pages/<page-name>.html`.
- Use local vendor scripts (CDN-free, proxy-free, works offline and via `file://`):
  ```html
  <link rel="stylesheet" href="../assets/vendor/reset.css">
  <link rel="stylesheet" href="../assets/css/common.css">
  <script src="../assets/vendor/dayjs-bundle.min.js"></script>
  <script src="../assets/vendor/vue.global.prod.js"></script>
  <script src="../assets/vendor/antd.min.js"></script>
  <script src="../assets/vendor/iconify-icon.min.js"></script>
  ```

### 5.2 Dayjs Compatibility
- Never call un-bundled Dayjs locale functions that throw `t.locale is not a function`.
- Always wrap dates in `window.dayjs(val)`:
  ```js
  editingItem.occurDate = record.occurDate ? window.dayjs(record.occurDate) : window.dayjs();
  ```

### 5.3 Automated Verification via Playwright
Always verify rendered pages using headless Playwright before presenting results to the user:
```bash
NODE_PATH=/Users/blank/code/FeightForwardingSystem/node_modules node capture.js
```
Capture at 1440×960 (deviceScaleFactor: 2) for:
1. Main page view (with rows selected, toolbar enabled).
2. Edit modal view (in both foreign currency USD and local currency RMB states).
3. Check browser console logs for zero runtime errors.

---

## 6. Optimization Checklist (优化落地自检清单)

Before submitting any enterprise UI optimization to the user, run this checklist:
- [ ] **去 AI 杂质**：是否移除了所有自行臆造的 AI 风控/评分/彩条/多余卡片？
- [ ] **状态去重复**：驳回原因是否仅在审批流时间轴呈现，而非在页面 3 处重复？
- [ ] **字段 100% 对齐**：是否补齐了所有业务字段（币别提示、关联客户、业务类型+委托号搜索、本位币、全量发票要素）？
- [ ] **操作列顶部统一**：表格是否移除了每行重复的“操作”列，改为顶部工具栏（添加、编辑、上移、下移、删除）？
- [ ] **行交互齐全**：是否支持 Checkbox 多选、单选上移下移、双击行打开编辑弹窗？
- [ ] **表单网格和谐**：
  - 外币时：`币别` $\rightarrow$ `汇率` 垂直对齐，`申报金额` $\rightarrow$ `本位币金额` 垂直对齐并靠右展示。
  - 本位币时：`关联业务` 自然跨 2 列，`本位币金额` 右侧对齐。
  - 专属明细（交通/住宿）是否独立在基础要素下方，严禁上下挤压和列错位？
- [ ] **发票全交互**：发票卡片是否支持展开全字段编辑、收起摘要、同步金额、移除文件？
- [ ] **凭证附件可删**：附件列表是否带 `[预览]` 和 `[删除]`（带 Popconfirm 防误删）？
- [ ] **离线高保真**：是否无网络代理依赖，双击即可秒级加载？
