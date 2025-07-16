from ninja import Router
from kyc.models import Person, Religion, Denomination, House, Role
from kyc.schema import PersonCreate, PersonUpdate, PersonOut
from django.http import Http404

router = Router(tags=['Person'])

@router.get("/{person_id}", response=PersonOut, summary="Get a single person by ID")
def get_person(request, person_id: int):
    try:
        person = Person.objects.select_related('house', 'father', 'mother').get(id=person_id)
        return person
    except Person.DoesNotExist:
        raise Http404("Person not found")

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




