from marshmallow import Schema, fields, post_load, post_dump, validate
from main.models import UserModel

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True, validate=validate.Email())
    plain_password = fields.String(required=True)
    role = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return UserModel(**data)