const fs = require('fs');
const path = require('path');

const targetFilePath = path.resolve(__dirname, '../pages/bank-statement-edit.html');
let content = fs.readFileSync(targetFilePath, 'utf8');

// 1. 查找并替换主体内容区 (从 top-cockpit-grid 到 </template>)
const startMarker = '<!-- 4. 主体内容区 (首屏驾驶舱 + 下方核销决策表) -->';
const endMarker = '<!-- ======================================================================\n           模态框与抽屉交互系统 (Modals & Drawers)';

const startIndex = content.indexOf(startMarker);
const endIndex = content.indexOf(endMarker);

if (startIndex === -1 || endIndex === -1) {
  console.error('Markers not found!', { startIndex, endIndex });
  process.exit(1);
}

const replacementBody = `<!-- 4. 主体内容区 (Master-Detail Dual-Rail 左右双轨沉浸式对账工作台) -->
        <template v-else>
          <div class="studio-split-container">

            <!-- ==================== 左轨：390px 独立常驻资金底账 (Pinned Financial Ledger Rail) ==================== -->
            <aside class="studio-left-rail">
              <!-- 1. 资金总成与核销水位大盘 (Pinned Liquidity Billboard) -->
              <div class="rail-card rail-liquidity-card">
                <div class="rail-card-head">
                  <span class="rail-card-title">
                    <iconify-icon icon="ant-design:pie-chart-outlined" style="color: #0284c7;"></iconify-icon>
                    <span>资金盘面与核销水位</span>
                  </span>
                  <div class="rail-extra-badge">
                    <a-popover title="可核销经办人" trigger="click" placement="bottomRight">
                      <template #content>
                        <div style="width: 240px;">
                          <p style="font-size: 12px; color: #64748b; margin-bottom: 8px;">具备此流水核销操作权限的人员：</p>
                          <a-tag v-for="user in currentStatement.operators" :key="user.id" color="blue" style="margin-bottom: 4px;">
                            {{ user.name }} ({{ user.remark || '核销经办' }})
                          </a-tag>
                        </div>
                      </template>
                      <a-button type="link" size="small" style="padding: 0; font-size: 11px;">
                        经办人 ({{ currentStatement.operators?.length || 1 }})
                      </a-button>
                    </a-popover>
                  </div>
                </div>

                <div class="rail-card-body" style="padding: 10px 12px;">
                  <!-- 三维资金大盘指标 -->
                  <div class="rail-metric-grid">
                    <div class="rail-metric-box">
                      <div class="metric-lbl">流水到账总额</div>
                      <div class="metric-num num-total">{{ formatMoney(savedSnapshot.amount) }}</div>
                      <span class="currency-tag" style="margin-top: 2px;">{{ currentStatement.currencyCode }}</span>
                    </div>
                    <div class="rail-metric-box">
                      <div class="metric-lbl">已核销金额</div>
                      <div class="metric-num num-settled">{{ formatMoney(currentSettledAmount) }}</div>
                      <span class="metric-sub" :style="{ color: isOverSettled ? '#dc2626' : (remainingAmount <= 0.005 ? '#16a34a' : '#0284c7') }">
                        消清率 {{ progressPercent }}%
                      </span>
                    </div>
                    <div class="rail-metric-box">
                      <div class="metric-lbl">剩余可用额度</div>
                      <div class="metric-num" :class="remainingClass">{{ formatMoney(remainingAmount) }}</div>
                      <span class="metric-sub" v-if="isOverSettled" style="color: #dc2626; font-weight: 700;">⚠️ 溢出风险</span>
                      <span class="metric-sub" v-else-if="remainingAmount <= 0.005" style="color: #16a34a; font-weight: 600;">✓ 全部结清</span>
                      <span class="metric-sub" v-else style="color: #16a34a;">可用于核销</span>
                    </div>
                  </div>

                  <!-- 交互式分段资金分配条 -->
                  <div class="split-bar-track" style="margin-top: 8px;">
                    <div
                      v-for="seg in allocationSegments"
                      :key="seg.id"
                      class="split-segment"
                      :class="{ 'is-highlighted-seg': hoveredSettlementId === seg.id }"
                      :style="{ width: seg.percent + '%', background: seg.color }"
                      :title="\`\${seg.settlementNo} (\${seg.type === 0 ? '按费用' : '按发票'})：\${formatMoney(seg.actualSettled)} (\${seg.percent}%)\`"
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
                  </div>

                  <!-- 图例列表 -->
                  <div class="split-legend-list" style="margin-top: 6px;">
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
                </div>
              </div>

              <!-- 2. 水单入账凭据事实卡片 (Bank Receipt Voucher Facts) -->
              <div class="rail-card bank-voucher-card">
                <div class="rail-card-head">
                  <span class="rail-card-title">
                    <iconify-icon icon="ant-design:file-protect-outlined" style="color: #475569;"></iconify-icon>
                    <span>水单交易事实</span>
                  </span>
                  <div class="rail-extra-badge">
                    <span v-if="currentStatement.locked" style="color: #dc2626; font-size: 11px;">
                      <iconify-icon icon="ant-design:lock-outlined"></iconify-icon> 关账冻结
                    </span>
                    <span v-else-if="currentStatement.inputType === 1" style="color: #0891b2; font-size: 11px;">
                      <iconify-icon icon="ant-design:info-circle-outlined"></iconify-icon> 银企直连
                    </span>
                    <span v-else-if="hasReceiveSettlements" style="color: #d97706; font-size: 11px;">
                      <iconify-icon icon="ant-design:lock-outlined"></iconify-icon> 要素锁定
                    </span>
                    <span v-else style="color: #16a34a; font-size: 11px;">
                      <iconify-icon icon="ant-design:edit-outlined"></iconify-icon> 待核销自由编辑
                    </span>
                  </div>
                </div>

                <div class="rail-card-body" style="padding: 10px 12px;">
                  <!-- 草稿与快照差异提示 -->
                  <div v-if="hasAmountDraftDifference" class="draft-alert-banner">
                    <span>
                      <iconify-icon icon="ant-design:warning-outlined"></iconify-icon>
                      草稿金额 {{ formatMoney(currentStatement.amount) }} (落库 {{ formatMoney(savedSnapshot.amount) }})
                    </span>
                    <a-button size="small" type="link" style="padding: 0; font-size: 11px;" @click="restoreSavedAmount">还原金额</a-button>
                  </div>

                  <div class="voucher-vertical-form">
                    <!-- 付款方客户 (打款抬头) -->
                    <div class="v-fact-item highlight-fact">
                      <div class="v-fact-lbl">
                        <span>付款客户 (打款抬头)</span>
                        <span v-if="canEditCurrencyAndPayer" class="required">*</span>
                      </div>
                      <a-select
                        v-if="canEditCurrencyAndPayer"
                        v-model:value="currentStatement.settlementId"
                        :options="payerOptions"
                        placeholder="请选择付款方"
                        show-search
                        size="small"
                        style="width: 100%;"
                        @change="onPayerChange"
                      ></a-select>
                      <div v-else class="v-readonly-pill is-locked" :title="currentStatement.settlementName">
                        <iconify-icon icon="ant-design:safety-certificate-filled" style="color: #0284c7; font-size: 13px;"></iconify-icon>
                        <span style="font-weight: 600; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                          {{ currentStatement.settlementName || '未指定' }}
                        </span>
                        <iconify-icon
                          icon="ant-design:copy-outlined"
                          class="copy-btn"
                          title="复制付款方名称"
                          @click="copyText(currentStatement.settlementName, '付款方名称已复制')"
                        ></iconify-icon>
                      </div>
                    </div>

                    <!-- 双列 1: 交易时间 + 流水币别 -->
                    <div class="v-fact-duo">
                      <div class="v-fact-sub">
                        <div class="v-fact-lbl">
                          <span>交易时间</span>
                          <span v-if="canEditStatementFields" class="required">*</span>
                        </div>
                        <a-date-picker
                          v-if="canEditStatementFields"
                          v-model:value="currentStatement.statementTimeDayjs"
                          format="YYYY-MM-DD"
                          style="width: 100%;"
                          size="small"
                          @change="markFormDirty"
                        ></a-date-picker>
                        <div v-else class="v-readonly-pill is-locked">
                          <iconify-icon icon="ant-design:calendar-outlined" style="color: #94a3b8;"></iconify-icon>
                          {{ currentStatement.statementDate || '-' }}
                        </div>
                      </div>

                      <div class="v-fact-sub">
                        <div class="v-fact-lbl">
                          <span>币别</span>
                          <span v-if="canEditCurrencyAndPayer" class="required">*</span>
                        </div>
                        <a-select
                          v-if="canEditCurrencyAndPayer"
                          v-model:value="currentStatement.currencyCode"
                          :options="currencyOptions"
                          size="small"
                          style="width: 100%;"
                          @change="markFormDirty"
                        ></a-select>
                        <div v-else class="v-readonly-pill is-locked">
                          <b style="color: #0284c7;">{{ currentStatement.currencyCode || '-' }}</b>
                        </div>
                      </div>
                    </div>

                    <!-- 双列 2: 流水金额 + 手续费 -->
                    <div class="v-fact-duo">
                      <div class="v-fact-sub">
                        <div class="v-fact-lbl">
                          <span>总金额 (流水币)</span>
                          <span v-if="canEditCurrentAmount" class="required">*</span>
                        </div>
                        <a-input-number
                          v-if="canEditCurrentAmount"
                          v-model:value="currentStatement.amount"
                          :min="0"
                          :precision="2"
                          :controls="false"
                          size="small"
                          style="width: 100%; font-family: monospace; font-weight: 700; color: #0f172a;"
                          :status="isAmountInvalid ? 'error' : ''"
                          @change="markFormDirty"
                        ></a-input-number>
                        <div v-else class="v-readonly-pill is-money">
                          {{ formatMoney(currentStatement.amount) }}
                        </div>
                      </div>

                      <div class="v-fact-sub">
                        <div class="v-fact-lbl">手续费</div>
                        <a-input-number
                          v-if="canEditStatementFields"
                          v-model:value="currentStatement.transactionFee"
                          :min="0"
                          :precision="2"
                          :controls="false"
                          size="small"
                          style="width: 100%; font-family: monospace;"
                          @change="markFormDirty"
                        ></a-input-number>
                        <div v-else class="v-readonly-pill is-money">
                          {{ formatMoney(currentStatement.transactionFee) }}
                        </div>
                      </div>
                    </div>

                    <!-- 归属财务组织 -->
                    <div class="v-fact-item">
                      <div class="v-fact-lbl">
                        <span>归属组织</span>
                        <span v-if="canEditStatementFields" class="required">*</span>
                      </div>
                      <a-select
                        v-if="canEditStatementFields"
                        v-model:value="currentStatement.orgId"
                        :options="orgOptions"
                        size="small"
                        style="width: 100%;"
                        @change="markFormDirty"
                      ></a-select>
                      <div v-else class="v-readonly-pill is-locked" :title="currentStatement.orgName">
                        <iconify-icon icon="ant-design:apartment-outlined" style="color: #64748b;"></iconify-icon>
                        <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                          {{ currentStatement.orgName || '-' }}
                        </span>
                      </div>
                    </div>

                    <!-- 我司入账银行账户 -->
                    <div class="v-fact-item">
                      <div class="v-fact-lbl">我司入账银行账户</div>
                      <a-select
                        v-if="canEditStatementFields"
                        v-model:value="currentStatement.orgBankAccountId"
                        :options="myBankOptions"
                        allow-clear
                        size="small"
                        style="width: 100%;"
                        @change="markFormDirty"
                      ></a-select>
                      <div v-else class="v-readonly-pill is-locked" :title="currentStatement.orgBankAccountName">
                        <iconify-icon icon="ant-design:bank-outlined" style="color: #059669;"></iconify-icon>
                        <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-family: monospace;">
                          {{ currentStatement.orgBankAccountName || '-' }}
                        </span>
                      </div>
                    </div>

                    <!-- 对方开户银行 -->
                    <div class="v-fact-item">
                      <div class="v-fact-lbl">对方开户银行</div>
                      <a-select
                        v-if="canEditStatementFields"
                        v-model:value="currentStatement.clientInvoiceBankId"
                        :options="clientBankOptions"
                        allow-clear
                        size="small"
                        style="width: 100%;"
                        :placeholder="currentStatement.settlementId ? '选择对方开户行' : '请先选付款方'"
                        :disabled="!currentStatement.settlementId"
                        @change="markFormDirty"
                      ></a-select>
                      <div v-else class="v-readonly-pill" :title="currentStatement.clientInvoiceBankName">
                        <iconify-icon icon="ant-design:wallet-outlined" style="color: #64748b;"></iconify-icon>
                        <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                          {{ currentStatement.clientInvoiceBankName || '-' }}
                        </span>
                      </div>
                    </div>

                    <!-- 银行交易摘要 (原始回单) -->
                    <div class="v-fact-item">
                      <div class="v-fact-lbl">银行交易摘要 (原始回单)</div>
                      <a-input
                        v-if="canEditStatementFields"
                        v-model:value="currentStatement.statementRemark"
                        placeholder="回单原始摘要"
                        size="small"
                        allow-clear
                        @change="markFormDirty"
                      ></a-input>
                      <div v-else class="v-readonly-pill" :title="currentStatement.statementRemark">
                        {{ currentStatement.statementRemark || '-' }}
                      </div>
                    </div>

                    <!-- 付款方附言留言 -->
                    <div class="v-fact-item">
                      <div class="v-fact-lbl">付款方附言留言</div>
                      <a-input
                        v-if="canEditStatementFields"
                        v-model:value="currentStatement.message"
                        placeholder="附言打款备注"
                        size="small"
                        allow-clear
                        @change="markFormDirty"
                      ></a-input>
                      <div v-else class="v-readonly-pill" :title="currentStatement.message">
                        {{ currentStatement.message || '-' }}
                      </div>
                    </div>

                    <!-- 内部备注 (财务协作) -->
                    <div class="v-fact-item">
                      <div class="v-fact-lbl">内部备注 (财务协作)</div>
                      <a-input
                        v-if="canEditRemark"
                        v-model:value="currentStatement.remark"
                        placeholder="仅内部财务可见的审核备注"
                        size="small"
                        allow-clear
                        @change="markFormDirty"
                      ></a-input>
                      <div v-else class="v-readonly-pill" :title="currentStatement.remark">
                        {{ currentStatement.remark || '-' }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 3. 到账凭证与回单 (Receipt Attachments) -->
              <div class="rail-card voucher-hub-card">
                <div class="rail-card-head">
                  <span class="rail-card-title">
                    <iconify-icon icon="ant-design:paper-clip-outlined" style="color: #475569;"></iconify-icon>
                    <span>到账凭证与回单 ({{ currentStatement.attachments?.length || 0 }})</span>
                  </span>
                  <div class="rail-extra-badge">
                    <a-upload
                      :before-upload="handleUploadAttachment"
                      :show-upload-list="false"
                      :disabled="!canEditCurrentAmount || isUploading"
                    >
                      <a-button size="small" type="link" style="padding: 0; font-size: 11px;" :loading="isUploading" :disabled="!canEditCurrentAmount">
                        <template #icon><iconify-icon icon="ant-design:upload-outlined"></iconify-icon></template>
                        上传凭据
                      </a-button>
                    </a-upload>
                  </div>
                </div>

                <div class="rail-card-body" style="padding: 8px 12px; gap: 4px;">
                  <div v-if="currentStatement.attachments?.length" style="display: flex; flex-direction: column; gap: 4px;">
                    <div
                      v-for="item in currentStatement.attachments"
                      :key="item.attachmentId"
                      class="voucher-item-card"
                    >
                      <div class="voucher-file-left">
                        <iconify-icon icon="ant-design:file-pdf-outlined" style="color: #dc2626; font-size: 14px; flex-shrink: 0;"></iconify-icon>
                        <span
                          style="font-size: 12px; font-weight: 500; color: #1e293b; cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
                          :title="item.friendlyFileName"
                          @click="previewAttachment(item)"
                        >
                          {{ item.friendlyFileName }}
                        </span>
                        <span v-if="item.friendlyFileName.includes('中行') || currentStatement.inputType === 1" class="official-seal-tag">
                          回单已验
                        </span>
                      </div>

                      <div style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">
                        <span style="font-size: 11px; color: #94a3b8;">{{ item.fileSize || '120 KB' }}</span>
                        <a-button
                          v-if="canEditCurrentAmount"
                          type="link"
                          danger
                          size="small"
                          style="padding: 0; font-size: 11px;"
                          @click="removeAttachment(item)"
                        >
                          移除
                        </a-button>
                      </div>
                    </div>
                  </div>

                  <div v-else style="padding: 8px; text-align: center; color: #94a3b8; font-size: 11px; background: #f8fafc; border-radius: 4px;">
                    暂无凭证附件，可点击右上角上传
                  </div>

                  <div class="attachment-notice-compact" style="margin-top: 6px;">
                    💡 附件在点击「保存流水」后正式生效；银企直连回单已通过防伪核验。
                  </div>
                </div>
              </div>

              <!-- 4. 左轨底座快捷操作 (Action Dock) -->
              <div class="rail-action-dock">
                <a-button size="middle" @click="handleBackToList" style="flex: 1;">返回列表</a-button>
                <a-button
                  type="primary"
                  size="middle"
                  :loading="isSaving"
                  :disabled="!canEditCurrentAmount || !hasUnsavedChanges"
                  @click="handleSaveStatement"
                  style="flex: 1.4;"
                >
                  <template #icon><iconify-icon icon="ant-design:save-outlined"></iconify-icon></template>
                  保存流水
                  <span v-if="hasUnsavedChanges" class="dock-unsaved-dot"></span>
                </a-button>
              </div>
            </aside>

            <!-- ==================== 右轨：全高核销调度与对账画布 (Reconciliation Studio Canvas) ==================== -->
            <main class="studio-right-canvas">
              <!-- 画布顶部统筹指令条 (Command Strip) -->
              <div class="canvas-command-strip">
                <div class="strip-left-section">
                  <!-- 双模核销工作区切换器 -->
                  <a-segmented
                    v-model:value="activeCanvasTab"
                    :options="[
                      { label: \`关联收费核销单 (\${settlementListFiltered.length})\`, value: 'settlements' },
                      { label: \`即时对账候选池 (\${selectableFeeList.length}条应收待核)\`, value: 'pool' }
                    ]"
                  ></a-segmented>

                  <a-input
                    v-if="activeCanvasTab === 'settlements'"
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
                  <template v-if="activeCanvasTab === 'settlements'">
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
                      删除费用 {{ selectedFeeCount > 0 ? \`(\${selectedFeeCount})\` : '' }}
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
                      <a-button size="small" @click="activeCanvasTab = 'settlements'">
                        返回核销单表
                      </a-button>
                      <a-button
                        size="small"
                        type="primary"
                        :disabled="selectedWorkbenchFeeIds.length === 0 || inPlaceTotalSelectedAmount <= 0 || (remainingAmount - inPlaceTotalSelectedAmount) < -0.005"
                        @click="handleInPlaceInstantMatch"
                      >
                        <template #icon><iconify-icon icon="ant-design:check-outlined"></iconify-icon></template>
                        就地确认并生成核销单
                      </a-button>
                    </a-space>
                  </template>
                </div>
              </div>

              <!-- 视图 1：关联收费核销单高密度决策表 -->
              <div v-show="activeCanvasTab === 'settlements'" ref="settlementSectionRef" class="canvas-panel-view">
                <!-- 空态展示 -->
                <div v-if="settlementListFiltered.length === 0" class="settlement-empty-container">
                  <div class="empty-icon-wrap">
                    <iconify-icon :icon="searchSettlementNo ? 'ant-design:file-search-outlined' : 'ant-design:account-book-outlined'"></iconify-icon>
                  </div>
                  <div style="font-size: 14px; font-weight: 600; color: #1e293b;">
                    {{ searchSettlementNo ? '未找到匹配的收费核销单' : '暂无关联收费核销单' }}
                  </div>
                  <p style="font-size: 12px; color: #64748b; margin: 0; max-width: 480px;">
                    <template v-if="searchSettlementNo">
                      请尝试核对核销单号是否有误，或清除搜索条件重新查看。
                    </template>
                    <template v-else>
                      当前流水总金额 {{ formatMoney(savedSnapshot.amount) }}，剩余可用核销额度
                      <b style="color: #16a34a;">{{ formatMoney(remainingAmount) }}</b>。您可以立即基于本流水创建第一张核销单。
                    </template>
                  </p>
                  <div style="margin-top: 6px;">
                    <a-button v-if="searchSettlementNo" size="small" @click="searchSettlementNo = ''">清除搜索</a-button>
                    <a-space v-else-if="canCreateNewSettlement">
                      <a-button type="primary" size="small" @click="requestOpenWorkbench('fee')">
                        按费用核销
                      </a-button>
                      <a-button size="small" @click="requestOpenWorkbench('invoice')">
                        按发票核销
                      </a-button>
                    </a-space>
                  </div>
                </div>

                <!-- 关联核销单高密度数据表 -->
                <a-table
                  v-else
                  :data-source="settlementListFiltered"
                  :columns="settlementColumns"
                  :pagination="false"
                  row-key="id"
                  size="small"
                  class="settlement-table"
                  :row-selection="settlementRowSelection"
                  :row-class-name="getSettlementRowClassName"
                  v-model:expanded-row-keys="expandedRowKeys"
                  :scroll="{ y: 560 }"
                >
                  <!-- 展开行：费用明细 / 发票开出两级结构 -->
                  <template v-slot:[expandrowslot]="{ record }">
                    <!-- 1. 按费用核销明细展开 -->
                    <div v-if="record.type === 0" class="expanded-detail-box">
                      <div class="expanded-header-bar">
                        <span>
                          <iconify-icon icon="ant-design:bars-outlined"></iconify-icon>
                          <b>{{ record.settlementNo }}</b> · 费用明细清单 (共 {{ record.items?.length || 0 }} 条)
                          <span style="color: #94a3b8; margin-left: 8px;">
                            💡 支持勾选多条费用后，点击上方统一操作栏中的【删除费用】
                          </span>
                        </span>
                        <span class="amount-cell-number" style="color: #0284c7;">
                          本次结算小计: {{ formatMoney(record.actualSettled) }}
                        </span>
                      </div>

                      <a-table
                        :data-source="record.items"
                        :columns="feeItemColumns"
                        :pagination="false"
                        row-key="id"
                        size="small"
                        :row-selection="getFeeItemRowSelection(record.id)"
                      >
                        <template v-slot:[bodycellslot]="{ column, record: fee }">
                          <template v-if="column.key === 'orderNo'">
                            <span style="font-family: monospace; font-weight: 600;">{{ fee.orderNo }}</span>
                            <iconify-icon
                              icon="ant-design:copy-outlined"
                              class="copy-btn"
                              title="复制委托编号"
                              @click="copyText(fee.orderNo, '委托编号已复制')"
                            ></iconify-icon>
                          </template>

                          <template v-else-if="column.key === 'masterBl'">
                            <span style="font-family: monospace;">{{ fee.masterBl || '-' }}</span>
                            <iconify-icon
                              v-if="fee.masterBl"
                              icon="ant-design:copy-outlined"
                              class="copy-btn"
                              title="复制提单号"
                              @click="copyText(fee.masterBl, '主提单号已复制')"
                            ></iconify-icon>
                          </template>

                          <template v-else-if="column.key === 'voyageSummary'">
                            <span class="logistics-voyage-tag">
                              <span class="voyage-route">{{ fee.pol || '-' }} ➔ {{ fee.pod || '-' }}</span>
                              <span class="voyage-sep">·</span>
                              <span class="voyage-meta">{{ fee.container || '-' }}</span>
                              <span class="voyage-sep">·</span>
                              <span class="voyage-meta">{{ fee.carrier || '-' }}</span>
                              <span class="voyage-sep">·</span>
                              <span class="voyage-date">{{ fee.etd || '-' }}</span>
                            </span>
                          </template>

                          <template v-else-if="column.key === 'feeStaff'">
                            <span class="staff-pair-pill" :title="\`操作：\${fee.opName || '-'} / 揽货：\${fee.saleName || '-'}\`">
                              <span>操: {{ fee.opName || '-' }}</span>
                              <span style="color: #cbd5e1;">|</span>
                              <span>揽: {{ fee.saleName || '-' }}</span>
                            </span>
                          </template>

                          <template v-else-if="column.key === 'feeName'">
                            <span style="font-weight: 600;">{{ fee.feeName }}</span>
                          </template>

                          <template v-else-if="column.key === 'paySide'">
                            <a-tag :color="fee.paySide === 1 ? 'blue' : 'orange'" size="small">
                              {{ fee.paySide === 1 ? '应收' : '应付' }}
                            </a-tag>
                          </template>

                          <template v-else-if="column.key === 'feeCurrency'">
                            <a-tag size="small">{{ fee.feeCurrency }}</a-tag>
                          </template>

                          <template v-else-if="column.key === 'settledAmount'">
                            <span class="amount-cell-number amount-cell-emphasis">{{ formatMoney(fee.settledAmount) }}</span>
                          </template>

                          <template v-else-if="column.key === 'exchangeRate'">
                            <span class="amount-cell-number" style="color: #64748b;">{{ Number(fee.exchangeRate).toFixed(4) }}</span>
                          </template>

                          <template v-else-if="column.key === 'originalSettledAmount'">
                            <span class="amount-cell-number">{{ formatMoney(fee.originalSettledAmount) }}</span>
                          </template>
                        </template>
                      </a-table>
                    </div>

                    <!-- 2. 按发票开出核销明细展开 -->
                    <div v-else class="expanded-detail-box">
                      <div class="expanded-header-bar">
                        <span>
                          <iconify-icon icon="ant-design:file-done-outlined"></iconify-icon>
                          <b>{{ record.settlementNo }}</b> · 关联发票开出与费用拆解 (共 {{ record.invoiceIssues?.length || 0 }} 个开出单)
                        </span>
                        <span class="amount-cell-number" style="color: #0284c7;">
                          本次核销小计: {{ formatMoney(record.actualSettled) }}
                        </span>
                      </div>

                      <div v-for="inv in record.invoiceIssues" :key="inv.id" class="invoice-issue-card">
                        <div class="invoice-issue-card-head">
                          <span>发票开出单: <b style="font-family: monospace;">{{ inv.issueNo }}</b></span>
                          <span style="color: #64748b;">发票号码: <b style="font-family: monospace; color: #1e293b;">{{ inv.invoiceNo || '-' }}</b></span>
                          <span style="color: #64748b;">币别: <a-tag size="small">{{ inv.currencyCode }}</a-tag></span>
                          <span style="margin-left: auto;" class="amount-cell-number">
                            价税合计: {{ formatMoney(inv.totalAmount) }} ｜ 本次核销: <b style="color: #0284c7;">{{ formatMoney(inv.settledAmount) }}</b>
                          </span>
                        </div>

                        <a-table
                          :data-source="inv.feeItems"
                          :columns="invoiceFeeColumns"
                          :pagination="false"
                          row-key="id"
                          size="small"
                        >
                          <template v-slot:[bodycellslot]="{ column, record: item }">
                            <template v-if="column.key === 'orderNo'">
                              <span style="font-family: monospace; font-weight: 600;">{{ item.orderNo }}</span>
                            </template>
                            <template v-else-if="column.key === 'voyageSummary'">
                              <span class="logistics-voyage-tag">
                                <span class="voyage-route">{{ item.pol || '-' }} ➔ {{ item.pod || '-' }}</span>
                                <span class="voyage-sep">·</span>
                                <span class="voyage-meta">{{ item.container || '-' }}</span>
                                <span class="voyage-sep">·</span>
                                <span class="voyage-meta">{{ item.carrier || '-' }}</span>
                                <span class="voyage-sep">·</span>
                                <span class="voyage-date">{{ item.etd || '-' }}</span>
                              </span>
                            </template>
                            <template v-else-if="column.key === 'feeStaff'">
                              <span class="staff-pair-pill" :title="\`操作：\${item.opName || '-'} / 揽货：\${item.saleName || '-'}\`">
                                <span>操: {{ item.opName || '-' }}</span>
                                <span style="color: #cbd5e1;">|</span>
                                <span>揽: {{ item.saleName || '-' }}</span>
                              </span>
                            </template>
                            <template v-else-if="column.key === 'feeName'">
                              <span>{{ item.feeName }}</span>
                            </template>
                            <template v-else-if="column.key === 'invoicedAmount'">
                              <span class="amount-cell-number">{{ formatMoney(item.invoicedAmount) }}</span>
                            </template>
                            <template v-else-if="column.key === 'settledAmount'">
                              <span class="amount-cell-number amount-cell-emphasis">{{ formatMoney(item.settledAmount) }}</span>
                            </template>
                          </template>
                        </a-table>
                      </div>
                    </div>
                  </template>

                  <!-- 表体自定义单元格 -->
                  <template v-slot:[bodycellslot]="{ column, record }">
                    <template v-if="column.key === 'settlementNo'">
                      <a
                        href="javascript:void(0)"
                        style="font-family: monospace; font-weight: 700; color: #1677ff;"
                        @click="handleOpenEditSettlement(record)"
                        :title="\`点击进入核销单 \${record.settlementNo} 编辑工作台\`"
                      >
                        {{ record.settlementNo }}
                      </a>
                      <iconify-icon
                        icon="ant-design:copy-outlined"
                        class="copy-btn"
                        title="复制核销单号"
                        @click="copyText(record.settlementNo, '核销单号已复制')"
                      ></iconify-icon>
                    </template>

                    <template v-else-if="column.key === 'type'">
                      <a-tag :color="record.type === 0 ? 'blue' : 'purple'" size="small">
                        {{ record.type === 0 ? '按费用' : '按发票' }}
                      </a-tag>
                    </template>

                    <template v-else-if="column.key === 'status'">
                      <span class="status-glow-pill" :class="record.status === 2 ? 'pill-success' : 'pill-blue'">
                        <span class="pulse-dot"></span>
                        {{ record.status === 2 ? '已结算' : '审批中' }}
                      </span>
                    </template>

                    <template v-else-if="column.key === 'actualSettled'">
                      <span class="amount-cell-number amount-cell-emphasis">
                        {{ formatMoney(record.actualSettled) }}
                      </span>
                    </template>

                    <template v-else-if="column.key === 'originalSettledAmount'">
                      <span class="amount-cell-number">
                        {{ formatMoney(record.originalSettledAmount) }}
                      </span>
                    </template>

                    <template v-else-if="column.key === 'diffAmount'">
                      <span
                        class="amount-cell-number"
                        :class="Math.abs(Number(record.diffAmount || 0)) > 0.005 ? 'amount-diff-warn' : 'amount-diff-muted'"
                      >
                        {{ formatMoney(record.diffAmount) }}
                      </span>
                    </template>

                    <template v-else-if="column.key === 'itemCount'">
                      <span style="font-family: monospace;">{{ record.itemCount || 0 }} 条</span>
                    </template>

                    <template v-else-if="column.key === 'remark'">
                      <span style="color: #334155;">{{ record.remark || '-' }}</span>
                    </template>
                  </template>
                </a-table>
              </div>

              <!-- 视图 2：即时对账候选池 (In-Place Matching Canvas) -->
              <div v-show="activeCanvasTab === 'pool'" class="canvas-panel-view in-place-pool-view">
                <!-- 待核费用检索与快捷过滤 -->
                <div class="workbench-filter-box" style="margin: 12px 14px 6px; border-radius: 6px;">
                  <div style="display: grid; grid-template-columns: repeat(4, 1fr) auto; gap: 8px 10px; align-items: end;">
                    <div>
                      <div class="v-fact-lbl">委托客户</div>
                      <a-input v-model:value="feeFilter.clientName" placeholder="委托客户名" size="small" allow-clear></a-input>
                    </div>
                    <div>
                      <div class="v-fact-lbl">业务编号 (委托/提单)</div>
                      <a-input v-model:value="feeFilter.keyword" placeholder="模糊匹配三类编号" size="small" allow-clear></a-input>
                    </div>
                    <div>
                      <div class="v-fact-lbl">开船日期区间</div>
                      <a-range-picker v-model:value="feeFilter.etdRange" size="small" style="width: 100%;"></a-range-picker>
                    </div>
                    <div>
                      <div class="v-fact-lbl">收付方向</div>
                      <a-select v-model:value="feeFilter.paySide" size="small" style="width: 100%;">
                        <a-select-option :value="1">仅应收</a-select-option>
                        <a-select-option :value="2">全部 (应收应付互抵)</a-select-option>
                      </a-select>
                    </div>
                    <div>
                      <a-button type="primary" size="small" style="margin-right: 6px;" @click="handleFilterFees">查询</a-button>
                      <a-button size="small" @click="resetFeeFilter">重置</a-button>
                    </div>
                  </div>
                </div>

                <!-- 自动分配快捷栏 -->
                <div class="auto-alloc-box" style="margin: 0 14px 8px;">
                  <div style="font-size: 12px; color: #166534;">
                    <iconify-icon icon="ant-design:thunderbolt-outlined" style="font-size: 14px; margin-right: 4px;"></iconify-icon>
                    <b>按金额自动分配：</b>录入分配金额，系统按净额小的业务自动勾选并分配流水额度。
                  </div>
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 12px; color: #475569;">分配额度:</span>
                    <a-input-number
                      v-model:value="autoAllocAmount"
                      size="small"
                      :min="0.01"
                      :max="remainingAmount"
                      :precision="2"
                      placeholder="≤ 剩余可用"
                      style="width: 130px; font-family: monospace;"
                    ></a-input-number>
                    <a-button
                      size="small"
                      type="primary"
                      ghost
                      :disabled="!autoAllocAmount || autoAllocAmount <= 0"
                      @click="executeAutoAlloc"
                    >
                      自动分配选中
                    </a-button>
                  </div>
                </div>

                <!-- 候选费用数据表格 -->
                <div style="flex: 1; padding: 0 14px 10px; min-height: 0;">
                  <a-table
                    :data-source="selectableFeeList"
                    :columns="workbenchFeeColumns"
                    :pagination="false"
                    row-key="id"
                    size="small"
                    class="settlement-table"
                    :row-selection="workbenchFeeRowSelection"
                    :scroll="{ x: 1380, y: 380 }"
                  >
                    <template v-slot:[bodycellslot]="{ column, record: fee }">
                      <template v-if="column.key === 'orderNo'">
                        <span style="font-family: monospace; font-weight: 600;">{{ fee.orderNo }}</span>
                      </template>
                      <template v-else-if="column.key === 'paySide'">
                        <a-tag :color="fee.paySide === 1 ? 'blue' : 'orange'" size="small">
                          {{ fee.paySide === 1 ? '应收' : '应付' }}
                        </a-tag>
                      </template>
                      <template v-else-if="column.key === 'feeCurrency'">
                        <a-tag size="small">{{ fee.feeCurrency }}</a-tag>
                      </template>
                      <template v-else-if="column.key === 'unsettledAmount'">
                        <span class="amount-cell-number">{{ formatAmountPlain(fee.unsettledAmount) }}</span>
                      </template>
                      <template v-else-if="column.key === 'exchangeRate'">
                        <a-input-number
                          v-model:value="fee.exchangeRate"
                          size="small"
                          :min="0.000001"
                          :precision="6"
                          style="width: 100px; font-family: monospace;"
                          @change="updateFeeConverted(fee)"
                        ></a-input-number>
                      </template>
                      <template v-else-if="column.key === 'thisSettled'">
                        <a-input-number
                          v-model:value="fee.thisSettled"
                          size="small"
                          :precision="2"
                          style="width: 110px; font-family: monospace; font-weight: 600;"
                          @change="updateFeeConverted(fee)"
                        ></a-input-number>
                      </template>
                    </template>
                  </a-table>
                </div>

                <!-- 底部即时结算动态冲击条 (In-Place Impact Dock Bar) -->
                <div class="in-place-dock-bar">
                  <div class="in-place-stat-group">
                    <span>当前可用结余: <b style="font-family: monospace; color: #16a34a;">{{ formatMoney(remainingAmount) }}</b></span>
                    <span>｜</span>
                    <span>本次勾选核销: <b style="font-family: monospace; color: #0284c7;">{{ formatMoney(inPlaceTotalSelectedAmount) }}</b> ({{ selectedWorkbenchFeeIds.length }} 笔)</span>
                    <span>｜</span>
                    <span>核销后预计结余:
                      <b
                        style="font-family: monospace;"
                        :style="{ color: (remainingAmount - inPlaceTotalSelectedAmount) < -0.005 ? '#dc2626' : '#16a34a' }"
                      >
                        {{ formatMoney(remainingAmount - inPlaceTotalSelectedAmount) }}
                      </b>
                    </span>
                  </div>

                  <a-space>
                    <a-button size="small" @click="activeCanvasTab = 'settlements'">返回核销单表</a-button>
                    <a-button size="small" @click="requestOpenWorkbench('fee')">高级模式 (抽屉)</a-button>
                    <a-button
                      size="small"
                      type="primary"
                      :disabled="selectedWorkbenchFeeIds.length === 0 || inPlaceTotalSelectedAmount <= 0 || (remainingAmount - inPlaceTotalSelectedAmount) < -0.005"
                      @click="handleInPlaceInstantMatch"
                    >
                      <template #icon><iconify-icon icon="ant-design:check-outlined"></iconify-icon></template>
                      就地确认并生成核销单
                    </a-button>
                  </a-space>
                </div>
              </div>
            </main>

          </div>
        </template>

      </div>\n\n      `;

