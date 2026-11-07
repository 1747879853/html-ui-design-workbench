const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  page.on('pageerror', err => errors.push(err.message));

  const filePath = 'file://' + path.resolve('pages/bank-statement-edit.html');
  await page.goto(filePath, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  console.log('Console/Page errors count:', errors.length);
  if (errors.length > 0) {
    console.log('Errors:', errors);
  }

  const hasSummaryBar = (await page.$('.settlement-currency-summary-bar')) !== null;
  console.log('Summary bar rendered:', hasSummaryBar);

  const hasTable = (await page.$('.settlement-table')) !== null;
  console.log('Settlement table rendered:', hasTable);

  const textSummary = await page.evaluate(() => {
    const el = document.querySelector('.settlement-currency-summary-bar');
    return el ? el.innerText : 'NOT FOUND';
  });
  console.log('Summary bar text:\n', textSummary);

  await page.screenshot({ path: 'scratch/current_test.png', fullPage: false });
  await browser.close();
})();
