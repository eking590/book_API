import os 
from flask import Flask #import flask module, this help for backend development in python (CRUD -> Create,Read,Update, Delete); 
from flask_restful import Resource, Api #resources are mapped into database tables 
from flask import json, jsonify 
from flask_jwt_extended import (
    JWTManager, 
    jwt_required, 
    get_jwt
)
from dotenv import load_dotenv 
from marshmallow import ValidationError 

from db import db
from ma import ma

from resources.user import UserRegister, User, UserLogin
from resources.book import Book, BookList 
from resources.books import Books, BooksList

app = Flask(__name__) #our server application(app) mapped to our Flask 
 #this enables our Api to uses resources(GET,POST, DELETE, PUT etc)

#to import or use our environment variables 
load_dotenv(".env", verbose=True) #loads all .env files 
app.config.from_object("default_config") #load all the variables in default_config.py here 
app.config.from_envvar("APPLICATION_SETTINGS") 
api = Api(app)






#to create our database table 
@app.before_first_request
def create_tables(): 
    db.create_all() 


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err): 
    return jsonify(err.messages), 400 


jwt = JWTManager(app) #to import our JWTs to our app 

api.add_resource(UserRegister, '/register') #route to access our UserRegister resources 
api.add_resource(User, '/user/<int:user_id>') #route to access our UserId resources 
api.add_resource(UserLogin, '/login') #route to access UserLogin resources 
api.add_resource(Book, '/book/<string:name>') 
api.add_resource(BookList, '/books') 
api.add_resource(Books, '/books/<string:name>')
api.add_resource(BooksList, '/bookslist')

db.init_app(app)

if __name__ == '__main__': 
    from db import db 
    
    ma.init_app(app)
    app.run(port=5000, debug=True) #our app or server runs on port=5000 