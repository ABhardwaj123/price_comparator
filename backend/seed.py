#this seed script is some manual insertion of starting data into database.
#run it once to populate the tables

from database import SessionLocal
from models import Platform , Product , ProductPlatform

db = SessionLocal()



blinkit = Platform(name="blinkit")
db.add(blinkit)
db.commit()
db.refresh(blinkit)



nutella = Product(name="nutella")
db.add(nutella)
db.commit()
db.refresh(nutella)


amul_butter = Product(name="amul butter")
db.add(amul_butter)
db.commit()
db.refresh(amul_butter)



pf1 = ProductPlatform(
    product_id=nutella.id,
    platform_id=blinkit.id,
    product_url="https://blinkit.com/s/?q=nutella"
)
db.add(pf1)
db.commit()


pf2 = ProductPlatform(
    product_id=amul_butter.id,
    platform_id=blinkit.id,
    product_url="https://blinkit.com/s/?q=amul%20butter"
)
db.add(pf2)
db.commit()

db.close()
