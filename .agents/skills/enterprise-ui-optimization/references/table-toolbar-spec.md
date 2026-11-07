# Enterprise Table Toolbar & Row Selection Spec

## 1. Rationale & Pattern Overview

In traditional CRUD designs, developers often place a repetitive `操作` column on the far right of every single row:
```html
<!-- ANTI-PATTERN: Cluttered row-level actions -->
<a-table-column title="操作" width="160">
  <template #default="{ record }">
    <a>编辑</a> <a-divider type="vertical" />
    <a>上移</a> <a-divider type="vertical" />
    <a>下移</a> <a-divider type="vertical" />
    <a style="color: #ff4d4f;">删除</a>
  </template>
</a-table-column>
```

### Why this is an Anti-Pattern in High-Density B2B Systems:
1. **Wasted Screen Real Estate**: Every row consumes 140px~180px of horizontal width just repeating identical action buttons.
2. **Visual Noise**: 20 rows mean 80 links cluttering the right side, distracting users from actual financial data.
3. **Accidental Mis-clicks**: Dense tables make it easy to accidentally click "删除" instead of "编辑".
4. **No Batch Support**: Row-level operations cannot handle batch actions (e.g. multi-row deletion).

### The Solution: Top Unified Table Toolbar
Move all row operations to the **Table Header Toolbar** above the data grid:
- **Left**: Table Title + Summary Statistics (`共 5 笔明细` | `已选择 1 项`).
- **Right**: Integrated Action Buttons with dynamic state binding.
- **Table Body**: Interactive checkboxes, row click to toggle selection, and **double-click to edit**.

---

## 2. Toolbar Action Matrix & State Binding

| Button | Label | Enabled Condition | Click Behavior |
| :--- | :--- | :--- | :--- |
| **Primary** | `+ 添加费用行` | Always Enabled | Opens empty modal for new record |
| **Default** | `✎ 编辑明细` | `selectedRowKeys.length === 1` | Opens edit modal for the selected record |
| **Default** | `↑ 上移` | `selectedRowKeys.length === 1 && selectedIndex > 0` | Moves row up by 1 position |
| **Default** | `↓ 下移` | `selectedRowKeys.length === 1 && selectedIndex < total - 1` | Moves row down by 1 position |
| **Danger** | `🗑 批量删除` | `selectedRowKeys.length > 0` | Prompts `a-popconfirm`, deletes all checked rows |

---

## 3. Template Architecture

```html
<div class="table-section-card">
  <!-- Table Top Toolbar -->
  <div class="table-toolbar">
    <!-- Left: Title & Stat Badges -->
    <div class="table-toolbar-left">
      <span class="table-toolbar-title">费用明细清单</span>
      <span class="toolbar-stat-tag">共 {{ items.length }} 笔明细</span>
      <span v-if="selectedRowKeys.length > 0" class="toolbar-selected-tag">
        已选择 {{ selectedRowKeys.length }} 项
      </span>
    </div>

    <!-- Right: Unified Actions -->
    <div class="table-toolbar-right">
      <a-button type="primary" size="small" @click="openAddItemModal">
        <template #icon><iconify-icon icon="lucide:plus"></iconify-icon></template>
        添加费用行
      </a-button>

      <a-button
        size="small"
        :disabled="selectedRowKeys.length !== 1"
        @click="editSelectedRow"
      >
        <template #icon><iconify-icon icon="lucide:edit-3"></iconify-icon></template>
        编辑明细
      </a-button>

      <a-button
        size="small"
        :disabled="!canMoveUp"
        @click="moveRow('up')"
      >
        <template #icon><iconify-icon icon="lucide:arrow-up"></iconify-icon></template>
        上移
      </a-button>

      <a-button
        size="small"
        :disabled="!canMoveDown"
        @click="moveRow('down')"
      >
        <template #icon><iconify-icon icon="lucide:arrow-down"></iconify-icon></template>
        下移
      </a-button>

      <a-popconfirm
        :title="`确认删除选中的 ${selectedRowKeys.length} 笔明细？`"
        ok-text="确认删除"
        cancel-text="取消"
        ok-type="danger"
        :disabled="selectedRowKeys.length === 0"
        @confirm="deleteSelectedRows"
      >
        <a-button
          danger
          size="small"
          :disabled="selectedRowKeys.length === 0"
        >
          <template #icon><iconify-icon icon="lucide:trash-2"></iconify-icon></template>
          删除
        </a-button>
      </a-popconfirm>
    </div>
  </div>

  <!-- Data Table -->
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
    <!-- Column scoped slots... -->
  </a-table>
</div>
```

