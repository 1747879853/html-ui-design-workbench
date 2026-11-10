const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1.5
  });
  const page = await context.newPage();

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
      console.error('Browser Error:', msg.text());
    }
  });
  page.on('pageerror', err => {
    consoleErrors.push(err.message);
    console.error('Page Error:', err.message);
  });

  const outDir = '/Users/blank/.gemini/antigravity/brain/dca9b18f-6fc1-442f-8374-882ebabcdb41';
  const pagePath = 'file://' + path.resolve(__dirname, '../pages/comprehensive-business-edit.html');
  console.log('Opening page:', pagePath);
  await page.goto(pagePath, { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  // 1. 标准态 - 基础信息
  console.log('Capturing 01_standard_basic...');
  await page.screenshot({ path: path.join(outDir, '01_standard_basic.png') });

  // 2. 展开收发通
  console.log('Expanding ShouFaTong...');
  await page.click('.shoufatoggle-btn');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(outDir, '01_basic_shoufa_expanded.png') });

  // 3. 切换至空白新业务
  console.log('Switching to empty sample...');
  await page.click('.ant-radio-button-wrapper:has-text("2. 空白新业务")');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '02_empty_sample.png') });

  // 4. 切换至应收应付 (有费用标准态)
  console.log('Switching to fee tab...');
  await page.click('.ant-radio-button-wrapper:has-text("1. 标准待补全")');
  await page.waitForTimeout(400);
  await page.click('.ant-tabs-tab:has-text("应收应付")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '03_fee_standard.png') });

  // 5. 勾选合并更改单·只读态
  console.log('Toggling fee merge readonly...');
  await page.click('.ant-checkbox-wrapper:has-text("合并更改单")');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '04_fee_merge_readonly.png') });

  // 6. 更改单未锁费用拦截态
  console.log('Switching to co blocked...');
  await page.click('.ant-radio-button-wrapper:has-text("4. 更改单未锁费用拦截")');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '05_co_precondition_blocked.png') });

  // 7. 解锁更改单录入态
  console.log('Unlocking change order...');
  await page.click('button:has-text("原型模拟：立即锁账原费用")');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '06_co_unlocked_entry.png') });

  // 8. 附件未配置类型态
  console.log('Switching to attach empty...');
  await page.click('.ant-radio-button-wrapper:has-text("5. 附件未配置类型")');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '07_attach_empty.png') });

  // 9. 附件正常管理态
  console.log('Switching to standard attach...');
  await page.click('.ant-radio-button-wrapper:has-text("1. 标准待补全")');
  await page.waitForTimeout(400);
  await page.click('.ant-tabs-tab:has-text("附件")');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '08_attach_standard.png') });

  // 10. 复制业务弹窗
  console.log('Opening copy modal...');
  await page.click('button:has-text("更多")');
  await page.waitForTimeout(300);
  await page.click('.ant-dropdown-menu-item:has-text("复制本票业务")');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '09_copy_modal.png') });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);

  // 11. 关联海运主单弹窗
  console.log('Opening related master order modal...');
  await page.click('.ant-tabs-tab:has-text("基础信息")');
  await page.waitForTimeout(400);
  await page.click('button:has-text("关联海运主单")');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '11_related_order_modal.png') });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);

  // 12. index.html 工作台画布
  const indexPath = 'file://' + path.resolve(__dirname, '../index.html');
  console.log('Opening index workbench:', indexPath);
  await page.goto(indexPath, { waitUntil: 'load' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(outDir, '10_workbench_simulator.png') });

  console.log('Screenshots captured successfully!');
  console.log('Console Errors Count:', consoleErrors.length);
  if (consoleErrors.length > 0) {
    console.error('Errors found:', consoleErrors);
    process.exit(1);
  }

  await browser.close();
})();
