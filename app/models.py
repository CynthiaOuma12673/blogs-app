from xml.etree.ElementTree import Comment
from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    blogs = db.relationship('Blog', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('Password attribute cannot be read')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User{self.username}'

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    post = db.Column(db.Text())
    time = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment = db.relationship("Comment",backref="blog",lazy="dynamic")

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def get_blog(id):
        blog = Blog.query.filter_by(id = id).first()
        return blog


    def __repr__(self):
        return f'comment: {self.comment}'

class Quote:
    def __init__(self,author,quote):
        self.author=author
        self.quote=quote
        
class Subscribe(db.Model):
    __tablename__= 'subscribe'
    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),index=True)
    
    def save_subscribe(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'subscribe:{self.email}'

class Comment(db.Model):
    __tablename__= 'comments'
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.Text(), nullable = False )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable = False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, blog_id):
        comments = Comment.query.filter_by(blog_id = blog_id).all()
        return comments

    def __repr__(self):
        return f'comment:{self.comment}'
