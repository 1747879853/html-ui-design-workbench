const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1
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

  const pagePath = 'file://' + path.resolve(__dirname, '../pages/receive-settlement-add.html');
  console.log('Opening:', pagePath);
  await page.goto(pagePath, { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  const outDir = path.resolve(__dirname, '../scratch');
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  // 1. Capture Main Page (Scenario 1)
  console.log('Capturing 01_main_page...');
  await page.screenshot({ path: path.join(outDir, '01_receive_settlement_add_main.png') });

  // 2. Switch to Scenario 2 (WF346 foreign draft)
  console.log('Switching to Scenario 2...');
  await page.click('label:has-text("场景 2")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '02_scenario2_foreign_draft.png') });

  // 3. Switch to Scenario 4 (Over-limit alert)
  console.log('Switching to Scenario 4...');
  await page.click('label:has-text("场景 4")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '03_scenario4_over_limit.png') });

  // 4. Open Fee Drawer (Scenario 5)
  console.log('Switching to Scenario 5 (Auto allocation & fee drawer)...');
  await page.click('label:has-text("场景 5")');
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(outDir, '04_fee_drawer.png') });

  // 5. Trigger Auto Allocation confirmation modal
  console.log('Triggering auto allocation modal...');
  await page.click('button:has-text("自动核销确认")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '05_auto_confirm_modal.png') });

  await browser.close();

  console.log('Verification finished with', consoleErrors.length, 'console errors.');
  if (consoleErrors.length > 0) {
    process.exit(1);
  }
})();
