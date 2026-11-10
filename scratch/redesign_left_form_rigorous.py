import re

with open('scratch/build_comprehensive_workbench.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. New CSS for Left Panel: Clean, Unified, Strict Grid, No Card Inception
left_panel_css = '''    /* ==========================================================================
       左侧业务信息面板 (410px 严格对齐网格、单画布无框套框、高清晰层级)
       ========================================================================== */
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
      background: #fafafa;
    }
    .panel-header-bar {
      height: 38px;
      padding: 0 12px;
      background: #fafafa;
      border-bottom: 1px solid #e8e8e8;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .panel-title-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .panel-title {
      font-size: 13px;
      font-weight: 700;
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
      padding: 14px 0;
      background: #fafafa;
    }
    .collapsed-vertical-text {
      writing-mode: vertical-lr;
      letter-spacing: 4px;
      font-weight: 600;
      color: #374151;
      font-size: 13px;
    }

    /* 左侧表单滚动体：纯净单画布，去除嵌套卡片与杂乱边框 */
    .business-form-scroll {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 10px 14px 16px 14px;
    }
    .business-form-scroll::-webkit-scrollbar {
      width: 4px;
    }
    .business-form-scroll::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 2px;
    }

    /* 区段分割标题 (Section Divider) */
    .form-section-divider {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin: 14px 0 8px 0;
      padding-bottom: 4px;
      border-bottom: 1px solid #f0f0f0;
    }
    .form-section-divider:first-child {
      margin-top: 0;
    }
    .form-section-title {
      font-size: 12px;
      font-weight: 700;
      color: #1f2937;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .form-section-title::before {
      content: '';
      display: inline-block;
      width: 3px;
      height: 12px;
      background: #1677ff;
      border-radius: 1.5px;
    }
    .form-section-sub {
      font-size: 11px;
      color: #9ca3af;
      font-weight: normal;
    }

    /* 严谨 2 列表单网格 (Strict 2-Column Grid) */
    .biz-form-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 7px 10px;
    }
    .grid-col-1 {
      grid-column: span 1;
    }
    .grid-col-2 {
      grid-column: span 2;
    }

    /* 表单项单元 (Form Item) */
    .biz-form-item {
      display: flex;
      flex-direction: column;
      gap: 3px;
      min-width: 0;
    }
    .biz-form-label {
      font-size: 11px;
      font-weight: 500;
      color: #4b5563;
      display: flex;
      align-items: center;
      justify-content: space-between;
      line-height: 1.3;
      white-space: nowrap;
    }
    .biz-form-label.required::before {
      content: '*';
      color: #ff4d4f;
      margin-right: 3px;
      font-weight: bold;
    }
    .biz-label-hint {
      font-size: 10px;
      color: #9ca3af;
      font-weight: normal;
    }

    /* 等宽等高只读展示框 */
    .readonly-box {
      height: 24px;
      line-height: 22px;
      padding: 0 7px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 2px;
      font-size: 11px;
      color: #1e293b;
      font-family: -apple-system, BlinkMacSystemFont, monospace;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: space-between;
      overflow: hidden;
      white-space: nowrap;
    }

    /* 主单关联紧凑卡片 */
    .linked-master-box {
      background: #f0f7ff;
      border: 1px solid #bae0ff;
      border-radius: 3px;
      padding: 4px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
    }

    /* 追加干系人岗位紧凑表格 */
    .stakeholder-grid-row {
      display: grid;
      grid-template-columns: 50px 1fr 24px;
      gap: 6px;
      align-items: center;
      margin-top: 5px;
    }
    .stakeholder-tag-lbl {
      font-size: 11px;
      color: #4b5563;
      text-align: right;
      font-weight: 500;
    }'''

# Replace old left panel CSS
css_pattern = re.compile(
    r'/\* ==========================================================================\s+左侧业务信息卡片.*?\/\* ==========================================================================\s+右侧费用工作区',
    re.DOTALL
)
assert css_pattern.search(text), "CSS pattern not found"
text = css_pattern.sub(left_panel_css + '\n\n    /* ==========================================================================\n       右侧费用工作区', text)

# 2. New HTML for Left Business Panel
left_panel_html = '''<div class="left-business-panel" :class="{ 'is-collapsed': isLeftCollapsed }">
        <!-- 面板顶栏 (清晰标题 + 独立保存 + 折叠) -->
        <div class="panel-header-bar">
          <div class="panel-title-wrap">
            <div class="panel-title">
              <iconify-icon icon="ant-design:form-outlined" style="color: #1677ff; font-size: 14px;"></iconify-icon>
              <span v-if="!isLeftCollapsed">业务基础信息</span>
              <a-tag v-if="!isLeftCollapsed" color="blue" :bordered="false" style="font-size: 10px; line-height: 18px; padding: 0 4px; margin: 0;">综合业务</a-tag>
              <span v-if="!isLeftCollapsed && dirtyStates.basic" style="color: #fa8c16; font-size: 11px; font-weight: 600;">(未存*)</span>
            </div>
          </div>
          <div class="panel-actions">
            <template v-if="!isLeftCollapsed">
              <!-- 业务信息独立保存按钮 (明确只存业务) -->
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
                <a-button type="text" size="small" style="color: #64748b; padding: 0 4px;" @click="isLeftCollapsed = true">
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
          <div class="collapsed-vertical-text">业务信息 · {{ ticketData.jobNo }}</div>
          <a-tooltip title="点击展开">
            <a-button type="link" size="small">
              <iconify-icon icon="ant-design:right-outlined"></iconify-icon>
            </a-button>
          </a-tooltip>
        </div>

        <!-- 展开后的完整业务字段表单 (纯净单画布，严谨网格对齐，清晰层次) -->
        <div v-else class="business-form-scroll">

          <!-- 模块 1: 单据归属与期间 (Identification & Accounting) -->
          <div class="form-section-divider">
            <div class="form-section-title">单据归属与期间</div>
            <span class="form-section-sub">核对识别与组织隔离</span>
          </div>

          <div class="biz-form-grid">
            <!-- 提单号 (BL No.) - 全宽 -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label">
                <span>提单号 (BL No.)</span>
                <span class="biz-label-hint">外部运输号 · 优先展示</span>
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
                  <iconify-icon icon="ant-design:copy-outlined" style="cursor: pointer; color: #9ca3af;" title="复制提单号" @click="copyText(form.blNo)"></iconify-icon>
                </template>
              </a-input>
            </div>

            <!-- 委托编号 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>委托编号</span>
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
              <div class="readonly-box">
                <span>{{ form.jobNo }}</span>
                <iconify-icon icon="ant-design:lock-outlined" style="color: #94a3b8; font-size: 12px;"></iconify-icon>
              </div>
            </div>

            <!-- 会计月份 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>会计月份</span>
                <a-tooltip title="后端决定的会计月份，只读">
                  <iconify-icon icon="ant-design:question-circle-outlined" style="color: #94a3b8; font-size: 11px;"></iconify-icon>
                </a-tooltip>
              </div>
              <div class="readonly-box" style="color: #1d4ed8;">
                <span>{{ form.accountingPeriod }}</span>
                <iconify-icon icon="ant-design:calendar-outlined" style="color: #94a3b8; font-size: 12px;"></iconify-icon>
              </div>
            </div>

            <!-- 所属公司 (销售直属组织) - 全宽 -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label required">
                <span>所属公司 (销售直属组织)</span>
                <a-tooltip title="当前选择的是销售直属组织路径；切换销售将联动更新组织">
                  <iconify-icon icon="ant-design:info-circle-outlined" style="color: #1677ff; font-size: 11px;"></iconify-icon>
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

            <!-- 关联主单 - 全宽 -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label">
                <span>关联主单 (海出/海进/件杂货)</span>
                <span class="biz-label-hint">同公司校验 · 最多1票</span>
              </div>
              <div v-if="form.relatedMasterOrder" class="linked-master-box">
                <span style="color: #1e40af; font-weight: 500;">
                  <iconify-icon icon="ant-design:link-outlined"></iconify-icon>
                  {{ form.relatedMasterOrder.type }} · {{ form.relatedMasterOrder.no }}
                  <span style="color: #4b5563; font-weight: normal; margin-left: 4px;">({{ form.relatedMasterOrder.customer }})</span>
                </span>
                <a-button type="text" size="small" danger style="padding: 0 4px; height: 18px;" @click="unlinkMasterOrder" title="解除关联">
                  <iconify-icon icon="ant-design:close-outlined"></iconify-icon>
                </a-button>
              </div>
              <div v-else>
                <a-button type="dashed" size="small" block :disabled="ticketData.isLocked" @click="openMasterOrderModal">
                  <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 关联海运主单 / 件杂货单
                </a-button>
              </div>
            </div>
          </div>

          <!-- 模块 2: 往来单位与干系人 (Customer & Stakeholders) -->
          <div class="form-section-divider">
            <div class="form-section-title">客户委托与干系人</div>
            <span class="form-section-sub">往来信用与权责分配</span>
          </div>

          <div class="biz-form-grid">
            <!-- 委托单位 - 全宽 (保证长客户名绝不截断) -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label required">
                <span>委托单位 (客户)</span>
                <a-tag color="orange" :bordered="false" style="font-size: 10px; padding: 0 4px; line-height: 16px; margin: 0;">账期: 30天</a-tag>
              </div>
              <a-select 
                v-model:value="form.customerId" 
                size="small"
                show-search 
                :options="customerOptions" 
                placeholder="请选择委托客户"
                :disabled="ticketData.isLocked"
                @change="handleCustomerChange">
              </a-select>
            </div>

            <!-- 联系人 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>单位联系人</span>
              </div>
              <a-select 
                v-model:value="form.contactPerson" 
                size="small"
                allow-clear 
                :options="contactOptions" 
                placeholder="选择联系人"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 应结日期 - 半宽 (1列，与联系人严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>应结日期</span>
                <a-tooltip title="按委托单位账期与业务日期联动试算">
                  <iconify-icon icon="ant-design:clock-circle-outlined" style="color: #9ca3af; font-size: 11px;"></iconify-icon>
                </a-tooltip>
              </div>
              <div class="readonly-box" style="color: #b45309;">
                <span>{{ form.settlementDate }}</span>
                <iconify-icon icon="ant-design:schedule-outlined" style="color: #94a3b8; font-size: 12px;"></iconify-icon>
              </div>
            </div>

            <!-- 销售负责人 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label required">
                <span>销售负责人</span>
              </div>
              <a-select 
                v-model:value="form.salesPerson" 
                size="small"
                :options="salesPersonOptions" 
                :disabled="ticketData.isLocked"
                @change="handleSalesChange">
              </a-select>
            </div>

            <!-- 操作人员 - 半宽 (1列，与销售负责人严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>操作人员</span>
              </div>
              <a-select 
                v-model:value="form.operator" 
                size="small"
                allow-clear 
                :options="operatorOptions" 
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 动态追加岗位 - 全宽容器 -->
            <div v-if="form.additionalRoles.length > 0 || !ticketData.isLocked" class="biz-form-item grid-col-2" style="background: #f9fafb; border: 1px solid #f3f4f6; border-radius: 4px; padding: 6px 8px; margin-top: 2px;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 2px;">
                <span style="font-size: 10px; font-weight: 600; color: #475569;">其他协作干系人:</span>
                <a-button type="link" size="small" style="padding: 0; height: auto; font-size: 10px;" :disabled="ticketData.isLocked" @click="openAddStakeholderModal">
                  + 追加岗位
                </a-button>
              </div>

              <div v-for="(item, idx) in form.additionalRoles" :key="idx" class="stakeholder-grid-row">
                <span class="stakeholder-tag-lbl">{{ item.roleName }}:</span>
                <a-select 
                  v-model:value="item.staffName" 
                  size="small"
                  :options="staffOptions" 
                  :disabled="ticketData.isLocked"
                  @change="markDirty('basic')">
                </a-select>
                <a-button type="text" size="small" danger style="padding: 0 4px;" :disabled="ticketData.isLocked" @click="removeRole(idx)">
                  <iconify-icon icon="ant-design:close-outlined"></iconify-icon>
                </a-button>
              </div>
            </div>
          </div>

          <!-- 模块 3: 航程与物流路径 (Voyage & Routing) -->
          <div class="form-section-divider">
            <div class="form-section-title">航程与物流路径</div>
            <span class="form-section-sub">船期港口与节点</span>
          </div>

          <div class="biz-form-grid">
            <!-- 船公司 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>船公司 (Carrier)</span>
              </div>
              <a-select 
                v-model:value="form.carrier" 
                size="small"
                allow-clear 
                show-search 
                :options="carrierOptions" 
                placeholder="船公司代码/简称"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 业务发生日 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>业务日期</span>
              </div>
              <a-date-picker 
                v-model:value="form.bizDate" 
                size="small"
                value-format="YYYY-MM-DD" 
                placeholder="业务发生日" 
                style="width: 100%;"
                :disabled="ticketData.isLocked"
                @change="handleBizDateChange">
              </a-date-picker>
            </div>

            <!-- 船名 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>船名 (Vessel)</span>
                <span class="biz-label-hint">限64字</span>
              </div>
              <a-input 
                v-model:value="form.vesselName" 
                size="small"
                placeholder="船名 (Vessel)" 
                :maxlength="64"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-input>
            </div>

            <!-- 航次 - 半宽 (1列，与船名严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>航次 (Voyage)</span>
                <span class="biz-label-hint">限64字</span>
              </div>
              <a-input 
                v-model:value="form.voyage" 
                size="small"
                placeholder="航次 (Voyage)" 
                :maxlength="64"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-input>
            </div>

            <!-- 起运港 (POL) - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>起运港 (POL)</span>
              </div>
              <a-select 
                v-model:value="form.pol" 
                size="small"
                show-search 
                :options="portOptions" 
                placeholder="起运港代码/港口"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>

            <!-- 目的港 (POD) - 半宽 (1列，与起运港严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>目的港 (POD)</span>
              </div>
              <a-select 
                v-model:value="form.pod" 
                size="small"
                show-search 
                :options="portOptions" 
                placeholder="目的港代码/港口"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>
          </div>

          <!-- 模块 4: 货物规格与包装 (Cargo & Packaging) -->
          <div class="form-section-divider">
            <div class="form-section-title">货物规格与包装</div>
            <span class="form-section-sub">品名件毛体计量</span>
          </div>

          <div class="biz-form-grid">
            <!-- 品名 - 全宽 (商品档案多选) -->
            <div class="biz-form-item grid-col-2">
              <div class="biz-form-label">
                <span>品名 (Commodities)</span>
                <span class="biz-label-hint">商品档案多选</span>
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

            <!-- 件数 - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>件数 (Pieces)</span>
              </div>
              <a-input-number 
                v-model:value="form.pieces" 
                size="small"
                :min="0" 
                :precision="0" 
                placeholder="数量" 
                style="width: 100%;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-input-number>
            </div>

            <!-- 包装字典 - 半宽 (1列，与件数严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>包装 (Package)</span>
              </div>
              <a-select 
                v-model:value="form.packageType" 
                size="small"
                :options="packageOptions" 
                placeholder="包装字典" 
                style="width: 100%;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-select>
            </div>

            <!-- 毛重(KGS) - 半宽 (1列) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
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

            <!-- 尺码(CBM 体积) - 半宽 (1列，与毛重严格水平对齐) -->
            <div class="biz-form-item grid-col-1">
              <div class="biz-form-label">
                <span>尺码 (Volume 体积)</span>
                <span class="biz-label-hint">最多4位</span>
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

            <!-- 业务备注 - 全宽 -->
            <div class="biz-form-item grid-col-2" style="margin-top: 2px;">
              <div class="biz-form-label">
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

panel_pattern = re.compile(
    r'<div class="left-business-panel".*?<!-- 右侧费用双轨工作区',
    re.DOTALL
)
assert panel_pattern.search(text), "Panel pattern not found"
text = panel_pattern.sub(left_panel_html, text)

with open('scratch/build_comprehensive_workbench.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied rigorous left form successfully to scratch/build_comprehensive_workbench.py!")
