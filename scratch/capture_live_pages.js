const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const artifactDir = '/Users/blank/Documents/antigravity/intelligent-hopper/scratch/live_captures';
  if (!fs.existsSync(artifactDir)) {
    fs.mkdirSync(artifactDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  console.log('Opening login page...');
  await page.goto('http://43.138.14.122:188/#/auth/login', { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  // Fill in login
  const usernameInput = page.locator('input[placeholder*="用户"], input[name="username"]').first();
  const passwordInput = page.locator('input[type="password"]').first();
  await usernameInput.fill('admin');
  await passwordInput.fill('jiayue+5159');

  // Drag slider
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

  // Click login
  console.log('Clicking login button...');
  const submitBtn = page.locator('button:has-text("立即登录")').first();
  await submitBtn.click();
  await page.waitForTimeout(3000);

  // Close announcement modal if present
  const readBtn = page.locator('button:has-text("我已阅读")').first();
  if (await readBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
    console.log('Closing announcement modal...');
    await readBtn.click();
    await page.waitForTimeout(1000);
  }

  // 1. Visit bank statement list
  console.log('Navigating to bank statement list via hash change...');
  await page.evaluate(() => { window.location.hash = '#/bank-statement'; });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: path.join(artifactDir, '11_bank_statement_list.png') });

  // Search SH261022020
  console.log('Searching for SH261022020...');
  // Check inputs on page
  const searchInputs = await page.locator('.ant-form input, input.ant-input').all();
  console.log(`Found ${searchInputs.length} inputs in search form`);
  if (searchInputs.length > 0) {
    await searchInputs[0].fill('SH261022020');
    const searchBtn = page.locator('button:has-text("查询"), button:has-text("搜索")').first();
    if (await searchBtn.isVisible()) {
      await searchBtn.click();
      await page.waitForTimeout(2000);
    }
  }
  await page.screenshot({ path: path.join(artifactDir, '12_bank_statement_filtered.png') });

  // Open SH261022020 edit page
  const row = page.locator('tr:has-text("SH261022020")').first();
  let statementId = '';
  if (await row.isVisible({ timeout: 3000 }).catch(() => false)) {
    console.log('Found SH261022020 row!');
    await row.dblclick();
    await page.waitForTimeout(3000);
    console.log('URL after dblclick:', page.url());
    await page.screenshot({ path: path.join(artifactDir, '13_bank_statement_edit_SH261022020.png') });

    const match = page.url().match(/\/bank-statement\/edit\/([a-zA-Z0-9\-]+)/);
    if (match) {
      statementId = match[1];
      console.log('Extracted statementId:', statementId);
    }
  } else {
    console.log('SH261022020 row not found directly, dumping table text:');
    const tableText = await page.locator('.ant-table').innerText().catch(() => 'no table');
    console.log(tableText.slice(0, 500));
  }

  // If statementId not found from table, search API or inspect
  if (!statementId) {
    // Try to get statementId from the first row of table if any
    const firstRow = page.locator('.ant-table-tbody tr').first();
    if (await firstRow.isVisible()) {
      await firstRow.dblclick();
      await page.waitForTimeout(3000);
      console.log('Opened first row URL:', page.url());
      await page.screenshot({ path: path.join(artifactDir, '13_first_statement_edit.png') });
      const match = page.url().match(/\/bank-statement\/edit\/([a-zA-Z0-9\-]+)/);
      if (match) {
        statementId = match[1];
      }
    }
  }

  // If statementId found, navigate to direct add page
  if (statementId) {
    console.log('Navigating to direct receive settlement URL with id:', statementId);
    await page.evaluate((id) => {
      window.location.hash = `#/settlement-management/receive-settlement/add?bankStatementId=${id}`;
    }, statementId);
    await page.waitForTimeout(3500);
    await page.screenshot({ path: path.join(artifactDir, '14_receive_settlement_direct_add.png') });

    // Try to open Add Fee Drawer ("添加明细")
    console.log('Attempting to open Add Fee Drawer...');
    const addFeeBtn = page.locator('button:has-text("添加明细"), button:has-text("添加费用明细")').first();
    if (await addFeeBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await addFeeBtn.click();
      await page.waitForTimeout(2500);
      await page.screenshot({ path: path.join(artifactDir, '15_receive_settlement_drawer.png') });

      // Check if candidate row can be expanded
      const expandBtn = page.locator('.ant-drawer .ant-table-row-expand-icon').first();
      if (await expandBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
        await expandBtn.click();
        await page.waitForTimeout(1000);
        await page.screenshot({ path: path.join(artifactDir, '16_receive_settlement_drawer_expanded.png') });
      }
    }
  }

  await browser.close();
  console.log('Live inspection completed successfully!');
})();
