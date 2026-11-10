const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 2
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

  // 1. Capture high-res close-up of Left Panel (Top half: Card 01 & Card 02)
  await page.screenshot({
    path: path.join(outDir, 'dossier_closeup_top.png'),
    clip: { x: 0, y: 0, width: 440, height: 760 }
  });

  // 2. Scroll Left Panel to bottom and capture Card 03 & Card 04
  await page.evaluate(() => {
    const scroller = document.querySelector('.business-form-scroll');
    if (scroller) scroller.scrollTop = scroller.scrollHeight;
  });
  await page.waitForTimeout(300);
  await page.screenshot({
    path: path.join(outDir, 'dossier_closeup_bottom.png'),
    clip: { x: 0, y: 80, width: 440, height: 990 }
  });

  // 3. Test interactive actions:
  // Scroll back to top
  await page.evaluate(() => {
    const scroller = document.querySelector('.business-form-scroll');
    if (scroller) scroller.scrollTop = 0;
  });
  await page.waitForTimeout(200);

  // Click "+商务" quick role chip (leaving 3 roles = odd count -> tests dashed slot!)
  await page.click('.quick-role-chip:has-text("+商务")');
  await page.waitForTimeout(200);
  // Click "同步船期/港口" on Master Order stub
  await page.click('.stub-sync-btn');
  await page.waitForTimeout(200);
  // Click "互换港口" on Boarding Pass Route Selector
  await page.click('.port-swap-btn');
  await page.waitForTimeout(200);
  // Click "同步件重尺至费用" on Card 04
  await page.click('.card-action-link:has-text("同步件重尺至费用")');
  await page.waitForTimeout(300);

  // Hide transient toast to inspect clean UI state after interactions
  await page.addStyleTag({ content: '.ant-message { display: none !important; }' });
  await page.screenshot({
    path: path.join(outDir, 'dossier_after_interactions.png')
  });

  console.log('Console errors:', consoleErrors.length);
  if (consoleErrors.length > 0) {
    console.error(consoleErrors);
    process.exit(1);
  }
  await browser.close();
})();
