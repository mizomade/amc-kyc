from ninja import Router
from kyc.models import Person, House
from kyc.models import Person, PersonalQualification, PersonalOccupation, House
from ninja import Schema
from typing import List, Optional
from datetime import date, timedelta

router = Router()

class QualificationSchema(Schema):
    education: str
    year_of_passing: int
    institution_name: str

class OccupationSchema(Schema):
    occupation: str
    employer_name: str
    position_title: str

class PersonReportSchema(Schema):
    id: int
    first_name: str
    hnam_hming: str
    gender: str
    dob: Optional[str]
    qualifications: List[QualificationSchema]
    occupations: List[OccupationSchema]

class HouseReportSchema(Schema):
    id: int
    house_number: str
    veng: str
    is_verified: bool
    owner: Optional[PersonReportSchema]
    tenants: List[PersonReportSchema]

@router.get("/summary")
def summary_report(request):
    """
    Returns a summary report of the number of persons, houses, and families.
    """
    person_count = Person.objects.count()
    house_count = House.objects.count()
    # family_count = Family.objects.count()

    return {
        "persons": person_count,
        "houses": house_count,
        # "families": family_count,
    }

@router.get("/persons", response=List[PersonReportSchema])
def person_report(request, gender: Optional[str] = None, min_age: Optional[int] = None, max_age: Optional[int] = None):
    """
    Returns a list of people with their qualifications and occupations.
    Supports filtering by gender and age.
    """
    persons = Person.objects.all()

    if gender:
        persons = persons.filter(gender=gender)
    
    if min_age:
        persons = persons.filter(dob__lte=date.today() - timedelta(days=min_age * 365))

    if max_age:
        persons = persons.filter(dob__gte=date.today() - timedelta(days=max_age * 365))

    report = []
    for person in persons:
        qualifications = PersonalQualification.objects.filter(person=person)
        occupations = PersonalOccupation.objects.filter(person=person)

        qual_list = [{"education": q.education.name, "year_of_passing": q.year_of_passing, "institution_name": q.institution_name} for q in qualifications]
        occ_list = [{"occupation": o.occupation.name, "employer_name": o.employer_name, "position_title": o.position_title} for o in occupations]

        report.append({
            "id": person.id,
            "first_name": person.first_name,
            "hnam_hming": person.hnam_hming,
            "gender": person.gender,
            "dob": person.dob,
            "qualifications": qual_list,
            "occupations": occ_list,
        })

    return report

@router.get("/houses", response=List[HouseReportSchema])
def house_report(request, is_verified: Optional[bool] = None):
    """
    Returns a list of houses with their owners and tenants.
    Supports filtering by verification status.
    """
    houses = House.objects.all()

    if is_verified is not None:
        houses = houses.filter(is_verified=is_verified)

    report = []
    for house in houses:
        owner = Person.objects.filter(house=house, is_househead=True).first()
        tenants = Person.objects.filter(house=house, is_househead=False)

        owner_data = None
        if owner:
            owner_data = {
                "id": owner.id,
                "first_name": owner.first_name,
                "hnam_hming": owner.hnam_hming,
                "gender": owner.gender,
                "dob": owner.dob,
                "qualifications": [],
                "occupations": [],
            }

        tenants_data = []
        for tenant in tenants:
            tenants_data.append({
                "id": tenant.id,
                "first_name": tenant.first_name,
                "hnam_hming": tenant.hnam_hming,
                "gender": tenant.gender,
                "dob": tenant.dob,
                "qualifications": [],
                "occupations": [],
            })

        report.append({
            "id": house.id,
            "house_number": house.house_number,
            "veng": house.veng.name,
            "is_verified": house.is_verified,
            "owner": owner_data,
            "tenants": tenants_data,
        })

    return report
