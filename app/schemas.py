from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    articul: str = Field(..., example="211695539")
    name: str
    price: float
    rating: float
    total_quantity: int

class ProductRequest(BaseModel):
    articul: str = Field(..., example="211695539")

class ProductOut(BaseModel):
    articul: str
    name: str
    price: float
    rating: float
    total_quantity: int

    class Config:
        from_attributes = True  # чтобы можно было напрямую брать из модели SQLAlchemy
