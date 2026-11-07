const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const artifactDir = '/Users/blank/.gemini/antigravity/brain/814ca890-03ae-4ec0-8f88-31d1333285ca';
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
    const text = msg.text();
    if (msg.type() === 'error' && !text.includes('api.iconify.design') && !text.includes('ERR_CONNECTION_CLOSED')) {
      errors.push(text);
      console.error('[Browser Console Error]:', text);
    }
  });
  page.on('pageerror', err => {
    errors.push(err.message);
    console.error('[Page Error]:', err.message);
  });

  const pageUrl = 'file://' + path.resolve(__dirname, '../pages/bank-direct-workbench.html');
  console.log('Navigating to:', pageUrl);
  await page.goto(pageUrl, { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  // 1. 默认主视图 (1920×1080)
  console.log('Capturing 01_bank_direct_main...');
  await page.screenshot({ path: path.join(artifactDir, '01_bank_direct_main.png') });

  // 2. 展开高级筛选
  console.log('Expanding advanced filters...');
  await page.locator('.filter-actions button:has-text("展开高级筛选")').click();
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(artifactDir, '02_filter_expanded.png') });
  await page.locator('.filter-actions button:has-text("收起高级筛选")').click();
  await page.waitForTimeout(300);

  // 3. 双击打开交易抽屉
  console.log('Double clicking first row to open drawer...');
  await page.locator('.wb-table .ant-table-tbody > tr').first().dblclick();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(artifactDir, '03_transaction_drawer.png') });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);

  // 4. 认领弹窗
  console.log('Opening Claim modal...');
  await page.locator('.wb-stat-pill').first().click();
  await page.waitForTimeout(400);
  await page.locator('.wb-table .ant-table-tbody .ant-checkbox-input').first().click();
  await page.waitForTimeout(300);
  await page.locator('button:has-text("认领")').first().click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(artifactDir, '04_claim_modal.png') });
  await page.locator('.ant-modal-wrap:not([style*="display: none"]) button:has-text("取 消")').click();
  await page.waitForTimeout(400);

  // 5. 关联手录流水弹窗
  console.log('Opening Link modal...');
  await page.locator('.wb-stat-pill:has-text("疑似重复来账")').click();
  await page.waitForTimeout(400);
  await page.locator('.wb-table .ant-table-tbody .ant-checkbox-input').first().click();
  await page.waitForTimeout(300);
  await page.locator('button:has-text("关联手录流水")').click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(artifactDir, '05_link_modal.png') });
  await page.locator('.ant-modal-wrap:not([style*="display: none"]) button:has-text("取 消")').click();
  await page.waitForTimeout(400);

  // 6. 批量忽略弹窗
  console.log('Opening Batch Ignore modal...');
  const isChecked = await page.locator('.wb-table .ant-table-tbody .ant-checkbox-input').first().isChecked();
  if (!isChecked) {
    await page.locator('.wb-table .ant-table-tbody .ant-checkbox-input').first().click();
    await page.waitForTimeout(300);
  }
  await page.locator('button:has-text("批量忽略")').click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(artifactDir, '06_batch_ignore_modal.png') });
  await page.locator('.ant-modal-wrap:not([style*="display: none"]) button:has-text("取 消")').click();
  await page.waitForTimeout(400);

  // 7. 手动拉取弹窗
  console.log('Opening Pull modal...');
  await page.locator('button:has-text("手动拉取")').click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(artifactDir, '07_pull_modal.png') });
  await page.locator('.ant-modal-wrap:not([style*="display: none"]) button:has-text("关 闭")').click();
  await page.waitForTimeout(400);

  // 8. 下载回单弹窗 (两步式 3 分钟倒计时)
  console.log('Opening Receipt modal...');
  await page.locator('button:has-text("下载回单")').first().click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(artifactDir, '08_receipt_modal_step1.png') });

  // 触发第一步银行打包
  console.log('Submitting Step 1 Receipt download...');
  await page.locator('button:has-text("第一步：提交银行准备")').click();
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(artifactDir, '09_receipt_modal_countdown.png') });
  await page.locator('.ant-modal-wrap:not([style*="display: none"]) button:has-text("关 闭")').click();
  await page.waitForTimeout(500);

  // 9. 切换到「每日同步任务」页签
  console.log('Switching to Daily Jobs tab...');
  await page.locator('.ant-segmented-item:has-text("每日任务")').click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(artifactDir, '10_daily_jobs_tab.png') });

  // 双击失败任务打开抽屉
  console.log('Double clicking failed daily job row...');
  await page.locator('.wb-table .ant-table-tbody > tr:has-text("失败")').first().dblclick();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(artifactDir, '11_daily_job_drawer.png') });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);

  // 10. 切回交易页签并演示空态
  console.log('Switching back to transactions and testing empty scenarios...');
  await page.locator('.ant-segmented-item:has-text("银行交易明细")').click();
  await page.waitForTimeout(400);

  // 空态 1: 尚未配置直连账户
  console.log('Switching to empty-no-account scenario...');
  await page.locator('.wb-scope-right .ant-select').nth(1).click();
  await page.waitForTimeout(300);
  await page.locator('.ant-select-item-option-content:has-text("尚未配置直连账户")').click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(artifactDir, '12_empty_no_account.png') });

  // 空态 2: 筛选无结果
  console.log('Switching to empty-filter scenario...');
  await page.locator('.wb-scope-right .ant-select').nth(1).click();
  await page.waitForTimeout(300);
  await page.locator('.ant-select-item-option-content:has-text("筛选条件无结果")').click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(artifactDir, '13_empty_filter.png') });

  await browser.close();

  if (errors.length > 0) {
    console.error('FAILED with errors:', errors);
    process.exit(1);
  } else {
    console.log('ALL VERIFICATIONS PASSED CLEANLY WITH ZERO ERRORS!');
  }
})();
