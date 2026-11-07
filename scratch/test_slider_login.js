const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  await page.goto('http://43.138.14.122:188/#/auth/login', { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  // Fill in login
  const usernameInput = page.locator('input[placeholder*="用户"], input[name="username"]').first();
  const passwordInput = page.locator('input[type="password"]').first();
  await usernameInput.fill('admin');
  await passwordInput.fill('jiayue+5159');

  // Inspect slider bar and children
  const sliderBar = page.locator('div.border-border.bg-background-deep').first();
  const children = await sliderBar.locator('> *').all();
  console.log(`Found ${children.length} direct children in slider bar`);

  // Let's find any child that is a button or draggable
  for (let i = 0; i < children.length; i++) {
    const box = await children[i].boundingBox();
    const cls = await children[i].getAttribute('class');
    console.log(`Child ${i}: class=${cls}, box=`, box);
  }

  // Find the draggable action handle. Usually it has an icon or is absolute positioned on left
  const actionHandle = sliderBar.locator('[class*="cursor-pointer"], [class*="action"], [class*="handler"], [class*="drag"], [class*="bar"]').first();
  let handleBox = await actionHandle.boundingBox();
  if (!handleBox) {
    // If not found by class, find the element at left:0
    for (const child of children) {
      const b = await child.boundingBox();
      if (b && b.width < 100 && b.width > 20) {
        handleBox = b;
        break;
      }
    }
  }

  console.log('Target handle box:', handleBox);
  if (handleBox) {
    const sliderBox = await sliderBar.boundingBox();
    const dragDistance = sliderBox.width - handleBox.width + 10;
    console.log('Dragging distance:', dragDistance);

    await page.mouse.move(handleBox.x + handleBox.width / 2, handleBox.y + handleBox.height / 2);
    await page.mouse.down();
    await page.mouse.move(handleBox.x + handleBox.width / 2 + dragDistance, handleBox.y + handleBox.height / 2, { steps: 30 });
    await page.mouse.up();
    await page.waitForTimeout(1000);
  }

  const afterDragText = await sliderBar.innerText();
  console.log('Slider text after drag:', afterDragText);

  await page.screenshot({ path: path.join(__dirname, 'live_captures/01_drag_result.png') });

  // Click login
  const submitBtn = page.locator('button:has-text("立即登录")').first();
  await submitBtn.click();
  await page.waitForTimeout(3000);
  console.log('URL after submit:', page.url());
  await page.screenshot({ path: path.join(__dirname, 'live_captures/02_after_login.png') });

  await browser.close();
})();
