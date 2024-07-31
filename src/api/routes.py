"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Characters, Planets, Ships
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    get_user = User.query.filter_by(email=email).first()

    if not get_user:
        return jsonify({"msg": "User does not exist"}), 401
    if email != get_user.email or password != get_user.password:
        return jsonify({"msg": "Bad email or password"}), 401
    access_token = create_access_token(identity=email)
    return jsonify({'access_token':access_token, 'current_user':get_user.serialize()})

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@api.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    # Get and Show user profile data
    results_query = User.query.filter_by(email=current_user).first()
    if not results_query:
        return jsonify({"error": "User not found"}), 404
    response_body = {
        "msg": "Your user profile:",
        "results": results_query.serialize()
    }
    return jsonify(response_body), 200

# Create a route to signup a new user.
@api.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if not email or not password:
        return jsonify({"error": "Neither email nor password can be blank"}), 404

    check_email = User.query.filter_by(email = email).first()
    if check_email:
        return jsonify({"error": "Email address already exists"}), 404
    
    new_user = User(email = email, is_active = True, password = password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "New user created", "new user": new_user.serialize()}), 200

# my endpoints
# obtener todos los usuarios
@api.route('/users', methods=['GET'])
def get_all_users():
    results_query = User.query.all()
    if not results_query:
        return jsonify({"error": "Users not found"}), 404
    results = list(map(lambda item: item.serialize(),results_query))
    response_body = {
        "msg": "All good",
        "results": results
    }
    return jsonify(response_body), 200

# obtener un usuario
@api.route('/users/<int:id>', methods=['GET'])
def get_one_user(id):
    results_query = User.query.filter_by(id=id).first()
    if not results_query:
        return jsonify({"error": "User not found"}), 404
    response_body = {
        "msg": "All good",
        "results": results_query.serialize()
    }
    return jsonify(response_body), 200

# obtener todos los characters
@api.route('/characters', methods=['GET'])
def get_all_characters():
    results_query = Characters.query.all()
    if not results_query:
        return jsonify({"error": "Characters not found"}), 404
    results = list(map(lambda item: item.serialize(),results_query))
    response_body = {
        "msg": "All good",
        "results": results
    }
    return jsonify(response_body), 200

# obtener un character
@api.route('/characters/<int:id>', methods=['GET'])
def get_one_character(id):
    results_query = Characters.query.filter_by(id=id).first()
    if not results_query:
        return jsonify({"error": "Character not found"}), 404
    response_body = {
        "msg": "All good",
        "results": results_query.serialize()
    }
    return jsonify(response_body), 200

# obtener todos los planets
@api.route('/planets', methods=['GET'])
def get_all_planets():
    results_query = Planets.query.all()
    if not results_query:
        return jsonify({"error": "Planets not found"}), 404
    results = list(map(lambda item: item.serialize(),results_query))
    response_body = {
        "msg": "All good",
        "results": results
    }
    return jsonify(response_body), 200

# obtener un planet
@api.route('/planets/<int:id>', methods=['GET'])
def get_one_planet(id):
    results_query = Planets.query.filter_by(id=id).first()
    if not results_query:
        return jsonify({"error": "Planet not found"}), 404
    response_body = {
        "msg": "All good",
        "results": results_query.serialize()
    }
    return jsonify(response_body), 200

# obtener todos los ships
@api.route('/ships', methods=['GET'])
def get_all_ships():
    results_query = Ships.query.all()
    if not results_query:
        return jsonify({"error": "Ships not found"}), 404
    results = list(map(lambda item: item.serialize(),results_query))
    response_body = {
        "msg": "All good",
        "results": results
    }
    return jsonify(response_body), 200

# obtener un ship
@api.route('/ships/<int:id>', methods=['GET'])
def get_one_ships(id):
    results_query = Ships.query.filter_by(id=id).first()
    if not results_query:
        return jsonify({"error": "Ship not found"}), 404
    response_body = {
        "msg": "All good",
        "results": results_query.serialize()
    }
    return jsonify(response_body), 200

# obtener todos los favoritos de un usuario
@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    fav_chars = user.fav_chars
    fav_planets = user.fav_planets
    fav_ships = user.fav_ships
    response = {
        "username": user.username,
        "favorite_characters": list(map(lambda item: item.name,fav_chars)),
        "favorite_planets": list(map(lambda item: item.name,fav_planets)),
        "favorite_ships": list(map(lambda item: item.name,fav_ships))
    }
    return jsonify(response)

