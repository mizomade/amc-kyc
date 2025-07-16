from ninja import Router
from kyc.models import PersonalOccupation
from kyc.schema import PersonalOccupationCreate, PersonalOccupationUpdate
from django.http import Http404
from typing import List

router = Router(tags=['Personal Occupations'])

@router.post("/", summary="Create a new personal occupation")
def create_personal_occupation(request, data: PersonalOccupationCreate):
    occupation = PersonalOccupation.objects.create(
        person_id=data.person_id,
        occupation_id=data.occupation_id,
        employer_name=data.employer_name,
        position_title=data.position_title,
        start_date=data.start_date,
        end_date=data.end_date,
        remarks=data.remarks,
    )
    return {"id": occupation.id, "message": "Personal occupation created successfully"}



@router.get("/{person_id}", summary="Get all personal occupations for a person", response=List[PersonalOccupationCreate])
def get_personal_occupations(request, person_id: int):
    return PersonalOccupation.objects.filter(person_id=person_id)

@router.put("/{occupation_id}", summary="Update a personal occupation")
def update_personal_occupation(request, occupation_id: int, data: PersonalOccupationUpdate):
    try:
        occupation = PersonalOccupation.objects.get(id=occupation_id)
        for attr, value in data.dict().items():
            setattr(occupation, attr, value)
        occupation.save()
        return {"message": "Personal occupation updated successfully"}
    except PersonalOccupation.DoesNotExist:
        raise Http404("Personal occupation not found")

@router.delete("/{occupation_id}", summary="Delete a personal occupation")
def delete_personal_occupation(request, occupation_id: int):
    try:
        occupation = PersonalOccupation.objects.get(id=occupation_id)
        occupation.delete()
        return {"message": "Personal occupation deleted successfully"}
    except PersonalOccupation.DoesNotExist:
        raise Http404("Personal occupation not found")
