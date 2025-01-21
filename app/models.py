from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    articul = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=True)
    total_quantity = Column(Integer, nullable=False)
