const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  const pagePath = 'file://' + path.resolve(__dirname, '../pages/comprehensive-business-edit.html');
  await page.goto(pagePath, { waitUntil: 'load' });
  await page.waitForTimeout(500);

  const fields = await page.evaluate(() => {
    const getVal = sel => {
      const el = document.querySelector(sel);
      return el ? (el.value || el.innerText) : 'NOT FOUND';
    };

    return {
      vessel: getVal('input[placeholder="船名 (Vessel)"]'),
      voyage: getVal('input[placeholder="航次 (Voyage)"]'),
      pieces: getVal('input[placeholder="数量"]'),
      weight: getVal('input[placeholder="毛重"]'),
      volume: getVal('input[placeholder="体积"]')
    };
  });

  console.log('Inspected fields:', JSON.stringify(fields, null, 2));

  // Let's capture a focused screenshot of the left business panel
  const panel = await page.$('.left-business-panel');
  if (panel) {
    await panel.screenshot({ path: path.resolve(__dirname, 'left_panel_fixed.png') });
    console.log('Saved left_panel_fixed.png');
  }

  await browser.close();
})();
