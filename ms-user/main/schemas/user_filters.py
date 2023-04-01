from main.models import UserModel


class UserFiltros():
    def __init__(self, user):
        self.__user = user
        self.__dict_filters = {"id": self.__filtro_por_id,
                            "first_name": self.__filtro_por_nombre,
                            "last_name": self.__filtro_por_apellido,
                            "email": self.__filtro_por_email
                            }

    def __filtro_por_id(self, value):
        return self.__user.filter(UserModel.id == int(value))

    def __filtro_por_nombre(self, value):
        return self.__user.filter(UserModel.first_name.like('%' + value + '%'))

    def __filtro_por_apellido(self, value):
        return self.__user.filter(UserModel.last_name.like('%' + value + '%'))

    def __filtro_por_email(self, value):
        return self.__User.filter(UserModel.email.like('%' + value + '%'))

    def aplicar_filtro(self, key, value):
        return self.__dict_filters[key](value)