content = content.substring(0, startIndex) + replacementBody + content.substring(endIndex);

// 2. 更新 Vue Script Setup：添加 activeCanvasTab 与 handleInPlaceInstantMatch
const setupStateMarker = "const workbenchMode = ref('fee');";
if (content.includes(setupStateMarker)) {
  content = content.replace(setupStateMarker, "const activeCanvasTab = ref('settlements'); // 'settlements' | 'pool'\n        const workbenchMode = ref('fee');");
}

const methodMarker = "function executeAutoAlloc() {";
const inPlaceMethodCode = `const inPlaceTotalSelectedAmount = computed(() => {
          return selectableFeeList.value
            .filter(f => selectedWorkbenchFeeIds.value.includes(f.id))
            .reduce((sum, f) => sum + (Number(f.thisSettled) || 0), 0);
        });

        function handleInPlaceInstantMatch() {
          if (hasUnsavedChanges.value) {
            pendingActionAfterSave.value = () => handleInPlaceInstantMatch();
            showUnsavedAlertModal.value = true;
            return;
          }
          if (selectedWorkbenchFeeIds.value.length === 0) {
            antd.message.warning('请先在待核销费用池中勾选费用');
            return;
          }
          const takeTotal = inPlaceTotalSelectedAmount.value;
          if (takeTotal <= 0) {
            antd.message.warning('本次核销金额必须大于 0');
            return;
          }
          if ((remainingAmount.value - takeTotal) < -0.005) {
            antd.message.error('所选核销金额已超出流水剩余可用额度');
            return;
          }

          const newNo = \`HX\${dayjs().format('YYMMDD')}\${String(Math.floor(Math.random() * 900) + 100)}\`;
          const chosenFees = selectableFeeList.value.filter(f => selectedWorkbenchFeeIds.value.includes(f.id));
          const newSettlement = {
            id: \`NEW_SETTLE_\${Date.now()}\`,
            settlementNo: newNo,
            type: 0,
            status: 2,
            actualSettled: takeTotal,
            originalSettledAmount: takeTotal,
            diffAmount: 0.00,
            itemCount: chosenFees.length,
            settlementTime: dayjs().format('YYYY-MM-DD HH:mm'),
            creatorUserName: '当前经办人',
            remark: '就地直核生成的收费核销单',
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
          activeCanvasTab.value = 'settlements';
          selectedSettlementId.value = newSettlement.id;
          expandedRowKeys.value = [newSettlement.id];
          antd.message.success(\`已成功就地生成核销单 \${newNo}，流水额度已即时划扣！\`);
        }

        function executeAutoAlloc() {`;

if (content.includes(methodMarker)) {
  content = content.replace(methodMarker, inPlaceMethodCode);
}

// 3. 在 setup 的 return 对象中暴露新属性
const returnMarker = 'bodycellslot,';
if (content.includes(returnMarker)) {
  content = content.replace(returnMarker, 'bodycellslot,\n          activeCanvasTab,\n          inPlaceTotalSelectedAmount,\n          handleInPlaceInstantMatch,');
}

fs.writeFileSync(targetFilePath, content, 'utf8');
console.log('Successfully updated bank-statement-edit.html to Master-Detail Dual-Rail Studio!');
