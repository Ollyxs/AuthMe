from .. import db
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __id = db.Column(db.Integer, primary_key=True)
    __apellido = db.Column('apellido', db.String(50), nullable=False)
    __nombre = db.Column('nombre', db.String(50), nullable=False)
    __email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    __password = db.Column(db.String(30), nullable=False)
    __role = db.Column(db.String(10), nullable=False)
    

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
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, apellido):
        self.__apellido = apellido

    @apellido.deleter
    def apellido(self):
        del self.__apellido

    @hybrid_property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @nombre.deleter
    def nombre(self):
        del self.__nombre

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
        
        
