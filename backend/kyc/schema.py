from pydantic import BaseModel
from typing import Optional, List
from datetime import date

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
    epic_number: Optional[str] = None
    aadhar_number: Optional[str] = None
    house_number: Optional[str] = None
    mobile: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None

    class Config:
        orm_mode = True

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
