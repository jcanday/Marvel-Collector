from lib2to3.pgen2 import token
from flask import Blueprint, request, jsonify
from marvel.help import token_required
from marvel.models import db, User, Character, char_schema, chars_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/test')
@token_required
def test(current_user_token):
    return {'some':'value'}


# CREATE API ROUTES
@api.route('/collections', methods = ['POST'])
@token_required
def add_character(current_user_token):
    name = request.json['name']
    desc = request.json['desc']
    comics_appeared = request.json['comics_appeared']
    super_power = request.json['super_power']
    user_token = current_user_token.token
    
    print(f"Battler: {current_user_token.token}")
    
    character = Character(name,desc,comics_appeared,super_power, user_token = user_token)

    db.session.add(character)
    db.session.commit()
    
    res = char_schema.dump(character)
    
    return jsonify(res)

@api.route('/collections' , methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    chars = Character.query.filter_by(user_token = owner).all()
    res = chars_schema.dump(chars)
    
    return jsonify(res) 


@api.route('/collections/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        char = Character.query.get(id)
        res = char_schema.dump(char)
        return jsonify(res)
        
    else:
        return jsonify({'message': "Valid Token Required"}), 401
    
    
@api.route('/collections/<id>', methods = ['POST', 'PUT'])
@token_required
def update_character(current_user_token, id):
    char = Character.query.get(id)
    
    char.name = request.json['name']
    char.desc = request.json['desc']
    char.comics_appeared = request.json['comics_appeared']
    char.super_power = request.json['super_power']
    char.user_token = current_user_token.token
    
    db.session.commit()
    
    res = char_schema.dump(char)
    
    return jsonify(res)

@api.route('/collections/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    char = Character.query.get(id)
    
    db.session.delete(char)
    
    db.session.commit()
    
    res = char_schema.dump(char)
    
    return jsonify(res)