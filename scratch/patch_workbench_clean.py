with open('scratch/build_right_tabbed_workbench.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace biz-form-label CSS
old_css = '''    .biz-form-label {
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
    }'''

new_css = '''    .biz-form-label {
      font-size: 11px;
      color: #4b5563;
      display: flex;
      align-items: center;
      justify-content: space-between;
      line-height: 16px;
      margin-bottom: 2px;
      white-space: nowrap;
    }
    .biz-label-title {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-weight: 500;
      color: #374151;
    }
    .biz-label-title.is-required::before {
      content: '*';
      color: #ff4d4f;
      font-weight: bold;
      font-size: 12px;
      line-height: 1;
    }
    .biz-label-hint {
      font-size: 10px;
      color: #9ca3af;
      font-weight: normal;
    }
    .customer-credit-pill {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      background: #fff7ed;
      border: 1px solid #fed7aa;
      color: #c2410c;
      font-size: 10px;
      font-weight: 500;
      padding: 0 5px;
      height: 16px;
      line-height: 14px;
      border-radius: 2px;
    }'''

assert old_css in content, 'CSS biz-form-label not found'
content = content.replace(old_css, new_css)

# 2. Replace transit route card CSS
old_route_css = '''    /* 🌟 亮点 1: 航程拓扑可视化微路线图 (Transit Route Trajectory Map) */
    .transit-route-card {
      grid-column: span 2;
      background: linear-gradient(135deg, #f0fdfa 0%, #f0f9ff 100%);
      border: 1px solid #ccfbf1;
      border-radius: 4px;
      padding: 6px 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 2px;
    }
    .route-node {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
    }
    .route-node.dest {
      align-items: flex-end;
    }
    .node-code {
      font-size: 12px;
      font-weight: 700;
      color: #0f766e;
      font-family: monospace;
      letter-spacing: 0.5px;
    }
    .node-name {
      font-size: 10px;
      color: #64748b;
    }
    .route-transit-line {
      flex: 1;
      margin: 0 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
    }
    .transit-carrier-tag {
      font-size: 10px;
      color: #0369a1;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.85);
      border: 1px solid #bae6fd;
      padding: 1px 6px;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      white-space: nowrap;
    }
    .transit-arrow-track {
      width: 100%;
      height: 2px;
      background: #cbd5e1;
      position: relative;
    }
    .transit-arrow-track::after {
      content: '';
      position: absolute;
      right: 0;
      top: -3px;
      width: 0;
      height: 0;
      border-top: 4px solid transparent;
      border-bottom: 4px solid transparent;
      border-left: 6px solid #0d9488;
    }'''

new_route_css = '''    /* 🌟 亮点 1: 航程拓扑可视化微路线图 (Transit Route Trajectory Map) */
    .transit-route-card {
      grid-column: span 2;
      background: linear-gradient(135deg, #f0fdfa 0%, #f0f9ff 100%);
      border: 1px solid #ccfbf1;
      border-radius: 4px;
      padding: 6px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 2px;
    }
    .route-node {
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }
    .route-node.origin {
      align-items: flex-start;
    }
    .route-node.dest {
      align-items: flex-end;
    }
    .node-code {
      font-size: 12px;
      font-weight: 700;
      color: #0f766e;
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", monospace;
      letter-spacing: 0.5px;
      line-height: 1.2;
    }
    .node-name {
      font-size: 10px;
      color: #64748b;
      margin-top: 1px;
    }
    .route-transit-line {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-width: 0;
      padding: 0 4px;
    }
    .transit-track-wrap {
      width: 100%;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 20px;
    }
    .transit-arrow-track {
      position: absolute;
      left: 0;
      right: 0;
      top: 50%;
      height: 1.5px;
      background: #99f6e4;
      transform: translateY(-50%);
    }
    .transit-arrow-track::after {
      content: '';
      position: absolute;
      right: 0;
      top: -3px;
      width: 0;
      height: 0;
      border-top: 3.5px solid transparent;
      border-bottom: 3.5px solid transparent;
      border-left: 6px solid #0d9488;
    }
    .transit-carrier-tag {
      position: relative;
      z-index: 2;
      font-size: 10px;
      color: #0369a1;
      font-weight: 600;
      background: #ffffff;
      border: 1px solid #7dd3fc;
      padding: 1px 8px;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      white-space: nowrap;
      box-shadow: 0 1px 2px rgba(15, 118, 110, 0.08);
    }
    .transit-sub-hint {
      font-size: 9px;
      color: #0f766e;
      margin-top: 1px;
      letter-spacing: 0.2px;
    }'''

assert old_route_css in content, 'CSS transit-route-card not found'
content = content.replace(old_route_css, new_route_css)

# 3. Section 1 label updates
content = content.replace('<span>提单号 (BL No.)</span>', '<span class="biz-label-title">提单号 (BL No.)</span>')
content = content.replace('<span>委托编号</span>', '<span class="biz-label-title">委托编号</span>')
content = content.replace('<span>会计月份</span>', '<span class="biz-label-title">会计月份</span>')

old_sales_org = '''          <!-- 所属公司 (销售直属组织) - 全宽 -->
          <div class="biz-form-item grid-col-2">
            <div class="biz-form-label required">
              <span>所属公司 (销售直属组织)</span>'''

new_sales_org = '''          <!-- 所属公司 (销售直属组织) - 全宽 -->
          <div class="biz-form-item grid-col-2">
            <div class="biz-form-label">
              <span class="biz-label-title is-required">所属公司 (销售直属组织)</span>'''

assert old_sales_org in content, 'old_sales_org not found'
content = content.replace(old_sales_org, new_sales_org)

content = content.replace('<span>关联主单 (海出/海进/件杂货)</span>', '<span class="biz-label-title">关联主单 (海出/海进/件杂货)</span>')

# 4. Section 2: 往来单位与干系人 (Re-architect to 50/50 grid, remove gray box, clean labels)
old_section2 = '''        <!-- 模块 2: 往来单位与干系人 (Customer & Stakeholders) -->
        <div class="form-section-divider">
          <div class="form-section-title">客户委托与干系人</div>
          <span class="form-section-sub">往来信用与权责分配</span>
        </div>

        <div class="biz-form-grid">
          <!-- 委托单位 - 全宽 (保证长客户名绝不截断) -->
          <div class="biz-form-item grid-col-2">
            <div class="biz-form-label required">
              <span>委托单位 (客户)</span>
              <a-tag color="orange" :bordered="false" style="font-size: 10px; padding: 0 4px; line-height: 16px; margin: 0;">
                <iconify-icon icon="ant-design:safety-certificate-outlined"></iconify-icon> 账期: 30天 · 信用正常
              </a-tag>
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
        </div>'''

new_section2 = '''        <!-- 模块 2: 往来单位与干系人 (Customer & Stakeholders) -->
        <div class="form-section-divider">
          <div class="form-section-title">客户委托与干系人</div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span class="form-section-sub">往来信用与权责分配</span>
            <a-button 
              type="link" 
              size="small" 
              style="padding: 0; height: auto; font-size: 11px; font-weight: 500;" 
              :disabled="ticketData.isLocked" 
              @click="openAddStakeholderModal">
              + 追加岗位
            </a-button>
          </div>
        </div>

        <div class="biz-form-grid">
          <!-- 委托单位 - 全宽 (保证长客户名绝不截断) -->
          <div class="biz-form-item grid-col-2">
            <div class="biz-form-label">
              <span class="biz-label-title is-required">委托单位 (客户)</span>
              <span class="customer-credit-pill">
                <iconify-icon icon="ant-design:safety-certificate-outlined"></iconify-icon>
                账期: 30天 · 信用正常
              </span>
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
              <span class="biz-label-title">单位联系人</span>
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
              <span class="biz-label-title">应结日期</span>
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
            <div class="biz-form-label">
              <span class="biz-label-title is-required">销售负责人</span>
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
              <span class="biz-label-title">操作人员</span>
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

          <!-- 动态追加岗位 - 完全融入 50/50 网格！每个岗位占 1 列 (半宽) -->
          <div v-for="(item, idx) in form.additionalRoles" :key="idx" class="biz-form-item grid-col-1">
            <div class="biz-form-label">
              <span class="biz-label-title">
                <iconify-icon icon="ant-design:usergroup-add-outlined" style="color: #64748b; font-size: 11px;"></iconify-icon>
                {{ item.roleName }}
              </span>
              <a-button 
                type="link" 
                size="small" 
                danger 
                style="padding: 0; height: 16px; font-size: 10px; line-height: 16px;" 
                :disabled="ticketData.isLocked" 
                @click="removeRole(idx)"
                title="移除此岗位干系人">
                <iconify-icon icon="ant-design:close-outlined"></iconify-icon> 移除
              </a-button>
            </div>
            <a-select 
              v-model:value="item.staffName" 
              size="small"
              :options="staffOptions" 
              :disabled="ticketData.isLocked"
              @change="markDirty('basic')">
            </a-select>
          </div>
        </div>'''

assert old_section2 in content, 'old_section2 not found'
content = content.replace(old_section2, new_section2)

# 5. Section 3: Transit Route Card and voyage fields
old_route_card = '''          <!-- 🌟 亮点 1: 航程拓扑可视化微路线图 (Transit Route Trajectory Map) -->
          <div class="transit-route-card">
            <div class="route-node origin">
              <span class="node-code">{{ form.pol }}</span>
              <span class="node-name">青岛港 (POL)</span>
            </div>
            <div class="route-transit-line">
              <div class="transit-carrier-tag">
                <iconify-icon icon="ant-design:send-outlined" style="transform: rotate(45deg);"></iconify-icon>
                <span>{{ form.carrier }} · {{ form.vesselName }} / {{ form.voyage }}</span>
              </div>
              <div class="transit-arrow-track"></div>
            </div>
            <div class="route-node dest">
              <span class="node-code">{{ form.pod }}</span>
              <span class="node-name">洛杉矶港 (POD)</span>
            </div>
          </div>'''

new_route_card = '''          <!-- 🌟 亮点 1: 航程拓扑可视化微路线图 (Transit Route Trajectory Map) -->
          <div class="transit-route-card">
            <div class="route-node origin">
              <span class="node-code">{{ form.pol }}</span>
              <span class="node-name">青岛港 (POL)</span>
            </div>
            <div class="route-transit-line">
              <div class="transit-track-wrap">
                <div class="transit-arrow-track"></div>
                <div class="transit-carrier-tag">
                  <iconify-icon icon="ant-design:compass-outlined" style="color: #0284c7; font-size: 12px;"></iconify-icon>
                  <span>{{ form.carrier }} · {{ form.vesselName }} / {{ form.voyage }}</span>
                </div>
              </div>
              <div class="transit-sub-hint">
                <span>海运干线 · 直达快船</span>
              </div>
            </div>
            <div class="route-node dest">
              <span class="node-code">{{ form.pod }}</span>
              <span class="node-name">洛杉矶港 (POD)</span>
            </div>
          </div>'''

assert old_route_card in content, 'old_route_card not found'
content = content.replace(old_route_card, new_route_card)

# Section 3 & 4 labels
content = content.replace('<span>船公司 (Carrier)</span>', '<span class="biz-label-title">船公司 (Carrier)</span>')
content = content.replace('<span>业务日期</span>', '<span class="biz-label-title">业务日期</span>')
content = content.replace('<span>船名 (Vessel)</span>', '<span class="biz-label-title">船名 (Vessel)</span>')
content = content.replace('<span>航次 (Voyage)</span>', '<span class="biz-label-title">航次 (Voyage)</span>')
content = content.replace('<span>起运港 (POL)</span>', '<span class="biz-label-title">起运港 (POL)</span>')
content = content.replace('<span>目的港 (POD)</span>', '<span class="biz-label-title">目的港 (POD)</span>')
content = content.replace('<span>品名 (Commodities)</span>', '<span class="biz-label-title">品名 (Commodities)</span>')
content = content.replace('<span>件数 (Pieces)</span>', '<span class="biz-label-title">件数 (Pieces)</span>')
content = content.replace('<span>包装 (Package)</span>', '<span class="biz-label-title">包装 (Package)</span>')
content = content.replace('<span>毛重 (Weight)</span>', '<span class="biz-label-title">毛重 (Weight)</span>')
content = content.replace('<span>尺码 (Volume 体积)</span>', '<span class="biz-label-title">尺码 (Volume 体积)</span>')
content = content.replace('<span>业务备注 (最多1024字符)</span>', '<span class="biz-label-title">业务备注 (最多1024字符)</span>')

with open('scratch/build_right_tabbed_workbench.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated scratch/build_right_tabbed_workbench.py cleanly!')
