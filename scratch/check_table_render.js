const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  page.on('console', msg => console.log('[Console]:', msg.type(), msg.text()));
  page.on('pageerror', err => console.log('[PageError]:', err.message));

  await page.goto('file://' + path.resolve(__dirname, '../pages/bank-statement-edit.html'), { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  const html = await page.locator('.wb-table-card').innerHTML();
  console.log('wb-table-card innerHTML:\n', html);

  await browser.close();
})();
