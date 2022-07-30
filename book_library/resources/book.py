from flask import request 
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required 
from models.book import BookModel
#from marshmallow import VallidationError 
from schemas.book import BookSchema  
from libs.strings import gettext 
from marshmallow import INCLUDE, EXCLUDE 



book_schema = BookSchema(unknown=INCLUDE)
book_list_schema = BookSchema(many=True)


class Book(Resource):
    @classmethod
    def get(cls, name: str):
        book = BookModel.find_by_name(name)    #search for any book in the database by its name 
        if book:
            return book_schema.dump(book), 200  #If found return the book information from the database 
        return {"message": gettext("book_not_found")}, 404 #otherwise return error message(404 - not found)

    @classmethod
    #@jwt_required(refresh=True)   #requires a JsonWebToken(JWT) before you add a new book to the database 
    def post(cls, name: str):
        if BookModel.find_by_name(name):  #search the database if the name of this new_book exists
            return {"message": gettext("book_name_exists ").format(name)}, 400 #if its exist flag (400 - bad request)

        book_json = request.get_json() #receiving name, id, price, author, content, and date 
        book_json["name"] = name 
        
       
        book = book_schema.load(book_json)
        
        try:
            book.save_to_db()    #save the book information into the database 
        except:
            return {"message": gettext("item_error_inserting")}, 500 #else flag (500 - internal server error)

        return book_schema.dump(book), 200  #return successful (200 - Ok)

    @classmethod
    #@jwt_required() #requires a JsonWebToken(JWT) before you add a new book to the database
    def delete(cls, name: str):  #to delete a book from the database 
        Book = BookModel.find_by_name(name)  #search the database for the book with the name you want to delete
        if Book:
            Book.delete_from_db()  #if book is in the database then delete it 
            return {"message": gettext("book_deleted")}, 200 #display/return book successfully deleted(200-ok)
        return {"message": gettext("book_not_found")}, 404 #else return error book not found (404-not found)

    @classmethod
    def put(cls, name: str): #to update the book information in the database 
        Book_json = request.get_json() 
        Book = BookModel.find_by_name(name)
        if Book: #if the book is in the database then change the content 
            #return {"message": gettext("book_name_exists ").format(name)} 
            Book.content = Book_json["content"] #change/replace the existing content 
            Book.author = Book_json["author"]  #change/replace the  existing content 
            Book.price = Book_json["price"] #change/replace the existing price 
            Book.date = Book_json["date"]  #change/replace the existing date 
            
        else: #otherwise insert a new book by name, price, author, content and date  
            Book_json["name"] = name 
            
            Book = book_schema.load(Book_json)
            
            
        Book.save_to_db() #save the new book information into the database 

        return book_schema.dump(Book),  200  #return successfully save (200 - ok)


class BookList(Resource):  #this return/display all the list of books in the database 
    @classmethod
    def get(cls):
        return {"books": book_list_schema.dump(BookModel.find_all())}, 200 #returns success (200 - Ok)