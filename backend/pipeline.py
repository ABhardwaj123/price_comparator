import asyncio
from database import SessionLocal
from datetime import datetime, timedelta
from models import ProductPlatform , Product ,Platform
from scrapers import blinkit , zepto
from crud import get_latest_price , save_prices



#async is used as if the scraper is scraping data , our server can handle other requests as well
#await is always used with async
#this is meant to be run on a schedule , independently in background
async def run_pipeline():
    db = SessionLocal()

    #selecting all the products of blinkit , zepto till now
    #ProductPlatform only has {id , productId , platformId}
    products = db.query(ProductPlatform).all()

    #iterating through each product
    for product in products:
        
        #getting the platform object for each product in the ProductPlatform thing
        platform = db.query(Platform).filter(Platform.id == product.platform_id).first()
        #getting the Price object
        latest = get_latest_price(db , product.id)

        if not latest or (datetime.utcnow() - latest.scraped_at) > timedelta(hours=6):
            prod = db.query(Product).filter(Product.id == product.product_id).first()

            if platform.name == "blinkit":
                results = await blinkit.scrape_blinkit(prod.name)
            elif platform.name == "zepto":
                results = await zepto.scrape_zepto(prod.name)
            else:
                results = []

            if results:
                save_prices(db, product.id, results)


    db.close()
        


asyncio.run(run_pipeline())