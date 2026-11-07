const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const artifactDir = '/Users/blank/Documents/antigravity/intelligent-hopper/scratch/live_captures';

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1
  });
  const page = await context.newPage();

  await page.goto('http://43.138.14.122:188', { waitUntil: 'networkidle' });

  // Fill in login
  const usernameInput = page.locator('input[type="text"]').first();
  const passwordInput = page.locator('input[type="password"]').first();
  await usernameInput.fill('admin');
  await passwordInput.fill('jiayue+5159');

  // Find slider handle
  console.log('Finding slider handle...');
  const slider = page.locator('div:has-text("请按住滑块拖动"), .vben-slider-captcha, [class*="slider"]').last();
  const handle = page.locator('div:has-text(">>"), [class*="slider-button"], [class*="drag-bar"], [class*="handle"]').first();
  
  const handleBox = await handle.boundingBox();
  console.log('Handle box:', handleBox);
  
  if (handleBox) {
    await page.mouse.move(handleBox.x + handleBox.width / 2, handleBox.y + handleBox.height / 2);
    await page.mouse.down();
    await page.mouse.move(handleBox.x + handleBox.width / 2 + 300, handleBox.y + handleBox.height / 2, { steps: 20 });
    await page.mouse.up();
    await page.waitForTimeout(1000);
  }

  await page.screenshot({ path: path.join(artifactDir, '01_slider_done.png') });

  const submitBtn = page.locator('button:has-text("立即登录"), button:has-text("登录")').first();
  await submitBtn.click();

  console.log('Waiting for login...');
  await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 10000 }).catch(e => console.log(e.message));
  await page.waitForTimeout(2000);
  console.log('Current URL:', page.url());
  await page.screenshot({ path: path.join(artifactDir, '02_logged_in.png') });

  await browser.close();
})();
