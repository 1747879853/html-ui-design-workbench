const fs = require('fs');
const path = require('path');

const targetFile = path.resolve(__dirname, '../pages/bank-statement-edit.html');
let content = fs.readFileSync(targetFile, 'utf8');

// 1. Add CSS for Create Mode
const styleMarker = '.workbench-filter-box {';
const newStyles = `
    /* 新增银行流水录入场景专属高保真样式 */
    .create-pending-no-pill {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 12px;
      color: #d97706;
      background: #fef3c7;
      border: 1px dashed #f59e0b;
      padding: 1px 8px;
      border-radius: 4px;
      font-weight: 600;
    }

    .create-guide-container {
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: #f8fafc;
      overflow-y: auto;
      height: 100%;
      box-sizing: border-box;
    }

    .create-guide-hero {
      background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
      border: 1px solid #bae0ff;
      border-radius: 8px;
      padding: 14px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 1px 3px rgba(22, 119, 255, 0.05);
    }

    .create-hero-title {
      font-size: 14px;
      font-weight: 700;
      color: #0958d9;
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
    }

    .create-hero-desc {
      font-size: 12px;
      color: #475569;
      line-height: 1.5;
    }

    .create-hero-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-shrink: 0;
    }

    .readiness-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
    }

    .readiness-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      transition: all 0.2s ease;
    }

    .readiness-card.is-ready {
      border-color: #bbf7d0;
      background: #f0fdf4;
    }

    .readiness-card.is-pending {
      border-color: #fde68a;
      background: #fffbeb;
    }

    .readiness-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
      color: #64748b;
      font-weight: 600;
    }

    .readiness-val {
      font-size: 13px;
      font-weight: 700;
      color: #1e293b;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .readiness-tip {
      font-size: 11px;
      color: #94a3b8;
    }

    .create-flow-steps-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 12px 16px;
    }
`;

if (!content.includes('.create-pending-no-pill')) {
  content = content.replace(styleMarker, newStyles + '\n    ' + styleMarker);
}

// 2. Add preset_create to radio group
const radioMarker = `<a-radio-group v-model:value="currentPreset" button-style="solid" size="small" @change="onPresetChange">`;
const newRadioBtn = `<a-radio-group v-model:value="currentPreset" button-style="solid" size="small" @change="onPresetChange">
              <a-radio-button value="preset_create">
                场景0：新增银行流水 (创建录入场景)
              </a-radio-button>`;

if (!content.includes('value="preset_create"')) {
  content = content.replace(radioMarker, newRadioBtn);
}

// 3. Update cockpit-header
const oldHeaderRegex = /<div class="cockpit-header">[\s\S]*?<\/div>\s*<\/div>\s*<!-- 3\. 加载与失败状态视图/;

