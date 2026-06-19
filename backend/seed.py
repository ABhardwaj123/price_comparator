#this seed script is some manual insertion of starting data into database. good to have some initial data to work on
#run it once to populate the tables

from database import SessionLocal
from models import Platform, Product, ProductPlatform

db = SessionLocal()

#if checks so that data is not duplicated
blinkit = db.query(Platform).filter(Platform.name == "blinkit").first()
if not blinkit:
    blinkit = Platform(name="blinkit")
    db.add(blinkit)
    db.commit()
    db.refresh(blinkit)

zepto = db.query(Platform).filter(Platform.name == "zepto").first()
if not zepto:
    zepto = Platform(name="zepto")
    db.add(zepto)
    db.commit()
    db.refresh(zepto)


nutella = db.query(Product).filter(Product.name == "nutella").first()
if not nutella:
    nutella = Product(name="nutella")
    db.add(nutella)
    db.commit()
    db.refresh(nutella)


amul_butter = db.query(Product).filter(Product.name == "amul butter").first()
if not amul_butter:
    amul_butter = Product(name="amul butter")
    db.add(amul_butter)
    db.commit()
    db.refresh(amul_butter)


links = [
    (nutella.id,      blinkit.id, "https://blinkit.com/s/?q=nutella"),
    (amul_butter.id,  blinkit.id, "https://blinkit.com/s/?q=amul%20butter"),
    (nutella.id,      zepto.id,   "https://www.zepto.com/search?query=nutella"),
    (amul_butter.id,  zepto.id,   "https://www.zepto.com/search?query=amul%20butter"),
]


for product_id, platform_id, url in links:
    exists = db.query(ProductPlatform).filter(
        ProductPlatform.product_id == product_id,
        ProductPlatform.platform_id == platform_id
    ).first()

    #if any of the 4 combinations of the links is not in ProductPlatform , add it
    if not exists:
        pp = ProductPlatform(product_id=product_id, platform_id=platform_id, product_url=url)
        db.add(pp)
        db.commit()

db.close()
print("Seed complete!")