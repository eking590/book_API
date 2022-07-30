from db import db 

class UserModel(db.Model): 
    __tablename__ = 'users'   #to create the users database: __users__ 

    id = db.Column(db.Integer, primary_key=True)  #the id column
    username = db.Column(db.String(80), nullable=False, unique=True) #the username column 
    password = db.Column(db.String(80), nullable=False) #the password column 

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":  #to find a user by username in the database 
        return cls.query.filter_by(username=username).first() 
    
    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":   #to find a user by id in the database 
        return cls.query.filter_by(id=_id).first()
    

    def save_to_db(self) -> None:   #to save our usernames and passwords to our database 
        db.session.add(self)
        db.session.commit() 
    
    def delete_from_db(self) -> None: #to delete usernames and passwords from our database 
        db.session.delete(self)
        db.session.commit() 

    