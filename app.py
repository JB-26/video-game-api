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
    #get fields from JSON request
    name = request.json.get("name", None)
    platform = request.json.get("platform", None)
    publisher = request.json.get("publisher", None)
    genre = request.json.get("genre", None)
    year = request.json.get("year", None)

    #use values from JSON to create new object
    game = VideoGame(name=name, platform=platform, publisher=publisher, genre=genre, year=year)

    #add new object to DB
    db.session.add(game)
    db.session.commit()

    return game.json(), 201

@app.route("/deleteGame", methods=["DELETE"])
@jwt_required()
def deleteGame():
     # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    id = request.json.get("id", None)
    game = VideoGame.query.filter_by(id=id).first()
    if game:
        db.session.delete(game)
        db.session.commit()
        return {'The following has been deleted': game.json()}
    else: 
        {'No game found': None}, 404

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = authenticate(username=username, password=password)
    if user == None:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
