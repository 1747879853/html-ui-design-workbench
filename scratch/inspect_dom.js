const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('http://43.138.14.122:188/#/auth/login', { waitUntil: 'networkidle' });

  const elements = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('*')).filter(el => {
      const text = el.innerText || '';
      return text.includes('滑块') || text.includes('>>');
    }).map(el => ({
      tagName: el.tagName,
      className: el.className,
      rect: el.getBoundingClientRect()
    }));
  });

  console.log('Slider elements:', JSON.stringify(elements, null, 2));
  await browser.close();
})();
