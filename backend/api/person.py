from ninja import Router
from kyc.models import Person, Religion, Denomination, House, Role, PersonalQualification, PersonalOccupation, Attachment
from kyc.schema import PersonCreate, PersonUpdate, PersonOut
from django.http import Http404
from django.shortcuts import get_object_or_404

router = Router(tags=['Person'])

@router.get("/{person_id}", response=PersonOut, summary="Get a single person by ID")
def get_person(request, person_id: int):
    person = get_object_or_404(
        Person.objects.select_related(
            'house__veng',
            'religion',
            'denomination',
            'role',
            'father',
            'mother',
            'spouse'
        ).prefetch_related(
            'qualifications__education',
            'occupations__occupation',
            'attachments__document_type'
        ),
        id=person_id
    )

    # Manually serialize related managers to lists and photo to URL
    person_data = {
        **person.__dict__,
        "qualifications": [{"id": q.id, "education": q.education, "year_of_passing": q.year_of_passing, "institution_name": q.institution_name, "grade_or_marks": q.grade_or_marks, "certificate_number": q.certificate_number, "remarks": q.remarks} for q in person.qualifications.all()],
        "occupations": [{"id": o.id, "occupation": o.occupation, "employer_name": o.employer_name, "position_title": o.position_title, "start_date": o.start_date, "end_date": o.end_date, "remarks": o.remarks} for o in person.occupations.all()],
        "attachments": [{"id": a.id, "document_type": a.document_type, "file": a.file.url if a.file else None, "remarks": a.remarks, "uploaded_at": a.uploaded_at} for a in person.attachments.all()],
        "photo": person.photo.url if person.photo else None,
    }
    # Handle related objects that are not automatically serialized by Pydantic from __dict__
    if person.house:
        house_data = person.house.__dict__.copy()
        house_data["maids"] = list(person.house.maids.all())
        person_data["house"] = house_data
    if person.religion:
        person_data["religion"] = person.religion
    if person.denomination:
        person_data["denomination"] = person.denomination
    if person.role:
        person_data["role"] = person.role
    if person.father:
        person_data["father"] = person.father
    if person.mother:
        person_data["mother"] = person.mother
    if person.spouse:
        person_data["spouse"] = person.spouse

    return PersonOut.model_validate(person_data)

@router.get("/", summary="List all persons")
def list_persons(request):
    persons = list(Person.objects.all().values())
    return {"persons": persons}


@router.post("/", summary="Create a new person")
def create_person(request, data: PersonCreate):
    person = Person.objects.create(
        first_name=data.first_name,
        hnam_hming=data.hnam_hming,
        gender=data.gender,
        dob=data.dob,
        blood_group=data.blood_group,
        mobile=data.mobile,
        epic_number=data.epic_number,
        aadhar_number=data.aadhar_number,
        marital_status=data.marital_status,

        father_id=data.father_id,
        mother_id=data.mother_id,
        spouse_id=data.spouse_id,

        house_id=data.house_id,
        religion_id=data.religion_id,
        denomination_id=data.denomination_id,
        role_id=data.role_id,
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




