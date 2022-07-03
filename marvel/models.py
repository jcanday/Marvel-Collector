from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()

login = LoginManager()

marsh = Marshmallow()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key= True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String,nullable=True,default="")
    token = db.Column(db.String, default="", unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
    character = db.relationship('Character', backref = 'owner', lazy=True)
    
    
    
    def __init__(self,email,name="",password="", id="", token="" ):
        self.id = self.set_id()
        self.name = name
        self.password= self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        
    def set_token(self,length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.email} has been added to the database"  
    
class Character(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(300), nullable=True, default ="")
    comics_appeared = db.Column(db.Integer)
    super_power = db.Column(db.String(100), nullable=True, default ="")
    date_created = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    
    def __init__(self, name,desc="",comics_appeared=None,super_power="", id="",user_token=""):
        self.id = self.set_id()
        self.name = name
        self.desc = desc
        self.comics_appeared = comics_appeared
        self.super_power = super_power
        self.user_token = user_token
        
    def __repr__(self):
        return f"The following character has been added {self.name}"
    
    def set_id(self):
        return(secrets.token_urlsafe())
    
class CharacterSchema(marsh.Schema):
    class Meta:
        fields = ['id','name','desc','comics_appeared','super_power','date_created']
        
char_schema = CharacterSchema()
chars_schema = CharacterSchema(many=True)

class Comment(db.Model):
    id = db.Column(db.String, primary_key=True)
    post = db.Column(db.String(300), nullable=False, default ="")
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    user_name = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    poster = db.Column(db.String, db.ForeignKey('user.email'), nullable= False)
    comments = db.relationship('User', backref = 'own_post', lazy=True, foreign_keys=[user_name])
    posts = db.relationship('User', backref='poster', lazy=True,foreign_keys=[poster])
    
    def __init__(self, post,user_name="",poster="", id = ""):
        self.id = self.set_id()
        self.post = post
        self.user_name = user_name
        self.poster = poster
        
    def __repr__(self):
        return f"THe following post has been made {self.post} by {self.name}"

    def set_id(self):
        return(secrets.token_urlsafe())
    
    
    
       