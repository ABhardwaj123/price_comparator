from playwright.async_api import async_playwright
import asyncio

async def scrape_blinkit(product_name):
    
    blinkit_url = f"https://blinkit.com/s/?q={product_name}"

    async with async_playwright() as p:
        print("playwright started")

        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()

        await page.goto(blinkit_url)

        await page.wait_for_timeout(5000)

        await page.fill("pincode" , 201310)
        await page.keyboard.click("button")

        await browser.close()


asyncio.run(scrape_blinkit("nutella"))