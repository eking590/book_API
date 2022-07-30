from typing import List 
from db import db


class BooksModel(db.Model):   #created the BooksModel object 
    __tablename__ = "books"   #created the books table with id and name as it rows 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    book = db.relationship("BookModel", lazy="dynamic")  #link the book.py model table here!

    
    @classmethod
    def find_by_name(cls, name: str) -> "BooksModel":  #find by name of the books in the books database 
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["BooksModel"]:  #find all the books 
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()