const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 960 },
    deviceScaleFactor: 2
  });
  const page = await context.newPage();

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
      console.error('Browser Error:', msg.text());
    }
  });
  page.on('pageerror', err => {
    consoleErrors.push(err.message);
    console.error('Page Error:', err.message);
  });

  const pagePath = 'file://' + path.resolve(__dirname, 'pages/lock-account-period.html');
  console.log('Opening:', pagePath);
  await page.goto(pagePath, { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  const outDir = '/Users/blank/.gemini/antigravity/brain/b91b7a83-09fb-4606-be81-3d31ba2b5a53';

  // 1. Main Page Screenshot
  console.log('Capturing 01_main_page...');
  await page.screenshot({ path: path.join(outDir, '01_period_main_page.png') });

  // 2. Open Close Wizard Modal (Step 0)
  console.log('Opening close wizard modal (Step 0)...');
  await page.click('button:has-text("结转当期")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '02_close_wizard_step0.png') });

  // Step 1: 处理未锁账
  console.log('Going to Step 1...');
  await page.click('button:has-text("下一步：处理未锁账单据")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '03_close_wizard_step1.png') });

  // Step 2: 确认结转
  console.log('Going to Step 2...');
  await page.click('button:has-text("下一步：确认结转影响")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '04_close_wizard_step2.png') });

  // Close wizard modal by clicking close button
  console.log('Closing wizard modal...');
  await page.click('.ant-modal-close');
  await page.waitForTimeout(600);

  // 3. Open Reopen Modal
  console.log('Opening reopen modal...');
  await page.click('button:has-text("反结转")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '05_reopen_modal.png') });

  // Close reopen modal
  console.log('Closing reopen modal...');
  await page.click('.ant-modal-close');
  await page.waitForTimeout(600);

  // 4. Open Snapshot Drawer
  console.log('Opening snapshot drawer...');
  await page.click('button:has-text("查看结转快照")');
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(outDir, '06_snapshot_drawer.png') });

  // Close snapshot drawer
  console.log('Closing snapshot drawer...');
  await page.click('.ant-drawer-close');
  await page.waitForTimeout(600);

  // 5. Open Audit Drawer
  console.log('Opening audit checklist drawer...');
  await page.click('button:has-text("业务要素")');
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(outDir, '07_audit_drawer.png') });

  // Close audit drawer
  console.log('Closing audit drawer...');
  await page.click('.ant-drawer-close');
  await page.waitForTimeout(600);

  // 6. Test Company Switcher (Company without start period)
  console.log('Testing company switcher...');
  await page.click('.vben-search-card .ant-select-selector');
  await page.waitForTimeout(300);
  await page.click('div.ant-select-item-option-content:has-text("青岛黄岛分公司")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '08_unconfigured_company_state.png') });

  // 7. Workbench Index.html Preview (1920x1080 canvas simulator)
  console.log('Checking index.html workbench...');
  const indexPath = 'file://' + path.resolve(__dirname, 'index.html');
  await page.goto(indexPath, { waitUntil: 'load' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(outDir, '09_workbench_canvas_preview.png') });

  await browser.close();

  console.log('Console Errors count:', consoleErrors.length);
  if (consoleErrors.length > 0) {
    console.error('FAILED with console errors:', consoleErrors);
    process.exit(1);
  }
  console.log('SUCCESS! ALL 9 VERIFICATION STEPS PASSED WITH 0 CONSOLE ERRORS!');
})().catch(err => {
  console.error('Verification script failed:', err);
  process.exit(1);
});
