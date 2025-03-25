from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DATABASE_URL = "sqlite:///./inventory.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(500))
    image = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sales = relationship("Sale", back_populates="product")
    purchases = relationship("Purchase", back_populates="product")

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="sales")

class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="purchases")

# Pydantic models for request validation
class ProductCreate(BaseModel):
    name: str
    quantity: int
    price: float
    category: str
    description: Optional[str] = None
    image: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

class SaleCreate(BaseModel):
    product_id: int
    quantity: int
    total_price: float

class PurchaseCreate(BaseModel):
    product_id: int
    quantity: int
    cost: float

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

# Routes
@app.get("/api/products", response_model=List[Product])
async def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/api/products", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/api/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

@app.post("/api/sales", response_model=Sale)
async def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    db_sale = Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@app.post("/api/purchases", response_model=Purchase)
async def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    db_purchase = Purchase(**purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@app.get("/api/dashboard")
async def get_dashboard_data(db: Session = Depends(get_db)):
    # Calculate total sales
    total_sales = db.query(Sale).count()
    
    # Calculate total revenue
    total_revenue = db.query(Sale).with_entities(db.func.sum(Sale.total_price)).scalar() or 0
    
    # Get sales by category
    sales_by_category = db.query(Product.category, db.func.count(Sale.id), db.func.sum(Sale.total_price))\
        .join(Sale, Sale.product_id == Product.id)\
        .group_by(Product.category)\
        .all()
    
    # Format results
    dashboard_data = {
        "sales": {
            "value": total_sales,
            "byCategory": [{
                "category": category,
                "value": count,
                "revenue": revenue
            } for category, count, revenue in sales_by_category]
        },
        "revenue": {
            "value": total_revenue
        }
    }
    
    return dashboard_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
