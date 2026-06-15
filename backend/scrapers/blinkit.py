from playwright.async_api import async_playwright
import asyncio

delivery_location = "Greater Noida Alpha 1"

async def scrape_blinkit(product_name):
    
    blinkit_url = f"https://blinkit.com/s/?q={product_name}"

    async with async_playwright() as p:
        
        #this starts a new browser instance. headless=False opens a visible browser window
        browser = await p.chromium.launch(headless=False)
        #creates a new tab
        page = await browser.new_page()

        await page.goto(blinkit_url)
        await page.wait_for_timeout(5000)

        await page.get_by_placeholder("search delivery location").fill(delivery_location)
        await page.wait_for_timeout(2000)  

        #this is that div where our location is filled and we click the first option that is auto-suggested
        await page.locator('div[class*="LocationSearchList__LocationDetailContainer"]').first.click()
        await page.wait_for_timeout(6000)

        #waits for all products to load
        await page.wait_for_selector('div[role="button"].tw-bg-indigo-050')

        #selects all the products loaded
        cards = await page.query_selector_all('div[role="button"].tw-bg-indigo-050')
        #selecting only top3 matches
        cards = cards[:3]

        results = []

        #print(await cards[0].inner_html())

        for card in cards:

            #name element and extract text
            #we find the element that has three classes as -> 1.tw-text-300 2.tw-font-semibold 3.tw-line-clamp-2
            name_ele = await card.query_selector(".tw-text-300.tw-font-semibold.tw-line-clamp-2")
            name = await name_ele.inner_text() if name_ele else "N/A"

            # weight element and extract text
            weight_el = await card.query_selector(".tw-text-200.tw-font-medium.tw-line-clamp-1")
            weight = await weight_el.inner_text() if weight_el else "N/A"

            # price element and extract text
            price_el = await card.query_selector(".tw-text-200.tw-font-semibold")
            price_text = await price_el.inner_text() if price_el else "0"

            price = float(price_text.replace("₹" , "").replace(",", "").strip())

            img_el = await card.query_selector(".tw-overflow-hidden.tw-flex.tw-flex-col img")
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
    asyncio.run(scrape_blinkit("amul butter"))