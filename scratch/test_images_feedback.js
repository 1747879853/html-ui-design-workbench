const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve('pages/bank-statement-edit.html'), { waitUntil: 'networkidle' });

  // 1. Check if top stats exist in default preset (Preset 1)
  const headerStats = await page.$('.cockpit-stats-group');
  console.log('Preset 1: Top header stats element exists:', headerStats !== null);

  // 2. Switch to Preset 0 (Create mode)
  await page.click('button:has-text("新增银行流水 (创建录入场景)")');
  await page.waitForTimeout(500);
  const headerStatsCreate = await page.$('.cockpit-stats-group');
  console.log('Preset 0 (Create mode): Top header stats exists:', headerStatsCreate !== null);

  // Check buttons in right footer in candidate pool
  const candidatePoolTab = await page.$('div[role="tab"]:has-text("即时对账候选池")');
  if (candidatePoolTab) {
    await candidatePoolTab.click();
    await page.waitForTimeout(500);
    console.log('Switched to candidate pool tab');
  }

  // Check left rail scroll height vs client height
  const leftRailMetrics = await page.evaluate(() => {
    const aside = document.querySelector('.studio-left-rail');
    if (!aside) return null;
    return {
      scrollHeight: aside.scrollHeight,
      clientHeight: aside.clientHeight,
      scrollTop: aside.scrollTop,
      hasOverflow: aside.scrollHeight > aside.clientHeight
    };
  });
  console.log('Left rail metrics:', leftRailMetrics);

  // Check what buttons exist in the candidate pool tab footer
  const poolButtons = await page.evaluate(() => {
    const footer = document.querySelector('.pool-footer-actions, .workbench-card, .pool-panel');
    const btns = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
    return btns;
  });
  console.log('All buttons on page:', poolButtons);

  await page.screenshot({ path: 'scratch/preset0_candidate_pool.png' });
  await browser.close();
})();
