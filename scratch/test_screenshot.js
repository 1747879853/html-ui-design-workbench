const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.message));

  await page.goto('file://' + path.resolve('pages/payment-application-edit.html'), { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  
  await page.screenshot({ path: '/Users/blank/.gemini/antigravity/brain/dd5d25fe-e69a-4e4e-91aa-dccec9f9666f/screen_s1_current.png', fullPage: false });
  console.log('Saved screen_s1_current.png');

  // Click S3 scenario
  const s3Btn = await page.locator('text=S3 已驳回').first();
  if (await s3Btn.count() > 0) {
    await s3Btn.click();
    await page.waitForTimeout(800);
    await page.screenshot({ path: '/Users/blank/.gemini/antigravity/brain/dd5d25fe-e69a-4e4e-91aa-dccec9f9666f/screen_s3_current.png', fullPage: false });
    console.log('Saved screen_s3_current.png');
  } else {
    console.log('S3 btn not found');
  }

  // Also full page screenshot
  await page.screenshot({ path: '/Users/blank/.gemini/antigravity/brain/dd5d25fe-e69a-4e4e-91aa-dccec9f9666f/screen_s3_full.png', fullPage: true });

  await browser.close();
})();
