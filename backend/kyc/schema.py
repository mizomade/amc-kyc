from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, datetime

class VengOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class DistrictOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class HouseMaidOut(BaseModel):
    id: int
    name: str
    veng: str
    epic_number: Optional[str] = None
    aadhar_number: Optional[str] = None
    phone_number: Optional[str] = None
    blood_group: Optional[str] = None
    is_verified: bool
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    verification_remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class HouseOut(BaseModel):
    id: int
    house_number: str
    parent_house_id: Optional[int] = None
    veng: Optional[VengOut] = None
    street: Optional[str] = None
    landmarks: Optional[str] = None
    is_owner: bool
    have_tenant: bool
    is_tenant: bool
    lsc_number: Optional[str] = None
    awmtan_kum: Optional[int] = None
    pem_luh_chhan: Optional[str] = None
    household_size: Optional[int] = None
    landlord_name: Optional[str] = None
    landlord_phone: Optional[str] = None
    landlord_veng: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_verified: bool
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    verification_remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    rent_start_date: Optional[date] = None
    rent_end_date: Optional[date] = None
    members: List['PersonOut'] = []
    tenants: List['HouseOut'] = [] # Nested HouseOut for tenants
    maids: List[HouseMaidOut] = []
    model_config = ConfigDict(from_attributes=True)

class ReligionOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class DenominationOut(BaseModel):
    id: int
    name: str
    religion: ReligionOut
    model_config = ConfigDict(from_attributes=True)

class RoleOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class EducationOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class OccupationOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class DocumentTypeOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class PersonalQualificationOut(BaseModel):
    id: int
    education: EducationOut
    year_of_passing: Optional[int] = None
    institution_name: Optional[str] = None
    grade_or_marks: Optional[str] = None
    certificate_number: Optional[str] = None
    remarks: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class PersonalOccupationOut(BaseModel):
    id: int
    occupation: OccupationOut
    employer_name: Optional[str] = None
    position_title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    remarks: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class AttachmentOut(BaseModel):
    id: int
    document_type: DocumentTypeOut
    file: str
    remarks: Optional[str] = None
    uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PersonRelationOut(BaseModel):
    id: int
    first_name: str
    hnam_hming: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class PersonCreate(BaseModel):
    first_name: str
    hnam_hming: Optional[str] = None
    gender: str
    dob: Optional[date] = None
    blood_group: Optional[str] = None
    mobile: Optional[str] = None
    epic_number: Optional[str] = None
    aadhar_number: Optional[str] = None
    marital_status: Optional[str] = None

    father_id: Optional[int] = None
    mother_id: Optional[int] = None
    spouse_id: Optional[int] = None

    house_id: Optional[int] = None
    religion_id: Optional[int] = None
    denomination_id: Optional[int] = None
    role_id: Optional[int] = None

class PersonOut(BaseModel):
    id: int
    first_name: str
    hnam_hming: Optional[str] = None
    gender: str
    dob: Optional[date] = None
    blood_group: Optional[str] = None
    mobile: Optional[str] = None
    epic_number: Optional[str] = None
    aadhar_number: Optional[str] = None
    marital_status: Optional[str] = None
    is_househead: Optional[bool] = None
    photo: Optional[str] = None

    father: Optional[PersonRelationOut] = None
    mother: Optional[PersonRelationOut] = None
    spouse: Optional[PersonRelationOut] = None

    house: Optional[HouseOut] = None
    religion: Optional[ReligionOut] = None
    denomination: Optional[DenominationOut] = None
    role: Optional[RoleOut] = None

    qualifications: List[PersonalQualificationOut] = []
    occupations: List[PersonalOccupationOut] = []
    attachments: List[AttachmentOut] = []

    is_verified: bool
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    verification_remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class PersonSearchOut(BaseModel):
    id: int
    name: str

class PersonUpdate(BaseModel):
    first_name: Optional[str] = None
    hnam_hming: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[str] = None
    blood_group: Optional[str]= None
    mobile: Optional[str]= None
    epic_number: Optional[str]= None
    aadhar_number: Optional[str]= None
    marital_status: Optional[str]= None

    # Foreign key IDs
    father: Optional[int]= None
    mother: Optional[int]= None
    spouse: Optional[int]= None
    house: Optional[int]= None
    religion: Optional[int]= None
    denomination: Optional[int]= None
    role: Optional[int] = None

class HouseCreate(BaseModel):
    house_number: str
    parent_house_id: Optional[int] = None
    veng_id: int
    street: Optional[str] = None
    landmarks: Optional[str] = None
    is_owner: Optional[bool] = True
    lsc_number: Optional[str] = None
    awmtan_kum: Optional[int] = None
    pem_luh_chhan: Optional[str] = None
    have_tenant: Optional[bool] = False
    household_size: Optional[int] = None
    is_tenant: Optional[bool] = False

    landlord_name: Optional[str] = None
    landlord_phone: Optional[str] = None
    landlord_veng: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None
    household_head_id: Optional[int] = None

class HouseUpdate(BaseModel):
    house_number: Optional[str] = None
    parent_house: Optional[int] = None
    veng: Optional[int] = None
    street: Optional[str] = None
    landmarks: Optional[str] = None
    is_owner: Optional[bool] = None
    lsc_number: Optional[str] = None
    awmtan_kum: Optional[int] = None
    pem_luh_chhan: Optional[str] = None
    have_tenant: Optional[bool] = None
    household_size: Optional[int] = None
    is_tenant: Optional[bool] = None
    landlord_name: Optional[str] = None
    landlord_phone: Optional[str] = None
    landlord_veng: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    household_head_id: Optional[int] = None

class PersonalQualificationCreate(BaseModel):
    person_id: int
    education_id: int
    year_of_passing: Optional[int] = None
    institution_name: Optional[str] = None
    grade_or_marks: Optional[str] = None
    certificate_number: Optional[str] = None
    remarks: Optional[str] = None

class PersonalQualificationUpdate(BaseModel):
    education_id: Optional[int] = None
    year_of_passing: Optional[int] = None
    institution_name: Optional[str] = None
    grade_or_marks: Optional[str] = None
    certificate_number: Optional[str] = None
    remarks: Optional[str] = None

class PersonalOccupationCreate(BaseModel):
    person_id: int
    occupation_id: int
    employer_name: Optional[str] = None
    position_title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    remarks: Optional[str] = None

class PersonalOccupationUpdate(BaseModel):
    occupation_id: Optional[int] = None
    employer_name: Optional[str] = None
    position_title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    remarks: Optional[str] = None

class AttachmentCreate(BaseModel):
    person_id: int
    document_type_id: int
    remarks: Optional[str] = None

class AttachmentUpdate(BaseModel):
    document_type_id: Optional[int] = None
    remarks: Optional[str] = None