const newHeader = `<div class="cockpit-header">
          <div class="cockpit-left-brand">
            <div class="bank-avatar-icon" :style="isCreateMode ? 'background: #eff6ff; color: #1677ff; border-color: #bfdbfe;' : ''">
              <iconify-icon :icon="isCreateMode ? 'ant-design:plus-circle-outlined' : 'ant-design:bank-outlined'"></iconify-icon>
            </div>
            <div class="statement-title-wrap">
              <div class="statement-main-num">
                <span class="statement-no-title">
                  {{ isCreateMode ? '新增银行流水录入' : ('银行流水 ' + currentStatement.bankStatementNo) }}
                </span>
                <span v-if="isCreateMode" class="create-pending-no-pill">
                  [保存入库后自动生成流水编号]
                </span>
                <iconify-icon
                  v-else
                  icon="ant-design:copy-outlined"
                  class="copy-btn"
                  title="复制流水号"
                  @click="copyText(currentStatement.bankStatementNo, '流水号已复制')"
                ></iconify-icon>

                <!-- 状态徽章 -->
                <span class="status-glow-pill" :class="'pill-' + writeOffStatusTag.color">
                  <span class="pulse-dot"></span>
                  {{ writeOffStatusTag.label }}
                </span>

                <!-- 锁定状态 -->
                <span v-if="currentStatement.locked" class="status-glow-pill pill-locked">
                  <iconify-icon icon="ant-design:lock-outlined"></iconify-icon>
                  审计冻结
                </span>

                <!-- 自动导入 -->
                <span v-if="currentStatement.inputType === 1" class="status-glow-pill pill-cyan">
                  <iconify-icon icon="ant-design:api-outlined"></iconify-icon>
                  银企直连
                </span>

                <!-- 未保存草稿 -->
                <span v-if="hasUnsavedChanges && !isCreateMode" class="unsaved-draft-tag">
                  <iconify-icon icon="ant-design:exclamation-circle-outlined"></iconify-icon>
                  流水有未保存修改
                </span>
              </div>

              <div class="statement-sub-meta">
                <span>付款客户：<b>{{ currentStatement.settlementName || (isCreateMode ? '待在左侧选择' : '-') }}</b></span>
                <span class="meta-sep">/</span>
                <span>入账账户：<b>{{ currentStatement.orgBankAccountName || '-' }}</b></span>
                <span class="meta-sep">/</span>
                <span>归属组织：{{ currentStatement.orgName || '-' }}</span>
                <span class="meta-sep">/</span>
                <span>币别：<b class="currency-tag">{{ currentStatement.currencyCode }}</b></span>
                <span class="meta-sep">/</span>
                <span>录入：{{ isCreateMode ? '财务录入中 (草稿)' : (currentStatement.inputType === 1 ? '直连自动入账' : '财务手工录入') }}</span>
                <template v-if="currentStatement.locked">
                  <span class="meta-sep">/</span>
                  <span style="color: #dc2626;">锁定：{{ currentStatement.lockedUserName }} ({{ currentStatement.lockedTime }})</span>
                </template>
              </div>
            </div>
          </div>

          <!-- 右侧资产大盘看板 + 动作栏 -->
          <div class="cockpit-right-section">
            <div class="cockpit-stat-billboard">
              <div class="billboard-item">
                <div class="billboard-label">{{ isCreateMode ? '拟录入总金额' : '流水到账金额' }}</div>
                <div class="billboard-val val-total">{{ formatMoney(isCreateMode ? (currentStatement.amount || 0) : savedSnapshot.amount) }}</div>
              </div>
              <div class="billboard-divider"></div>
              <div class="billboard-item">
                <div class="billboard-label">已核销业务额</div>
                <div class="billboard-val val-settled">{{ formatMoney(currentSettledAmount) }}</div>
              </div>
              <div class="billboard-divider"></div>
              <div class="billboard-item">
                <div class="billboard-label">{{ isCreateMode ? '保存后可用额度' : '剩余可用结余' }}</div>
                <div class="billboard-val" :class="isCreateMode ? 'is-positive' : remainingClass">
                  {{ formatMoney(isCreateMode ? (currentStatement.amount || 0) : remainingAmount) }}
                </div>
              </div>
            </div>

            <div class="header-action-btns">
              <template v-if="isCreateMode">
                <a-button @click="handleBackToList">取消并返回</a-button>
                <a-button
                  type="default"
                  :loading="isSaving"
                  @click="handleSaveStatement"
                >
                  保存流水入库
                </a-button>
                <a-button
                  type="primary"
                  :loading="isSaving"
                  @click="handleSaveAndStartReconcile"
                >
                  <template #icon><iconify-icon icon="ant-design:thunderbolt-outlined"></iconify-icon></template>
                  保存并立即开启对账
                </a-button>
              </template>
              <template v-else>
                <a-button @click="handleBackToList">返回列表</a-button>
                <a-button
                  type="primary"
                  :loading="isSaving"
                  :disabled="!canEditCurrentAmount || !hasUnsavedChanges"
                  @click="handleSaveStatement"
                >
                  保存流水
                </a-button>
              </template>
            </div>
          </div>
        </div>

        <!-- 3. 加载与失败状态视图`;

content = content.replace(oldHeaderRegex, newHeader);

// 4. Update Left Rail Liquidity Box & Split Bar
const oldLeftRailHeadRegex = /<div class="rail-metric-grid">[\s\S]*?<\/div>\s*<\/div>\s*<!-- 2\. 水单入账凭据事实卡片/;

