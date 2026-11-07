const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const artifactDir = '/Users/blank/Documents/antigravity/intelligent-hopper/scratch/live_captures';
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  await page.goto('http://43.138.14.122:188/#/auth/login', { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  const usernameInput = page.locator('input[placeholder*="用户"], input[name="username"]').first();
  const passwordInput = page.locator('input[type="password"]').first();
  await usernameInput.fill('admin');
  await passwordInput.fill('jiayue+5159');

  const handle = page.locator('.cursor-move').first();
  const handleBox = await handle.boundingBox();
  const sliderBar = page.locator('div.border-border.bg-background-deep').first();
  const sliderBox = await sliderBar.boundingBox();
  const dragDistance = sliderBox.width - handleBox.width;

  await page.mouse.move(handleBox.x + handleBox.width / 2, handleBox.y + handleBox.height / 2);
  await page.mouse.down();
  await page.mouse.move(handleBox.x + handleBox.width / 2 + dragDistance + 10, handleBox.y + handleBox.height / 2, { steps: 25 });
  await page.mouse.up();
  await page.waitForTimeout(600);

  const submitBtn = page.locator('button:has-text("立即登录")').first();
  await submitBtn.click();
  await page.waitForTimeout(3000);

  const readBtn = page.locator('button:has-text("我已阅读")').first();
  if (await readBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
    await readBtn.click();
    await page.waitForTimeout(1000);
  }

  // Go to direct receive settlement URL
  const statementId = '22c30f01-10c0-42b5-9edf-f3db46f2c6e8';
  await page.evaluate((id) => {
    window.location.hash = `#/settlement-management/receive-settlement/add?bankStatementId=${id}`;
  }, statementId);
  await page.waitForTimeout(3000);

  // Open drawer
  const addFeeBtn = page.locator('button:has-text("添加明细")').first();
  await addFeeBtn.click();
  await page.waitForTimeout(2000);

  // Click expand icon
  const expandIcon = page.locator('.ant-drawer .ant-table-row-expand-icon').first();
  console.log('Expand icon visible:', await expandIcon.isVisible());
  if (await expandIcon.isVisible()) {
    await expandIcon.click();
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(artifactDir, '16_drawer_expanded.png') });
  }

  // Also let's check what happens if we click "保存" on direct add page
  await page.locator('.ant-drawer-close').click();
  await page.waitForTimeout(1000);
  const saveBtn = page.locator('button:has-text("保 存"), button:has-text("保存")').first();
  await saveBtn.click();
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(artifactDir, '17_direct_add_empty_save_error.png') });

  await browser.close();
  console.log('Done expanding and empty save check!');
})();
