from ninja import Router
from django.db.models import Q
from kyc.models import Person,House
from typing import List
from kyc.schema import PersonOut, PersonSearchOut

router = Router(tags=['Search'])
router = Router()


#Person Seach na tur 
@router.get("/person/", response=List[PersonSearchOut])
def search_person(
    request,
    epic: str = None,
    aadhar: str = None,
    name: str = None,
    hnam_hming: str = None,
    house_number: str = None,
    mobile: str = None,
):
    queryset = Person.objects.select_related("house", "father", "mother").all()

    if epic:
        queryset = queryset.filter(epic_number__icontains=epic)
    if aadhar:
        queryset = queryset.filter(aadhar_number__icontains=aadhar)
    if name:
        queryset = queryset.filter(
            Q(first_name__icontains=name) |
            Q(hnam_hming__icontains=name)
        )
    if hnam_hming:
        queryset = queryset.filter(hnam_hming__icontains=hnam_hming)
    if house_number:
        queryset = queryset.filter(house__house_number__icontains=house_number)
    if mobile:
        queryset = queryset.filter(mobile__icontains=mobile)

    return [
        PersonSearchOut(
            id=person.id,
            name=person.full_name
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

