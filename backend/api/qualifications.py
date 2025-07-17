from ninja import Router
from core.models import Education
from core.schema import EducationSchema
from kyc.models import PersonalQualification
from kyc.schema import PersonalQualificationCreate, PersonalQualificationUpdate, BulkPersonalQualificationCreate
from django.http import Http404
from typing import List

router = Router(tags=['Personal Qualifications'])



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

@router.get("/", response=List[EducationSchema], summary="List all  qualifications")
def list_all_qualifications(request):
    """
    Returns a list of all personal qualifications.
    """
    return Education.objects.all()


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