const newLeftRailHead = `<div class="rail-metric-grid">
                    <div class="rail-metric-box">
                      <div class="metric-lbl">{{ isCreateMode ? '拟录入总额' : '流水到账总额' }}</div>
                      <div class="metric-num num-total">{{ formatMoney(isCreateMode ? (currentStatement.amount || 0) : savedSnapshot.amount) }}</div>
                      <span class="currency-tag" style="margin-top: 2px;">{{ currentStatement.currencyCode }}</span>
                    </div>
                    <div class="rail-metric-box">
                      <div class="metric-lbl">已核销金额</div>
                      <div class="metric-num num-settled">{{ formatMoney(currentSettledAmount) }}</div>
                      <span class="metric-sub" :style="{ color: isCreateMode ? '#64748b' : (isOverSettled ? '#dc2626' : (remainingAmount <= 0.005 ? '#16a34a' : '#0284c7')) }">
                        {{ isCreateMode ? '待建单核销' : ('消清率 ' + progressPercent + '%') }}
                      </span>
                    </div>
                    <div class="rail-metric-box">
                      <div class="metric-lbl">{{ isCreateMode ? '保存后可用' : '剩余可用额度' }}</div>
                      <div class="metric-num" :class="isCreateMode ? 'is-positive' : remainingClass">
                        {{ formatMoney(isCreateMode ? (currentStatement.amount || 0) : remainingAmount) }}
                      </div>
                      <span class="metric-sub" v-if="isCreateMode" style="color: #16a34a; font-weight: 600;">
                        {{ Number(currentStatement.amount) > 0 ? '✓ 可全额核销' : '待输入金额' }}
                      </span>
                      <span class="metric-sub" v-else-if="isOverSettled" style="color: #dc2626; font-weight: 700;">⚠️ 溢出风险</span>
                      <span class="metric-sub" v-else-if="remainingAmount <= 0.005" style="color: #16a34a; font-weight: 600;">✓ 全部结清</span>
                      <span class="metric-sub" v-else style="color: #16a34a;">可用于核销</span>
                    </div>
                  </div>

                  <!-- 交互式分段资金分配条 -->
                  <div class="split-bar-track" style="margin-top: 8px;">
                    <template v-if="isCreateMode">
                      <div
                        v-if="Number(currentStatement.amount) > 0"
                        class="split-segment split-segment-remaining"
                        style="width: 100%; justify-content: center; background: #e0f2fe; color: #0369a1; border-color: #7dd3fc;"
                        :title="'待分配全额度：' + formatMoney(currentStatement.amount)"
                      >
                        待核销可用 {{ formatMoney(currentStatement.amount) }} (100%)
                      </div>
                      <div
                        v-else
                        class="split-segment"
                        style="width: 100%; justify-content: center; background: #f1f5f9; color: #94a3b8; border: 1px dashed #cbd5e1;"
                      >
                        请在下方录入到账总额
                      </div>
                    </template>
                    <template v-else>
                      <div
                        v-for="seg in allocationSegments"
                        :key="seg.id"
                        class="split-segment"
                        :class="{ 'is-highlighted-seg': hoveredSettlementId === seg.id }"
                        :style="{ width: seg.percent + '%', background: seg.color }"
                        :title="seg.settlementNo + ' (' + (seg.type === 0 ? '按费用' : '按发票') + ')：' + formatMoney(seg.actualSettled) + ' (' + seg.percent + '%)'"
                        @mouseenter="handleSegmentHover(seg.id)"
                        @mouseleave="handleSegmentHover(null)"
                        @click="handleSegmentClick(seg.id)"
                      >
                        <span v-if="seg.percent >= 15">{{ seg.settlementNo }} ({{ seg.percent }}%)</span>
                      </div>

                      <!-- 剩余未分配额度段 -->
                      <div
                        v-if="remainingAmount > 0.005 && !isOverSettled"
                        class="split-segment split-segment-remaining"
                        :style="{ flex: 1 }"
                        title="待分配剩余额度"
                      >
                        待分配 {{ formatMoney(remainingAmount) }}
                      </div>

                      <!-- 超核销溢出段 -->
                      <div
                        v-if="isOverSettled"
                        class="split-segment split-segment-over"
                        :style="{ width: '100%' }"
                        title="超核销异常警示"
                      >
                        ⚠️ 超额溢出 {{ formatMoney(Math.abs(remainingAmount)) }}
                      </div>
                    </template>
                  </div>

                  <!-- 图例列表 -->
                  <div v-if="!isCreateMode" class="split-legend-list" style="margin-top: 6px;">
                    <span
                      v-for="seg in allocationSegments"
                      :key="seg.id"
                      class="split-legend-pill"
                      :class="{ 'is-legend-active': hoveredSettlementId === seg.id }"
                      @mouseenter="handleSegmentHover(seg.id)"
                      @mouseleave="handleSegmentHover(null)"
                      @click="handleSegmentClick(seg.id)"
                    >
                      <span class="split-dot" :style="{ background: seg.color }"></span>
                      <b>{{ seg.settlementNo }}</b>: {{ formatMoney(seg.actualSettled) }}
                    </span>
                  </div>
                  <div v-else class="split-legend-list" style="margin-top: 6px;">
                    <span class="split-legend-pill is-legend-active">
                      <span class="split-dot" style="background: #0284c7;"></span>
                      待分配全额资金池 (100%)
                    </span>
                  </div>
                </div>
              </div>

              <!-- 2. 水单入账凭据事实卡片`;

content = content.replace(oldLeftRailHeadRegex, newLeftRailHead);

// 5. Update Right Canvas Segmented Bar & Add Create Guide View
const oldRightCanvasRegex = /<!-- 双模核销工作区切换器 -->[\s\S]*?<div v-show="activeCanvasTab === 'settlements'"/;

