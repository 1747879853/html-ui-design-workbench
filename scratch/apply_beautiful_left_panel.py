import re

with open('scratch/build_comprehensive_workbench.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS for left-business-panel
old_css = '''    /* 左侧业务信息卡片 */
    .left-business-panel {
      width: 410px;
      flex-shrink: 0;
      background: #ffffff;
      border-radius: 4px;
      border: 1px solid #d9d9d9;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transition: width 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .left-business-panel.is-collapsed {
      width: 44px;
      cursor: pointer;
    }
    .panel-header-bar {
      height: 36px;
      padding: 0 10px;
      background: #fafafa;
      border-bottom: 1px solid #e8e8e8;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .panel-title {
      font-size: 13px;
      font-weight: 600;
      color: #111827;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .panel-actions {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .panel-collapsed-strip {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 12px 0;
      background: #fafafa;
    }
    .collapsed-vertical-text {
      writing-mode: vertical-lr;
      letter-spacing: 4px;
      font-weight: 600;
      color: #374151;
      font-size: 13px;
    }

    /* 左侧表单滚动体 */
    .business-form-scroll {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 10px 12px;
    }
    .business-form-scroll::-webkit-scrollbar {
      width: 5px;
    }
    .business-form-scroll::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 3px;
    }

    /* 业务字段紧凑排布 */
    .biz-field-row {
      display: flex;
      gap: 8px;
      margin-bottom: 8px;
    }
    .biz-field-row.single {
      flex-direction: column;
      gap: 3px;
    }
    .biz-field-col {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 3px;
      min-width: 0;
    }
    .biz-label {
      font-size: 11px;
      color: #4b5563;
      font-weight: 500;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .biz-label.required::before {
      content: '*';
      color: #ff4d4f;
      margin-right: 3px;
    }
    .biz-helper {
      font-size: 10px;
      color: #9ca3af;
      line-height: 1.2;
    }

    /* 复合输入控件组合 */
    .compound-input-group {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* 干系人卡片 */
    .stakeholder-card {
      background: #f9fafb;
      border: 1px solid #e5e7eb;
      border-radius: 4px;
      padding: 8px 10px;
      margin-top: 8px;
    }
    .stakeholder-header {
      font-size: 11px;
      font-weight: 600;
      color: #374151;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
    }
    .stakeholder-row {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 6px;
    }
    .stakeholder-role-tag {
      width: 44px;
      font-size: 11px;
      color: #4b5563;
      flex-shrink: 0;
      text-align: right;
    }'''

new_css = '''    /* ==========================================================================
       左侧业务信息卡片 (410px 模块化微卡重构：去灰、去杂、立体呼吸感)
       ========================================================================== */
    .left-business-panel {
      width: 410px;
      flex-shrink: 0;
      background: #f1f5f9;
      border-radius: 6px;
      border: 1px solid #cbd5e1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transition: width 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .left-business-panel.is-collapsed {
      width: 44px;
      cursor: pointer;
    }
    .panel-header-bar {
      height: 38px;
      padding: 0 12px;
      background: #ffffff;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .panel-title-wrap {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .panel-title {
      font-size: 13px;
      font-weight: 700;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .panel-actions {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .panel-collapsed-strip {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 12px 0;
      background: #f8fafc;
    }
    .collapsed-vertical-text {
      writing-mode: vertical-lr;
      letter-spacing: 4px;
      font-weight: 600;
      color: #374151;
      font-size: 13px;
    }

    /* 左侧表单滚动体 */
    .business-form-scroll {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .business-form-scroll::-webkit-scrollbar {
      width: 4px;
    }
    .business-form-scroll::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 2px;
    }

    /* 模块化业务卡片 (Micro Cards) */
    .biz-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 8px 10px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }
    .biz-card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
      font-weight: 700;
      color: #334155;
      padding-bottom: 5px;
      margin-bottom: 6px;
      border-bottom: 1px solid #f1f5f9;
    }
    .biz-card-title {
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .biz-card-badge {
      font-size: 10px;
      font-weight: normal;
      color: #64748b;
    }

    /* 字段行与列 */
    .biz-field-row {
      display: flex;
      gap: 8px;
      margin-bottom: 6px;
    }
    .biz-field-row:last-child {
      margin-bottom: 0;
    }
    .biz-field-row.single {
      flex-direction: column;
      gap: 2px;
    }
    .biz-field-col {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2px;
      min-width: 0;
    }
    .biz-label {
      font-size: 11px;
      color: #64748b;
      font-weight: 500;
      display: flex;
      align-items: center;
      justify-content: space-between;
      line-height: 1.3;
    }
    .biz-label.required::before {
      content: '*';
      color: #ff4d4f;
      margin-right: 3px;
    }
    .biz-helper {
      font-size: 10px;
      color: #94a3b8;
    }

    /* 单据核心只读条 (Readonly Ticket Strip) */
    .ticket-meta-strip {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 5px 8px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px 8px;
      margin-bottom: 6px;
    }
    .meta-item {
      display: flex;
      flex-direction: column;
    }
    .meta-label {
      font-size: 10px;
      color: #64748b;
    }
    .meta-val {
      font-size: 11px;
      font-weight: 600;
      color: #0f172a;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* 干系人矩阵列表 */
    .stakeholder-compact-list {
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .stakeholder-compact-row {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .stakeholder-role-lbl {
      width: 44px;
      font-size: 11px;
      color: #475569;
      flex-shrink: 0;
      text-align: right;
    }'''

assert old_css in text, "old_css not found"
text = text.replace(old_css, new_css)

# 2. Update HTML of left-business-panel
old_panel_html_pattern = re.compile(
    r'<div class="left-business-panel".*?<!-- 右侧费用双轨工作区',
    re.DOTALL
)

new_panel_html = '''<div class="left-business-panel" :class="{ 'is-collapsed': isLeftCollapsed }">
        <!-- 面板顶栏 (精致标题 + 保存按钮 + 折叠) -->
        <div class="panel-header-bar">
          <div class="panel-title-wrap">
            <div class="panel-title">
              <iconify-icon icon="ant-design:file-text-outlined" style="color: #1677ff; font-size: 15px;"></iconify-icon>
              <span v-if="!isLeftCollapsed">业务单据要素</span>
              <a-tag v-if="!isLeftCollapsed" color="blue" style="font-size: 10px; line-height: 18px; padding: 0 4px; margin: 0;">综合业务</a-tag>
              <span v-if="!isLeftCollapsed && dirtyStates.basic" style="color: #fa8c16; font-size: 11px; font-weight: 600;">(未存*)</span>
            </div>
          </div>
          <div class="panel-actions">
            <template v-if="!isLeftCollapsed">
              <!-- 业务信息独立保存按钮 -->
              <a-button 
                type="primary" 
                size="small" 
                :loading="isSavingBasic" 
                :disabled="ticketData.isLocked"
                style="height: 26px; padding: 0 10px; font-size: 12px; font-weight: 500;"
                @click="saveBasicInfo">
                <iconify-icon icon="ant-design:save-outlined"></iconify-icon> 保存业务
              </a-button>
              <a-tooltip title="收起左栏，最大化右侧费用表格宽度">
                <a-button type="text" size="small" style="color: #64748b;" @click="isLeftCollapsed = true">
                  <iconify-icon icon="ant-design:menu-fold-outlined"></iconify-icon>
                </a-button>
              </a-tooltip>
            </template>
            <template v-else>
              <a-tooltip title="展开左侧业务信息栏">
                <a-button type="text" size="small" @click="isLeftCollapsed = false">
                  <iconify-icon icon="ant-design:menu-unfold-outlined"></iconify-icon>
                </a-button>
              </a-tooltip>
            </template>
          </div>
        </div>

        <!-- 折叠后的极窄竖向标识条 -->
        <div v-if="isLeftCollapsed" class="panel-collapsed-strip" @click="isLeftCollapsed = false">
          <div class="collapsed-vertical-text">业务要素 · {{ ticketData.jobNo }}</div>
          <a-tooltip title="点击展开">
            <a-button type="link" size="small">
              <iconify-icon icon="ant-design:right-outlined"></iconify-icon>
            </a-button>
          </a-tooltip>
        </div>

        <!-- 展开后的完整业务字段表单 (模块化微卡，呼吸感与高密度兼备) -->
        <div v-else class="business-form-scroll">

          <!-- 卡片 1: 单据归属与账期 -->
          <div class="biz-card">
            <div class="biz-card-header">
              <div class="biz-card-title">
                <iconify-icon icon="ant-design:idcard-outlined" style="color: #1677ff;"></iconify-icon>
                <span>单据凭证与归属</span>
              </div>
              <span class="biz-card-badge">期间核算</span>
            </div>

            <!-- 提单号 (BL No.) -->
            <div class="biz-field-row single">
              <div class="biz-label">
                <span style="font-weight: 600; color: #1e293b;">提单号 (BL No.)</span>
                <span class="biz-helper">优先展示标识</span>
              </div>
              <a-input 
                v-model:value="form.blNo" 
                size="small"
                placeholder="请输入提单号 (英文自动大写)" 
                :maxlength="64"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"
                @input="e => form.blNo = e.target.value.toUpperCase()">
                <template #suffix>
                  <iconify-icon icon="ant-design:copy-outlined" style="cursor: pointer; color: #94a3b8;" title="复制提单号" @click="copyText(form.blNo)"></iconify-icon>
                </template>
              </a-input>
            </div>

            <!-- 委托编号与期间元数据条 -->
            <div class="ticket-meta-strip">
              <div class="meta-item">
                <span class="meta-label">委托编号:</span>
                <div class="meta-val">
                  <span>{{ form.jobNo }}</span>
                  <a-popconfirm 
                    title="重新生成委托编号将直接向服务器申请新号并落库，是否确认？" 
                    ok-text="确认重生成" 
                    cancel-text="取消" 
                    :disabled="ticketData.isLocked"
                    @confirm="regenerateJobNo">
                    <a-button type="link" size="small" style="padding: 0; height: auto; font-size: 10px;" :disabled="ticketData.isLocked">
                      重生成
                    </a-button>
                  </a-popconfirm>
                </div>
              </div>

              <div class="meta-item">
                <span class="meta-label">会计月份:</span>
                <div class="meta-val" style="color: #1d4ed8;">
                  {{ form.accountingPeriod }}
                  <a-tooltip title="后端决定的会计月份，只读">
                    <iconify-icon icon="ant-design:info-circle-outlined" style="color: #94a3b8; font-size: 11px;"></iconify-icon>
                  </a-tooltip>
                </div>
              </div>

              <div class="meta-item">
                <span class="meta-label">应结日期:</span>
                <div class="meta-val" style="color: #b45309;">
                  {{ form.settlementDate }}
                  <a-tooltip title="按委托单位账期与业务日期联动试算">
                    <iconify-icon icon="ant-design:clock-circle-outlined" style="color: #94a3b8; font-size: 11px;"></iconify-icon>
                  </a-tooltip>
                </div>
              </div>

              <div class="meta-item">
                <span class="meta-label">业务来源:</span>
                <div class="meta-val" style="color: #475569;">
                  自揽业务 (普通)
                </div>
              </div>
            </div>

            <!-- 所属公司 (销售直属组织) -->
            <div class="biz-field-row single">
              <div class="biz-label required">
                <span>所属公司 (销售直属组织)</span>
                <a-tooltip title="当前选择的是销售直属组织路径；切换销售将联动更新组织">
                  <iconify-icon icon="ant-design:question-circle-outlined" style="color: #94a3b8;"></iconify-icon>
                </a-tooltip>
              </div>
              <a-select 
                v-model:value="form.salesOrgId" 
                size="small"
                :options="salesOrgOptions" 
                placeholder="请选择直属销售组织"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 关联主单 -->
            <div class="biz-field-row single" style="margin-top: 4px;">
              <div class="biz-label">
                <span>关联海运/件杂货主单</span>
                <span class="biz-helper">最多 1 票</span>
              </div>
              <div v-if="form.relatedMasterOrder">
                <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 4px; padding: 4px 8px; display: flex; align-items: center; justify-content: space-between;">
                  <span style="font-size: 11px; color: #1e40af; font-weight: 500;">
                    <iconify-icon icon="ant-design:link-outlined"></iconify-icon>
                    {{ form.relatedMasterOrder.type }} · {{ form.relatedMasterOrder.no }}
                    <span style="color: #4b5563; font-weight: normal;">({{ form.relatedMasterOrder.customer }})</span>
                  </span>
                  <a-button type="text" size="small" danger style="padding: 0 4px; height: 18px;" @click="unlinkMasterOrder" title="解除关联">
                    <iconify-icon icon="ant-design:close-outlined"></iconify-icon>
                  </a-button>
                </div>
              </div>
              <div v-else>
                <a-button type="dashed" size="small" block :disabled="ticketData.isLocked" @click="openMasterOrderModal">
                  <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 关联海运主单 / 件杂货单
                </a-button>
              </div>
            </div>
          </div>

          <!-- 卡片 2: 委托单位与干系人 -->
          <div class="biz-card">
            <div class="biz-card-header">
              <div class="biz-card-title">
                <iconify-icon icon="ant-design:team-outlined" style="color: #6366f1;"></iconify-icon>
                <span>客户委托与干系人</span>
              </div>
              <span class="biz-card-badge">权责分配</span>
            </div>

            <!-- 委托单位与联系人 -->
            <div class="biz-field-row">
              <div class="biz-field-col" style="flex: 1.4;">
                <div class="biz-label required">
                  <span>委托单位</span>
                  <a-tag color="orange" style="font-size: 10px; padding: 0 4px; line-height: 16px; margin: 0;">30天账期</a-tag>
                </div>
                <a-select 
                  v-model:value="form.customerId" 
                  size="small"
                  show-search 
                  :options="customerOptions" 
                  placeholder="选择委托客户"
                  :disabled="ticketData.isLocked"
                  @change="handleCustomerChange">
                </a-select>
              </div>

              <div class="biz-field-col" style="flex: 1;">
                <div class="biz-label">
                  <span>单位联系人</span>
                </div>
                <a-select 
                  v-model:value="form.contactPerson" 
                  size="small"
                  allow-clear 
                  :options="contactOptions" 
                  placeholder="联系人"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')">
                </a-select>
              </div>
            </div>

            <!-- 干系人列表 (紧凑列表) -->
            <div style="background: #f8fafc; border: 1px solid #f1f5f9; border-radius: 4px; padding: 6px 8px; margin-top: 6px;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-size: 10px; font-weight: 600; color: #475569;">内部协作团队:</span>
                <a-button type="link" size="small" style="padding: 0; height: auto; font-size: 10px;" :disabled="ticketData.isLocked" @click="openAddStakeholderModal">
                  + 追加岗位
                </a-button>
              </div>

              <div class="stakeholder-compact-list">
                <!-- 销售 -->
                <div class="stakeholder-compact-row">
                  <span class="stakeholder-role-lbl"><strong style="color: #ff4d4f;">*</strong>销售:</span>
                  <a-select 
                    v-model:value="form.salesPerson" 
                    size="small"
                    :options="salesPersonOptions" 
                    style="flex: 1;"
                    :disabled="ticketData.isLocked"
                    @change="handleSalesChange">
                  </a-select>
                </div>

                <!-- 操作 -->
                <div class="stakeholder-compact-row">
                  <span class="stakeholder-role-lbl">操作:</span>
                  <a-select 
                    v-model:value="form.operator" 
                    size="small"
                    allow-clear 
                    :options="operatorOptions" 
                    style="flex: 1;"
                    :disabled="ticketData.isLocked"
                    @change="markDirty('basic')">
                  </a-select>
                </div>

                <!-- 动态追加岗位 -->
                <div v-for="(item, idx) in form.additionalRoles" :key="idx" class="stakeholder-compact-row">
                  <span class="stakeholder-role-lbl">{{ item.roleName }}:</span>
                  <a-select 
                    v-model:value="item.staffName" 
                    size="small"
                    :options="staffOptions" 
                    style="flex: 1;"
                    :disabled="ticketData.isLocked"
                    @change="markDirty('basic')">
                  </a-select>
                  <a-button type="text" size="small" danger style="padding: 0 4px;" :disabled="ticketData.isLocked" @click="removeRole(idx)">
                    <iconify-icon icon="ant-design:close-outlined"></iconify-icon>
                  </a-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 卡片 3: 航程与物流路径 -->
          <div class="biz-card">
            <div class="biz-card-header">
              <div class="biz-card-title">
                <iconify-icon icon="ant-design:compass-outlined" style="color: #0d9488;"></iconify-icon>
                <span>航程与运输物流</span>
              </div>
              <span class="biz-card-badge">路径履约</span>
            </div>

            <!-- 船公司 与 业务日期 -->
            <div class="biz-field-row">
              <div class="biz-field-col">
                <div class="biz-label">
                  <span>船公司 (Carrier)</span>
                </div>
                <a-select 
                  v-model:value="form.carrier" 
                  size="small"
                  allow-clear 
                  show-search 
                  :options="carrierOptions" 
                  placeholder="船司简称"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')">
                </a-select>
              </div>

              <div class="biz-field-col">
                <div class="biz-label">
                  <span>业务发生日</span>
                </div>
                <a-date-picker 
                  v-model:value="form.bizDate" 
                  size="small"
                  value-format="YYYY-MM-DD" 
                  placeholder="业务日期" 
                  style="width: 100%;"
                  :disabled="ticketData.isLocked"
                  @change="handleBizDateChange">
                </a-date-picker>
              </div>
            </div>

            <!-- 船名 / 航次 (双列整齐对齐) -->
            <div class="biz-field-row">
              <div class="biz-field-col" style="flex: 1.3;">
                <div class="biz-label">
                  <span>船名 (Vessel)</span>
                  <span class="biz-helper">限64字</span>
                </div>
                <a-input 
                  v-model:value="form.vesselName" 
                  size="small"
                  placeholder="船名 (Vessel)" 
                  :maxlength="64"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')"></a-input>
              </div>
              <div class="biz-field-col" style="flex: 1;">
                <div class="biz-label">
                  <span>航次 (Voyage)</span>
                  <span class="biz-helper">限64字</span>
                </div>
                <a-input 
                  v-model:value="form.voyage" 
                  size="small"
                  placeholder="航次 (Voyage)" 
                  :maxlength="64"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')"></a-input>
              </div>
            </div>

            <!-- 起运港 (POL) 与 目的港 (POD) -->
            <div class="biz-field-row">
              <div class="biz-field-col">
                <div class="biz-label">
                  <span>起运港 (POL)</span>
                </div>
                <a-select 
                  v-model:value="form.pol" 
                  size="small"
                  show-search 
                  :options="portOptions" 
                  placeholder="起运地"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')">
                </a-select>
              </div>

              <div class="biz-field-col">
                <div class="biz-label">
                  <span>目的港 (POD)</span>
                </div>
                <a-select 
                  v-model:value="form.pod" 
                  size="small"
                  show-search 
                  :options="portOptions" 
                  placeholder="目的地"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')">
                </a-select>
              </div>
            </div>
          </div>

          <!-- 卡片 4: 货物规格与备注 -->
          <div class="biz-card">
            <div class="biz-card-header">
              <div class="biz-card-title">
                <iconify-icon icon="ant-design:inbox-outlined" style="color: #059669;"></iconify-icon>
                <span>货物规格与备注</span>
              </div>
              <span class="biz-card-badge">物理计量</span>
            </div>

            <!-- 品名 -->
            <div class="biz-field-row single">
              <div class="biz-label">
                <span>品名 (Commodities)</span>
                <span class="biz-helper">商品档案</span>
              </div>
              <a-select 
                v-model:value="form.commodities" 
                size="small"
                mode="multiple" 
                :options="commodityOptions" 
                placeholder="选择关联商品档案"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 件数 / 包装 -->
            <div class="biz-field-row">
              <div class="biz-field-col">
                <div class="biz-label">
                  <span>件数 (Pieces)</span>
                </div>
                <a-input-number 
                  v-model:value="form.pieces" 
                  size="small"
                  :min="0" 
                  :precision="0" 
                  placeholder="件数" 
                  style="width: 100%;"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')"></a-input-number>
              </div>
              <div class="biz-field-col">
                <div class="biz-label">
                  <span>包装字典</span>
                </div>
                <a-select 
                  v-model:value="form.packageType" 
                  size="small"
                  :options="packageOptions" 
                  placeholder="包装类型" 
                  style="width: 100%;"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')"></a-select>
              </div>
            </div>

            <!-- 重量(KGS) / 尺码(CBM) -->
            <div class="biz-field-row">
              <div class="biz-field-col">
                <div class="biz-label">
                  <span>毛重 (Weight)</span>
                </div>
                <a-input-number 
                  v-model:value="form.weight" 
                  size="small"
                  :min="0" 
                  :precision="2" 
                  addon-after="KGS" 
                  placeholder="毛重" 
                  style="width: 100%;"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')"></a-input-number>
              </div>
              <div class="biz-field-col">
                <div class="biz-label">
                  <span>尺码 (CBM 体积)</span>
                  <span class="biz-helper">4位小数</span>
                </div>
                <a-input-number 
                  v-model:value="form.volume" 
                  size="small"
                  :min="0" 
                  :precision="4" 
                  addon-after="CBM" 
                  placeholder="体积" 
                  style="width: 100%;"
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')"></a-input-number>
              </div>
            </div>

            <!-- 业务备注 -->
            <div class="biz-field-row single" style="margin-top: 4px;">
              <div class="biz-label">
                <span>业务备注 (最多1024字符)</span>
              </div>
              <a-textarea 
                v-model:value="form.remark" 
                size="small"
                :rows="2" 
                :maxlength="1024" 
                placeholder="录入对外业务备注信息..." 
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-textarea>
            </div>
          </div>

        </div>
      </div>

      <!-- 右侧费用双轨工作区'''

assert old_panel_html_pattern.search(text), "old panel html pattern not matched"
text = old_panel_html_pattern.sub(new_panel_html, text)

with open('scratch/build_comprehensive_workbench.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied beautiful left panel successfully to scratch/build_comprehensive_workbench.py!")
