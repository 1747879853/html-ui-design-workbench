import re

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update pa-acc-card CSS to solid border
html = re.sub(
    r'\.pa-acc-card\s*\{[^}]+\}',
    '''.pa-acc-card {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 4px;
      height: 24px;
      padding: 0 8px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      font-size: 11px;
      color: #1e293b;
      box-shadow: inset 0 1px 1px rgba(0,0,0,0.02);
    }''',
    html
)

# 2. Add Telemetry Banner CSS and tree guideline CSS
css_addon = '''
    /* 树状层级引导线 */
    .pa-inner-box {
      background: #f8fafc;
      padding: 6px 12px 8px 36px;
      border-bottom: 2px solid #cbd5e1;
      position: relative;
    }

    .pa-inner-box::before {
      content: "";
      position: absolute;
      left: 18px;
      top: 0;
      bottom: 12px;
      width: 2px;
      border-left: 2px dashed #93c5fd;
    }

    .pa-inner-box::after {
      content: "";
      position: absolute;
      left: 18px;
      top: 14px;
      width: 14px;
      height: 2px;
      border-top: 2px dashed #93c5fd;
    }

    /* 金融底账与风控透视条 (消除纯白空洞 · 充实货代金融决策上下文) */
    .pa-telemetry-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      padding: 8px 12px;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      flex-shrink: 0;
    }

    .pa-telem-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 6px 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .pa-telem-icon {
      width: 28px;
      height: 28px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      flex-shrink: 0;
    }

    .pa-telem-info {
      flex: 1;
      min-width: 0;
    }

    .pa-telem-label {
      font-size: 10px;
      color: #64748b;
      line-height: 1.2;
    }

    .pa-telem-val {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 4px;
      margin-top: 2px;
    }

    .pa-telem-val strong {
      font-size: 12px;
      color: #0f172a;
    }

    .pa-telem-sub {
      font-size: 10px;
      color: #94a3b8;
      white-space: nowrap;
    }

    /* 不开票合规卡片 */
    .pa-no-invoice-box {
      margin: 12px;
      padding: 12px 16px;
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      border-radius: 6px;
      display: flex;
      align-items: flex-start;
      gap: 12px;
    }

    .pa-no-inv-icon {
      width: 32px;
      height: 32px;
      border-radius: 6px;
      background: #dcfce7;
      color: #16a34a;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      flex-shrink: 0;
    }

    .pa-no-inv-content {
      flex: 1;
    }

    .pa-no-inv-title {
      font-size: 12px;
      font-weight: 600;
      color: #166534;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .pa-no-inv-desc {
      font-size: 11px;
      color: #15803d;
      margin-top: 4px;
      line-height: 1.5;
    }

    .pa-no-inv-actions {
      margin-top: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
      padding-top: 6px;
      border-top: 1px dashed #bbf7d0;
    }
'''

# Replace old pa-inner-box rule
html = re.sub(
    r'\.pa-inner-box\s*\{[^}]+\}',
    '',
    html
)

# Insert css_addon before </style>
html = html.replace('</style>', css_addon + '\n  </style>')

with open('pages/payment-application-edit.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('CSS updated successfully')
