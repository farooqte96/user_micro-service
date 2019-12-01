from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from passlib.hash import sha256_crypt

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)
    return db


def create_tables(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    #api_key = db.Column(db.String(255), unique=True, nullable=True)

# def encode_api_key(self):
        # self.api_key = sha256_crypt.hash(self.username + str(datetime.utcnow))

    def encode_password(self):
        self.password = sha256_crypt.hash(self.password)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' %(self.username)

    def to_json(self):
        return {
            # 'first_name': self.first_name,
            # 'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'id': self.id,
        }