const newRightCanvas = `<!-- 双模核销工作区切换器 -->
                  <a-segmented
                    v-model:value="activeCanvasTab"
                    :options="isCreateMode ? [
                      { label: '新建向导与对账预备', value: 'create_guide' },
                      { label: '即时对账候选池预览 (' + selectableFeeList.length + '条待核)', value: 'pool' }
                    ] : [
                      { label: '关联收费核销单 (' + settlementListFiltered.length + ')', value: 'settlements' },
                      { label: '即时对账候选池 (' + selectableFeeList.length + '条应收待核)', value: 'pool' }
                    ]"
                  ></a-segmented>

                  <a-input
                    v-if="activeCanvasTab === 'settlements' && !isCreateMode"
                    v-model:value="searchSettlementNo"
                    placeholder="搜索核销单号..."
                    size="small"
                    style="width: 200px;"
                    allow-clear
                  >
                    <template #prefix>
                      <iconify-icon icon="ant-design:search-outlined" style="color: #94a3b8;"></iconify-icon>
                    </template>
                  </a-input>

                  <!-- 当前单选核销单 / 多选费用提示 -->
                  <span v-if="selectedSettlementId && activeCanvasTab === 'settlements'" class="toolbar-selection-pill">
                    <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon>
                    已选核销单: <b>{{ selectedSettlementRow?.settlementNo }}</b> ({{ selectedSettlementTypeLabel }})
                  </span>

                  <span v-if="selectedFeeCount > 0 && activeCanvasTab === 'settlements'" class="toolbar-selection-pill" style="background: #fef2f2; border-color: #fecaca; color: #b91c1c;">
                    <iconify-icon icon="ant-design:delete-outlined"></iconify-icon>
                    已跨单勾选费用: <b>{{ selectedFeeCount }}</b> 条
                  </span>
                </div>

                <!-- 右侧顶部统一操作按钮 -->
                <div class="strip-right-actions">
                  <template v-if="isCreateMode">
                    <a-space size="small">
                      <a-button
                        size="small"
                        type="primary"
                        ghost
                        @click="handleQuickFillCreateSample"
                      >
                        <template #icon><iconify-icon icon="ant-design:thunderbolt-outlined"></iconify-icon></template>
                        填入测试样本 (捷顺达 · ¥10,000)
                      </a-button>
                      <a-button
                        size="small"
                        type="primary"
                        @click="handleSaveAndStartReconcile"
                      >
                        <template #icon><iconify-icon icon="ant-design:check-outlined"></iconify-icon></template>
                        保存并立即对账
                      </a-button>
                    </a-space>
                  </template>
                  <template v-else-if="activeCanvasTab === 'settlements'">
                    <!-- 添加费用 (单选核销单驱动) -->
                    <a-button
                      size="small"
                      :disabled="!canAddFeeToSelected"
                      @click="openAddFeeDrawer"
                    >
                      <template #icon><iconify-icon icon="ant-design:plus-outlined"></iconify-icon></template>
                      添加费用
                    </a-button>

                    <!-- 批量删除费用 (多选费用驱动) -->
                    <a-button
                      size="small"
                      danger
                      :disabled="selectedFeeCount === 0 || currentStatement.locked"
                      @click="openBatchDeleteFeeModal"
                    >
                      <template #icon><iconify-icon icon="ant-design:delete-outlined"></iconify-icon></template>
                      删除费用 {{ selectedFeeCount > 0 ? ('(' + selectedFeeCount + ')') : '' }}
                    </a-button>

                    <!-- 删除整单 (单选核销单驱动) -->
                    <a-button
                      size="small"
                      danger
                      :disabled="!canDeleteSelectedSettlement"
                      @click="confirmDeleteSelectedSettlement"
                    >
                      删除核销单
                    </a-button>

                    <!-- 新建核销 (Dropdown: 按费用 / 按发票) -->
                    <a-dropdown>
                      <template #overlay>
                        <a-menu @click="handleCreateSettlementMenu">
                          <a-menu-item key="fee">
                            <iconify-icon icon="ant-design:unordered-list-outlined" style="margin-right: 6px;"></iconify-icon>
                            按费用核销
                          </a-menu-item>
                          <a-menu-item key="invoice">
                            <iconify-icon icon="ant-design:file-done-outlined" style="margin-right: 6px;"></iconify-icon>
                            按发票核销
                          </a-menu-item>
                        </a-menu>
                      </template>
                      <a-button
                        type="primary"
                        size="small"
                        :disabled="!canCreateNewSettlement"
                        @click="requestOpenWorkbench('fee')"
                      >
                        <template #icon><iconify-icon icon="ant-design:plus-circle-outlined"></iconify-icon></template>
                        新建收费核销
                        <iconify-icon icon="ant-design:down-outlined" style="font-size: 10px; margin-left: 4px;"></iconify-icon>
                      </a-button>
                    </a-dropdown>
                  </template>

                  <!-- 模式 B 下的操作 -->
                  <template v-else>
                    <a-space size="small">
                      <span style="font-size: 12px; color: #64748b;">
                        已勾选待核费用: <b style="color: #0284c7;">{{ selectedWorkbenchFeeIds.length }}</b> 笔
                      </span>
                    </a-space>
                  </template>
                </div>
              </div>

              <!-- 视图 0：新建向导与对账预备中心 (仅在创建模式展示) -->
              <div v-show="isCreateMode && activeCanvasTab === 'create_guide'" class="canvas-panel-view create-guide-container">
                <!-- Hero 引导卡片 -->
                <div class="create-guide-hero">
                  <div>
                    <div class="create-hero-title">
                      <iconify-icon icon="ant-design:form-outlined" style="font-size: 18px;"></iconify-icon>
                      <span>录入银行流水收款事实 · 即时发起应收对账</span>
                    </div>
                    <div class="create-hero-desc">
                      在左侧资金底账录入到账事实（付款客户、金额、入账账户及电子回单）。录入完成后点击「保存流水」或「⚡ 保存并立即对账」，系统将自动生成流水编号并解锁对账调度。
                    </div>
                  </div>
                  <div class="create-hero-actions">
                    <a-button
                      type="primary"
                      ghost
                      size="middle"
                      @click="handleQuickFillCreateSample"
                    >
                      <template #icon><iconify-icon icon="ant-design:thunderbolt-outlined"></iconify-icon></template>
                      填入标准示例数据 (捷顺达 · ¥10,000)
                    </a-button>
                    <a-button
                      type="primary"
                      size="middle"
                      @click="handleSaveAndStartReconcile"
                    >
                      <template #icon><iconify-icon icon="ant-design:arrow-right-outlined"></iconify-icon></template>
                      保存并立即开启对账
                    </a-button>
                  </div>
                </div>

                <!-- 录入就绪度四维检测卡片网格 -->
                <div class="readiness-grid">
                  <!-- 维度 1: 付款客户 -->
                  <div class="readiness-card" :class="currentStatement.settlementId ? 'is-ready' : 'is-pending'">
                    <div class="readiness-head">
                      <span>付款客户 (打款抬头)</span>
                      <a-tag :color="currentStatement.settlementId ? 'success' : 'warning'" size="small">
                        {{ currentStatement.settlementId ? '✓ 已选定' : '待在左侧选择' }}
                      </a-tag>
                    </div>
                    <div class="readiness-val" :title="currentStatement.settlementName">
                      {{ currentStatement.settlementName || '尚未选择付款方' }}
                    </div>
                    <div class="readiness-tip">
                      {{ currentStatement.settlementId ? '对账时将优先匹配该客户名下费用' : '必填项，影响对账候选池范围' }}
                    </div>
                  </div>

                  <!-- 维度 2: 到账金额 -->
                  <div class="readiness-card" :class="Number(currentStatement.amount) > 0 ? 'is-ready' : 'is-pending'">
                    <div class="readiness-head">
                      <span>到账总金额 (流水币)</span>
                      <a-tag :color="Number(currentStatement.amount) > 0 ? 'success' : 'warning'" size="small">
                        {{ Number(currentStatement.amount) > 0 ? '✓ 已录入' : '待输入金额' }}
                      </a-tag>
                    </div>
                    <div class="readiness-val" style="font-family: monospace; color: #0284c7;">
                      {{ Number(currentStatement.amount) > 0 ? formatMoney(currentStatement.amount) : '¥ 0.00' }}
                    </div>
                    <div class="readiness-tip">
                      {{ Number(currentStatement.amount) > 0 ? '左侧资金盘面已实时联动' : '必填项，决定本次可核销资金额度上限' }}
                    </div>
                  </div>

                  <!-- 维度 3: 我司入账账户与时间 -->
                  <div class="readiness-card is-ready">
                    <div class="readiness-head">
                      <span>入账账户与时间</span>
                      <a-tag color="success" size="small">✓ 默认已就绪</a-tag>
                    </div>
                    <div class="readiness-val">
                      {{ currentStatement.statementDate }} · 中国银行
                    </div>
                    <div class="readiness-tip">
                      中国银行青岛市南支行 (028374910293)
                    </div>
                  </div>

                  <!-- 维度 4: 回单凭证与附件 -->
                  <div class="readiness-card" :class="currentStatement.attachments?.length ? 'is-ready' : ''">
                    <div class="readiness-head">
                      <span>电子回单附件</span>
                      <a-tag :color="currentStatement.attachments?.length ? 'success' : 'default'" size="small">
                        {{ currentStatement.attachments?.length ? ('✓ 已上传 (' + currentStatement.attachments.length + ')') : '选填 (建议上传)' }}
                      </a-tag>
                    </div>
                    <div class="readiness-val">
                      {{ currentStatement.attachments?.length ? currentStatement.attachments[0].friendlyFileName : '暂未上传电子凭证' }}
                    </div>
                    <div class="readiness-tip">
                      支持 PDF/图片格式，保存后归档入账
                    </div>
                  </div>
                </div>

                <!-- 流程图示与业务向导 -->
                <div class="create-flow-steps-card">
                  <div style="font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 12px; display: flex; align-items: center; gap: 6px;">
                    <iconify-icon icon="ant-design:branches-outlined" style="color: #1677ff;"></iconify-icon>
                    <span>银行流水录入与对账核销标准作业流程 (SOP)</span>
                  </div>
                  <a-steps :current="currentStatement.settlementId && Number(currentStatement.amount) > 0 ? 1 : 0" size="small">
                    <a-step title="事实录入" description="在左侧输入付款方、到账金额、入账账户并上传回单"></a-step>
                    <a-step title="流水入库" description="点击保存流水，系统自动分配 SH 流水号并落库生效"></a-step>
                    <a-step title="应收对账" description="在右侧即时对账候选池勾选费用，一键冲抵生成核销单"></a-step>
                    <a-step title="闭环归档" description="额度全额消清或生成部分核销凭据，支持随时追溯审计"></a-step>
                  </a-steps>
                </div>

                <!-- 预备候选池预览卡片提示 -->
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 14px 16px;">
                  <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                    <span style="font-size: 13px; font-weight: 600; color: #1e293b;">
                      <iconify-icon icon="ant-design:table-outlined" style="color: #0284c7; margin-right: 6px;"></iconify-icon>
                      待核费用预览雷达 (当前系统池共 {{ selectableFeeList.length }} 笔应收账款待认领)
                    </span>
                    <a-button type="link" size="small" @click="activeCanvasTab = 'pool'">
                      切换至候选池视图 ➔
                    </a-button>
                  </div>
                  <p style="font-size: 12px; color: #64748b; margin: 0;">
                    💡 贴心提示：您可以直接点击上方「⚡ 保存并立即开启对账」，系统将立即自动完成入库并切换至对账池，您可立即勾选海运费、港杂费或订舱费执行核销，实现「录入即对账」的极致流畅体验。
                  </p>
                </div>
              </div>

              <!-- 视图 1：已关联收费核销单穿透表 (仅在非创建模式展示) -->
              <div v-show="!isCreateMode && activeCanvasTab === 'settlements'"`;

