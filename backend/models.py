from sqlalchemy import Column, Float, ForeignKey , Integer , String , DateTime , Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id=Column(Integer , primary_key=True , index=True)
    name=Column(String , nullable=False)
    image_url=Column(String)


class Platform(Base):
    __tablename__ = "platforms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class ProductPlatform(Base):
    __tablename__ = "product_platform"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    product_url = Column(String)


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    product_platform_id = Column(Integer, ForeignKey("product_platform.id"))
    price = Column(Float)
    in_stock = Column(Boolean, default=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)

#utcnow without () means that SQLAlchemy calls at insert time and not at class definition time