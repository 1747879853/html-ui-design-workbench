# 静态 HTML UI 样式优化工作流指南（以代码代替设计稿）

## 1. 核心定位与设计哲学

传统敏捷开发中，产品经理出原型、UI 设计师出 Figma/草图设计稿、前端还原设计稿，流程长且往往存在以下断层：
- 设计稿与 Ant Design Vue 组件库规范脱节（非标间距、非标高度、难以还原的阴影）；
- 静态画板缺少真实动态交互、空数据态、长文本折行/省略测试；
- 前端还原时需要重新手写组件与排版，重复劳动率高。

**本项目核心宗旨：以真实可运行的 Ant Design Vue 4.0 静态 HTML 文件直接代替设计稿交付！**
- 100% 采用真实 Ant Design Vue 4.0 组件。
- 100% 采用标准 CDN 加载，双击或任意浏览器直接打开预览。
- 100% 业务一致性：字段数量、类型、必填项、按钮动作、表格列一个不漏。
- 100% 便于迁移：单文件代码结构，前端工程师可直接 `Ctrl+C / Ctrl+V` 迁入真实 Vue 3 SFC 项目。

---

## 2. 标准 5 步实施 SOP

```
   [1. 接收原页面] 
        │ 截图 / 旧版 Vue 页面 / Excel原型 / 业务需求文档
        ▼
   [2. 资产清点 (严格核对)]
        ├─ 字段清单：名称、类型、必填性、枚举选项
        ├─ 按钮清单：主次按钮、批量操作、行内操作
        └─ 表格列清单：列名、宽度、对齐、排序、状态映射
        ▼
   [3. 架构优化与重排]
        ├─ 信息分组：卡片化 / 标签页 / 栅格网格 (8px倍数)
        ├─ 视觉降噪：主色统一、字阶规范、Tag语义色
        └─ 空间利用：按 1920×1080 视口进行呼吸感与紧凑度平衡
        ▼
   [4. 数据真实化注入]
        ├─ 边界测试：超长文本 Tooltip、空值 `-` 处理
        ├─ 状态全量：待审核、处理中、成功、异常、已取消
        └─ 交互原型：抽屉、弹窗、下拉联动、勾选批量操作
        ▼
   [5. 交付物输出]
        ├─ 优化后的独立静态 HTML
        ├─ 字段、按钮、表格列核对报告
        └─ 布局调整说明与 Vue SFC 迁移指引
```

---

## 3. 关键技术标准

### 3.1 CDN 引入标准 (全版本对齐)
- **Vue 3**: `https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.prod.js`
- **Day.js**: 需同时引入常用插件（`customParseFormat`, `weekday`, `localeData` 等）确保 DatePicker 正常运转。
- **Ant Design Vue 4.0+**:
  - CSS: `https://cdn.jsdelivr.net/npm/ant-design-vue@4.2.6/dist/reset.css`
  - JS: `https://cdn.jsdelivr.net/npm/ant-design-vue@4.2.6/dist/antd.min.js`
- **Iconify 图标**: `https://cdn.jsdelivr.net/npm/iconify-icon@2.1.0/dist/iconify-icon.min.js`
  - 使用方式：`<iconify-icon icon="ant-design:filter-outlined"></iconify-icon>` 或任意开源图标库，灵活性极高。

### 3.2 1920×1080 CSS 视口规范
- 页面设计默认以标准桌面宽屏 1920×1080 为基准。
- 采用响应式容器布局（`min-height: 100vh`，`padding: 16px 24px`）。
- 搜索表单在 1920 宽度下推荐采用 **4 列网格（Col 6）** 或 **3 列网格（Col 8）**，折叠展开状态合理自适应。
- 表格支持 `scroll: { x: 'max-content', y: 'calc(100vh - 360px)' }`，实现表头吸顶与全屏视野优化。

---

## 4. 目录职责划分

| 目录/文件 | 职责说明 |
| :--- | :--- |
| `index.html` | **设计看板与工作台**：支持 1920 视口模拟、页面快速切换、核对报告对比查看 |
| `templates/` | **基础模板库**：包括高级列表页、复杂表单页、全息详情页 |
| `pages/` | **业务优化落地页**：存放针对具体业务优化后的完整 HTML 文件 |
| `assets/css/common.css` | **通用样式规范**：包含标准 8px 栅格间距、字体色彩、卡片阴影 |
| `assets/js/common.js` | **通用 Mock 库**：真实数据生成器、脱敏工具、货币格式化 |
| `docs/` | **交付核对文档**：核对清单模板、SFC 迁移文档 |
