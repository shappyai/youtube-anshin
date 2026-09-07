const fs = require('fs');
const path = require('path');
const { chromium } = require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

function argument(name) {
  const index = process.argv.indexOf(name);
  if (index < 0 || !process.argv[index + 1]) throw new Error(`missing ${name}`);
  return process.argv[index + 1];
}

function optionalArgument(name) {
  const index = process.argv.indexOf(name);
  return index >= 0 ? process.argv[index + 1] : null;
}

function optionalNumber(name, fallback) {
  const value = optionalArgument(name);
  return value ? Number(value) : fallback;
}

async function main() {
  const source = path.resolve(argument('--source'));
  const output = path.resolve(argument('--output'));
  const target = optionalArgument('--target');
  const content = optionalArgument('--content');
  const viewportWidth = optionalNumber('--width', 1440);
  const viewportHeight = optionalNumber('--height', 1000);
  const hideImages = process.argv.includes('--hide-images');
  if (!fs.existsSync(source)) throw new Error(`source missing: ${source}`);
  fs.mkdirSync(path.dirname(output), { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args: ['--disable-gpu', '--disable-software-rasterizer', '--no-sandbox'],
  });
  const page = await browser.newPage({ viewport: { width: viewportWidth, height: viewportHeight }, deviceScaleFactor: 1 });
  await page.goto(`file:///${source.replaceAll('\\', '/')}`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  if (hideImages) {
    // 保存HTMLでは公式の小さなインラインアイコンが取得できない場合がある。
    // 本文の公式文言を読ませる素材では、欠損アイコンだけを非表示にする。
    await page.addStyleTag({ content: 'img { display: none !important; }' });
  }
  if (target) {
    const locator = page.locator('h1, h2, h3').filter({ hasText: target }).first();
    if (await locator.count()) {
      await locator.scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
    } else {
      console.warn(`target heading not found: ${target}`);
    }
  }
  if (content) {
    const locator = page.locator('p, li').filter({ hasText: content }).first();
    if (await locator.count()) {
      await locator.scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
    } else {
      console.warn(`target content not found: ${content}`);
    }
  }
  await page.screenshot({ path: output, fullPage: false });
  await browser.close();
  console.log(JSON.stringify({ source, output, bytes: fs.statSync(output).size }));
}

main().catch((error) => { console.error(error.stack || error); process.exit(1); });
