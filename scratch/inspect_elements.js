const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  page.on('console', msg => console.log('LOG:', msg.text()));
  page.on('pageerror', err => console.error('ERR:', err));

  const pagePath = 'file://' + path.resolve(__dirname, '../pages/comprehensive-business-edit.html');
  await page.goto(pagePath, { waitUntil: 'load' });
  await page.waitForTimeout(500);

  const compoundGroups = await page.$$eval('.compound-input-group', els => {
    return els.map((el, idx) => {
      return {
        idx,
        innerHTML: el.innerHTML,
        childrenCount: el.children.length,
        childTagNames: Array.from(el.children).map(c => c.tagName + '.' + c.className + ' (w=' + c.offsetWidth + ', h=' + c.offsetHeight + ', disp=' + window.getComputedStyle(c).display + ')')
      };
    });
  });

  console.log(JSON.stringify(compoundGroups, null, 2));

  await browser.close();
})();
