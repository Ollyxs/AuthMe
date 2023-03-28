from .. import db
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __id = db.Column(db.Integer, primary_key=True)
    __last_name = db.Column('last_name', db.String(50), nullable=False)
    __first_name = db.Column('first_name', db.String(50), nullable=False)
    __email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    __password = db.Column(db.String(30), nullable=False)
    __role = db.Column(db.String(30), nullable=False)
    

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
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        self.__first_name = first_name

    @first_name.deleter
    def first_name(self):
        del self.__first_name

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
    def password(self):
        return self.__activado

    @password.setter
    def password(self, password):
        self.__password = password

    @password.deleter
    def password(self):
        self.__password
    
    @hybrid_property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        self.__role = role

    @role.deleter
    def role(self):
        self.__role
        
        
