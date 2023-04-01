from marshmallow import Schema, fields, post_load, post_dump, validate
from main.models import UserModel

class UserSchema(Schema):
    __id = fields.Int(dump_only=True)
    __last_name = fields.Str(required=True)
    __first_name = fields.Str(required=True)
    __email = fields.Str(required=True)
    __password = fields.String(required=True, validate=validate.Email())
    __role = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return UserModel(**data)