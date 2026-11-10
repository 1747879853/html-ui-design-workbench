const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1.5
  });
  const page = await context.newPage();

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', err => consoleErrors.push(err.message));

  const outDir = '/Users/blank/.gemini/antigravity/brain/8060e0f8-232b-480b-ac03-ce82456e507a';
  const pagePath = 'file://' + path.resolve(__dirname, '../pages/comprehensive-business-edit.html');
  await page.goto(pagePath, { waitUntil: 'load' });
  await page.waitForTimeout(800);

  await page.addStyleTag({ content: '.ant-message { display: none !important; }' });

  // 1. Switch to Attachment Full Cockpit (Default BL Preview)
  await page.evaluate(() => window.__workbench.applyScenario('attach_full'));
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(outDir, '07_attachment_management.png') });

  // 2. Click on VAT Invoice row & also test quick upload telex LOI
  const rows = await page.$$('.att-native-table tbody tr.att-row-item');
  if (rows.length >= 3) {
    await rows[2].click();
    await page.waitForTimeout(300);
  }
  await page.screenshot({ path: path.join(outDir, '07b_attachment_invoice_preview.png') });

  // 3. Switch to Attachment Empty No-Config State (Figure 05 + 4-state diagnostic)
  await page.evaluate(() => window.__workbench.applyScenario('attach_empty'));
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(outDir, '06_attachment_no_config_empty.png') });

  // 4. Switch to Change Order Unlocked State
  await page.evaluate(() => window.__workbench.applyScenario('co_unlocked'));
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(outDir, '05_change_order_unlocked.png') });

  console.log('Console errors:', consoleErrors.length);
  if (consoleErrors.length > 0) {
    console.error(consoleErrors);
    process.exit(1);
  }
  await browser.close();
})();
