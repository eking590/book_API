from flask_restful import Resource, reqparse #import Resource modules from flask_restful, this input the Resource to our code
from flask import request, json, jsonify  #import request, it help the api receive requests from the clients 
from werkzeug.security import safe_str_cmp  #werkzeug.security helps to compare strings(username&password) that is passed to the database
from flask_jwt_extended import (     #flask_jwt_entended is used to create our access_token and refresh token 
    create_access_token, 
    create_refresh_token
)
 
from schemas.user import UserSchema   #from the schemas folder, import user.py module and in it import the UserSchema class 
from models.user import UserModel   #from models folder, import user.py module and in it import UserModel class
  
from libs.strings import gettext  #from libs folder, import strings.json and import gettext in it. 
from marshmallow import INCLUDE, EXCLUDE  
from typing import Dict, List 

user_schema = UserSchema(unknown=INCLUDE) #call the UserSchema class in the variable user_schema 
 

class UserRegister(Resource): 
    @classmethod
    def post(cls): 
        user = user_schema.load(request.get_json())    #get the user username and password 
        
        if UserModel.find_by_username(user.username): 
            return {"message": gettext("user_username_exists")}, 400 #prompt that the user already exits 
            
        user.save_to_db()  #else save the username and password in the database 
            
        return {"message": gettext("user_registered")}, 201 #user created(201)

class User(Resource): 
    @classmethod
    def get(cls, user_id: int):  
        user = UserModel.find_by_id(user_id) #find user(s) by its id 
        if not user: 
            return {'message': gettext("user_not_found")}, 404 #if user_id not found prompt not found(404)
        return user_schema.dump(user), 200 #else return the username with successful(200)

    @classmethod 
    def delete(cls, user_id: int): 
        user = UserModel.find_by_id(user_id) #find user(s) by its id 
        if not user: 
            return {'message': gettext("user_not_found")}, 404 #if user_id not found prompt not found(404)
        user.delete_from_db() #else delete the user from the database 
        return {'message': gettext("user_deleted")}, 200  #return user(s) successfully deleted(200) 


class UserLogin(Resource):

    @classmethod 
    def post(cls): 
        user_json = request.get_json()  #receives a user(s) username and password 
        user_data = user_schema.load(user_json)
      
        user = UserModel.find_by_username(user_data.username)  #check if user(s) username is in the database

        if user and safe_str_cmp(user.password, user_data.password):  #checks if username and passwords matches with what is the database
                access_token = create_access_token(identity=user.id, fresh=True) #if it not in the database creates a new access token  
                refresh_token = create_refresh_token(user.id)  #and refresh_token 
                return {
                    'access_token' : access_token, 
                    'refresh_token': refresh_token
                        }, 200    #returns/display the access_token and refresh_token (200 - ok)
           
        return {'message': gettext("user_invalid_credentials")}, 401 #else return invalid credentials with (401 -unauthorized code)


    