const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  const page = await context.newPage();

  const pagePath = 'file://' + path.resolve(__dirname, '../pages/comprehensive-business-edit.html');
  await page.goto(pagePath, { waitUntil: 'load' });
  await page.waitForTimeout(600);

  const panel = await page.$('.left-business-panel');
  if (panel) {
    await panel.screenshot({ path: '/Users/blank/.gemini/antigravity/brain/8060e0f8-232b-480b-ac03-ce82456e507a/left_panel_redesigned.png' });
    console.log('Saved left_panel_redesigned.png');
  }

  await page.screenshot({ path: '/Users/blank/.gemini/antigravity/brain/8060e0f8-232b-480b-ac03-ce82456e507a/01_standard_workbench.png' });
  console.log('Saved 01_standard_workbench.png');

  await browser.close();
})();
