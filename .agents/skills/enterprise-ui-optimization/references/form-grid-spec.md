# Enterprise Form Grid & Financial Calculation Layout Spec

## 1. 4-Column Adaptive Grid Architecture

The standard layout for Ant Design Vue modals is a 4-column CSS grid:

```html
<div class="item-form-grid">
  <!-- 4 items per row -->
</div>
```

```css
.item-form-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px 12px;
}
.col-span-2 { grid-column: span 2; }
.col-span-3 { grid-column: span 3; }
.col-span-4 { grid-column: span 4; }
```

---

## 2. Dynamic Currency & Rate Adaptation (自适应外币与汇率对齐法则)

### Rule: Never create single-element rows
When fields conditionally appear (e.g. `汇率` on foreign currency selection), **never** let them occupy a full row alone with empty space.

### The 4×2 Symmetrical Sizing Table:

| Column | Row 1 (Header/Base) | Row 2 (When Foreign Currency: USD/EUR/HKD) | Row 2 (When Base Currency: RMB) |
| :--- | :--- | :--- | :--- |
| **Col 1** | `报销类型` (Required) | `关联客户` (Optional) | `关联客户` (Optional) |
| **Col 2** | `发生日期` (Required) | `关联业务` (1 Col: Type 98px + Search) | `关联业务` (2 Cols: Type 120px + Search) |
| **Col 3** | `币别` (Select) | `汇率` (Number, directly under `币别`) | *(Merged into Col 2)* |
| **Col 4** | `申报金额` (InputNumber) | `本位币金额` (Disabled Input, directly under `申报金额`) | `本位币金额` (Disabled Input, directly under `申报金额`) |

### Code Implementation:
```html
<div class="item-form-grid">
  <!-- Row 1 -->
  <a-form-item label="报销类型" required class="modal-form-item">
    <a-select v-model:value="model.expenseTypeId" :options="typeOptions" />
  </a-form-item>
  <a-form-item label="发生日期" required class="modal-form-item">
    <a-date-picker v-model:value="model.occurDate" value-format="YYYY-MM-DD" style="width: 100%;" />
  </a-form-item>
  <a-form-item label="币别" class="modal-form-item">
    <a-select v-model:value="model.currencyId" :options="currencyOptions" allow-clear placeholder="本位币（RMB）" @change="onCurrencyChange" />
    <div class="field-subtext">不选为本位币</div>
  </a-form-item>
  <a-form-item label="申报金额" required class="modal-form-item">
    <a-input-number v-model:value="model.amount" :min="0" :precision="2" style="width: 100%;" @change="recomputeAmounts" />
  </a-form-item>

  <!-- Row 2 -->
  <a-form-item label="关联客户" class="modal-form-item">
    <a-select v-model:value="model.clientId" :options="clientOptions" allow-clear placeholder="可选" />
  </a-form-item>
  <a-form-item
    label="关联业务"
    :class="['modal-form-item', (!model.currencyId || model.currencyId === 1) ? 'col-span-2' : '']"
  >
    <div style="display: flex; gap: 6px;">
      <a-select
        v-model:value="model.bizType"
        :options="bizTypeOptions"
        :style="{ width: (!model.currencyId || model.currencyId === 1) ? '120px' : '98px', flexShrink: 0 }"
      />
      <a-select
        v-model:value="model.orderId"
        :options="orderOptions"
        show-search
        allow-clear
        placeholder="先选类型再搜单号"
        style="flex: 1; min-width: 0;"
      />
    </div>
    <div class="field-subtext">先选类型再搜委托编号/主单号</div>
  </a-form-item>
  
  <!-- Row 2 Col 3 (Foreign Currency Only) -->
  <a-form-item v-if="model.currencyId && model.currencyId !== 1" label="汇率" class="modal-form-item">
    <a-input-number v-model:value="model.rate" :min="0" :precision="4" style="width: 100%;" @change="recomputeAmounts" />
    <div class="field-subtext">不填按发生日取应付汇率</div>
  </a-form-item>

  <!-- Row 2 Col 4: Base Amount -->
  <a-form-item label="本位币金额" class="modal-form-item">
    <a-input
      :value="model.localAmount ? ('¥ ' + Number(model.localAmount).toLocaleString('zh-CN', { minimumFractionDigits: 2 })) : '¥ 0.00'"
      disabled
      style="color: #111827; font-weight: 600; background: #f9fafb; border-color: #d9d9d9; text-align: right; font-variant-numeric: tabular-nums;"
    />
    <div class="field-subtext">预估，保存时可能按汇率重算</div>
  </a-form-item>
</div>
```

---

## 3. Category Specific Section (分类专属明细解耦)

Always place sub-category details **after** the core 2-row grid:

```html
<template v-if="category === 'transport'">
  <div class="category-detail-box">
    <div class="category-detail-title">
      <iconify-icon icon="lucide:plane" style="color: #2563eb;"></iconify-icon>
      <span>交通信息</span>
    </div>
    <div class="item-form-grid">
      <a-form-item label="出发地" required class="modal-form-item">
        <a-input v-model:value="model.fromPlace" placeholder="如：上海虹桥" />
      </a-form-item>
      <a-form-item label="目的地" required class="modal-form-item">
        <a-input v-model:value="model.toPlace" placeholder="如：深圳宝安" />
      </a-form-item>
      <a-form-item label="交通工具" required class="modal-form-item">
        <a-select v-model:value="model.vehicle" :options="vehicleOptions" placeholder="请选择" />
      </a-form-item>
    </div>
  </div>
</template>
```

```css
.category-detail-box {
  margin-top: 6px;
  margin-bottom: 6px;
  padding: 8px 12px 2px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
}
.category-detail-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 6px;
}
```
