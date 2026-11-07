# 静态 HTML 一键迁移至 Vue 3 SFC（单文件组件）开发指南

本项目的静态 HTML 采用纯正的 **Ant Design Vue 4.0 + Vue 3 组合式语法** 编写，结构与 Vue 官方单文件组件（SFC，`.vue` 文件）保持高度一对一映射，**前端研发人员在 3 分钟内即可完成工程化接入，无需重复切图或重写模板。**

---

## 1. 结构映射对照表

| 静态 HTML 中的位置 | 对应 Vue SFC (`.vue`) 位置 | 迁移注意点 |
| :--- | :--- | :--- |
| `<div id="app">` 内部模板 | `<template>` | 直接整段复制，组件标签（如 `<a-button>`）完全一致 |
| `<script>` 中的逻辑代码 | `<script setup lang="ts">` 或 `<script setup>` | 提取响应式变量 `ref`、`reactive` 和方法即可 |
| `<style>` 标签或局部样式 | `<style scoped>` | 本项目使用规范的 BEM 类名，直接粘贴至 scoped 块 |
| `common.css` | `src/styles/common.css` 或全局样式 | 作为项目级设计规范引入 |

---

## 2. 代码迁移实操对比示例

### 步骤 A：静态 HTML 中的原始代码
```html
<template id="app-template">
  <div class="page-container">
    <div class="search-card">
      <a-form layout="inline" :model="searchForm">
        <a-form-item label="订单编号">
          <a-input v-model:value="searchForm.orderNo" placeholder="请输入订单号" allow-clear />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="handleSearch">
            <template #icon><iconify-icon icon="ant-design:search-outlined"></iconify-icon></template>
            查询
          </a-button>
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>

<script>
  const { createApp, reactive } = Vue;
  const app = createApp({
    setup() {
      const searchForm = reactive({ orderNo: '' });
      const handleSearch = () => { console.log('查询:', searchForm); };
      return { searchForm, handleSearch };
    }
  });
  app.use(antd).mount('#app');
</script>
```

### 步骤 B：迁移为生产环境 Vue 3 SFC (`OrderList.vue`)
```vue
<template>
  <div class="page-container">
    <div class="search-card">
      <a-form layout="inline" :model="searchForm">
        <a-form-item label="订单编号">
          <a-input v-model:value="searchForm.orderNo" placeholder="请输入订单号" allow-clear />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="handleSearch">
            <template #icon><iconify-icon icon="ant-design:search-outlined" /></template>
            查询
          </a-button>
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';

interface SearchState {
  orderNo: string;
}

const searchForm = reactive<SearchState>({
  orderNo: ''
});

const handleSearch = () => {
  // 接入生产后端 API 接口
  console.log('触发搜索:', searchForm);
};
</script>

<style scoped>
/* 直接粘贴自定义样式，无任何破坏性覆盖 */
.search-card {
  margin-bottom: 16px;
  background: #ffffff;
  border-radius: 8px;
  padding: 18px 24px;
}
</style>
```

---

## 3. 图标迁移说明
在生产工程中，Iconify 可以通过以下两种方式使用：
1. **继续使用原生组件（推荐，无构建包负担）**：
   在 `main.ts` 中安装依赖：`npm i iconify-icon`，然后在入口引入 `import 'iconify-icon';`，模板中的 `<iconify-icon icon="..."></iconify-icon>` 即可无缝渲染。
2. **或替换为 `@ant-design/icons-vue`**：
   如 `<SearchOutlined />`，语义完全对等。

---

## 4. 样式避免污染的最佳实践
1. **遵循 scoped**：生产环境组件建议全部添加 `<style scoped>`。
2. **使用 Ant Design Vue Design Token**：如需定制品牌色，在根级 `<a-config-provider :theme="{ token: { colorPrimary: '#your-color' } }">` 配置，严禁使用 `!important` 强行修改底层按钮尺寸或表格内边距。
