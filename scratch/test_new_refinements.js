const { chromium } = require('playwright');
const path = require('path');

const outDir = '/Users/blank/.gemini/antigravity/brain/dd5d25fe-e69a-4e4e-91aa-dccec9f9666f/scratch';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', err => consoleErrors.push(String(err)));

  const url = 'file:///Users/blank/Documents/antigravity/intelligent-hopper/pages/payment-application-edit.html';
  console.log('Navigating to:', url);
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(600);

  console.log('Refined Layout Console Errors (S1):', consoleErrors.length);
  if (consoleErrors.length > 0) console.log(consoleErrors);

  await page.screenshot({ path: path.join(outDir, 'refined_perfect_01_S1.png') });
  console.log('Captured refined_perfect_01_S1.png');

  // Test S1 switching to 不开票
  await page.click('label:has-text("不开票")');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(outDir, 'refined_perfect_01_S1_no_invoice.png') });
  console.log('Captured refined_perfect_01_S1_no_invoice.png');

  // Also check workbench index.html
  await page.goto('file:///Users/blank/Documents/antigravity/intelligent-hopper/index.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(outDir, 'refined_perfect_02_workbench.png') });
  console.log('Captured refined_perfect_02_workbench.png');

  await browser.close();
  console.log('Done test_new_refinements!');
})();
