"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)



# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200


@app.route('/characters', methods=['GET'])
def get_characters():
     chars = []
     characters = Character.query.all()
     for character in characters:
        chars.append(character.name)
     return jsonify(chars), 200


@app.route('/characters/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
     character = Character.query.get(character_id)
     #for testing, character id's are "4,6,7,3,8,9,10,11,12,13"
     return jsonify(Character.serialize(character)), 200

@app.route('/planets', methods=['GET'])
def get_planets():
     names = []
     planets = Planet.query.all()
     for planet in planets:
        names.append(planet.name)
     return jsonify(names), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
     planet = Planet.query.get(planet_id)
     #for testing, planet id's start at 2-11
     return jsonify(Planet.serialize(planet)), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    characters = Character.query.all()
    fav_characters = []
    planets = Planet.query.all()
    fav_planets = []
    favorites = Favorites.query.all()
    for favorite in favorites:
        for character in characters:
            if favorite.character_id == character.id:
                fav_characters.append(Character.serialize(character))
        for planet in planets:
            if favorite.planet_id == planet.id:
                fav_planets.append(Planet.serialize(planet))

    return jsonify(fav_characters, fav_planets)

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    favorites = Favorites.query.all()
    for favorite in favorites:
        if favorite.planet_id == planet_id:
            return "planet is already a favorite"
    new_fav_planet = Favorites(user_id= 1, planet_id= planet_id)
    db.session.add(new_fav_planet)
    db.session.commit()
    response_body = {"msg": "New planet added to favorites"}
    return jsonify(response_body)
    

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_fav_character(character_id):
    favorites = Favorites.query.all()
    for favorite in favorites:
        if favorite.character_id == character_id:
            return jsonify({"msg": "character is already a favorite"})
    new_fav_char = Favorites(user_id= 1, character_id= character_id)
    db.session.add(new_fav_char)
    db.session.commit()
    response_body = {"msg": "New character added to favorites"}
    return jsonify(response_body)
    
    # print("Incoming request with the following body", request_body)
    # return get_favorites()

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    favorites = Favorites.query.all()
    for favorite in favorites:
        if favorite.planet_id == planet_id:
            fav_planet = Favorites.query.get(favorite.id)
            db.session.delete(fav_planet)
            db.session.commit()
            response_body = {"msg": "planet was deleted from favorites"}
            return jsonify(response_body)
    return jsonify({"msg": "planet is not in favorites"})

    

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_fav_character(character_id):
    favorites = Favorites.query.all()
    for favorite in favorites:
        if favorite.character_id == character_id:
            fav_char = Favorites.query.get(favorite.id)
            db.session.delete(fav_char)
            db.session.commit()
            response_body = {"msg": "character was deleted from favorites"}
            return jsonify(response_body)
    return jsonify({"msg": "character is not in favorites"})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