content = content.replace(oldRightCanvasRegex, newRightCanvas);

// 6. Update in-place dock bar for create mode support
const oldDockBarRegex = /<!-- 底部即时结算动态冲击条 \(In-Place Impact Dock Bar\) -->[\s\S]*?<a-space>[\s\S]*?<\/a-space>/;

const newDockBar = `<!-- 底部即时结算动态冲击条 (In-Place Impact Dock Bar) -->
                <div class="in-place-dock-bar">
                  <div class="in-place-stat-group">
                    <span>当前可用结余: <b style="font-family: monospace; color: #16a34a;">{{ formatMoney(isCreateMode ? (currentStatement.amount || 0) : remainingAmount) }}</b></span>
                    <span>｜</span>
                    <span>本次勾选核销: <b style="font-family: monospace; color: #0284c7;">{{ formatMoney(inPlaceTotalSelectedAmount) }}</b> ({{ selectedWorkbenchFeeIds.length }} 笔)</span>
                    <span>｜</span>
                    <span>核销后预计结余:
                      <b
                        style="font-family: monospace;"
                        :style="{ color: ((isCreateMode ? (currentStatement.amount || 0) : remainingAmount) - inPlaceTotalSelectedAmount) < -0.005 ? '#dc2626' : '#16a34a' }"
                      >
                        {{ formatMoney((isCreateMode ? (currentStatement.amount || 0) : remainingAmount) - inPlaceTotalSelectedAmount) }}
                      </b>
                    </span>
                  </div>

                  <a-space>
                    <a-button size="small" @click="activeCanvasTab = isCreateMode ? 'create_guide' : 'settlements'">
                      {{ isCreateMode ? '返回新建向导' : '返回核销单表' }}
                    </a-button>
                    <a-button v-if="!isCreateMode" size="small" @click="requestOpenWorkbench('fee')">高级模式 (抽屉)</a-button>
                    <a-button
                      size="small"
                      type="primary"
                      :disabled="selectedWorkbenchFeeIds.length === 0 || inPlaceTotalSelectedAmount <= 0 || ((isCreateMode ? (currentStatement.amount || 0) : remainingAmount) - inPlaceTotalSelectedAmount) < -0.005"
                      @click="isCreateMode ? handleSaveAndInstantMatchFees() : handleInPlaceInstantMatch()"
                    >
                      <template #icon><iconify-icon icon="ant-design:check-outlined"></iconify-icon></template>
                      {{ isCreateMode ? '保存流水并直接核销' : '就地确认并生成核销单' }}
                    </a-button>
                  </a-space>`;

