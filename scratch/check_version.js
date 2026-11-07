const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(__dirname, '../pages/bank-statement-edit.html'), { waitUntil: 'load' });
  const version = await page.evaluate(() => window.antd ? window.antd.version : 'none');
  console.log('antd version in browser:', version);
  await browser.close();
})();
