from .. import db
# from main.models import ClienteModel
from .repository_base import Create, Read, Update, Delete


class RepositoryUser(Create, Read, Update, Delete):
    def __init__(self):
        
        self.__model = UserModel   #Agregar nombre igual que en MODELOS


    def find_one(self, id):
        objeto = db.session.query(self.__model).get_or_404(id)
        return objeto

    def create(self, objeto):
        db.session.add(objeto)
        db.session.commit()
        return objeto

    def delete(self, id):
        objeto = db.session.query(self.__model).get_or_404(id)
        self.__soft_delete(objeto, id)

    # ! Para que sirve esto
    def __soft_delete(self, objeto):
        objeto.__activado = False
        self.update(objeto, id)

    def update(self, data, id):
        objeto = db.session.query(self.__model).get_or_404(id)
        for key, value in data:
            setattr(objeto, key, value)
        db.session.add(objeto)
        db.session.commit()
        return objeto

