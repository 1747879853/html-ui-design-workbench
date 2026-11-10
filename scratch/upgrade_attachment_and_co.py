with open('scratch/build_right_tabbed_workbench.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Replace CSS for TAB 2 & TAB 3 (from /* TAB 2: 更改单页签样式 to /* 浮动设计规范抽屉按钮 */)
css_start = code.find('    /* ==========================================================================\n       TAB 2: 更改单页签样式')
css_end = code.find('    /* 浮动设计规范抽屉按钮 */')
assert css_start != -1 and css_end != -1, f"CSS markers not found: {css_start}, {css_end}"

new_tab23_css = '''    /* ==========================================================================
       TAB 2: 更改单页签样式 (在右轨内呈现，与左轨业务保持上下文)
       ========================================================================== */
    .change-order-view {
      flex: 1;
      background: #f1f5f9;
      padding: 12px;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      gap: 10px;
    }
    .co-prerequisite-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 32px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 14px;
      max-width: 680px;
      margin: 36px auto;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .co-delta-strip {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 12px;
    }
    .co-delta-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 8px 12px;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .co-delta-lbl {
      font-size: 11px;
      color: #64748b;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .co-delta-val {
      font-size: 14px;
      font-weight: 800;
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", monospace;
      color: #0f172a;
    }

    /* ==========================================================================
       TAB 3: 附件凭证与单证齐套工作台 (Attachment & Voucher Cockpit)
       ========================================================================== */
    .attachment-view {
      flex: 1;
      background: #eef2f6;
      padding: 10px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      gap: 8px;
    }
    .attachment-card {
      background: #ffffff;
      border: 1px solid #dbe2ea;
      border-radius: 6px;
      padding: 12px;
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    /* 顶部 5 大单证分类齐套核对卡 (Document Category Checklist Grid) */
    .att-category-grid {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 8px;
      flex-shrink: 0;
    }
    .att-cat-card {
      background: #ffffff;
      border: 1px solid #dbe2ea;
      border-radius: 5px;
      padding: 7px 10px;
      cursor: pointer;
      transition: all 0.15s;
      display: flex;
      flex-direction: column;
      gap: 4px;
      position: relative;
      user-select: none;
    }
    .att-cat-card:hover {
      border-color: #93c5fd;
      background: #f8fafc;
    }
    .att-cat-card.is-active {
      background: linear-gradient(180deg, #eff6ff 0%, #ffffff 100%);
      border-color: #1677ff;
      box-shadow: 0 0 0 1px rgba(22, 119, 255, 0.15);
    }
    .att-cat-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 4px;
    }
    .att-cat-name {
      font-size: 12px;
      font-weight: 700;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .att-req-tag {
      font-size: 9px;
      font-weight: 700;
      padding: 0 4px;
      border-radius: 2px;
      line-height: 15px;
      flex-shrink: 0;
    }
    .att-req-tag.is-must {
      background: #fef2f2;
      color: #dc2626;
      border: 1px solid #fecaca;
    }
    .att-req-tag.is-opt {
      background: #f1f5f9;
      color: #64748b;
      border: 1px solid #e2e8f0;
    }
    .att-cat-bottom {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 10px;
      color: #64748b;
    }
    .att-status-pill {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-weight: 600;
      font-size: 10px;
    }
    .att-status-pill.is-done {
      color: #059669;
    }
    .att-status-pill.is-pending {
      color: #d97706;
    }

    /* 主体左右分栏：左侧列表与拖拽上传 (58%) + 右侧同屏单证预览与智能核对 (42%) */
    .att-split-body {
      flex: 1;
      display: flex;
      gap: 8px;
      overflow: hidden;
      min-height: 0;
    }
    .att-left-list-pane {
      width: 58%;
      background: #ffffff;
      border: 1px solid #dbe2ea;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .att-right-preview-pane {
      width: 42%;
      background: #ffffff;
      border: 1px solid #dbe2ea;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    /* 紧凑型拖拽快传条 (Compact Drag-and-Drop Upload Bar) */
    .att-upload-dropbar {
      margin: 8px 10px 6px 10px;
      padding: 7px 12px;
      background: linear-gradient(90deg, #f8fafc 0%, #f0f7ff 100%);
      border: 1px dashed #93c5fd;
      border-radius: 5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      flex-shrink: 0;
      transition: all 0.15s;
    }
    .att-upload-dropbar:hover {
      border-color: #1677ff;
      background: #eff6ff;
    }
    .dropbar-left {
      display: flex;
      align-items: center;
      gap: 8px;
      min-width: 0;
    }
    .dropbar-icon {
      width: 28px;
      height: 28px;
      border-radius: 5px;
      background: #dbeafe;
      color: #1d4ed8;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      flex-shrink: 0;
    }
    .dropbar-text-main {
      font-size: 11px;
      font-weight: 600;
      color: #1e293b;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .dropbar-text-sub {
      font-size: 10px;
      color: #64748b;
    }
    .dropbar-actions {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-shrink: 0;
    }

    /* 原生高密度凭证表格 (Native High-Density Voucher Table) */
    .att-table-wrap {
      flex: 1;
      overflow-y: auto;
      padding: 0 10px;
    }
    .att-native-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
    }
    .att-native-table th {
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      border-bottom: 1px solid #e2e8f0;
      color: #475569;
      font-weight: 600;
      text-align: left;
      padding: 6px 8px;
      position: sticky;
      top: 0;
      z-index: 2;
      white-space: nowrap;
    }
    .att-native-table td {
      padding: 7px 8px;
      border-bottom: 1px solid #f1f5f9;
      color: #1e293b;
      vertical-align: middle;
    }
    .att-row-item {
      cursor: pointer;
      transition: background 0.12s;
    }
    .att-row-item:hover {
      background: #f8fafc;
    }
    .att-row-item.is-selected {
      background: #eff6ff !important;
    }
    .att-row-item.is-selected td:first-child {
      border-left: 3px solid #1677ff;
    }
    .file-ext-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 26px;
      height: 22px;
      border-radius: 3px;
      font-size: 9px;
      font-weight: 800;
      font-family: monospace;
      flex-shrink: 0;
    }
    .file-ext-badge.is-pdf {
      background: #fef2f2;
      color: #dc2626;
      border: 1px solid #fecaca;
    }
    .file-ext-badge.is-img {
      background: #eff6ff;
      color: #2563eb;
      border: 1px solid #bfdbfe;
    }
    .ocr-match-pill {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-size: 10px;
      color: #059669;
      background: #ecfdf5;
      border: 1px solid #a7f3d0;
      padding: 1px 6px;
      border-radius: 3px;
      font-weight: 500;
    }
    .att-list-footer {
      height: 30px;
      padding: 0 12px;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 10px;
      color: #64748b;
      flex-shrink: 0;
    }

    /* 右侧同屏单证预览器与智能比对台 (In-Place Voucher Preview & Cross-Check Inspector) */
    .inspector-header {
      height: 34px;
      padding: 0 10px;
      background: #f8fafc;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .inspector-paper-scroll {
      flex: 1;
      background: #475569;
      padding: 12px;
      overflow-y: auto;
      display: flex;
      justify-content: center;
      align-items: flex-start;
    }
    .voucher-sheet {
      width: 100%;
      max-width: 440px;
      background: #ffffff;
      border-radius: 3px;
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.35);
      padding: 12px 14px;
      font-size: 10px;
      color: #1e293b;
      position: relative;
      border: 1px solid #cbd5e1;
    }
    .voucher-stamp {
      position: absolute;
      right: 16px;
      top: 14px;
      border: 2px solid #dc2626;
      color: #dc2626;
      font-size: 10px;
      font-weight: 800;
      padding: 1px 6px;
      border-radius: 3px;
      transform: rotate(-8deg);
      background: rgba(254, 242, 242, 0.85);
      letter-spacing: 0.5px;
      pointer-events: none;
    }
    .voucher-grid-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 6px;
    }
    .voucher-grid-table td, .voucher-grid-table th {
      border: 1px solid #cbd5e1;
      padding: 3px 6px;
      font-size: 10px;
    }
    .voucher-grid-lbl {
      color: #64748b;
      font-size: 9px;
      display: block;
    }
    .voucher-grid-val {
      font-weight: 700;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", monospace;
    }
    .inspector-crosscheck-footer {
      padding: 6px 10px;
      background: #f0fdf4;
      border-top: 1px solid #bbf7d0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      font-size: 10px;
      color: #166534;
      flex-shrink: 0;
    }

'''

code = code[:css_start] + new_tab23_css + code[css_end:]

# 2. Update right-wb-actions for attachment tab
att_top_target = '''          <template v-else-if="activeTabKey === 'attachment'">
            <span style="font-size: 11px; color: #64748b;">附件总计: {{ attachmentList.length }} 个文件</span>
          </template>'''

att_top_replacement = '''          <template v-else-if="activeTabKey === 'attachment'">
            <span class="status-glow-pill is-editable" style="font-size: 10px;">
              <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 必传单证齐套 3/3
            </span>
            <a-radio-group v-model:value="attachmentScenario" size="small">
              <a-radio-button value="configured">单证工作台 (有配置)</a-radio-button>
              <a-radio-button value="empty_no_config">无类型配置空态 (图05)</a-radio-button>
            </a-radio-group>
            <a-button size="small" :disabled="ticketData.isLocked" @click="openAddOtherAttachmentType">
              <iconify-icon icon="ant-design:AppstoreAddOutlined"></iconify-icon> 添加其他类型
            </a-button>
            <a-button size="small" @click="downloadAllAttachments">
              <iconify-icon icon="ant-design:CloudDownloadOutlined"></iconify-icon> 打包下载 ({{ attachmentList.length }})
            </a-button>
          </template>'''

assert att_top_target in code, "att_top_target not found"
code = code.replace(att_top_target, att_top_replacement, 1)

# 3. Replace TAB 2 and TAB 3 HTML blocks
tab23_html_start = code.find('      <!-- ==================================================================\n           TAB 2 内容: 更改单调账工作台')
tab23_html_end = code.find('  <!-- ========================================================================\n       4. 弹窗与抽屉矩阵')
assert tab23_html_start != -1 and tab23_html_end != -1, f"TAB23 HTML markers not found: {tab23_html_start}, {tab23_html_end}"

new_tab23_html = '''      <!-- ==================================================================
           TAB 2 内容: 更改单调账工作台 (右侧切换，左侧业务底账持续常驻！)
           ================================================================== -->
      <div v-show="activeTabKey === 'changeOrder'" class="change-order-view">

        <!-- 分支 1: 原票费用未锁定拦截态 (图04) -->
        <div v-if="!ticketData.isOriginalFeeLocked" class="co-prerequisite-card">
          <iconify-icon icon="ant-design:exclamation-circle-filled" style="font-size: 48px; color: #faad14;"></iconify-icon>
          <div style="font-size: 16px; font-weight: 600; color: #111827;">
            主单费用未锁定，不能添加更改单
          </div>
          <div style="font-size: 13px; color: #4b5563; max-width: 520px; line-height: 1.6;">
            更改单是针对<strong>已完成费用锁账的业务</strong>进行后续费用追溯、补充调账的正式单据。<br>
            当前主单费用尚未执行锁费，如需调整或录入费用，请直接在「应收应付明细」中增删改。若原票已完成核算，请先执行原票费用锁账。
          </div>

          <div style="display: flex; gap: 12px; margin-top: 10px;">
            <a-button type="primary" @click="activeTabKey = 'fee'">
              <iconify-icon icon="ant-design:arrow-left-outlined"></iconify-icon> 前往「应收应付明细」直接调整
            </a-button>
            <a-button @click="mockLockOriginalFee">
              <iconify-icon icon="ant-design:lock-outlined"></iconify-icon> 原型模拟：立即锁账原费用
            </a-button>
          </div>
        </div>

        <!-- 分支 2: 原票费用已锁定，正常更改单列表与调账前后财务对比 -->
        <div v-else style="background: #ffffff; border-radius: 6px; border: 1px solid #dbe2ea; padding: 14px; flex: 1; display: flex; flex-direction: column;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #f1f5f9;">
            <div>
              <div style="font-size: 14px; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 8px;">
                <span>更改单调账工作台 (Change Orders)</span>
                <a-tag color="green" style="font-size: 10px; margin: 0;">原票费用已锁账封存</a-tag>
              </div>
              <div style="font-size: 11px; color: #64748b; margin-top: 2px;">
                支持针对已锁账原票发起应收/应付调增与调减，审批生效后可勾选「合并更改单」透视全貌
              </div>
            </div>

            <div style="display: flex; gap: 8px;">
              <a-button type="primary" size="small" @click="addMockChangeOrder">
                <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 新建更改单
              </a-button>
              <a-button size="small" @click="mockUnlockOriginalFee">
                恢复未锁拦截态 (图04)
              </a-button>
            </div>
          </div>

          <!-- 原票 vs 更改单调账后财务对比条 -->
          <div class="co-delta-strip">
            <div class="co-delta-card">
              <div class="co-delta-lbl">
                <span>原票封存基准 (锁账)</span>
                <iconify-icon icon="ant-design:lock-outlined" style="color: #64748b;"></iconify-icon>
              </div>
              <div class="co-delta-val">收 17.80 / 付 7.80</div>
              <div style="font-size: 10px; color: #64748b;">原票毛利: RMB 10.00</div>
            </div>
            <div class="co-delta-card" style="background: #fffbeb; border-color: #fde68a;">
              <div class="co-delta-lbl">
                <span style="color: #b45309;">更改单累计调增 (应收)</span>
                <span style="color: #d97706; font-weight: 700;">{{ changeOrderList.length }} 份更改单</span>
              </div>
              <div class="co-delta-val" style="color: #d97706;">+ RMB 500.00</div>
              <div style="font-size: 10px; color: #b45309;">卸货港堆存天数补充调账</div>
            </div>
            <div class="co-delta-card">
              <div class="co-delta-lbl">
                <span>更改单累计调增 (应付)</span>
                <span>无变动</span>
              </div>
              <div class="co-delta-val">RMB 0.00</div>
              <div style="font-size: 10px; color: #64748b;">应付成本未发生追加</div>
            </div>
            <div class="co-delta-card" style="background: #f0fdf4; border-color: #bbf7d0;">
              <div class="co-delta-lbl">
                <span style="color: #166534;">合并调账后最新总毛利</span>
                <span style="color: #15803d; font-weight: 700;">↑ +5000%</span>
              </div>
              <div class="co-delta-val" style="color: #15803d;">RMB 510.00</div>
              <div style="font-size: 10px; color: #166534;">合并应收 517.80 / 应付 7.80</div>
            </div>
          </div>

          <!-- 原生高密度更改单表格 (确保所有状态标签与操作按钮 100% 渲染) -->
          <div style="flex: 1; overflow-y: auto;">
            <table class="att-native-table">
              <thead>
                <tr>
                  <th style="width: 40px; text-align: center;">#</th>
                  <th style="width: 140px;">更改单号</th>
                  <th style="width: 130px;">申请时间</th>
                  <th style="width: 90px;">申请人</th>
                  <th style="width: 110px; text-align: right;">应收调增/减</th>
                  <th style="width: 110px; text-align: right;">应付调增/减</th>
                  <th style="width: 110px; text-align: right;">毛利影响</th>
                  <th style="width: 90px; text-align: center;">审核状态</th>
                  <th>调账原因与科目说明</th>
                  <th style="width: 160px; text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(co, idx) in changeOrderList" :key="co.id" class="att-row-item">
                  <td style="text-align: center; color: #94a3b8;">{{ idx + 1 }}</td>
                  <td>
                    <strong style="font-family: monospace; color: #1d4ed8;">{{ co.changeNo }}</strong>
                  </td>
                  <td style="color: #64748b; font-family: monospace;">{{ co.createTime }}</td>
                  <td>{{ co.applicant }}</td>
                  <td style="text-align: right; font-weight: 700; color: #d97706; font-family: monospace;">{{ co.recDiff }}</td>
                  <td style="text-align: right; font-family: monospace; color: #64748b;">{{ co.payDiff }}</td>
                  <td style="text-align: right; font-weight: 700; color: #16a34a; font-family: monospace;">{{ co.profitDiff }}</td>
                  <td style="text-align: center;">
                    <a-tag :color="co.status === '已生效' ? 'green' : 'orange'" style="font-size: 10px; margin: 0;">
                      {{ co.status }}
                    </a-tag>
                  </td>
                  <td style="color: #334155;">{{ co.reason }}</td>
                  <td style="text-align: center;">
                    <a-button type="link" size="small" style="padding: 0 4px; font-size: 11px;" @click="enterMergeModeAndSwitchFee">
                      合并透视
                    </a-button>
                    <a-button type="link" size="small" style="padding: 0 4px; font-size: 11px;" @click="antd.message.info('已打开更改单 ' + co.changeNo + ' 调账明细抽屉')">
                      查看明细
                    </a-button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- ==================================================================
           TAB 3 内容: 附件凭证与单证齐套工作台 (右侧切换，左侧业务底账持续常驻！)
           ================================================================== -->
      <div v-show="activeTabKey === 'attachment'" class="attachment-view">

        <!-- 分支 1: 暂无附件类型配置空态 (100% 还原图05 + 4种空态诊断说明) -->
        <div v-if="attachmentScenario === 'empty_no_config'" class="attachment-card" style="align-items: center; justify-content: center; text-align: center;">
          <a-empty description="暂无附件类型配置">
            <template #image>
              <iconify-icon icon="ant-design:inbox-outlined" style="font-size: 56px; color: #94a3b8;"></iconify-icon>
            </template>
            <div style="color: #64748b; font-size: 12px; max-width: 520px; margin: 0 auto 14px auto; line-height: 1.6;">
              当前业务类型尚未在系统基础档案中预设标准附件分类（非系统故障或无权限）。您可以点击下方<strong>「添加其他类型」</strong>临时扩展分类上传，或切换至已配置单证工作台预览。
            </div>
            <a-space size="middle">
              <a-button type="primary" @click="openAddOtherAttachmentType">
                <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 添加其他类型
              </a-button>
              <a-button @click="attachmentScenario = 'configured'">
                <iconify-icon icon="ant-design:eye-outlined"></iconify-icon> 切换为标准单证齐套工作台
              </a-button>
            </a-space>
          </a-empty>

          <!-- 4类空态与权限边界清晰说明卡 (对齐交接文档第7节优化建议) -->
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; width: 100%; max-width: 820px; margin-top: 28px; text-align: left;">
            <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 5px; padding: 8px 10px;">
              <div style="font-size: 11px; font-weight: 700; color: #0284c7; margin-bottom: 3px;">● 状态 A：未配置类型 (当前)</div>
              <div style="font-size: 10px; color: #64748b;">后台未预设分类字典，允许通过「添加其他类型」补充自定义单证类别。</div>
            </div>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px;">
              <div style="font-size: 11px; font-weight: 700; color: #334155; margin-bottom: 3px;">○ 状态 B：已配置但暂未上传</div>
              <div style="font-size: 10px; color: #64748b;">展示必传/选传单证清单槽位（如提单、报关单），引导拖拽对号上传。</div>
            </div>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px;">
              <div style="font-size: 11px; font-weight: 700; color: #334155; margin-bottom: 3px;">○ 状态 C：锁账受限只读态</div>
              <div style="font-size: 10px; color: #64748b;">单据锁账后禁止删除已归档凭证，仅锁账白名单分类允许补充上传。</div>
            </div>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px;">
              <div style="font-size: 11px; font-weight: 700; color: #334155; margin-bottom: 3px;">○ 状态 D：请求异常可重试</div>
              <div style="font-size: 10px; color: #64748b;">网络失败时独立局部重试，绝不与「无类型配置」混淆且不丢失左栏草稿。</div>
            </div>
          </div>
        </div>

        <!-- 分支 2: 标准单证齐套与同屏预览工作台 (5大单证分类卡 + 左表拖拽快传 + 右侧同屏预览与OCR比对) -->
        <template v-else>
          <!-- 1. 顶部 5 大单证分类齐套核对矩阵 -->
          <div class="att-category-grid">
            <div 
              class="att-cat-card" 
              :class="{ 'is-active': attachmentCategoryFilter === 'all' }"
              @click="selectAttachmentCategory('all')">
              <div class="att-cat-top">
                <span class="att-cat-name">
                  <iconify-icon icon="ant-design:folder-open-outlined" style="color: #1677ff;"></iconify-icon>
                  全部单证凭证
                </span>
                <span class="att-req-tag is-opt">总览</span>
              </div>
              <div class="att-cat-bottom">
                <span class="att-status-pill is-done">已传 {{ attachmentList.length }} 份</span>
                <span>共 4.35 MB</span>
              </div>
            </div>

            <div 
              class="att-cat-card" 
              :class="{ 'is-active': attachmentCategoryFilter === 'bl' }"
              @click="selectAttachmentCategory('bl')">
              <div class="att-cat-top">
                <span class="att-cat-name">
                  <iconify-icon icon="ant-design:container-outlined" style="color: #0284c7;"></iconify-icon>
                  提单/运单 (MBL)
                </span>
                <span class="att-req-tag is-must">必传*</span>
              </div>
              <div class="att-cat-bottom">
                <span class="att-status-pill is-done">
                  <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 已齐备 ({{ getCategoryCount('bl') }})
                </span>
                <span>正本扫描</span>
              </div>
            </div>

            <div 
              class="att-cat-card" 
              :class="{ 'is-active': attachmentCategoryFilter === 'customs' }"
              @click="selectAttachmentCategory('customs')">
              <div class="att-cat-top">
                <span class="att-cat-name">
                  <iconify-icon icon="ant-design:audit-outlined" style="color: #0d9488;"></iconify-icon>
                  报关/放行凭证
                </span>
                <span class="att-req-tag is-must">必传*</span>
              </div>
              <div class="att-cat-bottom">
                <span class="att-status-pill is-done">
                  <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 已齐备 ({{ getCategoryCount('customs') }})
                </span>
                <span>海关放行</span>
              </div>
            </div>

            <div 
              class="att-cat-card" 
              :class="{ 'is-active': attachmentCategoryFilter === 'invoice' }"
              @click="selectAttachmentCategory('invoice')">
              <div class="att-cat-top">
                <span class="att-cat-name">
                  <iconify-icon icon="ant-design:account-book-outlined" style="color: #d97706;"></iconify-icon>
                  应收应付发票/账单
                </span>
                <span class="att-req-tag is-must">必传*</span>
              </div>
              <div class="att-cat-bottom">
                <span class="att-status-pill is-done">
                  <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 已齐备 ({{ getCategoryCount('invoice') }})
                </span>
                <span>匹配应付THC</span>
              </div>
            </div>

            <div 
              class="att-cat-card" 
              :class="{ 'is-active': attachmentCategoryFilter === 'other' }"
              @click="selectAttachmentCategory('other')">
              <div class="att-cat-top">
                <span class="att-cat-name">
                  <iconify-icon icon="ant-design:file-add-outlined" style="color: #7c3aed;"></iconify-icon>
                  保函/装箱单/其他
                </span>
                <span class="att-req-tag is-opt">选传</span>
              </div>
              <div class="att-cat-bottom">
                <span v-if="getCategoryCount('other') > 0" class="att-status-pill is-done">
                  <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon> 已上传 ({{ getCategoryCount('other') }})
                </span>
                <span v-else class="att-status-pill is-pending">
                  <iconify-icon icon="ant-design:clock-circle-outlined"></iconify-icon> 待补充 (0)
                </span>
                <span style="color: #1677ff;" @click.stop="mockQuickUploadTelex">+快传保函</span>
              </div>
            </div>
          </div>

          <!-- 2. 下方双栏工作区：左栏拖拽上传与结构化清单 (58%) + 右栏足不出户同屏单证预览与智能核对 (42%) -->
          <div class="att-split-body">

            <!-- 左栏：快传区 + 高密度原生单证表格 -->
            <div class="att-left-list-pane">
              <!-- 紧凑拖拽上传栏 -->
              <div class="att-upload-dropbar">
                <div class="dropbar-left">
                  <div class="dropbar-icon">
                    <iconify-icon icon="ant-design:cloud-upload-outlined"></iconify-icon>
                  </div>
                  <div style="min-width: 0;">
                    <div class="dropbar-text-main">
                      拖拽 PDF / JPG / PNG / Excel 单证至此，或选择归属分类上传
                    </div>
                    <div class="dropbar-text-sub">
                      单文件上限 10MB · 支持提单、报关单、增值税发票自动识别比对
                    </div>
                  </div>
                </div>

                <div class="dropbar-actions">
                  <a-select v-model:value="uploadTargetCategory" size="small" style="width: 112px;" :disabled="ticketData.isLocked">
                    <a-select-option value="bl">提单/运单</a-select-option>
                    <a-select-option value="customs">报关/放行单</a-select-option>
                    <a-select-option value="invoice">费用发票</a-select-option>
                    <a-select-option value="other">保函/其他</a-select-option>
                  </a-select>

                  <a-upload :show-upload-list="false" :before-upload="handleFileUpload">
                    <a-button type="primary" size="small" :disabled="ticketData.isLocked">
                      <iconify-icon icon="ant-design:upload-outlined"></iconify-icon> 上传凭证
                    </a-button>
                  </a-upload>

                  <a-tooltip title="一键模拟上传一份「电放保函_青岛万达.pdf」并实时预览">
                    <a-button size="small" :disabled="ticketData.isLocked" @click="mockQuickUploadTelex">
                      <iconify-icon icon="ant-design:thunderbolt-outlined" style="color: #0284c7;"></iconify-icon> 模拟传保函
                    </a-button>
                  </a-tooltip>
                </div>
              </div>

              <!-- 高密度原生单证列表 (点击任意行即可在右侧同屏预览！) -->
              <div class="att-table-wrap">
                <table class="att-native-table">
                  <thead>
                    <tr>
                      <th style="width: 32px; text-align: center;">#</th>
                      <th>凭证文件名称 (点击行同屏预览)</th>
                      <th style="width: 96px;">所属分类</th>
                      <th style="width: 175px;">左栏/费用联动核对</th>
                      <th style="width: 68px; text-align: right;">大小</th>
                      <th style="width: 120px;">上传人 / 时间</th>
                      <th style="width: 138px; text-align: center;">操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr 
                      v-for="(att, idx) in filteredAttachments" 
                      :key="att.id" 
                      class="att-row-item"
                      :class="{ 'is-selected': activePreviewAtt && activePreviewAtt.id === att.id }"
                      @click="selectPreviewAttachment(att)">
                      <td style="text-align: center; color: #94a3b8;">{{ idx + 1 }}</td>
                      <td>
                        <div style="display: flex; align-items: center; gap: 7px;">
                          <span class="file-ext-badge" :class="att.fileName.endsWith('.pdf') ? 'is-pdf' : 'is-img'">
                            {{ att.fileName.endsWith('.pdf') ? 'PDF' : 'JPG' }}
                          </span>
                          <div style="min-width: 0;">
                            <div style="font-weight: 600; color: #0f172a; display: flex; align-items: center; gap: 5px;">
                              <span>{{ att.fileName }}</span>
                              <span v-if="activePreviewAtt && activePreviewAtt.id === att.id" style="font-size: 9px; background: #dbeafe; color: #1d4ed8; padding: 0 4px; border-radius: 2px; font-weight: 700;">
                                预览中
                              </span>
                            </div>
                            <div style="font-size: 10px; color: #64748b;">
                              {{ att.docNoText || '单证编号: TEST-GH178-20261109' }}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td>
                        <a-tag :color="getCategoryTagColor(att.fileType)" style="font-size: 10px; margin: 0;">
                          {{ getCategoryLabel(att.fileType) }}
                        </a-tag>
                      </td>
                      <td>
                        <span class="ocr-match-pill">
                          <iconify-icon icon="ant-design:check-circle-filled"></iconify-icon>
                          {{ att.verifyNote || '与左侧档案一致' }}
                        </span>
                      </td>
                      <td style="text-align: right; font-family: monospace; color: #475569;">{{ att.fileSize }}</td>
                      <td>
                        <div style="font-size: 11px; color: #334155;">{{ att.uploader }}</div>
                        <div style="font-size: 10px; color: #94a3b8; font-family: monospace;">{{ att.uploadTime }}</div>
                      </td>
                      <td style="text-align: center;" @click.stop>
                        <a-button type="link" size="small" style="padding: 0 4px; font-size: 11px;" @click="selectPreviewAttachment(att)">
                          预览
                        </a-button>
                        <a-button type="link" size="small" style="padding: 0 4px; font-size: 11px;" @click="downloadAttachment(att)">
                          下载
                        </a-button>
                        <a-popconfirm title="确认从本票单据中删除此附件凭证？" @confirm="deleteAttachment(att.id)">
                          <a-button type="link" size="small" danger style="padding: 0 4px; font-size: 11px;" :disabled="ticketData.isLocked">
                            删除
                          </a-button>
                        </a-popconfirm>
                      </td>
                    </tr>

                    <!-- 当选定分类下无文件时的引导空态 -->
                    <tr v-if="filteredAttachments.length === 0">
                      <td colspan="7" style="text-align: center; padding: 36px 16px; color: #64748b;">
                        <iconify-icon icon="ant-design:folder-open-outlined" style="font-size: 28px; color: #cbd5e1; display: block; margin: 0 auto 6px auto;"></iconify-icon>
                        <div style="font-size: 12px; font-weight: 600; color: #334155;">当前「{{ getCategoryLabel(attachmentCategoryFilter) }}」分类下暂无文件</div>
                        <div style="font-size: 11px; color: #94a3b8; margin: 4px 0 10px 0;">可点击上方上传按钮或点击下方快捷按钮生成测试凭证</div>
                        <a-button type="dashed" size="small" :disabled="ticketData.isLocked" @click="mockQuickUploadTelex">
                          <iconify-icon icon="ant-design:plus-outlined"></iconify-icon> 立即补充上传「电放保函」样本
                        </a-button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- 底部权限与归档规则说明条 -->
              <div class="att-list-footer">
                <span>
                  <iconify-icon icon="ant-design:safety-certificate-outlined" style="color: #059669;"></iconify-icon>
                  归档规则：同公司数据隔离校验 · 锁账后受白名单保护
                </span>
                <span>当前展示 {{ filteredAttachments.length }} / {{ attachmentList.length }} 份凭证</span>
              </div>
            </div>

            <!-- 右栏：足不出户同屏单证预览与智能比对台 (In-Place Live Document Inspector) -->
            <div class="att-right-preview-pane">
              <div class="inspector-header">
                <div style="display: flex; align-items: center; gap: 6px; min-width: 0;">
                  <iconify-icon icon="ant-design:file-search-outlined" style="color: #1677ff; font-size: 14px;"></iconify-icon>
                  <strong style="font-size: 11px; color: #0f172a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    同屏凭证预览: {{ activePreviewAtt ? activePreviewAtt.fileName : '请选择左侧凭证' }}
                  </strong>
                </div>
                <div style="display: flex; align-items: center; gap: 4px; flex-shrink: 0;">
                  <a-tag color="blue" style="font-size: 10px; margin: 0;">100% 适宽</a-tag>
                  <a-button v-if="activePreviewAtt" type="text" size="small" style="padding: 0 4px; height: 22px; font-size: 11px;" @click="downloadAttachment(activePreviewAtt)">
                    <iconify-icon icon="ant-design:download-outlined"></iconify-icon> 原件
                  </a-button>
                </div>
              </div>

              <!-- 仿真单证票面预览画布 (随所选提单/报关单/发票动态切换票面！) -->
              <div class="inspector-paper-scroll">
                <!-- 预览模板 1: 海运提单 (BL) -->
                <div v-if="activePreviewAtt && activePreviewAtt.fileType === 'bl'" class="voucher-sheet">
                  <div class="voucher-stamp">ORIGINAL · 正本已核</div>
                  <div style="border-bottom: 2px solid #0f172a; padding-bottom: 5px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: flex-end;">
                    <div>
                      <div style="font-size: 13px; font-weight: 800; letter-spacing: 0.5px; color: #0f172a;">MAERSK LINE · BILL OF LADING</div>
                      <div style="font-size: 9px; color: #64748b;">COMBINED TRANSPORT OR PORT TO PORT SHIPMENT</div>
                    </div>
                    <div style="text-align: right;">
                      <span style="font-size: 9px; color: #64748b;">B/L NO.</span>
                      <div style="font-size: 11px; font-weight: 800; color: #1d4ed8; font-family: monospace;">{{ form.blNo }}</div>
                    </div>
                  </div>

                  <table class="voucher-grid-table">
                    <tr>
                      <td colspan="2">
                        <span class="voucher-grid-lbl">SHIPPER (托运人/委托单位)</span>
                        <span class="voucher-grid-val">{{ ticketData.customerName }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">OCEAN VESSEL (船名)</span>
                        <span class="voucher-grid-val">{{ form.vesselName }}</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">VOYAGE NO. (航次)</span>
                        <span class="voucher-grid-val">{{ form.voyage }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">PORT OF LOADING (起运港)</span>
                        <span class="voucher-grid-val">{{ form.pol }} ({{ getPortCnName(form.pol) }})</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">PORT OF DISCHARGE (目的港)</span>
                        <span class="voucher-grid-val">{{ form.pod }} ({{ getPortCnName(form.pod) }})</span>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="2">
                        <span class="voucher-grid-lbl">PARTICULARS FURNISHED BY SHIPPER (件数 · 毛重 · 体积 · 品名)</span>
                        <div style="display: flex; justify-content: space-between; margin-top: 2px; font-weight: 700; color: #0f172a; font-family: monospace;">
                          <span>{{ form.pieces }} {{ form.packageType }}</span>
                          <span>G.W.: {{ form.weight }} KGS</span>
                          <span>MEAS.: {{ form.volume }} CBM</span>
                        </div>
                        <div style="color: #475569; margin-top: 2px;">DESCRIPTION: {{ form.commodities.join(' / ') }} · FREIGHT PREPAID</div>
                      </td>
                    </tr>
                  </table>
                </div>

                <!-- 预览模板 2: 出口报关单 (Customs) -->
                <div v-else-if="activePreviewAtt && activePreviewAtt.fileType === 'customs'" class="voucher-sheet">
                  <div class="voucher-stamp" style="border-color: #059669; color: #059669; background: rgba(236, 253, 245, 0.9);">海关已放行 · 查验通过</div>
                  <div style="text-align: center; border-bottom: 1.5px solid #0f172a; padding-bottom: 5px; margin-bottom: 6px;">
                    <div style="font-size: 12px; font-weight: 800; color: #0f172a;">中华人民共和国海关出口货物报关单</div>
                    <div style="font-size: 9px; color: #475569; font-family: monospace; margin-top: 2px;">预录入编号: 425820260001892041 · 申报口岸: 青岛大港海关 (4258)</div>
                  </div>

                  <table class="voucher-grid-table">
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">境内发货人</span>
                        <span class="voucher-grid-val">{{ ticketData.customerName }}</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">出境关别 / 申报日期</span>
                        <span class="voucher-grid-val">青岛海关 · {{ form.bizDate }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">运输工具名称及航次号</span>
                        <span class="voucher-grid-val">{{ form.vesselName }} / {{ form.voyage }}</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">提运单号 (B/L No.)</span>
                        <span class="voucher-grid-val">{{ form.blNo }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">贸易国 / 运抵国(地区)</span>
                        <span class="voucher-grid-val">美国 (USLAX 洛杉矶)</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">件数 / 包装种类 / 毛重</span>
                        <span class="voucher-grid-val">{{ form.pieces }} {{ form.packageType }} · {{ form.weight }} KG</span>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="2">
                        <span class="voucher-grid-lbl">商品名称及规格型号 (HS编码核对)</span>
                        <span class="voucher-grid-val">01. 8708999990 {{ form.commodities.join(' / ') }} · 监管方式: 一般贸易</span>
                      </td>
                    </tr>
                  </table>
                </div>

                <!-- 预览模板 3: 增值税专用发票 (Invoice) -->
                <div v-else-if="activePreviewAtt && activePreviewAtt.fileType === 'invoice'" class="voucher-sheet" style="border-color: #fda4af;">
                  <div class="voucher-stamp">真伪查验通过 · 匹配应付</div>
                  <div style="text-align: center; border-bottom: 1.5px double #be123c; padding-bottom: 4px; margin-bottom: 6px;">
                    <div style="font-size: 12px; font-weight: 800; color: #9f1239; letter-spacing: 1px;">山东增值税专用发票 (电子发票)</div>
                    <div style="font-size: 9px; color: #64748b; font-family: monospace;">发票号码: No.263702000001928371 · 开票日期: 2026-11-09</div>
                  </div>

                  <table class="voucher-grid-table">
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">购买方名称</span>
                        <span class="voucher-grid-val">青岛佳越国际物流有限公司</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">销售方名称 (应付结算对象)</span>
                        <span class="voucher-grid-val">青岛中远海运集装箱运输有限公司</span>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="2">
                        <span class="voucher-grid-lbl">项目名称 / 规格型号 / 数量 / 单价</span>
                        <div style="display: flex; justify-content: space-between; font-weight: 700; color: #0f172a; margin-top: 2px;">
                          <span>*港口码头服务* 码头操作费 (THC)</span>
                          <span style="font-family: monospace;">1 票 × ¥7.36</span>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">不含税金额 / 税率 / 税额</span>
                        <span class="voucher-grid-val">¥7.36 · 税率 6% · 税额 ¥0.44</span>
                      </td>
                      <td style="background: #fff1f2;">
                        <span class="voucher-grid-lbl" style="color: #be123c;">价税合计 (小写)</span>
                        <span class="voucher-grid-val" style="color: #be123c; font-size: 12px;">RMB 7.80</span>
                      </td>
                    </tr>
                  </table>
                </div>

                <!-- 预览模板 4: 其他保函/通用单证 -->
                <div v-else class="voucher-sheet">
                  <div class="voucher-stamp" style="border-color: #2563eb; color: #2563eb; background: rgba(239, 246, 255, 0.9);">保函已归档</div>
                  <div style="text-align: center; border-bottom: 1.5px solid #0f172a; padding-bottom: 5px; margin-bottom: 6px;">
                    <div style="font-size: 12px; font-weight: 800; color: #0f172a;">海运出口货物电放保函 (TELEX RELEASE LOI)</div>
                    <div style="font-size: 9px; color: #64748b;">致：青岛佳越国际物流有限公司 / 承运船东 {{ form.carrier }}</div>
                  </div>
                  <table class="voucher-grid-table">
                    <tr>
                      <td>
                        <span class="voucher-grid-lbl">对应提单号 (B/L No.)</span>
                        <span class="voucher-grid-val">{{ form.blNo }}</span>
                      </td>
                      <td>
                        <span class="voucher-grid-lbl">船名 / 航次</span>
                        <span class="voucher-grid-val">{{ form.vesselName }} / {{ form.voyage }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="2">
                        <span class="voucher-grid-lbl">保函声明内容</span>
                        <div style="color: #334155; line-height: 1.4;">
                          兹有我司（{{ ticketData.customerName }}）出运至 {{ form.pod }} 货物共 {{ form.pieces }} {{ form.packageType }}，因贸易交单需要申请安排电放放货，一切法律责任由我司承担。
                        </div>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>

              <!-- 底部智能比对与一键同步栏 -->
              <div class="inspector-crosscheck-footer">
                <div style="display: flex; align-items: center; gap: 5px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">
                  <iconify-icon icon="ant-design:check-circle-filled" style="color: #16a34a; font-size: 13px;"></iconify-icon>
                  <span>
                    <strong>智能比对通过：</strong>单证提单号、船名航次、件毛体与左栏底账 100% 吻合
                  </span>
                </div>
                <a-button 
                  type="primary" 
                  size="small" 
                  style="height: 22px; font-size: 10px; padding: 0 8px; background: #16a34a; border-color: #16a34a; flex-shrink: 0;"
                  :disabled="ticketData.isLocked"
                  @click="syncVoucherToWorkbench(activePreviewAtt)">
                  <iconify-icon icon="ant-design:retweet-outlined"></iconify-icon> 提取单证数据至左栏
                </a-button>
              </div>
            </div>

          </div>
        </template>

      </div>

    </div>

  </div>

'''

code = code[:tab23_html_start] + new_tab23_html + code[tab23_html_end:]

# 4. Update attachment & changeOrder reactive models and helper methods in setup()
att_model_target = '''      // 附件模型
      const attachmentScenario = ref('empty_no_config'); // 'empty_no_config' | 'configured'
      const attachmentCategoryFilter = ref('all');
      const attachmentList = ref([
        { id: 'att-1', fileName: '提单正本扫描件_TEST-GH178.pdf', fileType: 'bl', fileSize: '2.4 MB', uploader: '李操作', uploadTime: '2026-11-09 11:20' },
        { id: 'att-2', fileName: '出口报关预录单_CNTAO.pdf', fileType: 'customs', fileSize: '1.1 MB', uploader: '孙报关', uploadTime: '2026-11-09 13:45' },
        { id: 'att-3', fileName: '码头THC增值税发票.jpg', fileType: 'invoice', fileSize: '850 KB', uploader: '王经理', uploadTime: '2026-11-09 15:10' }
      ]);'''

att_model_replacement = '''      // 附件凭证模型 (默认 configured，沙盘第 6 项切换为 empty_no_config 还原图05)
      const attachmentScenario = ref('configured'); // 'configured' | 'empty_no_config'
      const attachmentCategoryFilter = ref('all');
      const uploadTargetCategory = ref('bl');
      const attachmentList = ref([
        {
          id: 'att-1',
          fileName: '提单正本扫描件_TEST-GH178.pdf',
          fileType: 'bl',
          fileSize: '2.4 MB',
          uploader: '李操作',
          uploadTime: '2026-11-09 11:20',
          docNoText: 'MBL: TEST-GH178-20261109 · 500 CTNS',
          verifyNote: '提单号/件重尺与左栏一致'
        },
        {
          id: 'att-2',
          fileName: '出口报关预录单_CNTAO.pdf',
          fileType: 'customs',
          fileSize: '1.1 MB',
          uploader: '孙报关',
          uploadTime: '2026-11-09 13:45',
          docNoText: '报关单: 42582026000189 · 青岛海关',
          verifyNote: '船名航次/起目港核对一致'
        },
        {
          id: 'att-3',
          fileName: '码头THC增值税发票.jpg',
          fileType: 'invoice',
          fileSize: '850 KB',
          uploader: '王经理',
          uploadTime: '2026-11-09 15:10',
          docNoText: '专票: No.26370200 · 税率6%',
          verifyNote: '匹配应付 THC ¥7.80'
        }
      ]);
      const activePreviewAtt = ref(attachmentList.value[0]);'''

assert att_model_target in code, "att_model_target not found"
code = code.replace(att_model_target, att_model_replacement, 1)

# 5. Add attachment & changeOrder helper functions around openAddOtherAttachmentType
att_methods_target = '''      const openAddOtherAttachmentType = () => {
        antd.message.info('已调起自定义附件类型字典扩展窗口。');
      };
      const handleFileUpload = (file) => {
        if (file.size > 10 * 1024 * 1024) {
          antd.message.error('单文件大小超过 10MB 限制！');
          return false;
        }
        attachmentList.value.push({
          id: 'att-' + Date.now(),
          fileName: file.name,
          fileType: 'other',
          fileSize: (file.size / 1024).toFixed(1) + ' KB',
          uploader: '李操作',
          uploadTime: window.dayjs().format('YYYY-MM-DD HH:mm')
        });
        antd.message.success(`文件 ${file.name} 上传成功！`);
        return false;
      };
      const previewAttachment = (att) => {
        antd.message.info(`正在调起附件安全预览: ${att.fileName}`);
      };
      const downloadAttachment = (att) => {
        antd.message.success(`已开始下载: ${att.fileName}`);
      };
      const deleteAttachment = (id) => {
        attachmentList.value = attachmentList.value.filter(a => a.id !== id);
        antd.message.success('附件已删除。');
      };'''

att_methods_replacement = '''      const getCategoryCount = (cat) => {
        return attachmentList.value.filter(a => a.fileType === cat).length;
      };
      const getCategoryLabel = (cat) => {
        const map = { all: '全部单证', bl: '提单/运单', customs: '报关凭证', invoice: '费用发票', other: '保函/其他' };
        return map[cat] || '其他单证';
      };
      const getCategoryTagColor = (cat) => {
        const map = { bl: 'blue', customs: 'cyan', invoice: 'orange', other: 'purple' };
        return map[cat] || 'default';
      };
      const selectAttachmentCategory = (cat) => {
        attachmentCategoryFilter.value = cat;
        const list = cat === 'all' ? attachmentList.value : attachmentList.value.filter(a => a.fileType === cat);
        if (list.length > 0) {
          activePreviewAtt.value = list[0];
        }
      };
      const selectPreviewAttachment = (att) => {
        activePreviewAtt.value = att;
      };
      const mockQuickUploadTelex = () => {
        if (ticketData.isLocked) return;
        const newAtt = {
          id: 'att-' + Date.now(),
          fileName: '电放保函_青岛万达_盖章版.pdf',
          fileType: 'other',
          fileSize: '620 KB',
          uploader: '李操作',
          uploadTime: window.dayjs().format('YYYY-MM-DD HH:mm'),
          docNoText: '电放保函 · ' + form.blNo,
          verifyNote: '客户签章与委托单位一致'
        };
        attachmentList.value.push(newAtt);
        activePreviewAtt.value = newAtt;
        if (!form.remark.includes('电放保函已收')) {
          appendQuickRemark('电放保函已收');
        } else {
          antd.message.success('已上传「电放保函_青岛万达_盖章版.pdf」并自动打开右侧同屏预览！');
        }
      };
      const syncVoucherToWorkbench = (att) => {
        if (!att || ticketData.isLocked) return;
        if (att.fileType === 'bl' || att.fileType === 'customs') {
          form.blNo = 'TEST-GH178-20261109';
          form.vesselName = 'COSCO PRIDE';
          form.voyage = '024E';
          form.pieces = 500;
          form.weight = 2500.00;
          form.volume = 15.5000;
          markDirty('basic');
          antd.message.success(`已将「${att.fileName}」票面提单号、船名航次与件毛体数据同步回填至左侧业务档案！`);
        } else if (att.fileType === 'invoice') {
          antd.message.success('发票金额 RMB 7.80 已与应付明细「码头操作费 (THC)」核对一致！');
        } else {
          appendQuickRemark('电放保函已核对归档');
        }
      };
      const downloadAllAttachments = () => {
        antd.message.success(`已打包下载本票全部 ${attachmentList.value.length} 份单证凭证 (TEST130-0022_单证包.zip)！`);
      };
      const addMockChangeOrder = () => {
        const newCo = {
          id: 'co-' + Date.now(),
          changeNo: 'CO-202611-00' + (changeOrderList.value.length + 1),
          createTime: window.dayjs().format('YYYY-MM-DD HH:mm'),
          applicant: form.salesPerson || '王经理',
          recDiff: '+200.00',
          payDiff: '+120.00',
          profitDiff: '+80.00',
          status: '待审批',
          reason: '目的港查验掏箱费补充调账'
        };
        changeOrderList.value.unshift(newCo);
        antd.message.success(`已新建更改单 ${newCo.changeNo}！`);
      };
      const enterMergeModeAndSwitchFee = () => {
        activeTabKey.value = 'fee';
        enterMergeMode();
      };
      const openAddOtherAttachmentType = () => {
        attachmentScenario.value = 'configured';
        attachmentCategoryFilter.value = 'other';
        antd.message.success('已启用「保函/装箱单/其他」扩展单证分类，可直接上传凭证！');
      };
      const handleFileUpload = (file) => {
        if (file.size > 10 * 1024 * 1024) {
          antd.message.error('单文件大小超过 10MB 限制！');
          return false;
        }
        const newAtt = {
          id: 'att-' + Date.now(),
          fileName: file.name,
          fileType: uploadTargetCategory.value || 'other',
          fileSize: (file.size / 1024).toFixed(1) + ' KB',
          uploader: '李操作',
          uploadTime: window.dayjs().format('YYYY-MM-DD HH:mm'),
          docNoText: '新上传单证 · ' + form.jobNo,
          verifyNote: '已通过同公司权限校验'
        };
        attachmentList.value.push(newAtt);
        activePreviewAtt.value = newAtt;
        antd.message.success(`文件 ${file.name} 上传成功并已在右侧打开预览！`);
        return false;
      };
      const previewAttachment = (att) => {
        activePreviewAtt.value = att;
        antd.message.info(`已在右侧预览窗切换显示: ${att.fileName}`);
      };
      const downloadAttachment = (att) => {
        antd.message.success(`已开始下载原件: ${att.fileName}`);
      };
      const deleteAttachment = (id) => {
        attachmentList.value = attachmentList.value.filter(a => a.id !== id);
        if (activePreviewAtt.value && activePreviewAtt.value.id === id) {
          activePreviewAtt.value = attachmentList.value[0] || null;
        }
        antd.message.success('附件凭证已移除。');
      };'''

assert att_methods_target in code, "att_methods_target not found"
code = code.replace(att_methods_target, att_methods_replacement, 1)

# 6. In applyScenario('standard'), keep attachmentScenario as 'configured' so clicking the tab shows the full cockpit immediately
code = code.replace('''          dirtyStates.payCount = 0;
          attachmentScenario.value = 'empty_no_config';
          antd.message.success('已切换至「1. 标准待补全态 (TEST130-0022)」');''', '''          dirtyStates.payCount = 0;
          attachmentScenario.value = 'configured';
          antd.message.success('已切换至「1. 标准待补全态 (TEST130-0022)」');''')

# 7. Export new attachment & changeOrder properties in setup() return object
return_att_target = '''        attachmentScenario,
        attachmentCategoryFilter,
        attachmentList,
        attachmentColumns,
        filteredAttachments,'''

return_att_replacement = '''        attachmentScenario,
        attachmentCategoryFilter,
        uploadTargetCategory,
        attachmentList,
        activePreviewAtt,
        attachmentColumns,
        filteredAttachments,
        getCategoryCount,
        getCategoryLabel,
        getCategoryTagColor,
        selectAttachmentCategory,
        selectPreviewAttachment,
        mockQuickUploadTelex,
        syncVoucherToWorkbench,
        downloadAllAttachments,
        addMockChangeOrder,
        enterMergeModeAndSwitchFee,'''

assert return_att_target in code, "return_att_target not found"
code = code.replace(return_att_target, return_att_replacement, 1)

with open('scratch/build_right_tabbed_workbench.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully upgraded TAB 3 (Attachment Cockpit) and TAB 2 (Change Order Table)!")
