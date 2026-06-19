from sqlalchemy import Column, Float, ForeignKey , Integer , String , DateTime , Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Product(Base):
    __tablename__ = "products"
    id=Column(Integer , primary_key=True , index=True)
    name=Column(String , nullable=False)
    image_url=Column(String)


class Platform(Base):
    __tablename__ = "platforms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


#this table connects product to a platform
class ProductPlatform(Base):
    __tablename__ = "product_platform"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    product_url = Column(String)


#this price table stores various prices of same product on same platform
#this table is made to add the feature of showing the user the trend analysis
#product_platform_id is the attribute that helps us to identify a particular combination in productplatform table
#ex -> in product platform we have 1. {nutella , 1(blinkit) , url}. It can have many prices
#so in price table we will have product_platform_id = 1 and its various prices
class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    product_platform_id = Column(Integer, ForeignKey("product_platform.id"))
    price = Column(Float)
    in_stock = Column(Boolean, default=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)

#utcnow without () means that SQLAlchemy calls at insert time and not at class definition time