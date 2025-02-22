import os
import requests
import pandas as pd
from typing import List, Dict, Union
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from abc import ABC, abstractmethod
from models import Product, DBProduct, Base  # Ensure models.py defines necessary classes

# Database setup
DATABASE_URL = "sqlite:///products.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Abstract class for Product Extractor
class ProductExtractor(ABC):
    @abstractmethod
    def extract(self, product) -> Dict[str, Union[str, int, None]]:
        pass


# Abstract Data Storage
class DataStorage(ABC):
    @abstractmethod
    def save(self, data: List[Dict[str, Union[str, int, None]]]):
        pass


# Abstract Scraper Class
class Scraper(ABC):
    @abstractmethod
    def scrape(self) -> List[Dict[str, Union[str, int, None]]]:
        pass



# Concrete Implementation of Product Extractor
class TrendyolProductExtractor(ProductExtractor):
    def extract(self, product) -> Dict[str, Union[str, int, None]]:
        try:
            product_brand = product.find('span', {'data-testid': 'product-brand'})
            product_name_text = product.find('span', {'data-testid': 'product-name-text'})
            if not (product_brand and product_name_text):
                return None

            product_name = f"{product_brand.text.strip()} {product_name_text.text.strip()}"
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
            rating_count = "".join([v for v in rating_count_element.text.strip() if
                                    v != '(' and v != ')']) if rating_count_element else "N/A"
            promotions = [promo.find('span', class_='promotion-name').text.strip() for promo in
                          product.find_all('div', class_='promotion') if promo.find('span', class_='promotion-name')]
            promotions_str = ", ".join(promotions) if promotions else "N/A"

            return {
                'Product_Name': product_name,
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


# Concrete Scraper Implementation for Trendyol
class TrendyolScraper(Scraper):
    def __init__(self, extractor: ProductExtractor):
        self.extractor = extractor
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self) -> List[Dict[str, Union[str, int, None]]]:
        all_product_data = []
        for i in range(2, 4):  # Adjust the range as needed
            trendyol_url = f'https://www.trendyol.com/en/sr?wg=2&pi={i}'
            response = requests.get(trendyol_url, headers=self.headers)
            if response.status_code != 200:
                print(f"Failed to retrieve data for page {i}. Status code: {response.status_code}")
                continue
            print(f"Request successful for page {i}!")
            soup = BeautifulSoup(response.text, 'html.parser')
            product_blocks = soup.find_all('div', {'data-testid': 'info-with-rrp'})

            product_data = [self.extractor.extract(product) for product in product_blocks]
            product_data = [data for data in product_data if data is not None]
            all_product_data.extend(product_data)

        return all_product_data


# CSV Storage Implementation
class CSVStorage(DataStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, data: List[Dict[str, Union[str, int, None]]]):
        df = pd.DataFrame(data)
        df.to_csv(self.file_path, index=False)
        print(f"Data successfully saved to {self.file_path}")


# Database Storage Implementation
class DatabaseStorage(DataStorage):
    def save(self, data: List[Dict[str, Union[str, int, None]]]):
        db = SessionLocal()
        try:
            for product in data:
                db_product = DBProduct(
                    product_name=product['Product_Name'],
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


# Main Execution
if __name__ == "__main__":
    extractor = TrendyolProductExtractor()
    scraper = TrendyolScraper(extractor)
    csv_storage = CSVStorage("trendyol_products.csv")
    db_storage = DatabaseStorage()
    data = scraper.scrape()
    csv_storage.save(data)
    db_storage.save(data)


