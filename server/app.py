from flask import Flask, make_response, jsonify, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


from models import db, Admin, Product, Sale, NewSale, Supplier, Purchase, Customer

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/')
def home():
    return make_response(jsonify({"msg": "welcome"}), 200)



# @app.route('/admin', methods=['POST'])
# def create_admin():
#     data = request.get_json()
#     new_admin = Admin(
#         username=data['username'],
#         email=data['email'],
#         contact=data.get('contact'),  # Optional field
#         password=data['password']
#     )
#     db.session.add(new_admin)
#     db.session.commit()
#     return jsonify({'message': 'Admin created successfully'}), 201


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        # Retrieve all admins (list view)
        admins = Admin.query.all()
        admin_list = [{'id': admin.id, 'username': admin.username, 'email': admin.email} for admin in admins]
        return jsonify(admin_list), 200
    elif request.method == 'POST':
        # Create a new admin
        data = request.get_json()
        new_admin = Admin(
            username=data['username'],
            email=data['email'],
            contact=data.get('contact'),  # Optional field
            password=data['password']
        )
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({'message': 'Admin created successfully'}), 201

@app.route('/admin/<int:admin_id>', methods=['GET', 'PUT', 'DELETE'])
def admin_details(admin_id):
    admin = Admin.query.get_or_404(admin_id)
    if request.method == 'GET':
        # Retrieve admin details (single view)
        return jsonify({'id': admin.id, 'username': admin.username, 'email': admin.email}), 200
    elif request.method == 'PUT':
        # Update admin details
        data = request.get_json()
        admin.username = data['username']
        admin.email = data['email']
        admin.contact = data.get('contact')  # Optional field
        db.session.commit()
        return jsonify({'message': 'Admin updated successfully'}), 200
    elif request.method == 'DELETE':
        # Delete an admin
        db.session.delete(admin)
        db.session.commit()
        return jsonify({'message': 'Admin deleted successfully'}), 200
    
