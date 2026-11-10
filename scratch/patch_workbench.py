import re

with open('scratch/build_comprehensive_workbench.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace self-closing custom elements with explicit closing tags

# 1. accountingPeriod and settlementDate
text = text.replace(
    '<a-input :value="form.accountingPeriod" size="small" disabled />',
    '<a-input :value="form.accountingPeriod" size="small" disabled></a-input>'
)
text = text.replace(
    '<a-input :value="form.settlementDate" size="small" disabled />',
    '<a-input :value="form.settlementDate" size="small" disabled></a-input>'
)

# 2. 船名 / 航次
old_vessel_voyage = '''          <!-- 船名 / 航次 (同一组合控件，拆分存储) -->
          <div class="biz-field-row single">
            <div class="biz-label">
              <span>船名 / 航次 (Vessel / Voyage)</span>
              <span class="biz-helper">分别限64字符</span>
            </div>
            <div class="compound-input-group">
              <a-input 
                v-model:value="form.vesselName" 
                size="small"
                placeholder="船名 (Vessel)" 
                :maxlength="64"
                style="flex: 1.4;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')" />
              <span style="color: #9ca3af;">/</span>
              <a-input 
                v-model:value="form.voyage" 
                size="small"
                placeholder="航次 (Voyage)" 
                :maxlength="64"
                style="flex: 1;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')" />
            </div>
          </div>'''

new_vessel_voyage = '''          <!-- 船名 / 航次 (同一组合控件，双列整齐对齐，拆分存储) -->
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
          </div>'''

assert old_vessel_voyage in text, "old_vessel_voyage not found"
text = text.replace(old_vessel_voyage, new_vessel_voyage)

# 3. 件数 / 包装
old_pieces_pkg = '''          <!-- 件数 / 包装 (组合控件) -->
          <div class="biz-field-row single">
            <div class="biz-label">
              <span>件数 / 包装</span>
            </div>
            <div class="compound-input-group">
              <a-input-number 
                v-model:value="form.pieces" 
                size="small"
                :min="0" 
                :precision="0" 
                placeholder="数量" 
                style="width: 50%;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')" />
              <a-select 
                v-model:value="form.packageType" 
                size="small"
                :options="packageOptions" 
                placeholder="包装字典" 
                style="width: 50%;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')">
              </a-select>
            </div>
          </div>'''

new_pieces_pkg = '''          <!-- 件数 / 包装 (组合控件，整数数量 + 包装字典选择) -->
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
                placeholder="数量" 
                style="width: 100%;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')"></a-input-number>
            </div>
            <div class="biz-field-col">
              <div class="biz-label">
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
          </div>'''

assert old_pieces_pkg in text, "old_pieces_pkg not found"
text = text.replace(old_pieces_pkg, new_pieces_pkg)

# 4. 重量 / 尺码
old_weight_vol = '''          <!-- 重量(KGS) / 尺码(CBM) (组合控件，尺码为体积) -->
          <div class="biz-field-row single">
            <div class="biz-label">
              <span>重量 (KGS) / 尺码 (CBM 体积)</span>
              <span class="biz-helper">最多4位小数</span>
            </div>
            <div class="compound-input-group">
              <a-input-number 
                v-model:value="form.weight" 
                size="small"
                :min="0" 
                :precision="2" 
                addon-after="KGS" 
                placeholder="毛重" 
                style="width: 50%;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')" />
              <a-input-number 
                v-model:value="form.volume" 
                size="small"
                :min="0" 
                :precision="4" 
                addon-after="CBM" 
                placeholder="体积" 
                style="width: 50%;"
                :disabled="ticketData.isLocked"
                @change="markDirty('basic')" />
            </div>
          </div>'''

new_weight_vol = '''          <!-- 重量(KGS) / 尺码(CBM) (组合控件，分别带物理单位，尺码为体积，非负4位小数) -->
          <div class="biz-field-row">
            <div class="biz-field-col">
              <div class="biz-label">
                <span>重量 (Weight)</span>
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
                <span>尺码 (Volume 体积)</span>
                <span class="biz-helper">最多4位</span>
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
          </div>'''

assert old_weight_vol in text, "old_weight_vol not found"
text = text.replace(old_weight_vol, new_weight_vol)

# 5. remark textarea
old_remark = '''          <!-- 业务备注 -->
          <div class="biz-field-row single">
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
              @change="markDirty('basic')" />
          </div>'''

new_remark = '''          <!-- 业务备注 -->
          <div class="biz-field-row single">
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
          </div>'''

assert old_remark in text, "old_remark not found"
text = text.replace(old_remark, new_remark)

# 6. a-menu-divider
text = text.replace('<a-menu-divider />', '<a-menu-divider></a-menu-divider>')

# 7. Checkboxes in tables
text = text.replace(
    '''                      <a-checkbox 
                        :checked="isAllRecSelected" 
                        :indeterminate="isPartRecSelected"
                        @change="toggleSelectAllRec" />''',
    '''                      <a-checkbox 
                        :checked="isAllRecSelected" 
                        :indeterminate="isPartRecSelected"
                        @change="toggleSelectAllRec"></a-checkbox>'''
)

text = text.replace(
    '''                      <a-checkbox 
                        :checked="selectedRecKeys.includes(row.id)" 
                        @change="toggleSelectRec(row.id)" />''',
    '''                      <a-checkbox 
                        :checked="selectedRecKeys.includes(row.id)" 
                        @change="toggleSelectRec(row.id)"></a-checkbox>'''
)

text = text.replace(
    '''                      <a-checkbox 
                        :checked="isAllPaySelected" 
                        :indeterminate="isPartPaySelected"
                        @change="toggleSelectAllPay" />''',
    '''                      <a-checkbox 
                        :checked="isAllPaySelected" 
                        :indeterminate="isPartPaySelected"
                        @change="toggleSelectAllPay"></a-checkbox>'''
)

text = text.replace(
    '''                      <a-checkbox 
                        :checked="selectedPayKeys.includes(row.id)" 
                        @change="toggleSelectPay(row.id)" />''',
    '''                      <a-checkbox 
                        :checked="selectedPayKeys.includes(row.id)" 
                        @change="toggleSelectPay(row.id)"></a-checkbox>'''
)

# 8. masterOrderSearchKey
text = text.replace(
    '''      <a-input 
        v-model:value="masterOrderSearchKey" 
        size="small" 
        placeholder="搜索编号 / 主单号 / 客户名称..." 
        style="width: 280px;" />''',
    '''      <a-input 
        v-model:value="masterOrderSearchKey" 
        size="small" 
        placeholder="搜索编号 / 主单号 / 客户名称..." 
        style="width: 280px;"></a-input>'''
)

# 9. a-alert in spec drawer
text = text.replace(
    '''<a-alert message="100% 对齐《综合业务编辑页 UI／交互设计交接》规范标准" type="success" show-icon style="margin-bottom: 16px;" />''',
    '''<a-alert message="100% 对齐《综合业务编辑页 UI／交互设计交接》规范标准" type="success" show-icon style="margin-bottom: 16px;"></a-alert>'''
)

with open('scratch/build_comprehensive_workbench.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("build_comprehensive_workbench.py patched successfully!")
