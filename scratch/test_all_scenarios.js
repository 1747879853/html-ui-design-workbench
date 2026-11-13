const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  await page.goto('file://' + path.resolve('pages/payment-application-edit.html'), { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);

  const scenarios = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'];
  for (const s of scenarios) {
    const btn = await page.locator(`text=${s}`).first();
    if (await btn.count() > 0) {
      await btn.click();
      await page.waitForTimeout(600);
      await page.screenshot({ path: `/Users/blank/.gemini/antigravity/brain/dd5d25fe-e69a-4e4e-91aa-dccec9f9666f/screen_${s.toLowerCase()}.png` });
      console.log(`Saved screen_${s.toLowerCase()}.png`);
    }
  }

  await browser.close();
})();
