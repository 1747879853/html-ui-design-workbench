const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

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
      console.error('Console error:', msg.text());
    }
  });
  page.on('pageerror', err => {
    consoleErrors.push(err.message);
    console.error('Page error:', err.message);
  });

  const pagePath = 'file://' + path.resolve(__dirname, '../pages/receive-settlement-form.html');
  const outDir = '/Users/blank/.gemini/antigravity/brain/25f176a0-97e2-408d-925a-70f445b480fc';

  console.log('Opening receive-settlement-form.html...');
  await page.goto(pagePath, { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  // 1. Main Page Screenshot (Draft balanced state)
  console.log('Capturing 01_receive_settlement_main.png...');
  await page.screenshot({ path: path.join(outDir, '01_receive_settlement_main.png') });

  // 2. Switch to Foreign Currency mode
  console.log('Switching to foreign currency mode...');
  await page.locator('label.ant-radio-button-wrapper:has-text("美金外币换算")').click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '02_foreign_currency_mode.png') });

  // Reset back to draft
  await page.locator('label.ant-radio-button-wrapper:has-text("草稿未锁定")').click();
  await page.waitForTimeout(400);

  // 3. Open Add Fee Drawer
  console.log('Opening Add Fee Drawer...');
  await page.click('button:has-text("添加费用明细")');
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(outDir, '03_add_fee_drawer.png') });

  // Expand first candidate business order in drawer
  try {
    const expandBtn = page.locator('.ant-drawer .ant-table-row-expand-icon').first();
    if (await expandBtn.isVisible()) {
      await expandBtn.click();
      await page.waitForTimeout(600);
      await page.screenshot({ path: path.join(outDir, '04_add_fee_drawer_expanded.png') });
    }
  } catch (e) {}

  // Close drawer
  console.log('Closing drawer...');
  await page.click('.ant-drawer-close');
  await page.waitForTimeout(600);

  // 4. Open Bank Picker Modal
  console.log('Opening Bank Picker Modal...');
  await page.click('button:has-text("更换流水")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '05_bank_picker_modal.png') });

  // Close modal
  await page.keyboard.press('Escape');
  await page.waitForTimeout(600);

  // 5. Open Auto Allocation Wizard
  console.log('Opening Auto Alloc Wizard...');
  await page.click('button:has-text("自动核销分摊")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '06_auto_alloc_modal.png') });

  // Close modal
  await page.keyboard.press('Escape');
  await page.waitForTimeout(600);

  // 6. Switch to Locked State
  console.log('Switching to locked state...');
  await page.locator('label.ant-radio-button-wrapper:has-text("已锁定归档")').click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '07_locked_state.png') });

  // 7. Preview index.html workbench
  console.log('Testing index.html workbench preview...');
  const indexPath = 'file://' + path.resolve(__dirname, '../index.html');
  await page.goto(indexPath, { waitUntil: 'load' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(outDir, '08_index_workbench_preview.png') });

  console.log('Completed all captures!');
  console.log('Total console errors:', consoleErrors.length);
  if (consoleErrors.length > 0) {
    console.error('Console errors detected:', consoleErrors);
  }

  await browser.close();
})().catch(err => {
  console.error('Fatal execution error:', err);
  process.exit(1);
});
