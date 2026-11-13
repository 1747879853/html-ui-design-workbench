const { chromium } = require('playwright');
const path = require('path');
const outDir = '/Users/blank/.gemini/antigravity/brain/dd5d25fe-e69a-4e4e-91aa-dccec9f9666f/scratch';

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', err => consoleErrors.push(String(err)));

  const url = 'file:///Users/blank/Documents/antigravity/intelligent-hopper/pages/payment-application-edit.html';
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(600);

  console.log('Console Errors:', consoleErrors.length);
  if (consoleErrors.length > 0) console.log(consoleErrors);

  // 1. S1 with Invoice Tab active by default
  await page.screenshot({ path: path.join(outDir, 'quiet_01_S1_invoice.png') });
  console.log('Captured quiet_01_S1_invoice.png');

  // 2. Click 不开票
  await page.click('.ant-radio-wrapper:has-text("不开票")');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(outDir, 'quiet_02_S1_no_invoice.png') });
  console.log('Captured quiet_02_S1_no_invoice.png');

  // 3. Switch to Tab 凭证与单据附件
  await page.click('.ant-radio-button-wrapper:has-text("凭证与单据附件")');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(outDir, 'quiet_03_attachments.png') });
  console.log('Captured quiet_03_attachments.png');

  // 4. Switch to Tab 审批流与审核记录
  await page.click('.ant-radio-button-wrapper:has-text("审批流与审核记录")');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(outDir, 'quiet_04_workflow.png') });
  console.log('Captured quiet_04_workflow.png');

  // 5. Switch to Scenario S3 (Rejected)
  await page.click('.wb-scenario-pill:has-text("S3")');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(outDir, 'quiet_05_S3_rejected.png') });
  console.log('Captured quiet_05_S3_rejected.png');

  // 6. Check index.html workbench
  await page.goto('file:///Users/blank/Documents/antigravity/intelligent-hopper/index.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(outDir, 'quiet_06_workbench.png') });
  console.log('Captured quiet_06_workbench.png');

  await browser.close();
  console.log('All quiet verification captures succeeded!');
})();
