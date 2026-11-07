const fs = require('fs');
const path = require('path');

const targetFile = path.resolve(__dirname, '../pages/bank-statement-edit.html');
let content = fs.readFileSync(targetFile, 'utf8');

// 1. Update CSS: tighten Left Rail, remove attachment-notice-compact, compact item cards
const oldCssMarker = `.attachment-notice-compact {
      font-size: 11px;
      color: #64748b;
      margin-top: auto;
      line-height: 1.35;
      background: #f8fafc;
      padding: 4px 8px;
      border-radius: 4px;
      border: 1px dashed #cbd5e1;
    }`;

const newCssMarker = `.attachment-notice-compact {
      display: none;
    }

    .voucher-item-card {
      padding: 3px 8px !important;
      font-size: 11.5px !important;
    }

    .voucher-vertical-form {
      gap: 4px !important;
    }

    .v-readonly-pill {
      min-height: 24px !important;
      font-size: 11px !important;
      padding: 0 6px !important;
    }`;

if (content.includes(oldCssMarker)) {
  content = content.replace(oldCssMarker, newCssMarker);
}

// 2. Pair the 6 single rows into 3 Duos in the Left Rail form
const oldFormItemsRegex = /<!-- 归属财务组织 -->[\s\S]*?<!-- 内部备注 \(财务协作\) -->[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<\/div>\s*<!-- 3\. 到账凭证与回单/;

const newFormItems = `<!-- 双列 3: 归属组织 + 我司入账账户 -->
                    <div class="v-fact-duo">
                      <div class="v-fact-sub">
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

                      <div class="v-fact-sub">
                        <div class="v-fact-lbl">我司入账账户</div>
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
                    </div>

                    <!-- 双列 4: 对方开户行 + 银行交易摘要 -->
                    <div class="v-fact-duo">
                      <div class="v-fact-sub">
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

                      <div class="v-fact-sub">
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
                    </div>

                    <!-- 双列 5: 付款留言 + 内部备注 -->
                    <div class="v-fact-duo">
                      <div class="v-fact-sub">
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

                      <div class="v-fact-sub">
                        <div class="v-fact-lbl">内部备注 (财务协作)</div>
                        <a-input
                          v-if="canEditRemark"
                          v-model:value="currentStatement.remark"
                          placeholder="仅内部财务可见备注"
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
              </div>

              <!-- 3. 到账凭证与回单`;

content = content.replace(oldFormItemsRegex, newFormItems);

// 3. Remove redundant buttons from in-place dock bar
const oldDockBarRegex = /<!-- 底部即时结算动态冲击条 \(In-Place Impact Dock Bar\) -->[\s\S]*?<a-space>[\s\S]*?<\/a-space>\s*<\/div>/;

const newDockBar = `<!-- 底部即时结算动态冲击条 (In-Place Impact Dock Bar · 精简单一主动作) -->
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

                  <!-- 消除冗余按钮堆叠，仅保留 1 个明确的核销确认主动作 -->
                  <div>
                    <a-button
                      type="primary"
                      size="middle"
                      :disabled="selectedWorkbenchFeeIds.length === 0 || inPlaceTotalSelectedAmount <= 0 || ((isCreateMode ? (currentStatement.amount || 0) : remainingAmount) - inPlaceTotalSelectedAmount) < -0.005"
                      @click="isCreateMode ? handleSaveAndInstantMatchFees() : handleInPlaceInstantMatch()"
                    >
                      <template #icon><iconify-icon icon="ant-design:check-outlined"></iconify-icon></template>
                      {{ isCreateMode ? (selectedWorkbenchFeeIds.length > 0 ? ('保存流水并核销 (' + formatMoney(inPlaceTotalSelectedAmount) + ')') : '保存流水并直接核销') : (selectedWorkbenchFeeIds.length > 0 ? ('确认核销 (' + formatMoney(inPlaceTotalSelectedAmount) + ')') : '确认生成核销单') }}
                    </a-button>
                  </div>
                </div>`;

content = content.replace(oldDockBarRegex, newDockBar);

fs.writeFileSync(targetFile, content, 'utf8');
console.log('Successfully compacted Left Rail and streamlined Right Dock Bar buttons!');
