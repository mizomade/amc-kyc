from ninja import Schema
from typing import Optional

class GroupSchema(Schema):
    name: str

class UserSchema(Schema):
    id: int
    username: str
    email: Optional[str] = None
    groups: list[GroupSchema] = []

class MeSchema(Schema):
    username: str
    groups: list[GroupSchema] = []
    
class MeSchema(Schema):
    username: str
    email: Optional[str] = None
    groups: list[GroupSchema] = []

class UserInSchema(Schema):
    username: str
    email: Optional[str] = None
    password: str
    role: Optional[str] = None # This will be used to map to a group

class UserUpdateSchema(Schema):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None # This will be used to map to a group
