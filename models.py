from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class Product(BaseModel):
    Product_Name: str
    Price: str
    Added_to_Cart: str
    Favorites: str
    Rating_Score: str
    Rating_Count: str
    Promotions: str

# SQLAlchemy model for Product
Base = declarative_base()


class DBProduct(Base):
    """
    SQLAlchemy model for the Product table.
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
    product_name = Column(String, nullable=False)               # Product_Name
    price = Column(String, nullable=False)                      # Price
    added_to_cart = Column(String, nullable=False)              # Added_to_Cart
    favorites = Column(String, nullable=False)                 # Favorites
    rating_score = Column(String, nullable=False)              # Rating_Score
    rating_count = Column(String, nullable=False)              # Rating_Count
    promotions = Column(String, nullable=False)                # Promotions

    def __repr__(self):
        return f"<Product(id={self.id}, product_name='{self.product_name}', price='{self.price}')>"