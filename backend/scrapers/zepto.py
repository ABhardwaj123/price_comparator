from playwright.async_api import async_playwright
import asyncio
import tempfile
import os

user_data_dir = os.path.join(tempfile.gettempdir(), "zepto_playwright_profile")

async def scrape_zepto(product_name):
    
    zepto_url = f"https://www.zepto.com/search?query={product_name}"

    async with async_playwright() as p:
        
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=["--no-sandbox"]
        )

        page = await browser.new_page()

        await page.goto("https://www.zepto.com")

        # Check if location needs to be set
        address_check = await page.query_selector('h3[data-testid="user-address"]')
        address_text = await address_check.inner_text() if address_check else ""

        if "Select Location" in address_text or not address_text:
            print("⚠️  Please set your location in the browser window, then press Enter here...")
            input()  # ← script pauses here, browser stays open

        await page.goto(zepto_url)
        await page.wait_for_timeout(5000)

        await page.wait_for_selector('a.B4vNQ')

        cards = await page.query_selector_all('a.B4vNQ')
        cards = cards[:3]

        results = []

        # h3 with data-testid="user-address"
        address_el = await page.query_selector('h3[data-testid="user-address"]')
        address = await address_el.inner_text() if address_el else "N/A"

        for card in cards:

            name_ele = await card.query_selector('div[data-slot-id="ProductName"]')
            name = await name_ele.inner_text() if name_ele else "N/A"

            weight_el = await card.query_selector('div[data-slot-id="PackSize"]')
            weight = await weight_el.inner_text() if weight_el else "N/A"

            price_el = await card.query_selector('div[data-slot-id="EdlpPrice"]')
            price_text = await price_el.inner_text() if price_el else "0"

            first_price = price_text.strip().split("\n")[0]
            price = float(first_price.replace("₹", "").replace(",", "").strip())

            img_el = await card.query_selector("img.c2ahfT")
            image_url = await img_el.get_attribute("src") if img_el else None


            results.append({
                "name": name,
                "weight": weight,
                "price": price,
                "image_url": image_url
            })

        
        print(results)
        return results


if __name__ == "__main__":
    asyncio.run(scrape_zepto("nutella"))