content = content.replace(oldDockBarRegex, newDockBar);

// 7. Update JS presetsData & Methods
const presetDoneMarker = `// 7 大标准场景数据模板\n        const presetsData = {`;
const createPresetData = `// 7 大标准场景数据模板
        const presetsData = {
          // 场景 0：新增银行流水 (创建录入场景)
          preset_create: {
            isCreate: true,
            bankStatementNo: '',
            id: null,
            amount: null,
            currencyCode: 'RMB',
            statementDate: dayjs().format('YYYY-MM-DD'),
            statementTimeDayjs: dayjs(),
            transactionFee: 0.00,
            statementRemark: '',
            message: '',
            remark: '',
            orgId: 'ORG_001',
            orgName: '佳越国际物流（青岛）有限公司 / 财务部',
            orgBankAccountId: 'BANK_MY_01',
            orgBankAccountName: '中国银行青岛市南支行 (028374910293)',
            settlementId: null,
            settlementName: '',
            clientInvoiceBankId: null,
            clientInvoiceBankName: '',
            writeOffStatus: 0,
            inputType: 0,
            locked: false,
            creatorUserName: '当前操作员 (财务录入)',
            operators: [{ id: 1, name: '当前操作员', remark: '录入经办' }],
            attachments: [],
            settlements: []
          },`;

if (!content.includes('preset_create: {')) {
  content = content.replace(presetDoneMarker, createPresetData);
}

// 8. Update isCreateMode computed & Helper methods
const currentPresetMarker = `const currentPreset = ref('preset_done');`;
const isCreateComputed = `const currentPreset = ref('preset_done');

        const isCreateMode = computed(() => {
          return Boolean(currentStatement.isCreate);
        });`;

if (!content.includes('const isCreateMode = computed')) {
  content = content.replace(currentPresetMarker, isCreateComputed);
}

// 9. Update writeOffStatusTag
const oldWriteOffTagRegex = /const writeOffStatusTag = computed\(\(\) => \{[\s\S]*?return \{ label: '部分核销', color: 'warning' \};\s*\}\);/;
const newWriteOffTag = `const writeOffStatusTag = computed(() => {
          if (isCreateMode.value) {
            return { label: '草稿未入库', color: 'warning' };
          }
          if (currentSettledAmount.value <= 0) {
            return { label: '待核销', color: 'blue' };
          }
          if (Math.abs(remainingAmount.value) <= 0.005) {
            return { label: '核销完成', color: 'success' };
          }
          return { label: '部分核销', color: 'warning' };
        });`;

