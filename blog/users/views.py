from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required, login_user, logout_user
from blog.app import db
from blog.models import User,Post
from blog.users.forms import RegisterForm, LoginForm, UpdateUserForm
from blog.users.pictures import add_picture

users = Blueprint('users', __name__)

#register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name = form.name.data,
                    email = form.email.data,
                    password = form.password.data,
                    )


        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


#logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

#login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        #.first() so the query doesn't return a list
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if user.check_password(form.password.data) and user is not None:
                login_user(user)
                flash('Logged in successfully')

                #get the page the user was trying to access before logging in
                next = request.args.get('next')

                if next == None or next[0] != '/':
                    next = url_for('core.index')

                return redirect(next)

    return render_template('login.html', form=form)


#account
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():

        #check if the user is uploading a new picture
        if form.picture.data:

            #add_picture in pictures.py
            name = current_user.name

            pic = add_picture(form.picture.data, name)

            #update the user's picture
            current_user.profile_image = pic

        #update the user's email and name
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('users.account'))

    #if the user is not submitting the form, populate the form with the 
    #current user's data
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.name.data = current_user.name

    #get the user's profile image
    profile_image = url_for('static', filename='profile_picture/'
                            + current_user.profile_image)


    return render_template('account.html',profile_image=profile_image,
                           form=form)


#user's list of posts
@users.route('/<name>')
def user_posts(name):

    #get the page number from the url
    page = request.args.get('page', 1, type=int)

    #get the user's posts
    #first_or_404() returns a 404 error if the user doesn't exist
    user = User.query.filter_by(name=name).first_or_404()

    #112 get the user's posts
    #113 order by date descending
    #114 paginate the posts
    blog_posts = Post.query.filter_by(author=user)\
        .order_by(Post.date.desc())\
        .paginate(page=page, per_page=5)


    return render_template('user_posts.html', blog_posts=blog_posts, user=user)


#test page
@users.route('/test')
def test():
    return render_template('test.html')











