# Standalone HTML Prototype Boilerplate (Ant Design Vue 4.x + Vue 3)

This template provides a zero-dependency, self-contained, offline-compatible HTML boilerplate for enterprise B2B prototypes.

---

## 1. Directory Structure

```text
intelligent-hopper/
├── assets/
│   ├── css/
│   │   └── common.css              # Custom enterprise theme & typography resets
│   └── vendor/
│       ├── reset.css               # Eric Meyer reset / modern normalize
│       ├── dayjs-bundle.min.js     # Bundled Dayjs with plugin support
│       ├── vue.global.prod.js      # Vue 3 production runtime
│       ├── antd.min.js             # Ant Design Vue 4.x bundle
│       └── iconify-icon.min.js     # Iconify web component runtime
└── pages/
    └── <page-name>.html            # Production-grade standalone prototype
```

---

## 2. Complete HTML Prototype Skeleton

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>费用报销单详情 - 企业业务中台</title>
  
  <!-- Vendor CSS -->
  <link rel="stylesheet" href="../assets/vendor/reset.css">
  <link rel="stylesheet" href="../assets/css/common.css">

  <!-- Vendor JS (Strict loading order: Dayjs -> Vue -> Antd -> Iconify) -->
  <script src="../assets/vendor/dayjs-bundle.min.js"></script>
  <script src="../assets/vendor/vue.global.prod.js"></script>
  <script src="../assets/vendor/antd.min.js"></script>
  <script src="../assets/vendor/iconify-icon.min.js"></script>

  <style>
    /* Global Page Scaffolding */
    body {
      background-color: #f1f5f9;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      margin: 0;
      padding: 0;
    }

    #app {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Top Page Header */
    .page-header {
      background: #ffffff;
      border-bottom: 1px solid #e2e8f0;
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 20;
    }

    .page-header-title {
      font-size: 18px;
      font-weight: 700;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* Main Container */
    .page-container {
      max-width: 1440px;
      width: 100%;
      margin: 0 auto;
      padding: 20px 24px 60px;
      box-sizing: border-box;
      flex: 1;
    }

    /* Card Panels */
    .enterprise-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      margin-bottom: 16px;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }

    .enterprise-card-header {
      padding: 12px 20px;
      border-bottom: 1px solid #f1f5f9;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-weight: 600;
      font-size: 14px;
      color: #1e293b;
    }

    .enterprise-card-body {
      padding: 20px;
    }

    /* 4-Column Form Grid */
    .item-form-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px 12px;
    }
    .col-span-2 { grid-column: span 2; }
    .col-span-3 { grid-column: span 3; }
    .col-span-4 { grid-column: span 4; }

    .modal-form-item {
      margin-bottom: 8px;
    }
    .modal-form-item :deep(.ant-form-item-label > label) {
      font-size: 12px;
      color: #475569;
      height: 22px;
    }

    .field-subtext {
      font-size: 11px;
      color: #94a3b8;
      line-height: 1.4;
      margin-top: 2px;
    }
  </style>
