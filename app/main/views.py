from crypt import methods
from fileinput import filename
from os import uname
from turtle import title
from unittest.util import sorted_list_difference
from flask import render_template,request,redirect,url_for,abort,flash
from app import email
from app.email import mail_message
from . import main
from flask_login import login_required,current_user
from ..models import Subscribe, User,Blog,Comment
from .forms import UpdateProfile,BlogForm,CommentForm,UpdateBlog,SubscribeForm
from .. import db,photos
from ..request import get_quotes
from app.main import forms

@main.route('/', methods = ['POST', 'GET'])
def index():
    blogs = Blog.query.all()
    quotes = get_quotes()
    form = SubscribeForm()

    if form.validate_on_submit():
        email = form.email.data
        new_subscribe = Subscribe(email = email)
        new_subscribe.save_subscribe()
        mail_message('You have subscribed to blogs app', 'email/subscribe',new_subscribe.email,new_subscribe = new_subscribe)
        flash('You have successfully subscribed')

        return redirect(url_for('main.index'))

    return render_template('index.html',blogs = blogs, quotes = quotes, user = current_user, form = form)

@main.route('/create_new', methods = ['POST', 'GET'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        new_blog = Blog(title = title, post =post, user = current_user)
        new_blog.save_blog()
        return redirect(url_for('main.index'))

    return render_template('new_blog.html', form = form, title = 'Create Your Blog')


@main.route('/comment/<blog_id>/comment', methods = ['POST','GET'])
@login_required
def comment(blog_id):
    form = CommentForm()
    blog = Blog.query.get(blog_id)
    comments = Comment.query.filter_by(blog_id = blog_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        blog_id = blog_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment, blog_id = blog_id, use_id = user_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', blog_id = blog_id))
    return render_template('comment.html', form = form, blog = blog, comments = comments, user = current_user)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    posts = Blog.query.filter_by(user = current_user).all()
    if user is None:
        abort(404)

    return render_template('profile/profile.html', user = user, posts = posts)

@main.route('/user/<uname>/update', methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile', uname = user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<uname>/update/pic',methods = ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname = uname))

@main.route('/delete_post/<int:blog_id>/delete', methods = ['POST'])
@login_required
def delete_post(blog_id):
    blog_delete = Blog.query.get(blog_id)
    db.session.delete(blog_delete)
    db.session.commit()
    flash('Your blog has been deleted successfully')
    return redirect(url_for('main.index', blog_id= blog_id))

@main.route('/delete_comment/<int:blod_id>/<int:comment_id>', methods = ['POST'])
@login_required
def delete_comment(comment_id, blog_id):
    comment = Comment.query.filter_by(id = comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been successfully deleted')
    return redirect(url_for('.comment', blog_id = blog_id, comment_id = comment_id))

@main.route('/update_post/<blog_id>/update', methods = ['POST','GET'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.get(blog_id)
    form = UpdateBlog()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.post = form.post.data
        db.session.commit()
        flash('Your blog has been updated succesfully')
        return redirect(url_for('main.index', blog_id = blog_id))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.post.data = blog.post
    return render_template('new_blog.html', form = form, title = 'Update Your blog here' )

@main.route('/latest', methods = ['POST','GET'])
def latest_blog():
    blogs = Blog.query.order_by(Blog.time.desc()).all()
    quotes = get_quotes()
    form = SubscribeForm()

    return render_template('latest.html', blogs = blogs, quotes = quotes, form = form)



