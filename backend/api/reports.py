from ninja import Router, Schema
from typing import List, Optional, Dict
from datetime import date, timedelta
from django.db.models import Count, Avg, F
from django.db.models.functions import ExtractYear

from kyc.models import (
    Person,
    PersonalQualification,
    PersonalOccupation,
    House,
    Religion,
    Denomination,
    Education,
    Occupation,
)

router = Router()


# --------------------------
# 📌 SCHEMAS
# --------------------------

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
    hnam_hming: Optional[str]  # <-- allow null
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
    street: Optional[str]
    landlord_name: Optional[str]
    household_size: Optional[int]
    awmtan_kum: Optional[int]
    have_tenant: bool


class ChartDataSchema(Schema):
    label: str
    value: int

class DashboardDataSchema(Schema):
    # House Stats
    total_houses: int
    owned_houses: int
    rented_houses: int
    verified_houses_count: int
    unverified_houses_count: int
    houses_with_tenants: int
    houses_without_tenants: int
    timeseries_rent_start: Dict[str, int]
    average_household_size: Optional[float]

    # Citizen Stats
    total_citizens: int
    male_citizens: int
    female_citizens: int
    other_gender_citizens: int
    age_group_0_18: int
    age_group_18_35: int
    age_group_35_60: int
    age_group_60_plus: int
    verified_citizens_percentage: float

    # Religion
    religion_distribution: List[ChartDataSchema]
    top_5_denominations: List[ChartDataSchema]

    # Education/Occupation
    top_5_occupations: List[ChartDataSchema]
    top_5_education_levels: List[ChartDataSchema]
    graduation_trends: Dict[str, int]


# --------------------------
# 📌 ROUTES
# --------------------------

@router.get("/dashboard", response=DashboardDataSchema)
def get_dashboard_data(request):
    # A. House Stats
    total_houses = House.objects.count()
    owned_houses = House.objects.filter(is_owner=True).count()
    rented_houses = total_houses - owned_houses  # Assuming not owned means rented
    verified_houses_count = House.objects.filter(is_verified=True).count()
    unverified_houses_count = total_houses - verified_houses_count
    houses_with_tenants = House.objects.filter(have_tenant=True).count()
    houses_without_tenants = total_houses - houses_with_tenants

    # Timeseries house rent start
    timeseries_rent_start_data = House.objects.filter(rent_start_date__isnull=False)
    timeseries_rent_start_data = timeseries_rent_start_data.annotate(year=ExtractYear('rent_start_date'))                                     .values('year')                                     .annotate(count=Count('id'))                                     .order_by('year')
    timeseries_rent_start = {str(item['year']): item['count'] for item in timeseries_rent_start_data}

    average_household_size = House.objects.aggregate(avg_size=Avg('household_size'))['avg_size']
    if average_household_size is not None:
        average_household_size = round(average_household_size, 2)

    # B. Citizen Stats
    total_citizens = Person.objects.count()
    male_citizens = Person.objects.filter(gender='Male').count()
    female_citizens = Person.objects.filter(gender='Female').count()
    other_gender_citizens = Person.objects.exclude(gender__in=['Male', 'Female']).count()

    # Age group breakdown
    today = date.today()
    age_0_18 = Person.objects.filter(dob__gte=today - timedelta(days=18*365.25)).count()
    age_18_35 = Person.objects.filter(dob__lt=today - timedelta(days=18*365.25), dob__gte=today - timedelta(days=35*365.25)).count()
    age_35_60 = Person.objects.filter(dob__lt=today - timedelta(days=35*365.25), dob__gte=today - timedelta(days=60*365.25)).count()
    age_60_plus = Person.objects.filter(dob__lt=today - timedelta(days=60*365.25)).count()

    verified_citizens_count = Person.objects.filter(is_verified=True).count()
    verified_citizens_percentage = (verified_citizens_count / total_citizens * 100) if total_citizens > 0 else 0

    # C. Religion
    religion_distribution_data = Religion.objects.annotate(count=Count('person')).values('name', 'count').order_by('-count')
    religion_distribution = [{'label': item['name'], 'value': item['count']} for item in religion_distribution_data]

    denominations_data = Denomination.objects.annotate(count=Count('person')).values('name', 'count').order_by('-count')[:5]
    top_5_denominations = [{'label': item['name'], 'value': item['count']} for item in denominations_data]

    # D. Education/Occupation
    occupations_data = Occupation.objects.annotate(count=Count('holders')).values('name', 'count').order_by('-count')[:5]
    top_5_occupations = [{'label': item['name'], 'value': item['count']} for item in occupations_data]

    education_levels_data = Education.objects.annotate(count=Count('holders')).values('name', 'count').order_by('-count')[:5]
    top_5_education_levels = [{'label': item['name'], 'value': item['count']} for item in education_levels_data]

    graduation_trends_data = PersonalQualification.objects.filter(year_of_passing__isnull=False)
    graduation_trends_data = graduation_trends_data.annotate(year=F('year_of_passing'))                                 .values('year')                                 .annotate(count=Count('id'))                                 .order_by('year')
    graduation_trends = {str(item['year']): item['count'] for item in graduation_trends_data}

    return {
        "total_houses": total_houses,
        "owned_houses": owned_houses,
        "rented_houses": rented_houses,
        "verified_houses_count": verified_houses_count,
        "unverified_houses_count": unverified_houses_count,
        "houses_with_tenants": houses_with_tenants,
        "houses_without_tenants": houses_without_tenants,
        "timeseries_rent_start": timeseries_rent_start,
        "average_household_size": average_household_size,

        "total_citizens": total_citizens,
        "male_citizens": male_citizens,
        "female_citizens": female_citizens,
        "other_gender_citizens": other_gender_citizens,
        "age_group_0_18": age_0_18,
        "age_group_18_35": age_18_35,
        "age_group_35_60": age_35_60,
        "age_group_60_plus": age_60_plus,
        "verified_citizens_percentage": round(verified_citizens_percentage, 2),

        "religion_distribution": religion_distribution,
        "top_5_denominations": top_5_denominations,

        "top_5_occupations": top_5_occupations,
        "top_5_education_levels": top_5_education_levels,
        "graduation_trends": graduation_trends,
    }


