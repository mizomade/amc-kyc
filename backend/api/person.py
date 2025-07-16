from ninja import Router,Form,File
from kyc.models import Person, Religion, Denomination, House, Role
from kyc.schema import PersonCreate, PersonUpdate
from django.http import Http404
from ninja.errors import HttpError
from typing import Optional
from ninja.files import UploadedFile

router = Router(tags=['Person'])

@router.post("/", summary="Create a new person")
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
    rent_start_date: Optional[str] = Form(None),
    rent_end_date: Optional[str] = Form(None),
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
        rent_start_date=rent_start_date or None,
        rent_end_date=rent_end_date or None,  
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
            if fk_id:
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




