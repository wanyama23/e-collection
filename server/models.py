from flask import Flask, flash
# from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
# from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import MetaData


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
# db = SQLAlchemy()
# class User(db.Model, UserMixin):

# 
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}')"

# class Admin(db.Model):
#     __tablename__ = "admin"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     contact = db.Column(db.String)
#     password = db.Column(db.String(60), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

#     def __repr__(self):
#         return f"Admin('{self.username}', '{self.email}')"

class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    def __repr__(self):
        return f"Customer(id={self.id}, name='{self.name}', email='{self.email}')"
    

class Supplier(db.Model):
    __tablename__ = "supplier"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    def __repr__(self):
        return f"Supplier(id={self.id}, name='{self.name}', email='{self.email}')"


# class Purchase(db.Model):
#     __tablename__ = "purchase"
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, nullable=False)
#     customer_id = db.Column(db.Integer, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     purchase_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)

#     def __repr__(self):
#         return f"Purchase(id={self.id}, product_id={self.product_id}, customer_id={self.customer_id})"

class Purchase(db.Model):
    __tablename__ = "purchase"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    def __repr__(self):
        return f"Purchase(id={self.id}, product_id={self.product_id}, customer_id={self.customer_id})"






class Sale(db.Model):
    __tablename__ = "sale"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    # Define a foreign key relationship to the Product table
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', back_populates='sales')

    def __repr__(self):
        return f"Sale(id={self.id}, product_id={self.product_id}, customer_id={self.customer_id})"


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    # Define a one-to-many relationship with Sale
    sales = db.relationship('Sale', back_populates='product')

    def __repr__(self):
        return f"Products('{self.name.data}', '{self.price.data}')"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'image_url': self.image_url,
            'quantity': self.quantity,
            'admin_id': self.admin_id
        }



class NewSale(db.Model):
    __tablename__ = "new_sale"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    def __repr__(self):
        return f"NewSale(id={self.id}, product_id={self.product_id}, customer_id={self.customer_id})"














# class Sale(db.Model):
#     __tablename__ = "sale"
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, nullable=False)
#     customer_id = db.Column(db.Integer, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     sale_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)

#     def __repr__(self):
#         return f"Sale(id={self.id}, product_id={self.product_id}, customer_id={self.customer_id})"
    

# class Product(db.Model):
#     __tablename__ = "products"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     image_url = db.Column(db.String, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    
#     # orders = db.relationship('Order', back_populates='products')
#     # serialize_rules = ('-orders.products',)
#     sales = db.relationship('Sales', back_populates='products')
#     serialize_rules = ('-sales.products',)
    
#     def __repr__(self):
#         return f"Products('{self.name.data}', '{self.price.data}')"
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'price': self.price,
#             'description': self.description,
#             'image_url': self.image_url,
#             'quantity': self.quantity,
#             'admin_id': self.admin_id
#         }    


# class Setting(db.Model):
#     __tablename__ = "setting"
#     id = db.Column(db.Integer, primary_key=True)
#     setting_name = db.Column(db.String(50), nullable=False)
#     setting_value = db.Column(db.String(200))

#     def __repr__(self):
#         return f"Setting(id={self.id}, setting_name='{self.setting_name}', setting_value='{self.setting_value}')"






# class Products(db.Model):
#     __tablename__ = "products"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     description = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f"Products('{self.name}', '{self.price}')"

# 

    # def __repr__(self):
    #     return f"Cart('Product id:{self.product_id}','id: {self.id}','User id:{self.user_id}'')"





# from flask import Flask, flash
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy_serializer import SerializerMixin
# from flask_migrate import Migrate
# from sqlalchemy import Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship
# # from flask_login import UserMixin
# from datetime import datetime
# from sqlalchemy import MetaData
# from app import db, bcrypt, flash


# # from setup import db, bcrypt, flash
# # from sqlalchemy import Column, Integer, ForeignKey
# # from sqlalchemy_serializer import SerializerMixin
# # from sqlalchemy.ext.hybrid import hybrid_property
# # from sqlalchemy.orm import relationship
# # from datetime import datetime




# # class User(db.Model, UserMixin):

# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })
# db = SQLAlchemy(metadata=metadata)
# class Admin(db.Model, SerializerMixin):
#     __tablename__ = "admin"    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=False, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)
#     contact = db.Column(db.String)
#     address = db.Column(db.String, nullable=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     products = db.relationship('Product', backref='admin', lazy=True)
#     _password_hash = db.Column(db.String, nullable=False)

#     @hybrid_property
#     def password_hash(self):
#         return{"message": "You can't view password hashes"}
    
#     @password_hash.setter
#     def password_hash(self, password):
#         our_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
#         self._password_hash = our_hash.decode('utf-8')

#     def validate_password(self, password):
#         is_valid = bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
#         return is_valid

#     def __repr__(self):
#         return f"Admin('{self.name}', '{self.email}', '{self.id}')"
    


# class User(db.Model, SerializerMixin):
#     __tablename__ = "users"    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=False, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)
#     contact = db.Column(db.String)
#     role = db.Column(db.String)
#     address = db.Column(db.String, nullable=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     orders = db.relationship('Order', backref='users', lazy=True)
#     cart = db.relationship('Cart', backref='users', lazy=True)

#     _password_hash = db.Column(db.String, nullable=False)
#     @hybrid_property
#     def password_hash(self):
#         return{"message": "You can't view password hashes"}
    
#     @password_hash.setter
#     def password_hash(self, password):
#         our_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
#         self._password_hash = our_hash.decode('utf-8')

#     def validate_password(self, password):
#         is_valid = bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
#         return is_valid

#     def add_to_orders(self,product_id):
#         item_to_add = Order(product_id=product_id, user_id=self.id)
#         db.session.add(item_to_add)
#         db.session.commit()
#         flash('Your order has been made succesfully!', 'success')

#     def __repr__(self):
#         return f"User('{self.name}', '{self.email}','{self.id}')"



# class Product(db.Model, SerializerMixin):
#     __tablename__ = "products"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     category = db.Column(db.String, nullable=False)
#     brand = db.Column(db.String, nullable=False)
#     image_url = db.Column(db.String, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    
#     orders = db.relationship('Order', back_populates='products')
#     serialize_rules = ('-orders.products',)
#     sales = db.relationship('Sales', back_populates='products')
#     serialize_rules = ('-sales.products',)
    
#     def __repr__(self):
#         return f"Products('{self.name.data}', '{self.price.data}')"
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'price': self.price,
#             'description': self.description,
#             'category': self.category,
#             'brand': self.brand,
#             'image_url': self.image_url,
#             'quantity': self.quantity,
#             'admin_id': self.admin_id
#         }

# class Order(db.Model, SerializerMixin):
#     __tablename__ = 'orders'
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False, default=1)
#     review = db.Column(db.String(200))

#     products = db.relationship('Product', back_populates='orders')
#     serialize_rules = ('-products.orders',)

#     def __repr__(self):
#         return f"Order('Product id:{self.product_id}','id: {self.id}','User id:{self.user_id}')"
    
# class Cart(db.Model, SerializerMixin):
#     __tablename__ = 'cart'
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# class Newsletter(db.Model, SerializerMixin):
#     __tablename__ = 'newsletters'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#     def __repr__(self):
#         return f"Newsletter subscriber('{self.email}', ID:'{self.user_id}')"

   
# class Sales(db.Model, SerializerMixin):
#     __tablename__ = 'sales'
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
#     # quantity = db.Column(db.Integer)
#     total_sales = db.Column(db.Integer)
#     date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

#     products = db.relationship('Product', back_populates='sales')
#     serialize_rules = ('-products.sales',)
    





# class Cart(db.Model):
#     __tablename__ = 'cart'
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = relationship("User", back_populates="cart")
#     quantity = db.Column(db.Integer, nullable=False, default=1)



# class User(db.Model):
#     __tablename__ = "user"    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), unique=False, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     contact = db.Column(db.String)
#     password = db.Column(db.String(60), nullable=False)
#     address = db.relationship("Location", backref="user")
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     cart = db.relationship('Cart', backref='user', lazy=True)

#     def add_to_cart(self,product_id):
#         item_to_add = Cart(product_id=product_id, user_id=self.id)
#         db.session.add(item_to_add)
#         db.session.commit()
#         flash('Your item has been added to your cart!', 'success')

#     def __repr__(self):
#         return f"User('{self.firstname}','{self.lastname}', '{self.email}','{self.id}')"