# agregar un usuario
@api.route('/users/', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 404
    
    check_email = User.query.filter_by(email = data['email']).first()
    check_username = User.query.filter_by(username = data['username']).first()
    if check_email or check_username:
        return jsonify({"error": "Username or Email already exists"}), 404
    
    new_user = User(email = data["email"], is_active = data["is_active"], username = data["username"], password = data["password"])

    db.session.add(new_user)
    db.session.commit()
    new_user_add = new_user.serialize()

    return jsonify(new_user_add)

# agregar un character

# agregar un planeta

# agregar un ship

# eliminar un user
@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    deleted_user = user.serialize()
    return jsonify({"message": "user deleted", "user": deleted_user}), 200

# eliminar un character
@api.route('/characters/<int:char_id>', methods=['DELETE'])
def delete_character(char_id):
    character = Characters.query.get(char_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    
    db.session.delete(character)
    db.session.commit()
    deleted_character = character.serialize()
    return jsonify({"message": "Character deleted", "character": deleted_character}), 200

# eliminar un planet
@api.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"error": "planet not found"}), 404
    
    db.session.delete(planet)
    db.session.commit()
    deleted_planet = planet.serialize()
    return jsonify({"message": "planet deleted", "planet": deleted_planet}), 200

# eliminar un ship
@api.route('/ships/<int:ship_id>', methods=['DELETE'])
def delete_ship(ship_id):
    ship = Ships.query.get(ship_id)
    if not ship:
        return jsonify({"error": "ship not found"}), 404
    
    db.session.delete(ship)
    db.session.commit()
    deleted_ship = ship.serialize()
    return jsonify({"message": "ship deleted", "ship": deleted_ship}), 200



# agregar un character favorito a un usuario
@api.route('/users/<int:user_id>/add_fav_char/<int:char_id>', methods=['POST'])
def add_favorite_character(user_id, char_id):
    user = User.query.get(user_id)
    character = Characters.query.get(char_id)
    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404
    
    user.fav_chars.append(character)
    db.session.commit()
    return jsonify({"message": "Favorite character added"}), 200

# agregar un planet favorito a un usuario
@api.route('/users/<int:user_id>/add_fav_planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    if not user or not planet:
        return jsonify({"error": "User or Planet not found"}), 404
    
    user.fav_planets.append(planet)
    db.session.commit()
    return jsonify({"message": "Favorite planet added"}), 200

# agregar un ship favorito a un usuario
@api.route('/users/<int:user_id>/add_fav_ship/<int:ship_id>', methods=['POST'])
def add_favorite_ship(user_id, ship_id):
    user = User.query.get(user_id)
    ship = Ships.query.get(ship_id)
    if not user or not ship:
        return jsonify({"error": "User or Ship not found"}), 404
    
    user.fav_ships.append(ship)
    db.session.commit()
    return jsonify({"message": "Favorite ship added"}), 200

# eliminar un character favorito de un usuario
@api.route('/users/<int:user_id>/delete_fav_char/<int:char_id>', methods=['DELETE'])
def delete_favorite_character(user_id, char_id):
    user = User.query.get(user_id)
    character = Characters.query.get(char_id)
    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404
    
    if character in user.fav_chars:
        user.fav_chars.remove(character)
        db.session.commit()
        return jsonify({"message": "Favorite character removed"}), 200
    else:
        return jsonify({"error": "Character not in favorites"}), 404

# eliminar un planet favorito de un usuario
@api.route('/users/<int:user_id>/delete_fav_planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    if not user or not planet:
        return jsonify({"error": "User or Planet not found"}), 404
    
    if planet in user.fav_planet:
        user.fav_planet.remove(planet)
        db.session.commit()
        return jsonify({"message": "Favorite Planet removed"}), 200
    else:
        return jsonify({"error": "Planet not in favorites"}), 404

# eliminar un ship favorito de un usuario
@api.route('/users/<int:user_id>/delete_fav_ship/<int:ship_id>', methods=['DELETE'])
def delete_favorite_ship(user_id, ship_id):
    user = User.query.get(user_id)
    ship = Ships.query.get(ship_id)
    if not user or not ship:
        return jsonify({"error": "User or Ship not found"}), 404
    
    if ship in user.fav_ship:
        user.fav_ship.remove(ship)
        db.session.commit()
        return jsonify({"message": "Favorite Ship removed"}), 200
    else:
        return jsonify({"error": "Ship not in favorites"}), 404