@router.get("/persons", response=List[PersonReportSchema])
def person_report(
    request,
    gender: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    street: Optional[str] = None,
    marital_status: Optional[str] = None,
    blood_group: Optional[str] = None,
    religion_id: Optional[int] = None,
    denomination_id: Optional[int] = None,
    education_id: Optional[int] = None,
    occupation_id: Optional[int] = None,
    is_verified: Optional[bool] = None,
    veng_id: Optional[int] = None,
):
    """
    Filter persons by various criteria. Returns list with qualifications & occupations.
    Optimized to avoid N+1 queries.
    """
    persons = (
        Person.objects.all()
        .select_related("house", "religion", "denomination")
        .prefetch_related(
            "qualifications__education",
            "occupations__occupation",
        )
    )

    # Filters
    if gender:
        persons = persons.filter(gender=gender)

    if min_age:
        persons = persons.filter(dob__lte=date.today() - timedelta(days=min_age * 365.25))

    if max_age:
        persons = persons.filter(dob__gte=date.today() - timedelta(days=max_age * 365.25))

    if street:
        persons = persons.filter(house__street__icontains=street)

    if marital_status:
        persons = persons.filter(marital_status=marital_status)

    if blood_group:
        persons = persons.filter(blood_group=blood_group)

    if religion_id:
        persons = persons.filter(religion_id=religion_id)

    if denomination_id:
        persons = persons.filter(denomination_id=denomination_id)

    if education_id:
        persons = persons.filter(qualifications__education_id=education_id).distinct()

    if occupation_id:
        persons = persons.filter(occupations__occupation_id=occupation_id).distinct()

    if is_verified is not None:
        persons = persons.filter(is_verified=is_verified)

    if veng_id:
        persons = persons.filter(house__veng_id=veng_id)

    # Build report with pre-fetched data
    report = []
    for person in persons:
        qual_list = [
            {
                "education": q.education.name,
                "year_of_passing": q.year_of_passing,
                "institution_name": q.institution_name,
            }
            for q in person.qualifications.all()
        ]

        occ_list = [
            {
                "occupation": o.occupation.name,
                "employer_name": o.employer_name,
                "position_title": o.position_title,
            }
            for o in person.occupations.all()
        ]

        report.append(
            {
                "id": person.id,
                "first_name": person.first_name,
                    "hnam_hming": person.hnam_hming or "",   # fallback safe
                "gender": person.gender,
                "dob": str(person.dob) if person.dob else None,
                "qualifications": qual_list,
                "occupations": occ_list,
            }
        )

    return report


