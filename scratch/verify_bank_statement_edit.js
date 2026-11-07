const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const artifactDir = '/Users/blank/Documents/antigravity/intelligent-hopper/scratch/verification_captures';
  if (!fs.existsSync(artifactDir)) {
    fs.mkdirSync(artifactDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1
  });
  const page = await context.newPage();

  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
      console.error('[Console Error]:', msg.text());
    }
  });
  page.on('pageerror', err => {
    errors.push(err.message);
    console.error('[Page Error]:', err.message);
  });

  const pageUrl = 'file://' + path.resolve(__dirname, '../pages/bank-statement-edit.html');
  console.log('Navigating to:', pageUrl);
  await page.goto(pageUrl, { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  // 1. 默认样本1: SH261022020 (核销完成，余额0)
  console.log('Capturing 01_bank_statement_done...');
  await page.screenshot({ path: path.join(artifactDir, '01_bank_statement_done.png') });

  // 展开第一行关联核销单明细
  console.log('Expanding fee row...');
  const expandBtn = page.locator('.ant-table-row-expand-icon').first();
  if (await expandBtn.isVisible()) {
    await expandBtn.click();
    await page.waitForTimeout(400);
    await page.screenshot({ path: path.join(artifactDir, '02_bank_statement_expanded.png') });
  }

  // 2. 切换到样本2: 部分核销 (余额4,500.00)
  console.log('Switching to partial active preset...');
  await page.locator('label.ant-radio-button-wrapper:has-text("样本2")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '03_bank_statement_partial.png') });

  // 3. 打开新建核销抽屉
  console.log('Opening add settlement drawer...');
  await page.locator('button:has-text("新建收费核销")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '04_bank_statement_drawer.png') });
  await page.locator('.ant-drawer-close').click();
  await page.waitForTimeout(400);

  // 4. 切换到样本5: 流水已锁定
  console.log('Switching to locked preset...');
  await page.locator('label.ant-radio-button-wrapper:has-text("样本5")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '05_bank_statement_locked.png') });

  await browser.close();
  console.log('Verification completed! Errors count:', errors.length);
  if (errors.length > 0) {
    console.error('Errors found:', errors);
    process.exit(1);
  }
})();
