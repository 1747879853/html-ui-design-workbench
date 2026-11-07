const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const artifactDir = '/Users/blank/.gemini/antigravity/brain/eadd1c17-0a30-4ee4-9408-aa9110040c7f/captures_receive';
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

  const pageUrl = 'file://' + path.resolve(__dirname, '../pages/receive-settlement-edit.html');
  console.log('Navigating to:', pageUrl);
  await page.goto(pageUrl, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // 1. 场景 1 默认视图 (已选流水 · 正常核销 1,000 RMB · 多原币汇总)
  console.log('1. Checking default scenario (preset_create_fee_selected)...');
  await page.screenshot({ path: path.join(artifactDir, '01_receive_create_fee_selected.png') });

  // 2. 检查多原币汇总横幅内容
  const summaryText = await page.evaluate(() => {
    const el = document.querySelector('.settlement-currency-summary-bar');
    return el ? el.innerText.replace(/\n/g, ' ') : 'NOT_FOUND';
  });
  console.log('Summary banner text:', summaryText);

  // 3. 场景 0：未选流水初始引导态
  console.log('2. Switching to scenario 0 (preset_create_empty)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("场景0")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '00_receive_create_empty.png') });

  // 打开流水选择弹窗
  console.log('2b. Opening bank statement picker...');
  await page.locator('button:has-text("立即选择银行流水")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '00_receive_bank_picker.png') });
  // 选择第一条流水
  await page.locator('.ant-modal button:has-text("选择关联")').first().click();
  await page.waitForTimeout(500);

  // 4. 场景 2：新增发票结算
  console.log('3. Switching to scenario 2 (preset_create_invoice)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("场景2")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '02_receive_create_invoice.png') });

  // 5. 场景 3：编辑费用结算 (追加/删除本单明细)
  console.log('4. Switching to scenario 3 (preset_edit_fee)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("场景3")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '03_receive_edit_fee.png') });

  // 打开添加费用抽屉
  console.log('4b. Opening add fee drawer...');
  await page.locator('button:has-text("添加费用明细")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '03_receive_add_fee_drawer.png') });
  await page.locator('.ant-drawer-close').click();
  await page.waitForTimeout(400);

  // 6. 场景 4：编辑发票结算
  console.log('5. Switching to scenario 4 (preset_edit_invoice)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("场景4")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '04_receive_edit_invoice.png') });

  // 7. 场景 5：自动核销确认
  console.log('6. Switching to scenario 5 (preset_auto_allocation)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("场景5")').click();
  await page.waitForTimeout(500);
  await page.locator('button:has-text("按范围自动核销")').first().click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '05_receive_auto_alloc_modal.png') });
  await page.locator('.ant-modal-close').click();
  await page.waitForTimeout(400);

  // 8. 场景 6：单据锁定只读
  console.log('7. Switching to scenario 6 (preset_locked)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("场景6")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '06_receive_locked.png') });

  // 9. 场景 7：银行流水锁定
  console.log('8. Switching to scenario 7 (preset_statement_locked)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("场景7")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '07_receive_statement_locked.png') });

  // 10. 场景 8：超额拦截
  console.log('9. Switching to scenario 8 (preset_over_limit)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("场景8")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '08_receive_over_limit.png') });

  // 11. 场景 9：加载与超时重试
  console.log('10. Switching to scenario 9 (preset_loading_error)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("场景9")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '09_receive_loading_error.png') });

  console.log('\n=========================================');
  console.log('Total console/page errors:', errors.length);
  if (errors.length > 0) {
    console.error('Errors details:', errors);
  } else {
    console.log('Verification PASSED with ZERO ERRORS!');
  }
  console.log('=========================================\n');

  await browser.close();
})();
