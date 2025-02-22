import os
import requests
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict, Union
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from models import Product, DBProduct, Base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base



class Product(BaseModel):
    Product_Name: str
    Product_Brand: str
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
    product_brand = Column(String, nullable=True)              # Product_Brand
    price = Column(String, nullable=False)                      # Price
    added_to_cart = Column(String, nullable=False)              # Added_to_Cart
    favorites = Column(String, nullable=False)                 # Favorites
    rating_score = Column(String, nullable=False)              # Rating_Score
    rating_count = Column(String, nullable=False)              # Rating_Count
    promotions = Column(String, nullable=False)                # Promotions

    def __repr__(self):
        return f"<Product(id={self.id}, product_name='{self.product_name}', price='{self.price}')>"




class TrendyolScraper:

    def __init__(self, num_pages: int):
        self.num_pages = num_pages
        self.database_url = "sqlite:///products.db"
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }


    def extract_product_data(self, product) -> Dict[str, Union[str, int, None]]:
        try:
            product_brand = product.find('span', {'data-testid': 'product-brand'})
            product_name_text = product.find('span', {'data-testid': 'product-name-text'})

            if not (product_brand and product_name_text):
                return None

            # product_name = f"{product_brand.text.strip()} {product_name_text.text.strip()}"
            product_brand = product_brand.text.strip() if product_brand else 'N/A'
            product_name  = product_name_text.text.strip() if product_name_text else 'N/A'

            price_element = product.find('p', class_='selling-price')
            price = price_element.text.strip() if price_element else "N/A"

            added_to_cart_element = product.find('div', {'data-testid': 'social-proof-content-basketCount'})
            added_to_cart = added_to_cart_element.find('span').text.strip() if added_to_cart_element else "N/A"

            favorites_element = product.find('div', {'data-testid': 'social-proof-content-favoriteCount'})
            favorites = favorites_element.find('span').text.strip() if favorites_element else "N/A"

            rating_score_element = product.find('div', class_='p-rating-full')
            rating_score = (
                rating_score_element['style'].split(':')[1].strip()
                if rating_score_element and 'style' in rating_score_element.attrs and len(
                    rating_score_element['style'].split(':')) > 1
                else 'N/A'
            )

            rating_count_element = product.find('span', class_='p-total-rating-count')
            rating_count = "".join(
                [v for v in rating_count_element.text.strip() if v != '(' and v != ')']) \
                if rating_count_element \
                else "N/A"

            promotions = [promo.find('span', class_='promotion-name').text.strip()
                         for promo in product.find_all('div', class_='promotion')
                         if promo.find('span', class_='promotion-name')]
            promotions_str = ", ".join(promotions) if promotions else "N/A"

            return {
                'Product_Name': product_name,
                'Product_Brand': product_brand,
                'Price': price,
                'Added_to_Cart': added_to_cart,
                'Favorites': favorites,
                'Rating_Score': rating_score,
                'Rating_Count': rating_count,
                'Promotions': promotions_str
            }


        except Exception as e:
            print(f"Error extracting data for a product: {e}")
            return None


    def scrape_trendyol(self):
        all_product_data = pd.DataFrame()

        for i in range(1, self.num_pages + 1):
            trendyol_url = f'https://www.trendyol.com/en/sr?wg=2&pi={i}'
            response = requests.get(trendyol_url, headers=self.headers)

            if response.status_code != 200:
                print(f"Failed to retrieve data for page {i}. Status code: {response.status_code}")
                continue

            print(f"Request successful for page {i}!")
            soup = BeautifulSoup(response.text, 'html.parser')
            product_blocks = soup.find_all('div', {'data-testid': 'info-with-rrp'})

            product_data = [self.extract_product_data(product) for product in product_blocks]
            product_data = [data for data in product_data if data is not None]

            df = pd.DataFrame(product_data)
            all_product_data = pd.concat([all_product_data, df], ignore_index=True)

        return all_product_data.to_dict(orient='records')


    def save_to_csv(self):
        try:
            products = self.scrape_trendyol()
            df = pd.DataFrame(products)
            csv_file_path = "trendyol_products.csv"
            df.to_csv(csv_file_path, index=False)

            if os.path.exists(csv_file_path):
                print(f"Data successfully saved to {csv_file_path}")
            else:
                print("Failed to save CSV file")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def save_to_db(self):
        try:
            products = self.scrape_trendyol()
            db = self.SessionLocal()

            for product in products:
                db_product = DBProduct(
                    product_name=product['Product_Name'],
                    product_brand=product['Product_Brand'],
                    price=product['Price'],
                    added_to_cart=product['Added_to_Cart'],
                    favorites=product['Favorites'],
                    rating_score=product['Rating_Score'],
                    rating_count=product['Rating_Count'],
                    promotions=product['Promotions']
                )
                db.add(db_product)

            db.commit()
            print("Data successfully saved to the database")

        except Exception as e:
            db.rollback()
            print(f"An error occurred: {str(e)}")

        finally:
            db.close()


if __name__ == "__main__":
    num_pages = 50 # Set the desired number of pages to scrape
    scraper = TrendyolScraper(num_pages)
    scraper.save_to_csv()
    scraper.save_to_db()

