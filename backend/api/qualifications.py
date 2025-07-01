from ninja import Router
from kyc.models import PersonalQualification
from kyc.schema import PersonalQualificationCreate, PersonalQualificationUpdate
from django.http import Http404
from typing import List

router = Router(tags=['Personal Qualifications'])

@router.post("/", summary="Create a new personal qualification")
def create_personal_qualification(request, data: PersonalQualificationCreate):
    qualification = PersonalQualification.objects.create(
        person_id=data.person_id,
        education_id=data.education_id,
        year_of_passing=data.year_of_passing,
        institution_name=data.institution_name,
        grade_or_marks=data.grade_or_marks,
        certificate_number=data.certificate_number,
        remarks=data.remarks,
    )
    return {"id": qualification.id, "message": "Personal qualification created successfully"}

@router.get("/{person_id}", summary="Get all personal qualifications for a person", response=List[PersonalQualificationCreate])
def get_personal_qualifications(request, person_id: int):
    return PersonalQualification.objects.filter(person_id=person_id)

@router.put("/{qualification_id}", summary="Update a personal qualification")
def update_personal_qualification(request, qualification_id: int, data: PersonalQualificationUpdate):
    try:
        qualification = PersonalQualification.objects.get(id=qualification_id)
        for attr, value in data.dict().items():
            setattr(qualification, attr, value)
        qualification.save()
        return {"message": "Personal qualification updated successfully"}
    except PersonalQualification.DoesNotExist:
        raise Http404("Personal qualification not found")

@router.delete("/{qualification_id}", summary="Delete a personal qualification")
def delete_personal_qualification(request, qualification_id: int):
    try:
        qualification = PersonalQualification.objects.get(id=qualification_id)
        qualification.delete()
        return {"message": "Personal qualification deleted successfully"}
    except PersonalQualification.DoesNotExist:
        raise Http404("Personal qualification not found")
