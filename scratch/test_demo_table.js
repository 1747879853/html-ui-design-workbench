const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  page.on('console', msg => console.log('[BrowserConsole]:', msg.type(), msg.text()));
  await page.goto('file://' + path.resolve(__dirname, '../pages/demo-order-management.html'), { waitUntil: 'load' });
  const demoText = await page.evaluate(() => {
    return document.querySelector('table tbody tr td').innerText;
  });
  console.log('demo table first cell:', demoText);
  await browser.close();
})();
