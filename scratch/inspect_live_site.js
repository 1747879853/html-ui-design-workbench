const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const artifactDir = '/Users/blank/Documents/antigravity/intelligent-hopper/scratch/live_captures';
  if (!fs.existsSync(artifactDir)) {
    fs.mkdirSync(artifactDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1
  });
  const page = await context.newPage();

  page.on('console', msg => {
    console.log('[Browser Console]:', msg.type(), msg.text());
  });

  console.log('Navigating to http://43.138.14.122:188 ...');
  await page.goto('http://43.138.14.122:188', { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(artifactDir, '00_login_page.png') });

  // Fill in login
  console.log('Logging in with admin / jiayue+5159 ...');
  const userInputs = await page.locator('input').all();
  console.log(`Found ${userInputs.length} inputs on page`);
  
  // Usually login forms have username and password
  const usernameInput = page.locator('input[type="text"], input[placeholder*="账号"], input[placeholder*="用户"], input[id*="user"]').first();
  const passwordInput = page.locator('input[type="password"]').first();
  const submitBtn = page.locator('button[type="submit"], button:has-text("登 录"), button:has-text("登录")').first();

  await usernameInput.fill('admin');
  await passwordInput.fill('jiayue+5159');
  await page.screenshot({ path: path.join(artifactDir, '01_login_filled.png') });
  await submitBtn.click();

  console.log('Waiting for login redirect...');
  await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 15000 }).catch(e => console.log('Navigation timeout or already redirected:', e.message));
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(artifactDir, '02_after_login.png') });
  console.log('Current URL after login:', page.url());

  // Search or navigate to bank statement
  console.log('Navigating to bank statement page...');
  await page.goto('http://43.138.14.122:188/#/bank-statement', { waitUntil: 'networkidle' }).catch(e => {});
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(artifactDir, '03_bank_statement_list.png') });

  // Try to find SH261022020 in the table or search
  const searchInput = page.locator('input[placeholder*="流水号"], input[placeholder*="搜索"], input[placeholder*="编号"]').first();
  if (await searchInput.isVisible()) {
    await searchInput.fill('SH261022020');
    const searchBtn = page.locator('button:has-text("查询"), button:has-text("搜索")').first();
    if (await searchBtn.isVisible()) {
      await searchBtn.click();
      await page.waitForTimeout(1500);
      await page.screenshot({ path: path.join(artifactDir, '04_bank_statement_search.png') });
    }
  }

  // Look for row with SH261022020
  const row = page.locator('tr:has-text("SH261022020")').first();
  if (await row.isVisible()) {
    console.log('Found SH261022020 row!');
    // Look for edit link or double click row
    const editBtn = row.locator('button:has-text("编辑"), a:has-text("编辑")').first();
    if (await editBtn.isVisible()) {
      await editBtn.click();
    } else {
      await row.dblclick();
    }
    await page.waitForTimeout(2500);
    console.log('Current URL after opening edit:', page.url());
    await page.screenshot({ path: path.join(artifactDir, '05_bank_statement_edit.png') });
  }

  await browser.close();
  console.log('Done!');
})();
