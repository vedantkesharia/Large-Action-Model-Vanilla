const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const url = process.argv[2];
const timeout = 30000;

if (!url) {
    console.error('Error: No URL provided. Please provide a URL as an argument.');
    process.exit(1);
}

console.log(`Navigating to URL: ${url}`);



(async () => {
    const browser = await puppeteer.launch( {
        headless: "true",
        executablePath: 'C:\\Users\\Vedant Kesharia\\AppData\\Local\\Google\\Chrome SxS\\Application\\chrome.exe',
        userDataDir: 'C:\\Users\\Vedant Kesharia\\AppData\\Local\\Google\\Chrome SxS\\User Data',
    } );

    const page = await browser.newPage();

    await page.setViewport( {
        width: 1200,
        height: 1200,
        deviceScaleFactor: 1,
    } );

    try {
        console.log('Opening page...');
        await page.goto(url, {
            waitUntil: 'domcontentloaded',
            timeout: timeout,
        });

        console.log('Waiting for page to load completely...');
        await page.waitForTimeout(timeout);

        console.log('Taking screenshot...');
        await page.screenshot({
            path: 'screenshot.jpg',
            fullPage: true,
        });

        console.log('Screenshot captured successfully.');
    } catch (error) {
        console.error('Error during page navigation or screenshot capture:', error);
    } finally {
        await browser.close();
    }
})();