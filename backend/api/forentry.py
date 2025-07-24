from ninja import Router,Form,File
from django.db.models import Q,F
from kyc.models import Person,House,Religion,Denomination,Role
from typing import List,Optional
from pydantic import BaseModel
from datetime import date
from django.http import Http404
from ninja.errors import HttpError
from ninja.files import UploadedFile
router = Router(tags=['Search'])
router = Router()


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
    age: Optional[int] = None
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
    id:int
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



@router.post("/house/", summary="Create a new house")
def create_house(request, data: HouseCreate):
    house = House.objects.create(
        house_number=data.house_number,
        parent_house_id=data.parent_house_id,
        veng_id=data.veng_id,
        street=data.street,
        landmarks=data.landmarks,
        is_owner=data.is_owner,
        lsc_number=data.lsc_number,
        awmtan_kum=data.awmtan_kum,
        pem_luh_chhan=data.pem_luh_chhan,
        have_tenant=data.have_tenant,
        household_size=data.household_size,
        is_tenant=data.is_tenant,
        landlord_name=data.landlord_name,
        landlord_phone=data.landlord_phone,
        landlord_veng=data.landlord_veng,
        latitude=data.latitude,
        longitude=data.longitude,
    )
    return {"id": house.id, "message": "House created successfully"}



@router.get("/", summary="Get list of all houses")
def list_houses(request):
    return [{"id": h.id, "house_number": h.house_number} for h in House.objects.all()]



@router.get("/{house_id}/members/", response=List[PersonOut], summary="Get all persons in a house")
def list_house_members(request, house_id: int):
    try:
        house = House.objects.get(id=house_id)
    except House.DoesNotExist:
        raise Http404("House not found")

    return list(Person.objects.filter(house=house).values())

# person
@router.post("/person/", summary="Create a new person")
def create_person(
    request,
    first_name: str = Form(...),
    hnam_hming: Optional[str] = Form(None),
    gender: str = Form(...),
    dob: Optional[str] = Form(None),
    blood_group: Optional[str] = Form(None),
    mobile: Optional[str] = Form(None),
    epic_number: Optional[str] = Form(None),
    aadhar_number: Optional[str] = Form(None),
    marital_status: Optional[str] = Form(None),
    father_id: Optional[int] = Form(None),
    mother_id: Optional[int] = Form(None),
    spouse_id: Optional[int] = Form(None),
    house_id: Optional[int] = Form(None),
    religion_id: Optional[int] = Form(None),
    denomination_id: Optional[int] = Form(None),
    photo: Optional[UploadedFile] = File(None),
    # rent_start_date: Optional[str] = Form(None),
    # rent_end_date: Optional[str] = Form(None),
):
    # Uniqueness checks
    if epic_number and Person.objects.filter(epic_number=epic_number).exists():
        raise HttpError(400, "EPIC number must be unique")
    if aadhar_number and Person.objects.filter(aadhar_number=aadhar_number).exists():
        raise HttpError(400, "Aadhar number must be unique")

    person = Person.objects.create(
        first_name=first_name,
        hnam_hming=hnam_hming or None,
        gender=gender,
        dob=dob or None,
        blood_group=blood_group or None,
        mobile=mobile or None,
        epic_number=epic_number or None,
        aadhar_number=aadhar_number or None,
        marital_status=marital_status or None,
        father_id=father_id,
        mother_id=mother_id,
        spouse_id=spouse_id,
        house_id=house_id,
        religion_id=religion_id,
        denomination_id=denomination_id,
        photo=photo if photo else None,
        # rent_start_date=rent_start_date or None,
        # rent_end_date=rent_end_date or None,  
    )

    return {"id": person.id, "message": "Person created successfully"}




@router.put("/update/{person_id}", summary="Update a person")
def update_person(request, person_id: int, data: PersonUpdate):
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        raise Http404("Person not found")

    update_data = data.dict(exclude_unset=True)
    foreign_keys = {
        "father": Person,
        "mother": Person,
        "spouse": Person,
        "house": House,
        "religion": Religion,
        "denomination": Denomination,
        "role": Role,
    }

    for field, model in foreign_keys.items():
        if field in update_data:
            fk_id = update_data.pop(field)
            if fk_id is not None:
                try:
                    setattr(person, field, model.objects.get(id=fk_id))
                except model.DoesNotExist:
                    raise Http404(f"{field.capitalize()} with id {fk_id} not found")
            else:
                setattr(person, field, None)

    for attr, value in update_data.items():
        setattr(person, attr, value)

    person.save()
    return {"message": "Person updated successfully"}

@router.delete("/delete/{person_id}", summary="Delete a person")
def delete_person(request, person_id: int):
    try:
        person = Person.objects.get(id=person_id)
        person.delete()
        return {"message": "Person deleted successfully"}
    except Person.DoesNotExist:
        raise Http404("Person not found")

