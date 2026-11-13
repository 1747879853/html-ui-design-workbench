const { chromium } = require('playwright');
const path = require('path');

const directions = [
  'payment-app-dir1-linear-split.html',
  'payment-app-dir2-voucher-card.html',
  'payment-app-dir3-stepper-wizard.html',
  'payment-app-dir4-master-detail-side.html',
  'payment-app-dir5-high-density-excel.html',
  'payment-app-dir6-invoice-matching-deck.html',
  'payment-app-dir7-kanban-cards.html',
  'payment-app-dir8-compact-tabbed-pro.html',
  'payment-app-dir9-drawer-focused.html',
  'payment-app-dir10-executive-bilingual.html'
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  let errors = [];

  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.log('CONSOLE ERROR:', msg.text());
      errors.push(msg.text());
    }
  });
  page.on('pageerror', err => {
    console.log('PAGE ERROR:', err.message);
    errors.push(err.message);
  });

  for (let i = 0; i < directions.length; i++) {
    const filename = directions[i];
    const filepath = path.resolve('pages', filename);
    console.log(`[${i + 1}/10] Testing ${filename}...`);
    await page.goto('file://' + filepath, { waitUntil: 'networkidle' });
    await page.waitForTimeout(600);

    const shotPath = `/Users/blank/.gemini/antigravity/brain/dd5d25fe-e69a-4e4e-91aa-dccec9f9666f/dir${i + 1}_screen.png`;
    await page.screenshot({ path: shotPath });
    console.log(`  Saved ${shotPath}`);
  }

  await browser.close();

  if (errors.length > 0) {
    console.error(`FAILED: ${errors.length} errors found.`);
    process.exit(1);
  } else {
    console.log('ALL 10 DIRECTIONS VERIFIED CLEANLY WITH 0 ERRORS!');
  }
})();