content = content.replace(oldWriteOffTagRegex, newWriteOffTag);

// 10. Update canEditCurrentAmount, canEditCurrencyAndPayer, canEditStatementFields
const oldCanEditRegex = /const canEditCurrentAmount = computed\(\(\) => \{[\s\S]*?return !currentStatement\.locked;\s*\}\);/;
const newCanEdit = `const canEditCurrentAmount = computed(() => {
          if (isCreateMode.value) return true;
          if (currentStatement.locked) return false;
          if (currentStatement.inputType === 1) return false;
          return true;
        });

        const canEditCurrencyAndPayer = computed(() => {
          if (isCreateMode.value) return true;
          if (currentStatement.locked) return false;
          if (currentStatement.inputType === 1) return false;
          return !hasReceiveSettlements.value;
        });

        const canEditStatementFields = computed(() => {
          if (isCreateMode.value) return true;
          if (currentStatement.locked) return false;
          if (currentStatement.inputType === 1) return false;
          return !hasReceiveSettlements.value;
        });

        const canEditRemark = computed(() => {
          if (isCreateMode.value) return true;
          return !currentStatement.locked;
        });`;

content = content.replace(oldCanEditRegex, newCanEdit);

// 11. Add handleQuickFillCreateSample, handleSaveAndStartReconcile, handleSaveAndInstantMatchFees
const handleSaveMarker = `function handleSaveStatement() {`;
const newCreateMethods = `function handleQuickFillCreateSample() {
          currentStatement.settlementId = 'PAYER_001';
          currentStatement.settlementName = '青岛捷顺达国际供应链管理有限公司';
          currentStatement.clientInvoiceBankId = 'BANK_CLI_01';
          currentStatement.clientInvoiceBankName = '招商银行深圳科苑支行 (75591823901)';
          currentStatement.amount = 10000.00;
          currentStatement.transactionFee = 0.00;
          currentStatement.statementRemark = '网银转账贷记来账-10月美线运费';
          currentStatement.message = '请查收10月集装箱海运费';
          currentStatement.remark = '捷顺达常规结算款，已填入';
          currentStatement.attachments = [
            { attachmentId: 'ATT_NEW_01', friendlyFileName: '中行网银转账电子回单_10000.pdf', fileSize: '168 KB' }
          ];
          markFormDirty();
          antd.message.success('已自动填入标准到账样本，左侧盘面已即刻联动！');
        }

        function handleSaveAndStartReconcile() {
          if (!currentStatement.settlementId) {
            antd.message.warning('请选择打款抬头的付款客户');
            return;
          }
          if (!currentStatement.amount || Number(currentStatement.amount) <= 0) {
            antd.message.warning('请输入有效的到账总金额（大于 0）');
            return;
          }
          if (!currentStatement.currencyCode) {
            antd.message.warning('请选择流水币别');
            return;
          }

          isSaving.value = true;
          setTimeout(() => {
            isSaving.value = false;
            const newNo = 'SH' + dayjs().format('YYMMDD') + String(Math.floor(Math.random() * 800) + 100);
            currentStatement.bankStatementNo = newNo;
            currentStatement.id = 'statement_' + Date.now();
            currentStatement.isCreate = false;
            currentStatement.writeOffStatus = 0; // 待核销
            Object.assign(savedSnapshot, JSON.parse(JSON.stringify(currentStatement)));
            savedFingerprint.value = formFingerprint.value;

            activeCanvasTab.value = 'pool';
            antd.message.success('银行流水 ' + newNo + ' 已成功保存入库！已自动为您就地开启即时对账候选池。');
          }, 600);
        }

        function handleSaveAndInstantMatchFees() {
          if (!currentStatement.settlementId) {
            antd.message.warning('请先在左侧选择付款客户');
            return;
          }
          if (!currentStatement.amount || Number(currentStatement.amount) <= 0) {
            antd.message.warning('请先在左侧输入到账总金额');
            return;
          }
          if (selectedWorkbenchFeeIds.value.length === 0) {
            antd.message.warning('请勾选待核销的费用明细');
            return;
          }
          const takeTotal = inPlaceTotalSelectedAmount.value;
          if (takeTotal > Number(currentStatement.amount)) {
            antd.message.error('所选核销金额已超出流水到账总金额');
            return;
          }

          isSaving.value = true;
          setTimeout(() => {
            isSaving.value = false;
            const newStatementNo = 'SH' + dayjs().format('YYMMDD') + String(Math.floor(Math.random() * 800) + 100);
            const newSettleNo = 'HX' + dayjs().format('YYMMDD') + String(Math.floor(Math.random() * 800) + 100);
            currentStatement.bankStatementNo = newStatementNo;
            currentStatement.id = 'statement_' + Date.now();
            currentStatement.isCreate = false;

            const chosenFees = selectableFeeList.value.filter(f => selectedWorkbenchFeeIds.value.includes(f.id));
            const newSettlement = {
              id: 'SETTLE_' + Date.now(),
              settlementNo: newSettleNo,
              type: 0,
              status: 2,
              actualSettled: takeTotal,
              originalSettledAmount: takeTotal,
              diffAmount: 0.00,
              itemCount: chosenFees.length,
              settlementTime: dayjs().format('YYYY-MM-DD HH:mm'),
              creatorUserName: '当前操作员',
              remark: '新增流水即时直核生成的核销单',
              items: chosenFees.map(f => ({
                id: f.id,
                orderNo: f.orderNo,
                masterBl: 'MSK' + Math.floor(100000 + Math.random() * 900000),
                etd: dayjs().format('YYYY-MM-DD'),
                pol: '青岛', pod: '长滩', container: '1*40HQ', carrier: 'MSK', opName: '孙立', saleName: '赵明',
                feeName: f.feeName, paySide: f.paySide, feeCurrency: f.feeCurrency,
                settledAmount: f.thisSettled, exchangeRate: f.exchangeRate, originalSettledAmount: f.thisSettled
              })),
              invoiceGroups: []
            };

            settlementList.value.unshift(newSettlement);
            selectableFeeList.value = selectableFeeList.value.filter(f => !selectedWorkbenchFeeIds.value.includes(f.id));
            selectedWorkbenchFeeIds.value = [];

            Object.assign(savedSnapshot, JSON.parse(JSON.stringify(currentStatement)));
            savedFingerprint.value = formFingerprint.value;

            activeCanvasTab.value = 'settlements';
            selectedSettlementId.value = newSettlement.id;
            expandedRowKeys.value = [newSettlement.id];
            antd.message.success('银行流水 ' + newStatementNo + ' 保存成功，并已即时生成核销单 ' + newSettleNo + '！');
          }, 600);
        }

        `;

