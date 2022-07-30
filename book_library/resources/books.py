from flask_restful import Resource
from models.books import BooksModel
from schemas.books import BooksSchema 
from libs.strings import gettext 

books_schema = BooksSchema() #import the BooksSchema from schemas folder 
books_list_schema = BooksSchema(many=True) 


class Books(Resource):
    @classmethod
    def get(cls, name: str):
        books = BooksModel.find_by_name(name)
        if books:
            return books_schema.dump(books), 200
        return {"message": gettext("books_not_found")}, 404

    @classmethod
    def post(cls, name: str):
        if BooksModel.find_by_name(name):
            return {"message": gettext("books_name_exists").format(name)}, 400

        books = BooksModel(name=name)
        try:
            books.save_to_db()
        except:
            return {"message": gettext("books_error_inserting")}, 500

        return books_schema.dump(books), 200

    @classmethod
    def delete(cls, name: str):
        books = BooksModel.find_by_name(name)
        if books:
            books.delete_from_db()
            return {"message": gettext("books_deleted")}, 200

        return {"message": gettext("books_not_found")}, 404


class BooksList(Resource):
    @classmethod
    def get(cls):
        return {"books": books_list_schema.dump(BooksModel.find_all())}, 200