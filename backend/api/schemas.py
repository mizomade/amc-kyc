from ninja import Schema

class GroupSchema(Schema):
    name: str

class UserSchema(Schema):
    username: str
    groups: list[GroupSchema] = []