@router.get("/houses", response=List[HouseReportSchema])
def house_report(
    request,
    is_verified: Optional[bool] = None,
    veng_id: Optional[int] = None,
    street: Optional[str] = None,
    is_owner: Optional[bool] = None,
    have_tenant: Optional[bool] = None,
    is_tenant: Optional[bool] = None,
    house_number_search: Optional[str] = None,
    landlord_name_search: Optional[str] = None,
    household_size: Optional[int] = None,
    rent_start_date: Optional[date] = None,
    landlord_veng: Optional[str] = None,
):
    """
    Returns houses with owner & tenants.
    Optimized to avoid N+1 by using `select_related` & `prefetch_related`.
    """
    houses = (
        House.objects.all()
        .select_related("veng")
    )

    if is_verified is not None:
        houses = houses.filter(is_verified=is_verified)

    if veng_id:
        houses = houses.filter(veng_id=veng_id)

    if street:
        houses = houses.filter(street__icontains=street)

    if is_owner is not None:
        houses = houses.filter(is_owner=is_owner)

    if have_tenant is not None:
        houses = houses.filter(have_tenant=have_tenant)

    if is_tenant is not None:
        houses = houses.filter(is_tenant=is_tenant)

    if house_number_search:
        houses = houses.filter(house_number__icontains=house_number_search)

    if landlord_name_search:
        houses = houses.filter(landlord_name__icontains=landlord_name_search)

    if household_size:
        houses = houses.filter(household_size=household_size)

    if rent_start_date:
        houses = houses.filter(rent_start_date=rent_start_date)

    if landlord_veng:
        houses = houses.filter(landlord_veng__icontains=landlord_veng)

    report = []
    for house in houses:
        owner = (
            Person.objects.filter(house=house, is_househead=True)
            .prefetch_related("qualifications__education", "occupations__occupation")
            .first()
        )

        tenants = (
            Person.objects.filter(house=house, is_househead=False)
            .prefetch_related("qualifications__education", "occupations__occupation")
        )

        # Prepare owner data
        owner_data = None
        if owner:
            owner_qual = [
                {
                    "education": q.education.name,
                    "year_of_passing": q.year_of_passing,
                    "institution_name": q.institution_name,
                }
                for q in owner.qualifications.all()
            ]
            owner_occ = [
                {
                    "occupation": o.occupation.name,
                    "employer_name": o.employer_name,
                    "position_title": o.position_title,
                }
                for o in owner.occupations.all()
            ]
            owner_data = {
                "id": owner.id,
                "first_name": owner.first_name,
                "hnam_hming": owner.hnam_hming,
                "gender": owner.gender,
                "dob": str(owner.dob) if owner.dob else None,
                "qualifications": owner_qual,
                "occupations": owner_occ,
            }

        # Prepare tenants data
        tenants_data = []
        for tenant in tenants:
            tenant_qual = [
                {
                    "education": q.education.name,
                    "year_of_passing": q.year_of_passing,
                    "institution_name": q.institution_name,
                }
                for q in tenant.qualifications.all()
            ]
            tenant_occ = [
                {
                    "occupation": o.occupation.name,
                    "employer_name": o.employer_name,
                    "position_title": o.position_title,
                }
                for o in tenant.occupations.all()
            ]
            tenants_data.append(
                {
                    "id": tenant.id,
                    "first_name": tenant.first_name,
                    "hnam_hming": tenant.hnam_hming,
                    "gender": tenant.gender,
                    "dob": str(tenant.dob) if tenant.dob else None,
                    "qualifications": tenant_qual,
                    "occupations": tenant_occ,
                }
            )

        report.append(
            {
                "id": house.id,
                "house_number": house.house_number,
                "veng": house.veng.name if house.veng else "Unknown",
                "is_verified": house.is_verified,
                "owner": owner_data,
                "tenants": tenants_data,
                "street": house.street,
                "landlord_name": house.landlord_name,
                "household_size": house.household_size,
                "awmtan_kum": house.awmtan_kum,
                "have_tenant": house.have_tenant,
            }
        )

    return report
