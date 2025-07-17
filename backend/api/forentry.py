from ninja import Router
from django.db.models import Q
from kyc.models import Person,House
from typing import List,Optional
from pydantic import BaseModel
from kyc.schema import PersonOut, PersonSearchOut
from datetime import date
router = Router(tags=['Search'])
router = Router()

def calculate_age(dob):
    if not dob:
        return None
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


#Person Seach na tur plus filtering
@router.get("/person/", response=List[PersonOut])
def search_person(
    request,
    search: str = None,
    occupation: str = None,   
    age_group: str = None,    
    id: int = None,
):
    queryset = Person.objects.select_related("house", "father", "mother").prefetch_related("occupations__occupation").all()

    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(hnam_hming__icontains=search) |
            Q(epic_number__icontains=search) |
            Q(aadhar_number__icontains=search) |
            Q(house__house_number__icontains=search) |
            Q(mobile__icontains=search) |
            Q(dob__icontains=search)
        )

    if occupation:
        queryset = queryset.filter(occupations__occupation__name__iexact=occupation)

    if age_group:
        from datetime import date, timedelta

        today = date.today()
        age_ranges = {
            "0-18": (today - timedelta(days=18*365), today),
            "18-35": (today - timedelta(days=35*365), today - timedelta(days=18*365)),
            "35-60": (today - timedelta(days=60*365), today - timedelta(days=35*365)),
            "60 above": (None, today - timedelta(days=60*365)),
        }

        min_date, max_date = age_ranges.get(age_group, (None, None))

        if min_date and max_date:
            queryset = queryset.filter(dob__range=(min_date, max_date))
        elif max_date:
            queryset = queryset.filter(dob__lte=max_date)

    if id:
        queryset = queryset.filter(id=id)

    return [
        PersonOut(
            id=person.id,
            first_name=person.first_name,
            hnam_hming=person.hnam_hming,
            epic_number=person.epic_number,
            dob=person.dob.isoformat() if person.dob else None,
            aadhar_number=person.aadhar_number,
            house_number=person.house.house_number if person.house else None,
            mobile=person.mobile,
            father_name=f"{person.father.first_name} {person.father.hnam_hming}" if person.father else None,
            mother_name=f"{person.mother.first_name} {person.mother.hnam_hming}" if person.mother else None,
            photo_url=request.build_absolute_uri(person.photo.url) if person.photo and person.photo.name else None,
            age=calculate_age(person.dob),
            occupations=[po.occupation.name for po in person.occupations.all()],
        )
        for person in queryset[:50]
    ]



#Father search na fate regitered dawn a pa ber awlsam deuha search na , house_id mil zel in awmzia chu family member dang house dang ami a rawn lang dawnlo tihna
@router.get("/father/", summary="Search for father candidates in the same house")
def search_father(request, house_id: int, name: str = None):
    queryset = Person.objects.filter(house_id=house_id, gender="Male")

    if name:
        queryset = queryset.filter(
            Q(first_name__icontains=name) | Q(hnam_hming__icontains=name)
        )

    return [
        {
            "id": person.id,
            "first_name": person.first_name,
            "hnam_hming": person.hnam_hming
        }
        for person in queryset[:20]
    ]



#chutiang chiah in hetah pawh mother bik search na a ni tawp mai
@router.get("/mother/", summary="Search for mother candidates in the same house")
def search_mother(request, house_id: int, name: str = None):
    queryset = Person.objects.filter(house_id=house_id, gender="Female")

    if name:
        queryset = queryset.filter(
            Q(first_name__icontains=name) | Q(hnam_hming__icontains=name)
        )

    return [
        {
            "id": person.id,
            "first_name": person.first_name,
            "hnam_hming": person.hnam_hming
        }
        for person in queryset[:20]
    ]


#House search na;
#Hmanna tur chu House tamtak and register tawh chuan dropdown ah zawn abuaithllk dawn avangin searchable dropdown frontend ah kan siam anga chumi chuan hemi endpoint hi a connect ang
@router.get("/house/", summary="Search houses by house number for parent house")
def search_house(request, search: str = None):
    queryset = House.objects.all()

    if search:
        queryset = queryset.filter(house_number__icontains=search)

    return [
        {
            "id": house.id,
            "house_number": house.house_number
        }
        for house in queryset[:20]
    ]



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
    photo_url: Optional[str] = None
    age: Optional[int]
    occupations: List[str] = []
    class Config:
        orm_mode = True

        
class PersonListOut(BaseModel):
    id: int
    first_name: str
    hnam_hming: Optional[str] = None
    dob: Optional[date] = None
    epic_number: Optional[str] = None
    aadhar_number: Optional[str] = None
    house_number: Optional[str] = None
    mobile: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    photo_url: Optional[str] = None
    age: Optional[int]
#test
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

class HouseOut(BaseModel):
    house_number: str
    veng_name: Optional[str] = None
    is_owner: bool
    head_name: Optional[str] = None


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

class PersonalQualificationEntry(BaseModel):
    person_id: int
    education_id: int
    year_of_passing: Optional[int] = None
    institution_name: Optional[str] = None
    grade_or_marks: Optional[str] = None
    certificate_number: Optional[str] = None
    remarks: Optional[str] = None

# Bulk submission schema (list of entries)
class BulkPersonalQualificationCreate(BaseModel):
    qualifications: List[PersonalQualificationEntry]

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
    
class OccupationOut(BaseModel):
    id: int
    name: str