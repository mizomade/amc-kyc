from ninja import Router
from kyc.models import PersonalQualification
from kyc.schema import  PersonalQualificationUpdate,BulkPersonalQualificationCreate,PersonalQualificationEntry
from django.http import Http404
from typing import List

router = Router(tags=['Personal Qualifications'])

@router.post("/bulk/", summary="Bulk create personal qualifications")
def create_bulk_personal_qualifications(request, data: BulkPersonalQualificationCreate):
    created_ids = []
    for item in data.qualifications:
        qualification = PersonalQualification.objects.create(
            person_id=item.person_id,
            education_id=item.education_id,
            year_of_passing=item.year_of_passing,
            institution_name=item.institution_name,
            grade_or_marks=item.grade_or_marks,
            certificate_number=item.certificate_number,
            remarks=item.remarks,
        )
        created_ids.append(qualification.id)

    return {
        "created_ids": created_ids,
        "message": f"{len(created_ids)} personal qualifications created successfully"
    }



@router.get("/{person_id}", summary="Get all personal qualifications for a person", response=List[PersonalQualificationEntry])
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
