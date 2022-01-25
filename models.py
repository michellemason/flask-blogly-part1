"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG = 'https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png'

def connect_db(app):
     db.app = app
     db.init_app(app)  

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, default=DEFAULT_IMG)

    posts = db.relationship("Post", backref="user")

    @property
    def full_name(self):
        """REturns users full name"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
        __tablename__ = 'posts'

        id = db.Column(db.Integer, primary_key = True, autoincrement = True)
        title = db.Column(db.Text, nullable = False)
        content = db.Column(db.Text, nullable = False)
        created_at = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

        @property
        def friendly_data(self):
                """return nicely formated date"""
                return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")