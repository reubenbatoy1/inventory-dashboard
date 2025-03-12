from app import app, db, Product, Sale, Purchase
from datetime import datetime

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Add sample products
        sample_products = [
            Product(name='PE Uniform', quantity=30, price=15000, category='uniform'),
            Product(name='School Uniform', quantity=20, price=25000, category='uniform'),
            Product(name='Laboratory Uniform', quantity=100, price=499, category='uniform'),
            Product(name='Physics Book', quantity=200, price=250, category='book'),
            Product(name='Chemistry Book', quantity=25, price=2000, category='book'),
            Product(name='Calculator', quantity=50, price=999, category='others'),
            Product(name='School Supplies Set', quantity=75, price=1500, category='others')
        ]
        db.session.add_all(sample_products)
        db.session.commit()
        print("✓ Added sample products")

        # Add sample sales
        sample_sales = [
            Sale(product_id=1, quantity=5, total_price=75000),
            Sale(product_id=2, quantity=8, total_price=200000),
            Sale(product_id=4, quantity=15, total_price=3750)
        ]
        db.session.add_all(sample_sales)
        db.session.commit()
        print("✓ Added sample sales")

        # Add sample purchases
        sample_purchases = [
            Purchase(product_id=1, quantity=10, cost=120000),
            Purchase(product_id=2, quantity=15, cost=300000),
            Purchase(product_id=4, quantity=50, cost=10000)
        ]
        db.session.add_all(sample_purchases)
        db.session.commit()
        print("✓ Added sample purchases")

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("✓ Database initialization complete!")
