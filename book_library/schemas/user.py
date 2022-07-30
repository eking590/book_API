from ma import ma        #from the ma.py import ma(Marshmallow)
#from marshmallow import pre_dump
from models.user import UserModel   #from models folder import user.py and import UserModel class 


class UserSchema(ma.SQLAlchemyAutoSchema):  #creates the database rows and columns from UserModel class 
    
    class Meta: 
        model = UserModel #using the UserModel from the models.user folder for the model 
        dump_only = ("id",)   #skip during deserialization (read-only field)
        load_only = ("password", ) #skip during serialization (write-only field)
        load_instance = True #this enables the JSON payload to load the JSON files from any app 
    
    #@pre_dump
    #def _pre_dump(self, user:UserModel):
        ##user.confirmation =[user.most_recent_confirmation]
        #return user 