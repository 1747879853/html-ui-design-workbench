# coding: utf-8
import os

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    orig_text = f.read()

idx_drawers = orig_text.find('<!-- ====================================================================\n             弹窗 1：添加费用抽屉')
idx_script = orig_text.find('<script>')

modals_block = orig_text[idx_drawers:idx_script]
script_block = orig_text[idx_script:]

# Ensure pages directory exists
os.makedirs('pages', exist_ok=True)

# Shared snippet for top action bar
def get_top_action_bar():
    return """
      <div class="pa-voucher-toolbar">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="color: #64748b;">申请单号:</span>
          <span class="pa-doc-code">{{ formState.applicationNo }}</span>
          <iconify-icon icon="ant-design:copy-outlined" class="pa-copy-icon" @click="copyText(formState.applicationNo, '申请单号')"></iconify-icon>

          <span class="pa-status-tag" :class="'pa-status-' + formState.status">
            <iconify-icon :icon="getStatusIcon(formState.status)"></iconify-icon>
            {{ currentStatusMeta.stampText }}
          </span>

          <span style="color: #cbd5e1;">|</span>
          <span style="color: #64748b;">申请人:</span>
          <strong style="color: #334155;">{{ formState.creatorUserName }}</strong>

          <template v-if="formState.submitTime">
            <span style="color: #64748b; margin-left: 4px;">提交:</span>
            <span class="tabular-nums" style="color: #64748b;">{{ formState.submitTime }}</span>
          </template>
        </div>

        <div style="display: flex; align-items: center; gap: 6px;">
          <a-button size="small" style="font-size: 11px;" @click="handleCreateBlank">新建空白</a-button>
          <a-button size="small" style="font-size: 11px;" :disabled="!isMainFormEditable" @click="handleSaveDraft">保存草稿</a-button>
          <a-button size="small" type="primary" style="font-size: 11px;" :disabled="!canSubmit" @click="handleSubmitAudit">
            {{ formState.status === 2 ? '重新送审' : '提交送审' }}
          </a-button>
          <a-dropdown>
            <template #overlay>
              <a-menu @click="handleExportAction">
                <a-menu-item key="excel">导出 Excel</a-menu-item>
                <a-menu-item key="pdf">导出 PDF</a-menu-item>
              </a-menu>
            </template>
            <a-button size="small" style="font-size: 11px;">
              导出 <iconify-icon icon="ant-design:down-outlined" style="font-size: 9px;"></iconify-icon>
            </a-button>
          </a-dropdown>
          <a-button size="small" style="font-size: 11px;" @click="handlePrintDoc">打印</a-button>
        </div>
      </div>
    """

def get_status_alert():
    return """
      <div v-if="formState.status === 2" class="pa-status-alert pa-alert-reject">
        <div style="display: flex; align-items: center; gap: 6px;">
          <iconify-icon icon="ant-design:close-circle-filled" style="color: #dc2626; font-size: 13px;"></iconify-icon>
          <strong>审批已驳回：</strong>
          <span>{{ (workflowNodes[1] || {}).comment || '请补充水单盖章件后重新提交。' }}</span>
          <span style="color: #64748b; margin-left: 8px;">(审核人: {{ (workflowNodes[1] || {}).operatorName }} · {{ (workflowNodes[1] || {}).operateTime }})</span>
        </div>
        <a-tag color="error" style="font-size: 10px; line-height: 16px; margin: 0;">需修改后重新送审</a-tag>
      </div>
    """

def wrap_page(title, dir_tag, extra_css, body_html, extra_script=""):
    # If extra_script needs to add ref or something, we can inject into setup()
    script = script_block
    if extra_script:
        idx_ret = script.rfind('return {')
        script = script[:idx_ret] + extra_script + "\n" + script[idx_ret:]
    
    return f"""<!DOCTYPE html>
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
      background-color: #f8fafc;
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
    .pa-status-alert {{
      padding: 4px 12px; border-radius: 4px; display: flex; align-items: center; justify-content: space-between; gap: 8px; font-size: 11px; flex-shrink: 0;
    }}
    .pa-alert-reject {{ background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; }}
    .pa-doc-code {{ font-family: ui-monospace, SFMono-Regular, monospace; font-size: 14px; font-weight: 700; color: #0f172a; }}
    .pa-voucher-toolbar {{ padding: 5px 12px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #f1f5f9; background: #ffffff; border-radius: 6px 6px 0 0; }}
    {extra_css}
  </style>
</head>
<body>
  <div id="app" v-cloak>
    <div style="height: 100vh; max-height: 1080px; padding: 6px 12px 10px; box-sizing: border-box; display: flex; flex-direction: column; gap: 6px; max-width: 1920px; margin: 0 auto; overflow: hidden;">
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
    {script}
  </div>
</body>
</html>"""

print("Generator helper defined.")
