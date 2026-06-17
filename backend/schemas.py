#pydantic schemas -> response shapes
from pydantic import BaseModel
from datetime import datetime


class ProductOut(BaseModel):
    id : int
    name : str
    #using none because it can be empty
    image_url : str | None= None

    #pydantic can now read attributes directly from an object
    class Config:
        from_attributes = True


class PriceOut(BaseModel):
    platform_name : str
    price : float
    in_stock : bool
    scraped_at : datetime

    class Config:
        from_attributes = True