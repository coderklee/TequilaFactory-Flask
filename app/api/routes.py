from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Tequila, drink_schema, drinks_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/inventory', methods = ['POST'])
@token_required
def create_drink(current_user_token):
    brand = request.json['brand']
    color = request.json['color']
    region = request.json['region']
    alcohol = request.json['alcohol']
    price = request.json['price']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    drink = Tequila(brand, color, region, alcohol, price, user_token = user_token )

    db.session.add(drink)
    db.session.commit()

    response = drink_schema.dump(drink)
    return jsonify(response)

@api.route('/inventory', methods = ['GET'])
@token_required
def get_drinks(current_user_token):
    a_user = current_user_token.token
    drinks = Tequila.query.filter_by(user_token = a_user).all()
    response = drinks_schema.dump(drinks)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['GET'])
@token_required
def get_single_drink(current_user_token, id):
    drink = Tequila.query.get(id)
    response = drink_schema.dump(drink)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    drink = Tequila.query.get(id) 
    drink.brand = request.json['brand']
    drink.color = request.json['color']
    drink.region = request.json['region']
    drink.alcohol = request.json['alcohol']
    drink.price = request.json['price']
    drink.user_token = current_user_token.token

    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    drink = Tequila.query.get(id)
    db.session.delete(drink)
    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)