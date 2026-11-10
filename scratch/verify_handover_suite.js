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

  const outDir = '/Users/blank/.gemini/antigravity/brain/8060e0f8-232b-480b-ac03-ce82456e507a';
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  const pagePath = 'file://' + path.resolve(__dirname, '../pages/comprehensive-business-edit.html');
  console.log('Opening page:', pagePath);
  await page.goto(pagePath, { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  // Hide toast messages during scenario verification to prevent visual overlap
  await page.addStyleTag({ content: '.ant-message { display: none !important; }' });

  // 1. 标准态 - 左右同屏工作台 (全新微卡亮点设计，右侧集成Tab，左侧永久常驻)
  console.log('Capturing 01_standard_workbench...');
  await page.evaluate(() => window.__workbench.applyScenario('standard'));
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '01_standard_workbench.png') });

  // 2. 分区脏状态 (3大独立保存域，业务与应收未存指示)
  console.log('Switching to dirty state...');
  await page.evaluate(() => window.__workbench.applyScenario('dirty'));
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '02_partition_dirty_states.png') });

  // 3. 合并更改单·只读态 (两表增加来源列，警示条，动作置灰)
  console.log('Switching to merge readonly state...');
  await page.evaluate(() => window.__workbench.applyScenario('merge'));
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '03_merge_change_order_readonly.png') });

  // 4. 更改单未锁定前置拦截态 (图04高保真还原)
  console.log('Switching to CO blocked state...');
  await page.evaluate(() => window.__workbench.applyScenario('co_blocked'));
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '04_change_order_prerequisite_blocked.png') });

  // 5. 更改单原票已锁录入态
  console.log('Switching to CO unlocked state...');
  await page.evaluate(() => window.__workbench.applyScenario('co_unlocked'));
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '05_change_order_unlocked.png') });

  // 6. 附件无类型配置空态 (图05高保真还原)
  console.log('Switching to attachment empty state...');
  await page.evaluate(() => window.__workbench.applyScenario('attach_empty'));
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '06_attachment_no_config_empty.png') });

  // 7. 附件分类管理态
  console.log('Switching to attachment full state...');
  await page.evaluate(() => window.__workbench.applyScenario('attach_full'));
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '07_attachment_management.png') });

  // 8. 关联主单弹窗
  console.log('Opening master order modal...');
  await page.evaluate(() => window.__workbench.applyScenario('standard'));
  await page.waitForTimeout(400);
  const unlinkBtn = await page.$('.master-unlink-icon');
  if (unlinkBtn) {
    await unlinkBtn.click({ force: true });
    await page.waitForTimeout(300);
  }
  await page.click('button:has-text("关联海运主单")', { force: true });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '08_master_order_modal.png') });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);

  // 9. 整票提交范围确认弹窗
  console.log('Opening submit scope modal...');
  await page.click('button:has-text("整票提交审核")', { force: true });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '09_submit_scope_modal.png') });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);

  // 10. 交互规范与交接核对抽屉
  console.log('Opening spec drawer...');
  await page.click('.floating-spec-btn', { force: true });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '10_design_spec_drawer.png') });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);

  // 11. 验证 index.html 工作台画布
  const indexPath = 'file://' + path.resolve(__dirname, '../index.html');
  console.log('Opening index workbench simulator:', indexPath);
  await page.goto(indexPath, { waitUntil: 'load' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(outDir, '11_index_workbench_simulator.png') });

  console.log('Screenshots captured successfully!');
  console.log('Console Errors Count:', consoleErrors.length);
  if (consoleErrors.length > 0) {
    console.error('Errors found:', consoleErrors);
    process.exit(1);
  }

  await browser.close();
})();