if (!content.includes('function handleQuickFillCreateSample()')) {
  content = content.replace(handleSaveMarker, newCreateMethods + handleSaveMarker);
}

// 12. Also enhance handleSaveStatement when isCreateMode is true
const oldHandleSaveBodyRegex = /function handleSaveStatement\(\) \{[\s\S]*?if \(isAmountInvalid\.value\) \{[\s\S]*?return;\s*\}/;
const newHandleSaveBody = `function handleSaveStatement() {
          if (isCreateMode.value) {
            if (!currentStatement.settlementId) {
              antd.message.warning('请选择打款抬头的付款客户');
              return;
            }
            if (!currentStatement.amount || Number(currentStatement.amount) <= 0) {
              antd.message.warning('请输入有效的到账总金额（大于 0）');
              return;
            }
            if (!currentStatement.currencyCode) {
              antd.message.warning('请选择流水币别');
              return;
            }

            isSaving.value = true;
            setTimeout(() => {
              isSaving.value = false;
              const newNo = 'SH' + dayjs().format('YYMMDD') + String(Math.floor(Math.random() * 800) + 100);
              currentStatement.bankStatementNo = newNo;
              currentStatement.id = 'statement_' + Date.now();
              currentStatement.isCreate = false;
              currentStatement.writeOffStatus = 0;
              Object.assign(savedSnapshot, JSON.parse(JSON.stringify(currentStatement)));
              savedFingerprint.value = formFingerprint.value;
              activeCanvasTab.value = 'settlements';
              antd.message.success('银行流水 ' + newNo + ' 保存成功，当前状态为待核销！');
            }, 600);
            return;
          }

          if (!canEditCurrentAmount.value) {
            antd.message.warning('当前流水状态不可修改');
            return;
          }
          if (isAmountInvalid.value) {
            antd.message.error('银行流水金额不能小于已核销金额：' + formatMoney(currentSettledAmount.value));
            return;
          }`;

content = content.replace(oldHandleSaveBodyRegex, newHandleSaveBody);

// 13. Update onPresetChange to handle activeCanvasTab reset
const oldPresetChangeRegex = /if \(data\) \{[\s\S]*?expandedRowKeys\.value = data\.settlements\?\.length \? \[data\.settlements\[0\]\.id\] : \[\];\s*\}/;
const newPresetChange = `if (data) {
            Object.assign(currentStatement, JSON.parse(JSON.stringify(data)));
            currentStatement.statementTimeDayjs = dayjs(currentStatement.statementDate);
            Object.assign(savedSnapshot, JSON.parse(JSON.stringify(data)));
            settlementList.value = JSON.parse(JSON.stringify(data.settlements || []));
            savedFingerprint.value = formFingerprint.value;
            selectedSettlementId.value = null;
            selectedFeeIds.value = [];
            searchSettlementNo.value = '';
            hoveredSettlementId.value = null;
            expandedRowKeys.value = data.settlements?.length ? [data.settlements[0].id] : [];
            activeCanvasTab.value = data.isCreate ? 'create_guide' : 'settlements';
          }`;

content = content.replace(oldPresetChangeRegex, newPresetChange);

// 14. Return new variables and methods in Vue setup
const returnMarker = `return {
          bodycellslot,`;
const newReturn = `return {
          isCreateMode,
          handleQuickFillCreateSample,
          handleSaveAndStartReconcile,
          handleSaveAndInstantMatchFees,
          bodycellslot,`;

if (!content.includes('isCreateMode,')) {
  content = content.replace(returnMarker, newReturn);
}

fs.writeFileSync(targetFile, content, 'utf8');
console.log('Successfully updated bank-statement-edit.html with Create Mode scenario!');
