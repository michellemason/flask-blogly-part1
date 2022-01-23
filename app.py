"""Blogly application."""

from crypt import methods
from importlib.resources import read_text
from flask import Flask, request, render_template, redirect
from models import db, connect_db, User
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
    # This orders users by last name first
    return render_template('home.html', users=users)

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

