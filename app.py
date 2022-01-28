"""Blogly application."""

from crypt import methods
from importlib.resources import read_text
from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def list_users():
    """Homepage redirects to list of users"""
    return redirect('/users')


@app.route('/users')
def show_all_users():
    """Show all users with links to details for them"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    posts = Post.query.order_by(Post.created_at.desc()).limit(3).all()
    # This orders users by last name first
    return render_template('home.html', users=users, posts=posts)

@app.route('/users/new', methods=["GET"])
def show_add_user_form():
    """Shows add user form"""
    return render_template('create_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Processes adding a user"""
    fname = request.form['fname']
    lname = request.form['lname']
    url = request.form['url'] or None

    new_user = User(first_name=fname, last_name=lname, image_url=url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users")

@app.route('/users/<int:user_id>')
def user_info(user_id):
    """Show details about specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit page for a user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_user_edits():
    """Process the edits for this user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['fname']
    user.last_name = request.form['lname']
    user.image_url = request.form['url']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user on form submission"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

######## POSTS BELOW ########

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Show form to add a users post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """handle add form, add post & redirect to user detail"""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user=user)
    
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show post and edit/delete buttons"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show form to edit post & cancel button func"""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edit(post_id):
    """Handles edit of post & redirects to post view"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Deletes the post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

#########   TAGS BELOW   ########

@app.route('/tags')
def all_tags():
    """List all tags with links to their details"""
    tags = Tag.query.all()
    return render_template('list_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Show info on a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tags.html', tag=tag)

@app.route('/tags/new')
def add_new_tag():
    """Shows form to add new tag"""
    posts = Post.query.all()
    return render_template('add_tag.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def process_new_tag():
    """Form submission for new tag"""
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()

    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Show edit form for tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tag.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def handle_edit_tag(tag_id):
    """Processed edit form"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
