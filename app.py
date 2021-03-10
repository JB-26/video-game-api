#Flask
from flask import Flask, render_template, jsonify, request

#JWT
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

#RESTful
from flask_restful import Api

#Database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

#User for handling login
from user import authenticate

#creating new Flask app
app = Flask(__name__)
api = Api(app)

#set up JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

#create database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

#Table in DB
class VideoGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    platform = db.Column(db.Text)
    publisher = db.Column(db.Text)
    genre = db.Column(db.Text)
    year = db.Column(db.Integer)

    #initialise object
    def __init__(self, name, platform, publisher, genre, year):
        self.name = name
        self.platform = platform
        self.publisher = publisher
        self.genre = genre
        self.year = year
    
    def __repr__(self):
        return f'Game name: {self.name}\nPlatform: {self.platform}\nPublisher: {self.publisher}\nGenre: {self.genre}\nYear: {self.year}'
    
    #returns individual game as a dictionary/json
    def json(self):
        return {'Game':{'ID: ':self.id, 'Name: ' : self.name, 'Platform: ': self.platform, 'Publisher: ': self.publisher, 'Genre: ': self.genre, 'Year': self.year}}

@app.route("/displayGames", methods=["GET"])
@jwt_required()
def showGames():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    games = VideoGame.query.all()
    games_list = []
    for game in games:
        games_list.append(game.json())
    return jsonify({"Games": games_list})

@app.route("/addGame", methods=["POST"])
@jwt_required()
def addGame():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    try:
        #get fields from JSON request
        name = request.json.get("name", None)
        platform = request.json.get("platform", None)
        publisher = request.json.get("publisher", None)
        genre = request.json.get("genre", None)
        year = request.json.get("year", None)

        if type(year) != int:
            return {"You have entered an invalid year, please enter a number.": {"Value entered for year": year}}, 400
    
        if name == "" or platform == "" or publisher == "" or genre == "" or year == "" or name == None or platform == None or publisher == None or genre == None or year == None:
            return {"Your request includes empty values, please try again": None}, 400

        #use values from JSON to create new object
        game = VideoGame(name=name, platform=platform, publisher=publisher, genre=genre, year=year)

        #add new object to DB
        db.session.add(game)
        db.session.commit()

        return {"The following game has been added":game.json()}, 201
    except:
        return {"Your request is invalid, are you using the correct format?": {"Format": {"name": "Game name", "platform": "Platform for game", "publisher": "Name of company", "genre": "Game genre", "year": 2000}}}, 400

@app.route("/deleteGame", methods=["DELETE"])
@jwt_required()
def deleteGame():
    try:
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        id = request.json.get("id", None)

        if type(id) != int:
            return {"You have entered an invalid id, please enter a number.": {"Value entered for id": id}}, 400

        game = VideoGame.query.filter_by(id=id).first()
        if game:
            db.session.delete(game)
            db.session.commit()
            return {'The following has been deleted': game.json()}
        else: 
            return {'No game found': None}, 404
    except:
        return {"Your request is invalid, are you using the correct format?": {"Format": {"id": 1}}}, 400
    

@app.route("/findGame", methods=["GET"])
@jwt_required()
def findGame():
    try:
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        name = request.json.get("name", None)
        if name == None or name == "":
            return {"Your request includes empty values, please try again": None}, 400
        #creating search query with wild card each side
        search = "%{}%".format(name)
        games = VideoGame.query.filter(VideoGame.name.like(search)).all()
        games_list = []
        for game in games:
                games_list.append(game.json())
        if len(games_list) > 0:
            return jsonify({"Games": games_list})
        else:
            return {"No games were found for the search term": name},404
    except:
        return {"Your request is invalid, are you using the correct format?": {"Format": {"name": "Game name"}}}, 400

@app.route("/updateGame", methods=['PUT'])
@jwt_required()
def updateGame():
    try:
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        id = request.json.get("id", None)
        field = request.json.get("field", None)
        value = request.json.get("value", None)

        if id == None or field == None or field == "" or value == None or value == "":
            return {"Your request includes empty values, please try again": None}, 400
        
        if type(id) != int:
            return {"You have entered an invalid id, please enter a number.": {"Value entered for id": id}}, 400
        
        if field == "name":
            game = VideoGame.query.get(id)
            if game == None:
                return {'No game found': None}, 404
            game.name = value
            db.session.add(game)
            db.session.commit()
            return {"Game updated:": game.json(), "Value updated": field}, 200
        
        elif field == "platform":
            game = VideoGame.query.get(id)
            if game == None:
                return {'No game found': None}, 404
            game.platform = value
            db.session.add(game)
            db.session.commit()
            return {"Game updated:": game.json(), "Value updated": field}, 200

        elif field == "publisher":
            game = VideoGame.query.get(id)
            if game == None:
                return {'No game found': None}, 404
            game.publisher = value
            db.session.add(game)
            db.session.commit()
            return {"Game updated:": game.json(), "Value updated": field}, 200

        elif field == "genre":
            game = VideoGame.query.get(id)
            if game == None:
                return {'No game found': None}, 404
            game.genre = value
            db.session.add(game)
            db.session.commit()
            return {"Game updated:": game.json(), "Value updated": field}, 200
        
        elif field == "year":
            game = VideoGame.query.get(id)
            if game == None:
                return {'No game found': None}, 404
            game.year = value
            db.session.add(game)
            db.session.commit()
            return {"Game updated:": game.json(), "Value updated": field}, 200
        
        else:
            return {"Invalid field entered": field}, 400
    except:
        return {"Your request is invalid, are you using the correct format?": {"Format": {"id": 1, "field": "name", "value": "Super Mario 64"}}}, 400


@app.route("/login", methods=["POST"])
def login():
    try:
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        user = authenticate(username=username, password=password)
        if user == None:
            return jsonify({"Login failed": "Bad username or password"}), 401

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    except:
        return {"Your request is invalid, are you using the correct format?": {"Format": {"username": "username", "password": "password"}}}, 400


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
