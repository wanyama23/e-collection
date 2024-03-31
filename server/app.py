from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Cart, Products, Sale, Setting, NewSale, Supplier, User, Purchase, Customer

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return make_response(jsonify({"msg": "welcome"}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)