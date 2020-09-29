
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))

    pitches = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        self.pass_secure = generate_password_hash(password)
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))

    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class Pitch(db.Model):

    __tablename__='pitches'

    id = db.Column(db.Integer,primary_key = True)
    pitch_title = db.Column(db.String)
    pitch_category = db.Column(db.String)
    pitch_description = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    pitch_votes = db.Column(db.Integer, default=0)

    comments = db.relationship('Comment', backref = 'pitches',lazy = "dynamic")

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    #get pitches according to persons id
    @classmethod
    def get_userpitch(cls,id):
        pitches = Pitch.query.filter_by(user_id=id).all()
        return pitches

    #get pitches according to persons category
    @classmethod
    def get_pitchcat(cls,cat):
        pitches = Pitch.query.filter_by(pitch_category=cat).all()
        return pitches

    #get pitches according to id
    @classmethod
    def get_singlepitch(cls,id):
        pitches = Pitch.query.filter_by(id=id).first()
        return pitches

    #get all pitches
    @classmethod
    def get_pitches(cls):
        pitches = Pitch.query.all()
        return pitches

    #UPDATE pitches VOTES
    @classmethod
    def update_pitchvote(cls,id):
        pitches = Pitch.query.filter_by(id=id).first()
        pitches.pitch_votes += 10


class Comment(db.Model):

    __tablename__='comments'

    id = db.Column(db.Integer,primary_key = True)
    comment_description = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    pitch_id = db.Column(db.Integer,db.ForeignKey("pitches.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    #get comments according to  pitchid
    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments