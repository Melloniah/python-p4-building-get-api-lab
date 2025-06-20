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

    bakeries=Bakery.query.all()
    bakeries_serialized=[bakery.to_dict() for bakery in bakeries]

    response=make_response(jsonify(bakeries_serialized), 200)

    response.headers['Content-Type'] = 'application/json'

    return response

    

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if not bakery:
        return make_response(jsonify({"error": "Bakery not found"}), 404)

    bakery_serialized = bakery.to_dict()

    response = make_response(jsonify(bakery_serialized), 200)
    
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price=BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price=BakedGood.query.order_by(BakedGood.price.desc()).all()

    baked_goods_by_price_serialized =[
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        jsonify(baked_goods_by_price_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response
    
    

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        jsonify(most_expensive_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
