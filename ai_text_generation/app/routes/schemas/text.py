from marshmallow import Schema, fields

class GenerateTextSchema(Schema):
    id = fields.Int(dump_only=True)
    prompt = fields.Str(required=True)
    response = fields.Str(dump_only=True)
    user_id = fields.Int(dump_only=True)
