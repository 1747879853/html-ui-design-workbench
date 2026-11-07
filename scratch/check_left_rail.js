const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve('pages/bank-statement-edit.html'), { waitUntil: 'networkidle' });

  const metrics = await page.evaluate(() => {
    const rail = document.querySelector('.studio-left-rail');
    const cards = Array.from(rail.querySelectorAll('.rail-card')).map(c => ({
      title: c.querySelector('.rail-card-title')?.innerText?.trim(),
      clientHeight: c.clientHeight,
      scrollHeight: c.scrollHeight
    }));
    return {
      railClientHeight: rail.clientHeight,
      railScrollHeight: rail.scrollHeight,
      cards
    };
  });

  console.log('Left Rail Metrics:', JSON.stringify(metrics, null, 2));

  const railElem = await page.locator('.studio-left-rail');
  await railElem.screenshot({ path: 'scratch/left_rail.png' });

  await browser.close();
})();
