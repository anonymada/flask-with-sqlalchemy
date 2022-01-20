# wsgi.py
# pylint: disable=missing-docstring
BASE_URL = '/api/v1'

from flask import Flask, request, abort, jsonify
from config import Config
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow  # NEW LINE (L'ordre est important ici !)
db = SQLAlchemy(app)
ma = Marshmallow(app)  # NEW LINE

from models import Product
from schemas import many_product_schema
from schemas import one_product_schema

migrate = Migrate(app, db)
@app.route('/', methods=['GET'])
def hello():
    return "Hello World!", 200

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = db.session.query(Product).get(product_id)
    return one_product_schema.jsonify(product), 200

@app.route(f'{BASE_URL}/products', methods=['POST'])
def create_one_product():
    new_product = Product()
    new_product.name = request.form.get('name')
    db.session.add(new_product)
    db.session.commit()
    products = db.session.query(Product).all()
    return many_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['DELETE'])
def delete_one_product(product_id):
    product = db.session.query(Product).get(product_id)
    db.session.delete(product)
    db.session.commit()
    products = db.session.query(Product).all()
    return many_product_schema.jsonify(products), 200
    
@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['PATCH'])
def update_one_product(product_id):
    product = db.session.query(Product).get(product_id)
    product.name = request.form.get('name')
    db.session.commit()
    products = db.session.query(Product).all()
    return many_product_schema.jsonify(products), 200