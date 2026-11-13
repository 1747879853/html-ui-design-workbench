const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  try {
    console.log('Navigating to login page...');
    await page.goto('https://admin.jiayuebest.com', { waitUntil: 'networkidle', timeout: 15000 });
    await page.screenshot({ path: '/Users/blank/.gemini/antigravity/brain/dd5d25fe-e69a-4e4e-91aa-dccec9f9666f/real_login.png' });
    console.log('Saved real_login.png');

    // Fill login
    const userInputs = await page.$$('input');
    console.log('Found inputs:', userInputs.length);
    for (let i = 0; i < userInputs.length; i++) {
      const type = await userInputs[i].getAttribute('type');
      const placeholder = await userInputs[i].getAttribute('placeholder');
      console.log(`Input ${i}: type=${type}, placeholder=${placeholder}`);
    }

    // Attempt login
    await page.fill('input[type="text"], input:not([type="password"])', 'admin');
    await page.fill('input[type="password"]', 'jiayue+5159');
    
    // Click submit
    const submitBtn = await page.$('button[type="submit"], button.ant-btn-primary, .login-button, button:has-text("登录")');
    if (submitBtn) {
      await submitBtn.click();
      console.log('Clicked login button');
      await page.waitForTimeout(3000);
      await page.screenshot({ path: '/Users/blank/.gemini/antigravity/brain/dd5d25fe-e69a-4e4e-91aa-dccec9f9666f/real_home.png' });
      console.log('Saved real_home.png');
      console.log('Current URL:', page.url());
    }
  } catch (err) {
    console.error('Error during inspection:', err.message);
  } finally {
    await browser.close();
  }
})();
