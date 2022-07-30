from ma import ma 
from models.books import BooksModel 
from models.book import BookModel
from schemas.book import BookSchema 



class BooksSchema(ma.SQLAlchemyAutoSchema):
    book = ma.Nested(BookSchema, many=True)
    
    
    class Meta:
        model = BooksModel
        dump_only = ("id")
        include_fk = True 
        load_instance = True 