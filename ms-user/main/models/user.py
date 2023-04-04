from .. import db
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    __id = db.Column('id', db.Integer, primary_key=True)
    __name = db.Column('name', db.String(50), nullable=False)
    __last_name = db.Column('last_name', db.String(50), nullable=False)
    __email = db.Column('email', db.String(100), unique=True, index=True, nullable=False)
    __password = db.Column('password', db.String(128), nullable=False)
    __role = db.Column('role',  db.String(30), nullable=False)


    def __repr__(self):
        return '<User: %r %r>' % (self.__id, self.__email)

    @hybrid_property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @id.deleter
    def id(self):
        del self.__id

    @hybrid_property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = last_name

    @last_name.deleter
    def last_name(self):
        del self.__last_name

    @hybrid_property
    def name(self):
        return self.__name

    @name.setter
    def first_name(self, name):
        self.__name = name

    @name.deleter
    def name(self):
        del self.__name

    @hybrid_property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @email.deleter
    def email(self):
        del self.__email

    @hybrid_property
    def password(self,):
        return self.__password

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @hybrid_property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        self.__role = role

    @role.deleter
    def role(self):
        self.__role