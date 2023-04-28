from marshmallow import Schema, fields, validate

class CodeSchema(Schema):
    code = fields.Str(required=True, validate=validate.Length(min=6))