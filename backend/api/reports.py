from ninja import Router
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
from .report_schemas import (
    DashboardDataSchema,
    PersonReportSchema,
    HouseReportSchema,
    QualificationSchema,
    OccupationSchema,
    PersonsReportResponse,
    PersonStatisticsSchema,
    HousesReportResponse,
    HouseStatisticsSchema,
)

router = Router()


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

    gender_distribution = [
        {"label": "Male", "value": male_citizens},
        {"label": "Female", "value": female_citizens},
        {"label": "Other", "value": other_gender_citizens},
    ]

    # Age group breakdown
    today = date.today()
    age_0_18 = Person.objects.filter(dob__gte=today - timedelta(days=18*365.25)).count()
    age_18_35 = Person.objects.filter(dob__lt=today - timedelta(days=18*365.25), dob__gte=today - timedelta(days=35*365.25)).count()
    age_35_60 = Person.objects.filter(dob__lt=today - timedelta(days=35*365.25), dob__gte=today - timedelta(days=60*365.25)).count()
    age_60_plus = Person.objects.filter(dob__lt=today - timedelta(days=60*365.25)).count()

    age_group_distribution = [
        {"label": "0-18", "value": age_0_18},
        {"label": "18-35", "value": age_18_35},
        {"label": "35-60", "value": age_35_60},
        {"label": "60+", "value": age_60_plus},
    ]

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
        "gender_distribution": gender_distribution,
        "age_group_distribution": age_group_distribution,
        "verified_citizens_percentage": round(verified_citizens_percentage, 2),

        "religion_distribution": religion_distribution,
        "top_5_denominations": top_5_denominations,

        "top_5_occupations": top_5_occupations,
        "top_5_education_levels": top_5_education_levels,
        "graduation_trends": graduation_trends,
    }


@router.get("/persons", response=PersonsReportResponse)
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
    persons_queryset = (
        Person.objects.all()
        .select_related("house", "religion", "denomination")
        .prefetch_related(
            "qualifications__education",
            "occupations__occupation",
        )
    )

    # Filters
    if gender:
        persons_queryset = persons_queryset.filter(gender=gender)

    if min_age:
        persons_queryset = persons_queryset.filter(dob__lte=date.today() - timedelta(days=min_age * 365.25))

    if max_age:
        persons_queryset = persons_queryset.filter(dob__gte=date.today() - timedelta(days=max_age * 365.25))

    if street:
        persons_queryset = persons_queryset.filter(house__street__icontains=street)

    if marital_status:
        persons_queryset = persons_queryset.filter(marital_status=marital_status)

    if blood_group:
        persons_queryset = persons_queryset.filter(blood_group=blood_group)

    if religion_id:
        persons_queryset = persons_queryset.filter(religion_id=religion_id)

    if denomination_id:
        persons_queryset = persons_queryset.filter(denomination_id=denomination_id)

    if education_id:
        persons_queryset = persons_queryset.filter(qualifications__education_id=education_id).distinct()

    if occupation_id:
        persons_queryset = persons_queryset.filter(occupations__occupation_id=occupation_id).distinct()

    if is_verified is not None:
        persons_queryset = persons_queryset.filter(is_verified=is_verified)

    if veng_id:
        persons_queryset = persons_queryset.filter(house__veng_id=veng_id)

    # Calculate statistics before pagination
    total_citizens = persons_queryset.count()

    gender_distribution = dict(persons_queryset.values('gender').annotate(count=Count('gender')).order_by('gender').values_list('gender', 'count'))

    religion_distribution = dict(persons_queryset.values('religion__name').annotate(count=Count('religion__name')).order_by('religion__name').values_list('religion__name', 'count'))
    religion_distribution = {k if k is not None else "Unknown": v for k, v in religion_distribution.items()}

    denomination_distribution = dict(persons_queryset.values('denomination__name').annotate(count=Count('denomination__name')).order_by('denomination__name').values_list('denomination__name', 'count'))
    denomination_distribution = {k if k is not None else "Unknown": v for k, v in denomination_distribution.items()}

    education_distribution = {}
    for person in persons_queryset.prefetch_related('qualifications__education'):
        for q in person.qualifications.all():
            edu_name = q.education.name if q.education else "Unknown"
            education_distribution[edu_name] = education_distribution.get(edu_name, 0) + 1

    occupation_distribution = {}
    for person in persons_queryset.prefetch_related('occupations__occupation'):
        for o in person.occupations.all():
            occ_name = o.occupation.name if o.occupation else "Unknown"
            occupation_distribution[occ_name] = occupation_distribution.get(occ_name, 0) + 1

    statistics = PersonStatisticsSchema(
        total_citizens=total_citizens,
        gender_distribution=gender_distribution,
        religion_distribution=religion_distribution,
        denomination_distribution=denomination_distribution,
        education_distribution=education_distribution,
        occupation_distribution=occupation_distribution,
    )

    # Build report with pre-fetched data
    report = []
    for person in persons_queryset:
        qual_list = [
            {
                "education": q.education.name,
                "year_of_passing": q.year_of_passing,
                "institution_name": q.institution_name or "",
            }
            for q in person.qualifications.all()
        ]

        occ_list = [
            {
                "occupation": o.occupation.name,
                "employer_name": o.employer_name or "",
                "position_title": o.position_title or "",
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
                "religion_id": person.religion_id,
                "denomination_id": person.denomination_id,
                "qualifications": qual_list,
                "occupations": occ_list,
            }
        )

    return {"persons": report, "statistics": statistics}