---

## 4. Vue 3 Composition API Implementation

```javascript
import { ref, computed } from 'vue';
import { message } from 'ant-design-vue';

// 1. Data State
const items = ref([
  { id: 101, expenseTypeName: '国内差旅-机票', occurDate: '2026-10-12', amount: 1680.00, currency: 'CNY', localAmount: 1680.00 },
  { id: 102, expenseTypeName: '海外招待-餐费', occurDate: '2026-10-13', amount: 320.00, currency: 'USD', localAmount: 2288.00 },
]);

// 2. Selection State
const selectedRowKeys = ref([]);

const rowSelection = computed(() => ({
  selectedRowKeys: selectedRowKeys.value,
  onChange: (keys) => {
    selectedRowKeys.value = keys;
  },
}));

// 3. Movement State Helpers
const selectedIndex = computed(() => {
  if (selectedRowKeys.value.length !== 1) return -1;
  const singleId = selectedRowKeys.value[0];
  return items.value.findIndex(item => item.id === singleId);
});

const canMoveUp = computed(() => selectedIndex.value > 0);
const canMoveDown = computed(() => selectedIndex.value >= 0 && selectedIndex.value < items.value.length - 1);

// 4. Action Handlers
const openAddItemModal = () => {
  // Reset and open modal for new item
};

const editSelectedRow = () => {
  if (selectedRowKeys.value.length !== 1) return;
  const target = items.value.find(item => item.id === selectedRowKeys.value[0]);
  if (target) {
    openItemModal(target);
  }
};

const moveRow = (direction) => {
  const idx = selectedIndex.value;
  if (idx === -1) return;
  const targetIdx = direction === 'up' ? idx - 1 : idx + 1;
  if (targetIdx < 0 || targetIdx >= items.value.length) return;

  const [movedItem] = items.value.splice(idx, 1);
  items.value.splice(targetIdx, 0, movedItem);
  message.success(`费用行已${direction === 'up' ? '上移' : '下移'}`);
};

const deleteSelectedRows = () => {
  const count = selectedRowKeys.value.length;
  if (count === 0) return;
  const toDelete = new Set(selectedRowKeys.value);
  items.value = items.value.filter(item => !toDelete.has(item.id));
  selectedRowKeys.value = [];
  recalculateTotalSummary();
  message.success(`成功删除 ${count} 笔明细`);
};

// 5. Custom Row: Click to Toggle, Double Click to Edit
const customRow = (record) => {
  return {
    onClick: (event) => {
      // Avoid interference if user clicked directly on checkbox or input inside cell
      if (['INPUT', 'BUTTON', 'A', 'SVG', 'PATH'].includes(event.target.tagName)) return;
      const key = record.id;
      const exists = selectedRowKeys.value.includes(key);
      if (exists) {
        selectedRowKeys.value = selectedRowKeys.value.filter(k => k !== key);
      } else {
        selectedRowKeys.value = [...selectedRowKeys.value, key];
      }
    },
    onDblclick: () => {
      openItemModal(record);
    },
    style: {
      cursor: 'pointer',
      userSelect: 'none',
    }
  };
};
```

---

## 5. CSS Styling Standards

```css
.table-section-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 16px;
}

.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.table-toolbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.table-toolbar-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.toolbar-stat-tag {
  font-size: 12px;
  color: #64748b;
  background: #e2e8f0;
  padding: 2px 8px;
  border-radius: 4px;
}

.toolbar-selected-tag {
  font-size: 12px;
  color: #2563eb;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.table-toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Row Hover Highlight */
:deep(.ant-table-tbody > tr:hover > td) {
  background: #f1f5f9 !important;
}

/* Selected Row Highlight */
:deep(.ant-table-tbody > tr.ant-table-row-selected > td) {
  background: #eff6ff !important;
}
```
