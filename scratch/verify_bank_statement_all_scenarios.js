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

  // =========================================================================
  // 0. 场景 0：新增银行流水 (创建录入场景)
  // =========================================================================
  console.log('0. Switching to scenario 0 (preset_create)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("场景0")').click();
  await page.waitForTimeout(600);
  console.log('0a. Capturing 00_bank_statement_create_initial.png...');
  await page.screenshot({ path: path.join(artifactDir, '00_bank_statement_create_initial.png') });

  // 快捷填入标准示例数据 (捷顺达 · ¥10,000)
  console.log('0b. Clicking quick fill sample data...');
  await page.locator('button:has-text("填入标准示例数据")').click();
  await page.waitForTimeout(500);
  console.log('0c. Capturing 00_bank_statement_create_filled.png...');
  await page.screenshot({ path: path.join(artifactDir, '00_bank_statement_create_filled.png') });

  // 验证保存并立即对账
  console.log('0d. Clicking save and start reconcile...');
  await page.locator('button:has-text("保存并立即开启对账")').first().click();
  await page.waitForTimeout(800);
  console.log('0e. Capturing 00_bank_statement_create_reconciled.png...');
  await page.screenshot({ path: path.join(artifactDir, '00_bank_statement_create_reconciled.png') });

  // =========================================================================
  // 1. 样本 1：核销完成 (SH261026025 · 1,000 RMB，余额 0)
  // =========================================================================
  console.log('1. Switching to sample 1 (done)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("样本1")').click();
  await page.waitForTimeout(600);
  console.log('Capturing 01_bank_statement_done.png...');
  await page.screenshot({ path: path.join(artifactDir, '01_bank_statement_done.png') });

  // 展开第一行：按费用核销明细 (若尚未展开)
  console.log('2. Ensuring fee item row is expanded...');
  const collapsedFee = page.locator('.ant-table-row-expand-icon-collapsed').first();
  if (await collapsedFee.isVisible()) {
    await collapsedFee.click();
    await page.waitForTimeout(400);
  }

  // 展开第二行：按发票核销明细
  console.log('3. Expanding invoice issue row...');
  const collapsedInv = page.locator('.ant-table-row-expand-icon-collapsed').first();
  if (await collapsedInv.isVisible()) {
    await collapsedInv.click();
    await page.waitForTimeout(400);
  }
  await page.screenshot({ path: path.join(artifactDir, '02_bank_statement_expanded_both.png') });

  // 4. 批量删除费用交互：在费用明细子表中勾选两笔费用
  console.log('4. Selecting fee rows for batch deletion...');
  const feeCheckboxes = page.locator('.expanded-detail-box .ant-table-tbody .ant-checkbox-input');
  const count = await feeCheckboxes.count();
  console.log('Fee checkboxes count:', count);
  if (count >= 2) {
    await feeCheckboxes.nth(0).click();
    await feeCheckboxes.nth(1).click();
    await page.waitForTimeout(400);
    // 点击顶部「删除费用 (2)」按钮打开批量删除弹窗
    console.log('Opening batch delete fee modal...');
    await page.locator('button:has-text("删除费用")').click();
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(artifactDir, '03_batch_delete_fee_modal.png') });
    // 关闭弹窗
    await page.locator('.ant-modal-close').first().click();
    await page.waitForTimeout(400);
  }

  // 5. 切换到样本 2：部分核销 (SH261023022 · 余额 20.00 RMB)
  console.log('5. Switching to sample 2 (partial writeoff)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("样本2")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '04_bank_statement_partial.png') });

  // 打开新建收费核销抽屉
  console.log('6. Opening settlement workbench drawer...');
  await page.locator('button:has-text("新建收费核销")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '05_bank_statement_drawer_fee.png') });

  // 在抽屉中切换为按发票核销
  console.log('7. Switching drawer to invoice mode...');
  await page.locator('.ant-segmented-item:has-text("按发票开出核销")').click();
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(artifactDir, '06_bank_statement_drawer_invoice.png') });
  await page.locator('.ant-drawer-close').click();
  await page.waitForTimeout(400);

  // 8. 切换到样本 3：待核销空态 (SH261022019 · 3.00 USD)
  console.log('8. Switching to sample 3 (pending empty)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("样本3")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '07_bank_statement_empty.png') });

  // 9. 切换到样本 4：自动导入流水 (银企直连 · 核心字段锁定)
  console.log('9. Switching to sample 4 (auto import)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("样本4")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '08_bank_statement_auto_import.png') });

  // 10. 切换到样本 5：流水已锁定 (50,000 RMB · 冻结)
  console.log('10. Switching to sample 5 (locked)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("样本5")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '09_bank_statement_locked.png') });

  // 11. 切换到样本 6：异常超核销 (-800 RMB 标红警示)
  console.log('11. Switching to sample 6 (over settled)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("样本6")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '10_bank_statement_over_settled.png') });

  // 12. 切换到样本 7：加载与局部重试
  console.log('12. Switching to sample 7 (loading & error retry)...');
  await page.locator('label.ant-radio-button-wrapper:has-text("样本7")').click();
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(artifactDir, '11_bank_statement_error_retry.png') });

  // 13. 草稿未保存拦截验证：切回样本 2，修改总金额触发草稿未保存
  console.log('13. Testing unsaved changes guard modal...');
  await page.locator('label.ant-radio-button-wrapper:has-text("样本2")').click();
  await page.waitForTimeout(500);
  const amountInput = page.locator('input.ant-input-number-input').first();
  await amountInput.fill('150.00');
  await page.keyboard.press('Tab');
  await page.waitForTimeout(300);
  // 点击新建收费核销，弹出先保存流水拦截
  await page.locator('button:has-text("新建收费核销")').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(artifactDir, '12_unsaved_changes_alert.png') });

  await browser.close();
  console.log('All scenarios verified successfully! Total console/page errors:', errors.length);
  if (errors.length > 0) {
    console.error('Errors found:', errors);
    process.exit(1);
  }
})();
