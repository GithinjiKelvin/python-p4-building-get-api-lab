#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeriesLoc = []
    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        bakeriesLoc.append(bakery_dict)

    response = make_response(
        bakeriesLoc,
        200,
        {"Content-Type": "application/json"}
    )

    
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = bakery.to_dict()

    response = make_response(
        bakery_dict,
        200
    )
    return response

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods= BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_serialized = [baked_good.to_dict() for baked_good in baked_goods]
    return make_response(baked_goods_serialized, 200)
@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    baked_good_serialized = baked_good.to_dict()
    return make_response(baked_good_serialized, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
