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

  // 2. 切换至实测空样本态
  console.log('Switching to empty sample...');
  await page.click('span:has-text("场景2: 实测空数据样本")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '02_empty_sample.png') });

  // 3. 切换至应收应付
  console.log('Switching to fee tab...');
  await page.click('span:has-text("场景1: 完整录入标准态")');
  await page.waitForTimeout(400);
  await page.click('span:has-text("应收应付")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '03_fee_standard.png') });

  // 4. 切换至合并更改单只读态
  console.log('Switching to fee merge readonly...');
  await page.click('span:has-text("场景3: 费用合并更改单")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '04_fee_merge_readonly.png') });

  // 5. 更改单前置未锁拦截态
  console.log('Switching to co blocked...');
  await page.click('span:has-text("场景4: 更改单前置未锁")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '05_co_precondition_blocked.png') });

  // 6. 更改单正常录入态
  console.log('Switching to co unlocked...');
  await page.click('span:has-text("场景5: 更改单录入")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '06_co_unlocked_entry.png') });

  // 7. 附件未配置类型态
  console.log('Switching to attach empty...');
  await page.click('.ant-radio-button-wrapper:has-text("场景6: 附件未配置类型")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '07_attach_empty.png') });

  // 8. 附件正常管理态
  console.log('Switching to attach standard...');
  await page.click('.ant-radio-button-wrapper:has-text("场景1: 完整录入标准态")');
  await page.waitForTimeout(400);
  await page.click('.wb-tab-item:has-text("附件")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '08_attach_standard.png') });

  // 9. 复制确认弹窗
  console.log('Opening copy modal...');
  await page.click('button:has-text("预览复制弹窗")');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '09_copy_modal.png') });
  await page.click('.ant-modal-close');
  await page.waitForTimeout(400);

  // 10. index.html 工作台画布
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
