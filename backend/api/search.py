from ninja import Router
from django.db.models import Q
from kyc.models import Person,House
from typing import List
from kyc.schema import PersonOut, PersonSearchOut
from datetime import date
router = Router(tags=['Search'])
router = Router()

def calculate_age(dob):
    if not dob:
        return None
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

#Person Seach na tur plus filtering
@router.get("/person/", response=List[PersonOut])
def search_person(
    request,
    search: str = None,
    occupation: str = None,   
    age_group: str = None,    
    id: int = None,
):
    queryset = Person.objects.select_related("house", "father", "mother").prefetch_related("occupations__occupation").all()

    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(hnam_hming__icontains=search) |
            Q(epic_number__icontains=search) |
            Q(aadhar_number__icontains=search) |
            Q(house__house_number__icontains=search) |
            Q(mobile__icontains=search) |
            Q(dob__icontains=search)
        )

    if occupation:
        queryset = queryset.filter(occupations__occupation__name__iexact=occupation)

    if age_group:
        from datetime import date, timedelta

        today = date.today()
        age_ranges = {
            "0-18": (today - timedelta(days=18*365), today),
            "18-35": (today - timedelta(days=35*365), today - timedelta(days=18*365)),
            "35-60": (today - timedelta(days=60*365), today - timedelta(days=35*365)),
            "60 above": (None, today - timedelta(days=60*365)),
        }

        min_date, max_date = age_ranges.get(age_group, (None, None))

        if min_date and max_date:
            queryset = queryset.filter(dob__range=(min_date, max_date))
        elif max_date:
            queryset = queryset.filter(dob__lte=max_date)

    if id:
        queryset = queryset.filter(id=id)

    return [
        PersonOut(
            id=person.id,
            first_name=person.first_name,
            hnam_hming=person.hnam_hming,
            epic_number=person.epic_number,
            dob=person.dob.isoformat() if person.dob else None,
            aadhar_number=person.aadhar_number,
            house_number=person.house.house_number if person.house else None,
            mobile=person.mobile,
            father_name=f"{person.father.first_name} {person.father.hnam_hming}" if person.father else None,
            mother_name=f"{person.mother.first_name} {person.mother.hnam_hming}" if person.mother else None,
            photo_url=request.build_absolute_uri(person.photo.url) if person.photo and person.photo.name else None,
            age=calculate_age(person.dob),
            occupations=[po.occupation.name for po in person.occupations.all()],
        )
        for person in queryset[:50]
    ]



#Father search na fate regitered dawn a pa ber awlsam deuha search na , house_id mil zel in awmzia chu family member dang house dang ami a rawn lang dawnlo tihna
@router.get("/father/", summary="Search for father candidates in the same house")
def search_father(request, house_id: int, name: str = None):
    queryset = Person.objects.filter(house_id=house_id, gender="Male")

    if name:
        queryset = queryset.filter(
            Q(first_name__icontains=name) | Q(hnam_hming__icontains=name)
        )

    return [
        {
            "id": person.id,
            "first_name": person.first_name,
            "hnam_hming": person.hnam_hming
        }
        for person in queryset[:20]
    ]



#chutiang chiah in hetah pawh mother bik search na a ni tawp mai
@router.get("/mother/", summary="Search for mother candidates in the same house")
def search_mother(request, house_id: int, name: str = None):
    queryset = Person.objects.filter(house_id=house_id, gender="Female")

    if name:
        queryset = queryset.filter(
            Q(first_name__icontains=name) | Q(hnam_hming__icontains=name)
        )

    return [
        {
            "id": person.id,
            "first_name": person.first_name,
            "hnam_hming": person.hnam_hming
        }
        for person in queryset[:20]
    ]


#House search na;
#Hmanna tur chu House tamtak and register tawh chuan dropdown ah zawn abuaithllk dawn avangin searchable dropdown frontend ah kan siam anga chumi chuan hemi endpoint hi a connect ang
@router.get("/house/", summary="Search houses by house number for parent house")
def search_house(request, search: str = None):
    queryset = House.objects.all()

    if search:
        queryset = queryset.filter(house_number__icontains=search)

    return [
        {
            "id": house.id,
            "house_number": house.house_number
        }
        for house in queryset[:20]
    ]

