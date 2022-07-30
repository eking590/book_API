#POST/book/<string:name>  to create a new library/folder  with a name to a database 

#GET/book/<string:name> to retrieve a book item by name from the database 
#@app.route('/library/<string>:name')
#def get_library(name): 
    #return {name:' library is been created'}


#GET/books to retrieve all the books in the database 
#@app.route('/library')
#def get_library():
 #   pass 


#POST/book/<string:name>/ #to create a book directory in the library with a name 
#@app.route('/book/<string:name>/book', method=['POST'])
#def create_book(name): 
 #   pass 

#GET/library/book /to get a book in the library 
#@app.route('/library/<string>:name')
#def get_book_in_library(name): 
 #   return {name} 


from typing import List

from db import db




class BookModel(db.Model):   #creating the book model 
    __tablename__ = "book"   #create a table 'book' in the database 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(80), nullable=False) 
    date = db.Column(db.String(80), nullable=True) 

    books_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    books = db.relationship("BooksModel")

    
    @classmethod
    def find_by_name(cls, name: str) -> "BookModel":  #search the database (book) by the name of the book 
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls)-> List["BookModel"]:  #find all the books in the database (book) 
        return cls.query.all()

    #find my author and content below 

    def save_to_db(self) -> None:      #to save new information about books into the database 
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None: #to delete existing information from the database 
        db.session.delete(self)
        db.session.commit()