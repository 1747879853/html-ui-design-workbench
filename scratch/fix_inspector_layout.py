with open('scratch/build_right_tabbed_workbench.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix .inspector-paper-scroll to be flex-direction: column and add .ocr-verify-card styles
old_paper_css = '''    .inspector-paper-scroll {
      flex: 1;
      background: #475569;
      padding: 12px;
      overflow-y: auto;
      display: flex;
      justify-content: center;
      align-items: flex-start;
    }'''

new_paper_css = '''    .inspector-paper-scroll {
      flex: 1;
      background: #334155;
      padding: 12px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      gap: 10px;
    }
    .ocr-verify-card {
      width: 100%;
      max-width: 480px;
      background: #1e293b;
      border: 1px solid #475569;
      border-radius: 5px;
      padding: 9px 12px;
      color: #e2e8f0;
      font-size: 11px;
      box-shadow: 0 2px 8px rgba(15, 23, 42, 0.25);
    }
    .ocr-verify-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 6px 8px;
      margin-top: 7px;
    }
    .ocr-field-row {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid #334155;
      border-radius: 3px;
      padding: 4px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      font-size: 10px;
      white-space: nowrap;
    }'''

assert old_paper_css in code, "old_paper_css not found"
code = code.replace(old_paper_css, new_paper_css, 1)

# 2. Fix .voucher-sheet max-width and move .voucher-stamp to bottom-right so it never overlaps top header
old_sheet_and_stamp = '''    .voucher-sheet {
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
    }'''

new_sheet_and_stamp = '''    .voucher-sheet {
      width: 100%;
      max-width: 480px;
      background: #ffffff;
      border-radius: 4px;
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.35);
      padding: 12px 14px 14px 14px;
      font-size: 10px;
      color: #1e293b;
      position: relative;
      border: 1px solid #cbd5e1;
    }
    .voucher-stamp {
      position: absolute;
      right: 16px;
      bottom: 12px;
      border: 1.5px solid #dc2626;
      color: #dc2626;
      font-size: 10px;
      font-weight: 800;
      padding: 1px 7px;
      border-radius: 3px;
      transform: rotate(-6deg);
      background: rgba(254, 242, 242, 0.94);
      letter-spacing: 0.5px;
      pointer-events: none;
    }'''

assert old_sheet_and_stamp in code, "old_sheet_and_stamp not found"
code = code.replace(old_sheet_and_stamp, new_sheet_and_stamp, 1)

# 3. Fix .ocr-match-pill nowrap and table column widths so nothing wraps in .att-native-table
old_ocr_pill = '''    .ocr-match-pill {
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
    }'''

new_ocr_pill = '''    .ocr-match-pill {
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
      white-space: nowrap;
    }'''

assert old_ocr_pill in code, "old_ocr_pill not found"
code = code.replace(old_ocr_pill, new_ocr_pill, 1)

# Make 上传人 / 时间 compact single-line or clean, and 操作 column white-space: nowrap
old_thead = '''                    <tr>
                      <th style="width: 32px; text-align: center;">#</th>
                      <th>凭证文件名称 (点击行同屏预览)</th>
                      <th style="width: 96px;">所属分类</th>
                      <th style="width: 175px;">左栏/费用联动核对</th>
                      <th style="width: 68px; text-align: right;">大小</th>
                      <th style="width: 120px;">上传人 / 时间</th>
                      <th style="width: 138px; text-align: center;">操作</th>
                    </tr>'''

new_thead = '''                    <tr>
                      <th style="width: 28px; text-align: center;">#</th>
                      <th>凭证文件名称 (点击行同屏预览)</th>
                      <th style="width: 78px;">所属分类</th>
                      <th style="width: 162px;">左栏/费用联动核对</th>
                      <th style="width: 62px; text-align: right;">大小</th>
                      <th style="width: 108px;">上传人 / 时间</th>
                      <th style="width: 116px; text-align: center;">操作</th>
                    </tr>'''

assert old_thead in code, "old_thead not found"
code = code.replace(old_thead, new_thead, 1)

old_action_td = '''                      <td style="text-align: center;" @click.stop>'''
new_action_td = '''                      <td style="text-align: center; white-space: nowrap;" @click.stop>'''
assert old_action_td in code, "old_action_td not found"
code = code.replace(old_action_td, new_action_td, 1)

with open('scratch/build_right_tabbed_workbench.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed inspector column layout, stamp placement, and table nowrap!")
