from ma import ma 
from models.book import BookModel
from models.books import BooksModel 


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookModel
        
        load_only = ("book",)
        dump_only = ("id")
        include_fk = True 
        load_instance = True 