@router.get("/persons/", response=List[PersonListOut])
def list_persons(request, search: Optional[str] = None):
    queryset = Person.objects.select_related("house", "father", "mother").annotate(
        house_number=F("house__house_number"),
        father_name=F("father__first_name"),
        mother_name=F("mother__first_name"),
        photo_url=F("photo"),
    )

    # If search is provided, filter by first_name or hnam_hming
    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) | Q(hnam_hming__icontains=search)
        )

    person_list = list(queryset.values(
        "id", "first_name", "hnam_hming", "epic_number", "aadhar_number",
        "house_number", "mobile", "father_name", "mother_name", "photo_url", "dob"
    ))

    # Convert image field to absolute URL
    for person in person_list:
        if person["photo_url"]:
            person["photo_url"] = request.build_absolute_uri(person["photo_url"])
            # Calculate age
        dob = person["dob"]
        if dob:
            today = date.today()
            person["age"] = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        else:
            person["age"] = None

    return person_list




def calculate_age(dob):
    if not dob:
        return None
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def dob_range_for_age(min_age, max_age=None):
    today = date.today()

    # Max DOB is the youngest possible (e.g., 18 years ago)
    max_dob = date(today.year - min_age, today.month, today.day)

    # Min DOB is the oldest possible (e.g., 35 years ago)
    if max_age is not None:
        # Add 1 day so we don’t include someone who just turned (max_age + 1)
        min_dob = date(today.year - max_age - 1, today.month, today.day + 1)
    else:
        min_dob = None

    return (min_dob, max_dob)




#Person Seach na tur plus filtering
@router.get("/search/", response=List[PersonOut])
def search_person(
    request,
    search: str = None,
    occupation: str = None,   
    age_group: str = None,    
    id: int = None,
    new_voters: bool = False,
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
        if age_group == "18":
            # Born in the year they turn 18
            this_year = date.today().year
            dob_start = date(this_year - 18, 1, 1)
            dob_end = date(this_year - 18, 12, 31)
            queryset = queryset.filter(dob__range=(dob_start, dob_end))
        else:
            age_mapping = {
                "0-18": (0, 18),
                "18-35": (18, 35),
                "35-60": (35, 60),
                "60 above": (60, None),
            }

            if age_group in age_mapping:
                min_age, max_age = age_mapping[age_group]
                dob_start, dob_end = dob_range_for_age(min_age, max_age)

                if dob_start and dob_end:
                    queryset = queryset.filter(dob__range=(dob_start, dob_end))
                elif dob_end:
                    queryset = queryset.filter(dob__lte=dob_end)
    if new_voters:
        # People turning 18 this year
        this_year = date.today().year
        dob_start = date(this_year - 18, 1, 1)
        dob_end = date(this_year - 18, 12, 31)
        queryset = queryset.filter(dob__range=(dob_start, dob_end))


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


#House  list enna tur citizenlist ami
@router.get("/houses/", response=list[HouseOut])
def list_houses(request):
    houses = House.objects.all()
    results = []

    for house in houses:
        first_member = Person.objects.filter(house=house).first()
        head_name = (
            f"{first_member.first_name} {first_member.hnam_hming or ''}".strip()
            if first_member else None
        )

        results.append({
            "id": house.id,
            "house_number": house.house_number,
            "veng_name": house.veng.name if house.veng else None,
            "is_owner": house.is_owner,
            "head_name": head_name,
        })

    return results

#house search na tho search bar with filtering
@router.get("/houses/search/", response=list[HouseOut])
def search_houses(request, query: str = None, ownership: str = None, veng_id: int = None):
    houses = House.objects.all()

    if query:
        houses = houses.filter(house_number__icontains=query)

    if ownership:
        if ownership == "owned":
            houses = houses.filter(is_owner=True)
        elif ownership == "rented":
            houses = houses.filter(is_owner=False)

    if veng_id:
        houses = houses.filter(veng_id=veng_id)

    results = []
    for house in houses:
        first_member = Person.objects.filter(house=house).first()
        head_name = (
            f"{first_member.first_name} {first_member.hnam_hming or ''}".strip()
            if first_member else None
        )

        results.append({
            "id": house.id,
            "house_number": house.house_number,
            "veng_name": house.veng.name if house.veng else None,
            "is_owner": house.is_owner,
            "head_name": head_name,
        })

    return results



@router.delete("/delete/{person_id}", summary="Delete a person")
def delete_person(request, person_id: int):
    try:
        person = Person.objects.get(id=person_id)
        person.delete()
        return {"message": "Person deleted successfully"}
    except Person.DoesNotExist:
        raise Http404("Person not found")