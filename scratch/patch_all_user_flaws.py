with open('scratch/build_right_tabbed_workbench.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add CSS for master-unlink-icon, role-remove-icon, order-pager-wrap, order-pager-num
old_css_anchor = '''    /* 主单关联紧凑卡片 */
    .linked-master-box {
      background: #f0f7ff;
      border: 1px solid #bae0ff;
      border-radius: 3px;
      padding: 4px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
    }'''

new_css_anchor = '''    /* 主单关联紧凑卡片 */
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
    .master-unlink-icon {
      color: #94a3b8;
      cursor: pointer;
      font-size: 12px;
      padding: 2px 4px;
      border-radius: 2px;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
    }
    .master-unlink-icon:hover {
      color: #ef4444;
      background: rgba(239, 68, 68, 0.08);
    }
    .role-remove-icon {
      color: #94a3b8;
      cursor: pointer;
      font-size: 11px;
      padding: 0 2px;
      line-height: 1;
      display: inline-flex;
      align-items: center;
      transition: color 0.2s;
    }
    .role-remove-icon:hover {
      color: #ef4444;
    }
    .order-pager-wrap {
      display: inline-flex;
      align-items: center;
      gap: 2px;
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      border-radius: 3px;
      padding: 1px 3px;
    }
    .order-pager-num {
      font-size: 11px;
      font-weight: 600;
      color: #475569;
      padding: 0 6px;
      font-family: monospace;
    }'''

assert old_css_anchor in text, 'old_css_anchor not found'
text = text.replace(old_css_anchor, new_css_anchor)

# 2. Update wb-header-right: remove duplicate 更多, add pager indicator, direct 复制业务 button
old_wb_header_right = '''    <div class="wb-header-right">
      <a-button-group size="small">
        <a-button :disabled="orderIndex <= 0" @click="handlePrevOrder">
          <iconify-icon icon="ant-design:left-outlined"></iconify-icon> 上一票
        </a-button>
        <a-button :disabled="orderIndex >= totalOrders - 1" @click="handleNextOrder">
          下一票 <iconify-icon icon="ant-design:right-outlined"></iconify-icon>
        </a-button>
      </a-button-group>

      <a-dropdown size="small">
        <template #overlay>
          <a-menu>
            <a-menu-item key="copy" @click="openCopyModal">
              <iconify-icon icon="ant-design:copy-outlined"></iconify-icon> 复制本票业务 (带费用选择)
            </a-menu-item>
            <a-menu-item key="refresh" @click="reloadTicket">
              <iconify-icon icon="ant-design:reload-outlined"></iconify-icon> 重新读取本票数据
            </a-menu-item>
          </a-menu>
        </template>
        <a-button size="small">
          更多 <iconify-icon icon="ant-design:down-outlined"></iconify-icon>
        </a-button>
      </a-dropdown>
    </div>'''

new_wb_header_right = '''    <div class="wb-header-right">
      <!-- 翻票控制器 (带当前序号指示，杜绝歧义) -->
      <div class="order-pager-wrap">
        <a-button size="small" :disabled="orderIndex <= 0" @click="handlePrevOrder" title="上一票">
          <iconify-icon icon="ant-design:left-outlined"></iconify-icon> 上一票
        </a-button>
        <span class="order-pager-num">{{ orderIndex + 1 }} / {{ totalOrders }}</span>
        <a-button size="small" :disabled="orderIndex >= totalOrders - 1" @click="handleNextOrder" title="下一票">
          下一票 <iconify-icon icon="ant-design:right-outlined"></iconify-icon>
        </a-button>
      </div>

      <!-- 独立业务动作：消除与下方重复的“更多”按钮，明确功能语义 -->
      <a-button size="small" @click="openCopyModal" title="复制本票业务与费用">
        <iconify-icon icon="ant-design:copy-outlined"></iconify-icon> 复制业务
      </a-button>
      <a-tooltip title="重新读取本票最新数据">
        <a-button size="small" @click="reloadTicket">
          <iconify-icon icon="ant-design:reload-outlined"></iconify-icon>
        </a-button>
      </a-tooltip>
    </div>'''

assert old_wb_header_right in text, 'old_wb_header_right not found'
text = text.replace(old_wb_header_right, new_wb_header_right)

# 3. In left-business-panel: Remove is-collapsed, remove collapse button, remove collapsed strip completely
old_left_panel_header = '''    <div class="left-business-panel" :class="{ 'is-collapsed': isLeftCollapsed }">
      <!-- 面板顶栏 (清晰标题 + 独立保存 + 折叠) -->
      <div class="panel-header-bar">
        <div class="panel-title-wrap">
          <div class="panel-title">
            <iconify-icon icon="ant-design:profile-outlined" style="color: #1677ff; font-size: 15px;"></iconify-icon>
            <span v-if="!isLeftCollapsed">业务基础档案</span>
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
            <a-tooltip title="收起左栏，最大化右侧工作台宽度">
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
      <div v-else class="business-form-scroll">'''

new_left_panel_header = '''    <div class="left-business-panel">
      <!-- 面板顶栏 (清晰标题 + 独立保存；左侧业务底单永久常驻！) -->
      <div class="panel-header-bar">
        <div class="panel-title-wrap">
          <div class="panel-title">
            <iconify-icon icon="ant-design:profile-outlined" style="color: #1677ff; font-size: 15px;"></iconify-icon>
            <span>业务基础档案</span>
            <a-tag color="blue" :bordered="false" style="font-size: 10px; line-height: 18px; padding: 0 4px; margin: 0;">综合业务</a-tag>
            <span v-if="dirtyStates.basic" style="color: #fa8c16; font-size: 11px; font-weight: 600;">(未存*)</span>
          </div>
        </div>
        <div class="panel-actions">
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
        </div>
      </div>

      <!-- 永久常驻的完整业务字段表单 (纯净单画布，严谨网格对齐，清晰层次) -->
      <div class="business-form-scroll">'''

assert old_left_panel_header in text, 'old_left_panel_header not found'
text = text.replace(old_left_panel_header, new_left_panel_header)

# 4. In linked-master-box: replace harsh red button with elegant master-unlink-icon
old_unlink = '''            <div v-if="form.relatedMasterOrder" class="linked-master-box">
              <span style="color: #1e40af; font-weight: 500;">
                <iconify-icon icon="ant-design:link-outlined"></iconify-icon>
                {{ form.relatedMasterOrder.type }} · {{ form.relatedMasterOrder.no }}
                <span style="color: #4b5563; font-weight: normal; margin-left: 4px;">({{ form.relatedMasterOrder.customer }})</span>
              </span>
              <a-button type="text" size="small" danger style="padding: 0 4px; height: 18px;" @click="unlinkMasterOrder" title="解除关联">
                <iconify-icon icon="ant-design:close-outlined"></iconify-icon>
              </a-button>
            </div>'''

new_unlink = '''            <div v-if="form.relatedMasterOrder" class="linked-master-box">
              <span style="color: #1e40af; font-weight: 500;">
                <iconify-icon icon="ant-design:link-outlined"></iconify-icon>
                {{ form.relatedMasterOrder.type }} · {{ form.relatedMasterOrder.no }}
                <span style="color: #4b5563; font-weight: normal; margin-left: 4px;">({{ form.relatedMasterOrder.customer }})</span>
              </span>
              <span class="master-unlink-icon" @click="unlinkMasterOrder" title="解除关联主单">
                <iconify-icon icon="ant-design:close-outlined"></iconify-icon>
              </span>
            </div>'''

assert old_unlink in text, 'old_unlink not found'
text = text.replace(old_unlink, new_unlink)

# 5. In additionalRoles: replace harsh ✕ 移除 with subtle role-remove-icon, AND add dashed placeholder for odd items
old_roles = '''          <!-- 动态追加岗位 - 完全融入 50/50 网格！每个岗位占 1 列 (半宽) -->
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
          </div>'''

new_roles = '''          <!-- 动态追加岗位 - 完全融入 50/50 网格！每个岗位占 1 列 (半宽) -->
          <div v-for="(item, idx) in form.additionalRoles" :key="idx" class="biz-form-item grid-col-1">
            <div class="biz-form-label">
              <span class="biz-label-title">
                <iconify-icon icon="ant-design:usergroup-add-outlined" style="color: #64748b; font-size: 11px;"></iconify-icon>
                {{ item.roleName }}
              </span>
              <span class="role-remove-icon" @click="removeRole(idx)" title="移除此岗位干系人">
                <iconify-icon icon="ant-design:close-outlined"></iconify-icon>
              </span>
            </div>
            <a-select 
              v-model:value="item.staffName" 
              size="small"
              :options="staffOptions" 
              :disabled="ticketData.isLocked"
              @change="markDirty('basic')">
            </a-select>
          </div>

          <!-- 当追加岗位为奇数时，用占位追加卡填补右侧，杜绝右侧留白空洞！ -->
          <div v-if="form.additionalRoles.length % 2 !== 0 && !ticketData.isLocked" class="biz-form-item grid-col-1" style="justify-content: flex-end;">
            <a-button 
              type="dashed" 
              size="small" 
              style="height: 24px; font-size: 11px; color: #64748b; margin-top: 19px;" 
              block 
              @click="openAddStakeholderModal">
              <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 追加其他协作岗位
            </a-button>
          </div>'''

assert old_roles in text, 'old_roles not found'
text = text.replace(old_roles, new_roles)

with open('scratch/build_right_tabbed_workbench.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('All flaws patched successfully!')
