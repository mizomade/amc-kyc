from ninja import Schema

class RoleSchema(Schema):
    name: str

class UserSchema(Schema):
    username: str
    role: RoleSchema = None
