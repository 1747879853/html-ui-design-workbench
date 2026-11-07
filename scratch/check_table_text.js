const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  page.on('console', msg => console.log('[Console]:', msg.type(), msg.text()));

  await page.goto('file://' + path.resolve(__dirname, '../pages/bank-statement-edit.html'), { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  const colDebug = await page.evaluate(() => {
    // Check what is in the table headers or cells
    const cells = Array.from(document.querySelectorAll('.ant-table-cell')).map(c => c.innerText);
    return cells;
  });
  console.log('Cells:\n', colDebug);

  await browser.close();
})();
