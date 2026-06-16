from database import SessionLocal
from models import Price
from scrapers import blinkit


def save_prices(db , product_platform_id , scraped_results):
    

    for result in scraped_results:
        prod_name = result["name"]
        price = result["price"]
        size = result["weight"]
        image_url = result["image_url"]

        obj = Price()
        obj.product_platform_id = product_platform_id
        obj.price=price
        obj.in_stock=True

        db.add(obj)
        db.commit()


#this function gives the last recorded price of object 
def get_latest_price(db , product_platform_id):

    return db.query(Price).filter(Price.product_platform_id == product_platform_id).order_by(Price.scraped_at.desc()).first()