# ......................AUTHENTICATION................................
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = Admin(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Admin.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401    

# @app.route('/logout', methods=['POST'])
# @jwt_required()
# def logout():
#     # You can add any additional logout logic here
#     return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
   
    return jsonify({'message': 'Logged out successfully'}), 200




# Create a route to get all products
# @app.route('/products', methods=['GET'])
# def get_products():
#     products = Product.query.all()
#     serialized_products = [product.to_dict() for product in products]
#     return jsonify(serialized_products)



# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')

#         hashed_password = generate_password_hash(password, method='sha256')
#         new_admin = Admin(username=username, email=email, password=hashed_password)

#         db.session.add(new_admin)
#         db.session.commit()

#         flash('Account created successfully!', 'success')
#         return redirect(url_for('login'))

#     return render_template('signup.html')  # Create a signup form template

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         admin = Admin.query.filter_by(email=email).first()

#         if admin and check_password_hash(admin.password, password):
#             # Log in the user (you can use Flask-Login for session management)
#             flash('Logged in successfully!', 'success')
#             return redirect(url_for('dashboard'))

#         flash('Login failed. Please check your credentials.', 'danger')

#     return render_template('login.html')  # Create a login form template

# @app.route('/dashboard')
# def dashboard():
#     # Display the admin dashboard (requires authentication)
#     return render_template('dashboard.html')  # Create a dashboard template

# ,,,,,,,,,,,,,,,,,,,,,, PURCHASES ROUTE,,,,,,,,,,,,,,,,,,,,,,,,,
@app.route('/purchases', methods=['POST'])
def create_purchase():
    data = request.get_json()
    if not all(key in data for key in ('product_id', 'customer_id', 'quantity')):
        return jsonify(message="Missing required fields"), 400

    new_purchase = Purchase(
        product_id=data['product_id'],
        customer_id=data['customer_id'],
        quantity=data['quantity']
    )
    db.session.add(new_purchase)
    db.session.commit()
    return jsonify(message="Purchase created successfully", purchase_id=new_purchase.id), 201

@app.route('/purchases/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify(message="Purchase not found"), 404
    # Serialize the purchase data (you can use a schema or manual serialization)
    return jsonify(purchase={
        'id': purchase.id,
        'product_id': purchase.product_id,
        'customer_id': purchase.customer_id,
        'quantity': purchase.quantity,
        'purchase_date': purchase.purchase_date.isoformat()  # Convert to ISO format
    }), 200

@app.route('/purchases/<int:purchase_id>', methods=['PUT'])
def update_purchase(purchase_id):
    data = request.get_json()
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify(message="Purchase not found"), 404

    # Update fields if provided in the request data
    purchase.product_id = data.get('product_id', purchase.product_id)
    purchase.customer_id = data.get('customer_id', purchase.customer_id)
    purchase.quantity = data.get('quantity', purchase.quantity)
    db.session.commit()
    return jsonify(message="Purchase updated successfully"), 200

@app.route('/purchases/<int:purchase_id>', methods=['DELETE'])
def delete_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify(message="Purchase not found"), 404
    db.session.delete(purchase)
    db.session.commit()
    return jsonify(message="Purchase deleted successfully"), 200


# ,,,,,,,,,,,,,,,,,,,,,,,,SUPPLIERS ROUTE,,,,,,,,,,,,,,,,,,,,,,,,,,,,
# Create a new supplier
@app.route('/suppliers', methods=['POST'])
def create_supplier():
    data = request.get_json()
    new_supplier = Supplier(**data)
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({"message": "Supplier created successfully!"}), 201

# Get all suppliers
@app.route('/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([supplier.__repr__() for supplier in suppliers]), 200

# Get a specific supplier by ID
@app.route('/suppliers/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify({"message": "Supplier not found"}), 404
    return jsonify(supplier.__repr__()), 200

# Update a supplier by ID
@app.route('/suppliers/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify({"message": "Supplier not found"}), 404
    data = request.get_json()
    supplier.name = data.get('name', supplier.name)
    supplier.email = data.get('email', supplier.email)
    supplier.contact = data.get('contact', supplier.contact)
    supplier.address = data.get('address', supplier.address)
    db.session.commit()
    return jsonify({"message": "Supplier updated successfully!"}), 200

# Delete a supplier by ID
@app.route('/suppliers/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify({"message": "Supplier not found"}), 404
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({"message": "Supplier deleted successfully!"}), 200



# Create a new sale
@app.route('/sales', methods=['POST'])
def create_sale():
    data = request.get_json()
    new_sale = Sale(**data)
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({"message": "Sale created successfully!"}), 201

# Get all sales
@app.route('/sales', methods=['GET'])
def get_sales():
    sales = Sale.query.all()
    return jsonify([sale.__repr__() for sale in sales]), 200

# Get a specific sale by ID
@app.route('/sales/<int:sale_id>', methods=['GET'])
def get_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"message": "Sale not found"}), 404
    return jsonify(sale.__repr__()), 200

# Update a sale by ID
@app.route('/sales/<int:sale_id>', methods=['PUT'])
def update_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"message": "Sale not found"}), 404
    data = request.get_json()
    sale.product_id = data.get('product_id', sale.product_id)
    sale.customer_id = data.get('customer_id', sale.customer_id)
    sale.quantity = data.get('quantity', sale.quantity)
    db.session.commit()
    return jsonify({"message": "Sale updated successfully!"}), 200

# Delete a sale by ID
@app.route('/sales/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"message": "Sale not found"}), 404
    db.session.delete(sale)
    db.session.commit()
    return jsonify({"message": "Sale deleted successfully!"}), 200



# ......................NEW SALE ROUTE......................
# Create a new sale
@app.route('/add_sales', methods=['POST'])
def add_sales():
    data = request.get_json()
    new_sale = NewSale(**data)
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({"message": "Sale created successfully!"}), 201

# Get all sales
@app.route('/fetch_sales', methods=['GET'])
def fetch_sales():
    sales = NewSale.query.all()
    return jsonify([sale.__repr__() for sale in sales]), 200

# # Get a specific sale by ID
@app.route('/fetch_sales/<int:sale_id>', methods=['GET'], endpoint='get_sale_by_id')
def get_sale_by_id(sale_id):
    fetch_sales = NewSale.query.get(sale_id)
    if not fetch_sales:
        return jsonify({"message": "Sale not found"}), 404
    return jsonify(fetch_sales.__repr__()), 200



@app.route('/sales/<int:sale_id>', methods=['PUT'])
def update_sale_by_id(sale_id):
    try:
        sale = NewSale.query.get(sale_id)
        if not sale:
            return jsonify({"message": "Sale not found"}), 404
        data = request.get_json()
        sale.product_id = data.get('product_id', sale.product_id)
        sale.customer_id = data.get('customer_id', sale.customer_id)
        sale.quantity = data.get('quantity', sale.quantity)
        db.session.commit()
        return jsonify({"message": "Sale updated successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


# Delete a sale by ID
@app.route('/sales/<int:sale_id>', methods=['DELETE'])
def delete_sale_by_id(sale_id):
    try:
        sale = NewSale.query.get(sale_id)
        if not sale:
            return jsonify({"message": "Sale not found"}), 404
        db.session.delete(sale)
        db.session.commit()
        return jsonify({"message": "Sale deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500



# ,,,,,,,,,,,,,,,,,,,.......,CUSTOMERS ROUTE................................
@app.route('/customers', methods=['GET'])
def get_customers():
    # Retrieve all customers from the database
    customers = Customer.query.all()
    customer_list = [{'id': c.id, 'name': c.name, 'email': c.email} for c in customers]
    return jsonify(customer_list)

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    # Retrieve a specific customer by ID
    customer = Customer.query.get_or_404(customer_id)
    return jsonify({'id': customer.id, 'name': customer.name, 'email': customer.email})

@app.route('/customers', methods=['POST'])
def create_customer():
    # Create a new customer
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], contact=data.get('contact'), address=data.get('address'))
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully', 'id': new_customer.id}), 201

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    # Retrieve the existing customer
    customer = Customer.query.get_or_404(customer_id)

    # Update customer data based on request JSON
    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.contact = data.get('contact', customer.contact)
    customer.address = data.get('address', customer.address)

    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    # Retrieve the customer to be deleted
    customer = Customer.query.get_or_404(customer_id)

    # Delete the customer
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})




@event.listens_for(NewSale, 'after_insert')
def add_to_sales(mapper, connection, target):
    # Create a new Sale record based on the NewSale data
    new_sale = Sale(
        product_id=target.product_id,
        customer_id=target.customer_id,
        quantity=target.quantity,
        sale_date=target.sale_date
    )
    # Add the new sale to the session
    db.session.add(new_sale)
    db.session.commit()

# Now, when a NewSale record is inserted, it will automatically create a corresponding Sale record.



if __name__ == '__main__':
    app.run(port=5555, debug=True)












# @app.route('/purchases', methods=['POST'])
# def create_purchase():
#     data = request.get_json()
#     new_purchase = Purchase(
#         product_id=data['product_id'],
#         customer_id=data['customer_id'],
#         quantity=data['quantity']
#     )
#     db.session.add(new_purchase)
#     db.session.commit()
#     return jsonify(message="Purchase created successfully"), 201

# @app.route('/purchases/<int:purchase_id>', methods=['GET'])
# def get_purchase(purchase_id):
#     purchase = Purchase.query.get(purchase_id)
#     if not purchase:
#         return jsonify(message="Purchase not found"), 404
#     return jsonify(purchase=purchase.__repr__()), 200

# @app.route('/purchases/<int:purchase_id>', methods=['PUT'])
# def update_purchase(purchase_id):
#     data = request.get_json()
#     purchase = Purchase.query.get(purchase_id)
#     if not purchase:
#         return jsonify(message="Purchase not found"), 404
#     purchase.product_id = data.get('product_id', purchase.product_id)
#     purchase.customer_id = data.get('customer_id', purchase.customer_id)
#     purchase.quantity = data.get('quantity', purchase.quantity)
#     db.session.commit()
#     return jsonify(message="Purchase updated successfully"), 200

# @app.route('/purchases/<int:purchase_id>', methods=['DELETE'])
# def delete_purchase(purchase_id):
#     purchase = Purchase.query.get(purchase_id)
#     if not purchase:
#         return jsonify(message="Purchase not found"), 404
#     db.session.delete(purchase)
#     db.session.commit()
#     return jsonify(message="Purchase deleted successfully"), 200




# # Get a specific sale by ID
# @app.route('/fetch_sales/<int:sale_id>', methods=['GET'])
# def fetch_sales(sale_id):
#     fetch_sales = NewSale.query.get(sale_id)
#     if not fetch_sales:
#         return jsonify({"message": "Sale not found"}), 404
#     return jsonify(fetch_sales.__repr__()), 200



# @app.route('/sales/<int:sale_id>', methods=['PUT'])
# def update_sale(sale_id):
#     try:
#         sale = NewSale.query.get(sale_id)
#         if not sale:
#             return jsonify({"message": "Sale not found"}), 404
#         data = request.get_json()
#         sale.product_id = data.get('product_id', sale.product_id)
#         sale.customer_id = data.get('customer_id', sale.customer_id)
#         sale.quantity = data.get('quantity', sale.quantity)
#         db.session.commit()
#         return jsonify({"message": "Sale updated successfully!"}), 200
#     except Exception as e:
#         return jsonify({"message": f"An error occurred: {str(e)}"}), 500


# # Update a sale by ID
# @app.route('/sales/<int:sale_id>', methods=['PUT'])
# def update_sale(sale_id):
#     sale = NewSale.query.get(sale_id)
#     if not sale:
#         return jsonify({"message": "Sale not found"}), 404
#     data = request.get_json()
#     sale.product_id = data.get('product_id', sale.product_id)
#     sale.customer_id = data.get('customer_id', sale.customer_id)
#     sale.quantity = data.get('quantity', sale.quantity)
#     db.session.commit()
#     return jsonify({"message": "Sale updated successfully!"}), 200
