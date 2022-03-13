from ast import Str
from logging import PlaceHolder
from turtle import title
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectField
from wtforms.validators import Email, InputRequired

from app import email

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    post = TextAreaField('Your Blog', validators=[InputRequired()], render_kw= {'class': 'form-control','rows':5})
    submit = SubmitField('Submit Your Blog')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Kindly tell us about yourself', validators=[InputRequired()])
    submit = SubmitField('Save Bio')

class CommentForm(FlaskForm):
    comment = TextAreaField('Add a comment here', validators=[InputRequired()])
    submit = SubmitField('Comment')

class UpdateBlog(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    post = TextAreaField('Update your blog', validators=[InputRequired()], render_kw={'class':'form-control', 'rows':5})
    submit = SubmitField('Submit Your Blog')

class SubscribeForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),Email()], render_kw={'placeHolder':'Enter email address here....'})
    submit = SubmitField('Subscribe')

