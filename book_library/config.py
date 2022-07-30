import os

#from default_config import SQLALCHEMY_DATABASE_URI 

DEBUG = False 
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.db")
#JWT_SECRET_KEY="something-else-about" 
#APP_SECRET_KEY="jose"
