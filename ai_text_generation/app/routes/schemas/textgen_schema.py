from marshmallow import Schema, fields, validate

class GenerateTextSchema(Schema):
    id = fields.UUID(dump_only=True)
    prompt = fields.Str(required=True, validate=validate.Length(min=1))
    response = fields.Str(dump_only=True)
    user_id = fields.UUID(dump_only=True)
    timestamp = fields.DateTime(dump_only=True)





class ErrSchema(Schema):
    msg = fields.Str()
    code = fields.Int()
