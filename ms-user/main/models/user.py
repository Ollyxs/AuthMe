from .. import db
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False)
    last_name = db.Column('last_name', db.String(50), nullable=False)
    email = db.Column('email', db.String(100), unique=True, index=True, nullable=False)
    password = db.Column('password', db.String(128), nullable=False)
    role = db.Column('role', db.String(30), nullable=False)


    def __repr__(self):
        return '<User: %r %r>' % (self.name, self.email)

    @property
    def plain_password(self,):
        return self.password

    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)