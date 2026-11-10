with open('scratch/build_right_tabbed_workbench.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix 1: Prevent filename and "预览中" badge from wrapping in .att-native-table
old_filename_cell = '''                          <div style="min-width: 0;">
                            <div style="font-weight: 600; color: #0f172a; display: flex; align-items: center; gap: 5px;">
                              <span>{{ att.fileName }}</span>
                              <span v-if="activePreviewAtt && activePreviewAtt.id === att.id" style="font-size: 9px; background: #dbeafe; color: #1d4ed8; padding: 0 4px; border-radius: 2px; font-weight: 700;">
                                预览中
                              </span>
                            </div>
                            <div style="font-size: 10px; color: #64748b;">
                              {{ att.docNoText || '单证编号: TEST-GH178-20261109' }}
                            </div>
                          </div>'''

new_filename_cell = '''                          <div style="min-width: 0; flex: 1;">
                            <div style="font-weight: 600; color: #0f172a; display: flex; align-items: center; gap: 5px; white-space: nowrap;">
                              <span style="overflow: hidden; text-overflow: ellipsis;">{{ att.fileName }}</span>
                              <span v-if="activePreviewAtt && activePreviewAtt.id === att.id" style="font-size: 9px; background: #dbeafe; color: #1d4ed8; padding: 0 5px; line-height: 16px; border-radius: 2px; font-weight: 700; white-space: nowrap; flex-shrink: 0;">
                                预览中
                              </span>
                            </div>
                            <div style="font-size: 10px; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                              {{ att.docNoText || '单证编号: TEST-GH178-20261109' }}
                            </div>
                          </div>'''

assert old_filename_cell in code, "old_filename_cell not found"
code = code.replace(old_filename_cell, new_filename_cell, 1)

# Fix 2: Move .voucher-stamp to bottom-right seal area so it never overlaps header/B/L No.,
# and add a structured "OCR 票面提取与系统底账逐项核对清单" card inside .inspector-paper-scroll below .voucher-sheet!
old_stamp_css = '''    .voucher-stamp {
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
    }'''

new_stamp_css = '''    .inspector-paper-scroll {
      flex: 1;
      background: #334155;
      padding: 10px 12px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
    }
    .voucher-stamp {
      position: absolute;
      right: 14px;
      bottom: 10px;
      border: 1.5px solid #dc2626;
      color: #dc2626;
      font-size: 10px;
      font-weight: 800;
      padding: 1px 6px;
      border-radius: 3px;
      transform: rotate(-6deg);
      background: rgba(254, 242, 242, 0.92);
      letter-spacing: 0.5px;
      pointer-events: none;
    }
    .ocr-verify-card {
      width: 100%;
      max-width: 460px;
      background: #1e293b;
      border: 1px solid #475569;
      border-radius: 4px;
      padding: 8px 10px;
      color: #e2e8f0;
      font-size: 10px;
    }
    .ocr-verify-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 5px 8px;
      margin-top: 6px;
    }
    .ocr-field-row {
      background: rgba(15, 23, 42, 0.55);
      border: 1px solid #334155;
      border-radius: 3px;
      padding: 3px 6px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 4px;
    }'''

# Also remove the first .inspector-paper-scroll definition so there's only one clean definition
code = code.replace('''    .inspector-paper-scroll {
      flex: 1;
      background: #475569;
      padding: 12px;
      overflow-y: auto;
      display: flex;
      justify-content: center;
      align-items: flex-start;
    }
''' + old_stamp_css, new_stamp_css, 1)

# Add OCR field-by-field comparison card right after the 4 voucher-sheet templates inside .inspector-paper-scroll
target_paper_end = '''                  </table>
                </div>
              </div>

              <!-- 底部智能比对与一键同步栏 -->'''

replacement_paper_end = '''                  </table>
                </div>

                <!-- 票面关键字段智能提取与底账比对矩阵 (消除下方暗色空白，提供直观字段核对价值) -->
                <div class="ocr-verify-card" v-if="activePreviewAtt">
                  <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #334155; padding-bottom: 4px;">
                    <span style="font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 4px;">
                      <iconify-icon icon="ant-design:scan-outlined"></iconify-icon>
                      票面关键字段提取 vs 当前工作台底账比对
                    </span>
                    <span style="color: #4ade80; font-weight: 600;">✓ 4/4 字段完全一致</span>
                  </div>
                  <div class="ocr-verify-grid" v-if="activePreviewAtt.fileType !== 'invoice'">
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">提单号:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #f8fafc;">{{ form.blNo }}</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">船名/航次:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #f8fafc;">{{ form.vesselName }}/{{ form.voyage }}</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">起运/目的港:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #f8fafc;">{{ form.pol }}→{{ form.pod }}</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">件毛体:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #f8fafc;">{{ form.pieces }}件/{{ form.volume }}CBM</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                  </div>
                  <div class="ocr-verify-grid" v-else>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">匹配费用项:</span>
                      <span style="font-weight: 600; color: #f8fafc;">码头操作费 (THC)</span>
                      <span style="color: #4ade80;">✓应付表</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">销方结算对象:</span>
                      <span style="font-weight: 600; color: #f8fafc;">青岛中远海运</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">发票价税合计:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #fbbf24;">RMB 7.80</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                    <div class="ocr-field-row">
                      <span style="color: #94a3b8;">税率 / 不含税:</span>
                      <span style="font-family: monospace; font-weight: 600; color: #f8fafc;">6% / RMB 7.36</span>
                      <span style="color: #4ade80;">✓一致</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 底部智能比对与一键同步栏 -->'''

assert target_paper_end in code, "target_paper_end not found"
code = code.replace(target_paper_end, replacement_paper_end, 1)

# Fix 3: Add class="floating-spec-btn" to the top scenario-toolbar button and hide the fixed bottom-right floating button so it NEVER overlaps any footer button!
code = code.replace('''      <a-button size="small" type="link" @click="showSpecDrawer = true">
        <iconify-icon icon="ant-design:file-text-outlined"></iconify-icon> 规范交接与核对报告
      </a-button>''', '''      <a-button size="small" type="primary" ghost class="floating-spec-btn" style="position: static; box-shadow: none; height: 22px; font-size: 11px; padding: 0 8px; border-color: #38bdf8; color: #38bdf8;" @click="showSpecDrawer = true">
        <iconify-icon icon="ant-design:book-outlined"></iconify-icon> 设计交接规范
      </a-button>''')

code = code.replace('''  <!-- 浮动查看规范按钮 -->
  <a-button type="primary" shape="round" class="floating-spec-btn" @click="showSpecDrawer = true">
    <iconify-icon icon="ant-design:book-outlined"></iconify-icon> 设计交接规范
  </a-button>''', '''  <!-- 规范按钮已融合至顶部沙盘栏右侧 (.floating-spec-btn)，零遮挡底栏操作 -->''')

with open('scratch/build_right_tabbed_workbench.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Polished attachment table nowrap, stamp placement, OCR matrix, and removed floating button overlap!")