</head>
<body>
  <div id="app">
    <!-- Header -->
    <header class="page-header">
      <div class="page-header-title">
        <span>差旅与业务招待报销单 - EXP20261018-002</span>
        <a-tag color="error">已驳回</a-tag>
      </div>
      <div class="page-header-actions">
        <a-space>
          <a-button @click="handlePrint">打印预览</a-button>
          <a-button type="primary" @click="handleSave">保存并重新提交</a-button>
        </a-space>
      </div>
    </header>

    <!-- Main Content -->
    <main class="page-container">
      <!-- 1. Header Information Grid -->
      <section class="enterprise-card">
        <div class="enterprise-card-header">单据基本信息</div>
        <div class="enterprise-card-body">
          <a-descriptions :column="4" size="small" bordered>
            <a-descriptions-item label="单据编号">EXP20261018-002</a-descriptions-item>
            <a-descriptions-item label="报销人员">张三 (技术部)</a-descriptions-item>
            <a-descriptions-item label="申报总金额">¥ 3,968.00</a-descriptions-item>
            <a-descriptions-item label="申请日期">2026-10-18</a-descriptions-item>
          </a-descriptions>
        </div>
      </section>

      <!-- 2. Items Table with Unified Toolbar -->
      <section class="enterprise-card">
        <div class="table-toolbar">
          <div class="table-toolbar-left">
            <span class="table-toolbar-title">费用明细清单</span>
            <span class="toolbar-stat-tag">共 {{ items.length }} 笔明细</span>
            <span v-if="selectedRowKeys.length > 0" class="toolbar-selected-tag">
              已选 {{ selectedRowKeys.length }} 项
            </span>
          </div>
          <div class="table-toolbar-right">
            <a-space>
              <a-button type="primary" size="small" @click="openAddItemModal">添加费用行</a-button>
              <a-button size="small" :disabled="selectedRowKeys.length !== 1" @click="editSelectedRow">编辑明细</a-button>
              <a-button size="small" :disabled="!canMoveUp" @click="moveRow('up')">上移</a-button>
              <a-button size="small" :disabled="!canMoveDown" @click="moveRow('down')">下移</a-button>
              <a-popconfirm
                :title="`确认删除选中的 ${selectedRowKeys.length} 笔明细？`"
                :disabled="selectedRowKeys.length === 0"
                @confirm="deleteSelectedRows"
              >
                <a-button danger size="small" :disabled="selectedRowKeys.length === 0">删除</a-button>
              </a-popconfirm>
            </a-space>
          </div>
        </div>

        <a-table
          :data-source="items"
          :columns="columns"
          :row-selection="rowSelection"
          :custom-row="customRow"
          :pagination="false"
          size="small"
          row-key="id"
          bordered
        >
        </a-table>
      </section>
    </main>

    <!-- Modal for Editing Item -->
    <a-modal
      v-model:open="modalVisible"
      :title="isEditing ? '编辑费用明细' : '添加费用明细'"
      width="900px"
      :mask-closable="false"
      @ok="handleModalSave"
      @cancel="modalVisible = false"
    >
      <!-- Adaptive 4-column form grid goes here -->
    </a-modal>
  </div>

  <script>
    const { createApp, ref, reactive, computed, onMounted } = Vue;

    const app = createApp({
      setup() {
        const items = ref([
          { id: 1, expenseTypeName: '国内差旅-机票', occurDate: '2026-10-12', amount: 1680.00, currency: 'CNY', localAmount: 1680.00 },
          { id: 2, expenseTypeName: '海外招待-餐费', occurDate: '2026-10-13', amount: 320.00, currency: 'USD', localAmount: 2288.00 },
        ]);

        const selectedRowKeys = ref([]);
        const modalVisible = ref(false);
        const isEditing = ref(false);

        const columns = [
          { title: '费用类型', dataIndex: 'expenseTypeName', key: 'expenseTypeName', width: 140 },
          { title: '发生日期', dataIndex: 'occurDate', key: 'occurDate', width: 110 },
          { title: '币别', dataIndex: 'currency', key: 'currency', width: 80, align: 'center' },
          { title: '申报金额', dataIndex: 'amount', key: 'amount', width: 110, align: 'right' },
          { title: '本位币金额', dataIndex: 'localAmount', key: 'localAmount', width: 120, align: 'right' },
        ];

        const rowSelection = computed(() => ({
          selectedRowKeys: selectedRowKeys.value,
          onChange: (keys) => { selectedRowKeys.value = keys; },
        }));

        const selectedIndex = computed(() => {
          if (selectedRowKeys.value.length !== 1) return -1;
          return items.value.findIndex(item => item.id === selectedRowKeys.value[0]);
        });
        const canMoveUp = computed(() => selectedIndex.value > 0);
        const canMoveDown = computed(() => selectedIndex.value >= 0 && selectedIndex.value < items.value.length - 1);

        const customRow = (record) => ({
          onClick: (e) => {
            if (['INPUT', 'BUTTON', 'A'].includes(e.target.tagName)) return;
            const k = record.id;
            selectedRowKeys.value = selectedRowKeys.value.includes(k)
              ? selectedRowKeys.value.filter(id => id !== k)
              : [...selectedRowKeys.value, k];
          },
          onDblclick: () => openEditModal(record),
        });

        const openAddItemModal = () => {
          isEditing.value = false;
          modalVisible.value = true;
        };

        const editSelectedRow = () => {
          if (selectedRowKeys.value.length !== 1) return;
          const target = items.value.find(item => item.id === selectedRowKeys.value[0]);
          if (target) openEditModal(target);
        };

        const openEditModal = (record) => {
          isEditing.value = true;
          modalVisible.value = true;
        };

        const moveRow = (direction) => {
          const idx = selectedIndex.value;
          if (idx === -1) return;
          const targetIdx = direction === 'up' ? idx - 1 : idx + 1;
          const [moved] = items.value.splice(idx, 1);
          items.value.splice(targetIdx, 0, moved);
        };

        const deleteSelectedRows = () => {
          const set = new Set(selectedRowKeys.value);
          items.value = items.value.filter(i => !set.has(i.id));
          selectedRowKeys.value = [];
        };

        const handleModalSave = () => {
          modalVisible.value = false;
        };

        return {
          items,
          columns,
          selectedRowKeys,
          rowSelection,
          customRow,
          modalVisible,
          isEditing,
          canMoveUp,
          canMoveDown,
          openAddItemModal,
          editSelectedRow,
          moveRow,
          deleteSelectedRows,
          handleModalSave,
        };
      }
    });

    app.use(antd);
    app.mount('#app');
  </script>
</body>
</html>
```

---

## 3. Playwright Verification Script Template

To verify styling and behavior programmatically:

```javascript
// capture.js
const { chromium } = require('/Users/blank/code/FeightForwardingSystem/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1440, height: 960 },
    deviceScaleFactor: 2, // High-DPI retina capture
  });

  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.error('PAGE ERROR:', err));

  const targetUrl = 'file://' + path.resolve(__dirname, 'pages/expense_detail.html');
  await page.goto(targetUrl, { waitUntil: 'networkidle' });

  // 1. Capture Main View
  await page.screenshot({ path: 'main_view.png' });

  // 2. Open Modal and Capture
  await page.evaluate(() => {
    // Trigger modal via Vue instance or button click
    const btn = document.querySelector('.table-toolbar-right button');
    if (btn) btn.click();
  });
  await page.waitForTimeout(400); // Wait for modal animation
  await page.screenshot({ path: 'modal_view.png' });

  await browser.close();
  console.log('Verification completed successfully!');
})();
```

Run with:
```bash
NODE_PATH=/Users/blank/code/FeightForwardingSystem/node_modules node capture.js
```