@router.get("/houses", response=HousesReportResponse)
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
    houses_queryset = (
        House.objects.all()
        .select_related("veng")
    )

    if is_verified is not None:
        houses_queryset = houses_queryset.filter(is_verified=is_verified)

    if veng_id:
        houses_queryset = houses_queryset.filter(veng_id=veng_id)

    if street:
        houses_queryset = houses_queryset.filter(street__icontains=street)

    if is_owner is not None:
        houses_queryset = houses_queryset.filter(is_owner=is_owner)

    if have_tenant is not None:
        houses_queryset = houses_queryset.filter(have_tenant=have_tenant)

    if is_tenant is not None:
        houses_queryset = houses_queryset.filter(is_tenant=is_tenant)

    if house_number_search:
        houses_queryset = houses_queryset.filter(house_number__icontains=house_number_search)

    if landlord_name_search:
        houses_queryset = houses_queryset.filter(landlord_name__icontains=landlord_name_search)

    if household_size:
        houses_queryset = houses_queryset.filter(household_size=household_size)

    if rent_start_date:
        houses_queryset = houses_queryset.filter(rent_start_date=rent_start_date)

    if landlord_veng:
        houses_queryset = houses_queryset.filter(landlord_veng__icontains=landlord_veng)

    # Calculate statistics before pagination
    total_houses = houses_queryset.count()

    veng_distribution = dict(houses_queryset.values('veng__name').annotate(count=Count('veng__name')).order_by('veng__name').values_list('veng__name', 'count'))
    veng_distribution = {k if k is not None else "Unknown": v for k, v in veng_distribution.items()}

    ownership_distribution = dict(houses_queryset.values('is_owner').annotate(count=Count('is_owner')).order_by('is_owner').values_list('is_owner', 'count'))
    ownership_distribution = {("Owner" if k else "Not Owner"): v for k, v in ownership_distribution.items()}

    tenancy_distribution = dict(houses_queryset.values('have_tenant').annotate(count=Count('have_tenant')).order_by('have_tenant').values_list('have_tenant', 'count'))
    tenancy_distribution = {("Has Tenants" if k else "No Tenants"): v for k, v in tenancy_distribution.items()}

    average_household_size = houses_queryset.aggregate(avg_size=Avg('household_size'))['avg_size'] or 0.0
    average_household_size = round(average_household_size, 2)

    statistics = HouseStatisticsSchema(
        total_houses=total_houses,
        veng_distribution=veng_distribution,
        ownership_distribution=ownership_distribution,
        tenancy_distribution=tenancy_distribution,
        average_household_size=average_household_size,
    )

    report = []
    for house in houses_queryset:
        owner = (
            Person.objects.filter(house=house, is_househead=True)
            .select_related("religion", "denomination")
            .prefetch_related(
                "qualifications__education",
                "occupations__occupation",
            )
            .first()
        )

        tenants = (
            Person.objects.filter(house=house, is_househead=False)
            .select_related("religion", "denomination")
            .prefetch_related("qualifications__education", "occupations__occupation")
        )

        # Prepare owner data
        owner_data = None
        if owner:
            owner_qual = [
                {
                    "education": q.education.name,
                    "year_of_passing": q.year_of_passing,
                    "institution_name": q.institution_name or "",
                }
                for q in owner.qualifications.all()
            ]
            owner_occ = [
                {
                    "occupation": o.occupation.name,
                    "employer_name": o.employer_name or "",
                    "position_title": o.position_title or "",
                }
                for o in owner.occupations.all()
            ]
            owner_data = {
                "id": owner.id,
                "first_name": owner.first_name,
                "hnam_hming": owner.hnam_hming,
                "gender": owner.gender,
                "dob": str(owner.dob) if owner.dob else None,
                "religion_id": owner.religion_id,
                "denomination_id": owner.denomination_id,
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
                    "institution_name": q.institution_name or "",
                }
                for q in tenant.qualifications.all()
            ]
            tenant_occ = [
                {
                    "occupation": o.occupation.name,
                    "employer_name": o.employer_name or "",
                    "position_title": o.position_title or "",
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
                    "religion_id": tenant.religion_id,
                    "denomination_id": tenant.denomination_id,
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

    return {"houses": report, "statistics": statistics}