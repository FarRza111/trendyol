"""
Test module for models.py
Tests the Product and DBProduct models
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product, DBProduct, Base


class TestProductModel:
    """Test cases for the Product Pydantic model"""

    def test_product_creation(self):
        """Test creating a valid Product instance"""
        product = Product(
            Product_Name="Test Product",
            Price="100 TL",
            Added_to_Cart="50",
            Favorites="25",
            Rating_Score="4.5",
            Rating_Count="100",
            Promotions="Free Shipping"
        )
        
        assert product.Product_Name == "Test Product"
        assert product.Price == "100 TL"
        assert product.Added_to_Cart == "50"
        assert product.Favorites == "25"
        assert product.Rating_Score == "4.5"
        assert product.Rating_Count == "100"
        assert product.Promotions == "Free Shipping"

    def test_product_with_na_values(self):
        """Test creating a Product with N/A values"""
        product = Product(
            Product_Name="Test Product",
            Price="N/A",
            Added_to_Cart="N/A",
            Favorites="N/A",
            Rating_Score="N/A",
            Rating_Count="N/A",
            Promotions="N/A"
        )
        
        assert product.Price == "N/A"
        assert product.Added_to_Cart == "N/A"
        assert product.Favorites == "N/A"


class TestDBProductModel:
    """Test cases for the DBProduct SQLAlchemy model"""

    @pytest.fixture
    def db_session(self):
        """Create an in-memory SQLite database for testing"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        yield session
        session.close()

    def test_db_product_creation(self, db_session):
        """Test creating and saving a DBProduct to database"""
        db_product = DBProduct(
            product_name="Test Product",
            price="100 TL",
            added_to_cart="50",
            favorites="25",
            rating_score="4.5",
            rating_count="100",
            promotions="Free Shipping"
        )
        
        db_session.add(db_product)
        db_session.commit()
        
        # Query the product back
        saved_product = db_session.query(DBProduct).first()
        assert saved_product is not None
        assert saved_product.product_name == "Test Product"
        assert saved_product.price == "100 TL"
        assert saved_product.id is not None

    def test_db_product_repr(self, db_session):
        """Test the __repr__ method of DBProduct"""
        db_product = DBProduct(
            product_name="Test Product",
            price="100 TL",
            added_to_cart="50",
            favorites="25",
            rating_score="4.5",
            rating_count="100",
            promotions="Free Shipping"
        )
        
        db_session.add(db_product)
        db_session.commit()
        db_session.refresh(db_product)
        
        repr_str = repr(db_product)
        assert "Test Product" in repr_str
        assert "100 TL" in repr_str
        assert f"id={db_product.id}" in repr_str

    def test_multiple_products_in_db(self, db_session):
        """Test adding multiple products to database"""
        products = [
            DBProduct(
                product_name=f"Product {i}",
                price=f"{100 * i} TL",
                added_to_cart=str(i * 10),
                favorites=str(i * 5),
                rating_score="4.5",
                rating_count=str(i * 20),
                promotions="N/A"
            )
            for i in range(1, 4)
        ]
        
        for product in products:
            db_session.add(product)
        db_session.commit()
        
        all_products = db_session.query(DBProduct).all()
        assert len(all_products) == 3
        assert all_products[0].product_name == "Product 1"
        assert all_products[2].product_name == "Product 3"
