# coding: utf-8
import os

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    orig_text = f.read()

idx_drawers = orig_text.find('<!-- ====================================================================\n             弹窗 1：添加费用抽屉')
idx_script = orig_text.find('<script>')

modals_block = orig_text[idx_drawers:idx_script]
script_block = orig_text[idx_script:]

# Write script to generate all 10
gen_script = """# coding: utf-8
import os

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    orig_text = f.read()

idx_drawers = orig_text.find('<!-- ====================================================================\\n             弹窗 1：添加费用抽屉')
idx_script = orig_text.find('<script>')

modals_block = orig_text[idx_drawers:idx_script]
script_block = orig_text[idx_script:]

def wrap_html(title, dir_tag, extra_css, body_html, extra_script=""):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="../assets/vendor/reset.css">
  <link rel="stylesheet" href="../assets/css/common.css">
  <script src="../assets/vendor/dayjs-bundle.min.js"></script>
  <script src="../assets/vendor/vue.global.prod.js"></script>
  <script src="../assets/vendor/antd.min.js"></script>
  <script src="../assets/vendor/iconify-icon.min.js"></script>
  <script src="../assets/js/common.js"></script>
  <style>
    [v-cloak] {{ display: none !important; }}
    body {{
      background-color: #f1f5f9;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
      margin: 0; padding: 0; font-size: 12px; overflow-x: hidden;
    }}
    .tabular-nums {{ font-variant-numeric: tabular-nums; font-feature-settings: "tnum"; }}
    .wb-scenario-bar {{
      display: flex; align-items: center; justify-content: space-between; gap: 8px;
      background: #0f172a; color: #f8fafc; border-radius: 4px; padding: 3px 10px; flex-shrink: 0;
    }}
    .wb-scenario-left, .wb-scenario-right {{ display: flex; align-items: center; gap: 6px; }}
    .wb-scenario-title {{ font-size: 11px; font-weight: 600; color: #38bdf8; display: inline-flex; align-items: center; gap: 4px; }}
    .wb-scenario-pill {{
      display: inline-flex; align-items: center; gap: 4px; padding: 1px 7px; border-radius: 3px;
      font-size: 11px; cursor: pointer; background: rgba(255, 255, 255, 0.08); color: #cbd5e1;
      border: 1px solid rgba(255, 255, 255, 0.12); transition: all 0.15s ease; user-select: none;
    }}
    .wb-scenario-pill:hover {{ background: rgba(255, 255, 255, 0.15); color: #fff; }}
    .wb-scenario-pill.active {{ background: #2563eb; color: #ffffff; border-color: #3b82f6; font-weight: 600; }}
    .dir-badge-pill {{
      background: #3b82f6; color: #fff; font-size: 10px; padding: 1px 6px; border-radius: 3px; font-weight: 600;
    }}
    .pa-status-tag {{ display: inline-flex; align-items: center; gap: 3px; padding: 1px 6px; border-radius: 3px; font-size: 11px; font-weight: 600; }}
    .pa-status-0 {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}
    .pa-status-1 {{ background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }}
    .pa-status-2 {{ background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }}
    .pa-status-3 {{ background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }}
    .pa-status-4 {{ background: #ecfeff; color: #0e7490; border: 1px solid #a5f3fc; }}
    .pa-status-5 {{ background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; }}
    .pa-link {{ color: #2563eb; font-weight: 600; cursor: pointer; text-decoration: none; }}
    .pa-link:hover {{ text-decoration: underline; }}
    .pa-copy-icon {{ color: #94a3b8; cursor: pointer; margin-left: 3px; font-size: 11px; }}
    .pa-copy-icon:hover {{ color: #2563eb; }}
    .pa-dir-badge {{ display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 2px; font-size: 10px; font-weight: 700; }}
    .pa-dir-pay {{ background: #fff7ed; color: #ea580c; border: 1px solid #fdba74; }}
    .pa-dir-rec {{ background: #eff6ff; color: #2563eb; border: 1px solid #93c5fd; }}
    {extra_css}
  </style>
</head>
<body>
  <div id="app" v-cloak>
    <div class="dir-container">
      <!-- 场景沙盒栏 -->
      <div class="wb-scenario-bar">
        <div class="wb-scenario-left">
          <span class="wb-scenario-title">业务沙盒:</span>
          <div
            v-for="s in scenarioList"
            :key="s.key"
            class="wb-scenario-pill"
            :class="{{ active: currentScenarioKey === s.key }}"
            @click="switchScenario(s.key)"
          >
            <span>{{{{ s.label }}}}</span>
          </div>
        </div>
        <div class="wb-scenario-right">
          <span class="dir-badge-pill">{dir_tag}</span>
          <a-button size="small" type="primary" ghost style="font-size: 10px; height: 20px; padding: 0 6px;" @click="showAddFeeDrawer = true">
            + 选费测试
          </a-button>
          <a-button size="small" type="primary" style="font-size: 10px; height: 20px; padding: 0 6px;" @click="showHandoffDrawer = true">
            交接文档
          </a-button>
        </div>
      </div>

      {body_html}

    </div>
    {modals_block}
    {script_block}
  </div>
</body>
</html>'''

print("Generator script template ready.")
"""

with open('scratch/builder_core.py', 'w', encoding='utf-8') as f:
    f.write(gen_script)

print("builder_core.py created.")
