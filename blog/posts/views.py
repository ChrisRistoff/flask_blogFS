from blog.posts.forms import BlogPostForm
from flask import (render_template,url_for,flash,
                   redirect,request,Blueprint,abort)
from blog.app import db
from blog.models import Post
from flask_login import current_user,login_required


blog_posts = Blueprint('blog_posts',__name__)

#Create
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = Post(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id)

        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('core.index'))

    return render_template('create.html',form=form)

#Blog Post (View)
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    post = Post.query.get_or_404(blog_post_id)

    return render_template('blog_post.html',title=post.title,
                           post=post)

#update blog post
@blog_posts.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post = Post.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post.title = form.title.data
        blog_post.text = form.text.data

        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('core.index',blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create.html',title='Updating',form=form)

#delete blog post
@blog_posts.route('/<int:blog_post_id>/delete',methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = Post.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    return redirect(url_for('core.index'))






