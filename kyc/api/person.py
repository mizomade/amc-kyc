from ninja import Router
from ..models import Person,Education, Religion, Denomination,House
from ..schema import PersonCreate,PersonUpdate
from django.http import Http404 

router = Router(tags=['Person'])
#Person Siamna..Tah pawh hian Head of the family kha ziah luh hmasak ber angai, Tree structure and duh kher avangin
# Anih loh chuan Father mother son daughter te an in link thei dawn lo =....Buaithalkss
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
        occupation=data.occupation,

        father_id=data.father_id,
        mother_id=data.mother_id,
        spouse_id=data.spouse_id,

        house_id=data.house_id,
        education_id=data.education_id,
        religion_id=data.religion_id,
        denomination_id=data.denomination_id,
    )
    return {"id": person.id, "message": "Person created successfully"}


#Update na tur
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
        "education": Education,
        "religion": Religion,
        "denomination": Denomination,
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




#delete na
@router.delete("/delete/{person_id}", summary="Delete a person")
def delete_person(request, person_id: int):
    try:
        person = Person.objects.get(id=person_id)
        person.delete()
        return {"message": "Person deleted successfully"}
    except Person.DoesNotExist:
        raise Http404("Person not found")