import asyncio
from database import SessionLocal
from datetime import datetime, timedelta
from models import ProductPlatform , Product
from scrapers import blinkit
from crud import get_latest_price , save_prices

async def run_pipeline():
    db = SessionLocal()

    #selecting products of blinkit
    products = db.query(ProductPlatform).filter(ProductPlatform.platform_id == 1).all()

    for product in products:
        
        latest = get_latest_price(db , product.product_id)

        if not latest or (datetime.utcnow() - latest.scraped_at) > timedelta(hours=6):
            
            prod = db.query(Product).filter(Product.id == product.product_id).first()
            results = await blinkit.scrape_blinkit(prod.name)
            save_prices(db , product.id , results)


    db.close()
        


asyncio.run(run_pipeline())