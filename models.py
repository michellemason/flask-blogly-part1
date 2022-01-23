"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG = 'https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png'

def connect_db(app):
     db.app = app
     db.init_app(app)  

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
            primary_key = True,
            autoincrement = True)
    first_name = db.Column(db.Text,
            nullable = False)
    last_name = db.Column(db.Text,
            nullable = False)
    image_url = db.Column(db.Text,
            default=DEFAULT_IMG)

    @property
    def full_name(self):
        """REturns users full name"""
        return f"{self.first_name} {self.last_name}"