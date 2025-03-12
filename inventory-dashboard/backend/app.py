from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sales = db.relationship('Sale', backref='product', lazy=True)
    purchases = db.relationship('Purchase', backref='product', lazy=True)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/api/products', methods=['GET', 'POST'])
def handle_products():
    if request.method == 'GET':
        products = Product.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'quantity': p.quantity,
            'price': p.price,
            'category': p.category,
            'description': p.description,
            'image': p.image,
            'status': 'out' if p.quantity <= 0 else 'low' if p.quantity < 10 else 'in'
        } for p in products])
    
    if request.method == 'POST':
        data = request.json
        if data['category'] not in ['uniform', 'book', 'others']:
            return jsonify({'error': 'Invalid category. Must be uniform, book, or others'}), 400
        
        product = Product(
            name=data['name'],
            quantity=data['quantity'],
            price=data['price'],
            category=data['category'],
            description=data.get('description'),
            image=data.get('image')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully'}), 201

@app.route('/api/products/<int:id>', methods=['PUT', 'DELETE'])
def handle_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'PUT':
        data = request.json
        if 'category' in data and data['category'] not in ['uniform', 'book', 'others']:
            return jsonify({'error': 'Invalid category. Must be uniform, book, or others'}), 400
        
        for key, value in data.items():
            setattr(product, key, value)
        
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})
    
    if request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})

@app.route('/api/sales', methods=['GET', 'POST'])
def handle_sales():
    if request.method == 'GET':
        sales = Sale.query.all()
        return jsonify([{
            'id': s.id,
            'product_id': s.product_id,
            'product_name': s.product.name,
            'quantity': s.quantity,
            'total_price': s.total_price,
            'date': s.date.isoformat()
        } for s in sales])
    
    if request.method == 'POST':
        data = request.json
        product = Product.query.get_or_404(data['product_id'])
        if product.quantity < data['quantity']:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        sale = Sale(
            product_id=data['product_id'],
            quantity=data['quantity'],
            total_price=data['quantity'] * product.price
        )
        product.quantity -= data['quantity']
        
        db.session.add(sale)
        db.session.commit()
        return jsonify({'message': 'Sale recorded successfully'}), 201

@app.route('/api/purchases', methods=['GET', 'POST'])
def handle_purchases():
    if request.method == 'GET':
        purchases = Purchase.query.all()
        return jsonify([{
            'id': p.id,
            'product_id': p.product_id,
            'product_name': p.product.name,
            'quantity': p.quantity,
            'cost': p.cost,
            'date': p.date.isoformat()
        } for p in purchases])
    
    if request.method == 'POST':
        data = request.json
        product = Product.query.get_or_404(data['product_id'])
        
        purchase = Purchase(
            product_id=data['product_id'],
            quantity=data['quantity'],
            cost=data['cost']
        )
        product.quantity += data['quantity']
        
        db.session.add(purchase)
        db.session.commit()
        return jsonify({'message': 'Purchase recorded successfully'}), 201

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    products = Product.query.all()
    sales = Sale.query.all()
    purchases = Purchase.query.all()
    
    # Calculate totals
    total_inventory = sum(p.quantity for p in products)
    total_sales = sum(s.total_price for s in sales)
    total_purchases = sum(p.cost for p in purchases)
    
    # Get inventory by category
    inventory_by_category = {}
    for category in ['uniform', 'book', 'others']:
        category_products = [p for p in products if p.category == category]
        inventory_by_category[category] = {
            'count': len(category_products),
            'total_items': sum(p.quantity for p in category_products)
        }
    
    return jsonify({
        'inventory_summary': {
            'total_products': len(products),
            'total_inventory': total_inventory,
            'by_category': inventory_by_category
        },
        'sales_overview': {
            'total_sales': total_sales,
            'number_of_sales': len(sales)
        },
        'purchase_overview': {
            'total_purchases': total_purchases,
            'number_of_purchases': len(purchases)
        },
        'low_stock_items': [
            {
                'id': p.id,
                'name': p.name,
                'quantity': p.quantity,
                'category': p.category
            }
            for p in products if p.quantity < 10
        ]
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
