from ninja import ModelSchema, Schema
from typing import List, Optional
from .models import (
    District,
    Veng,
    Role,
    Religion,
    Denomination,
    Education,
    Occupation,
    DocumentType,
    Hnam,
    User
)

# ===================================
# Basic Schemas for master tables
# ===================================

class DistrictSchema(ModelSchema):
    class Meta:
        model = District
        fields = ['id', 'name']

class VengSchema(ModelSchema):
    district: Optional[DistrictSchema] = None
    class Meta:
        model = Veng
        fields = ['id', 'name', 'district']

class RoleSchema(ModelSchema):
    class Meta:
        model = Role
        fields = ['id', 'name']

class ReligionSchema(ModelSchema):
    class Meta:
        model = Religion
        fields = ['id', 'name']

class DenominationSchema(ModelSchema):
    religion: Optional[ReligionSchema] = None
    class Meta:
        model = Denomination
        fields = ['id', 'name', 'religion']

class EducationSchema(ModelSchema):
    class Meta:
        model = Education
        fields = ['id', 'name']

class OccupationSchema(ModelSchema):
    class Meta:
        model = Occupation
        fields = ['id', 'name']

class DocumentTypeSchema(ModelSchema):
    class Meta:
        model = DocumentType
        fields = ['id', 'name']

class HnamSchema(ModelSchema):
    class Meta:
        model = Hnam
        fields = ['id', 'name']

# ===================================
# User Schema
# ===================================

class UserSchema(ModelSchema):
    role: Optional[RoleSchema] = None
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'phone_number', 'role', 'details', 'is_verified',
            'created_at', 'updated_at'
        ]

# ===================================
# Schemas for creating related objects
# ===================================

class VengCreateSchema(Schema):
    name: str
    district_id: int

class DenominationCreateSchema(Schema):
    name: str
    religion_id: int
