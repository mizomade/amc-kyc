from ninja import Router
from kyc.models import House, Veng, Person
from kyc.schema import HouseCreate, HouseUpdate, PersonOut
from django.http import Http404
from typing import List

router = Router(tags=['House'])

@router.get("/", summary="Get list of all houses")
def list_houses(request):
    return [{"id": h.id, "house_number": h.house_number} for h in House.objects.all()]

@router.get("/{house_id}/members/", response=List[PersonOut], summary="Get all persons in a house")
def list_house_members(request, house_id: int):
    try:
        house = House.objects.get(id=house_id)
    except House.DoesNotExist:
        raise Http404("House not found")

    return list(Person.objects.filter(house=house).values())




@router.post("/", summary="Create a new house")
def create_house(request, data: HouseCreate):
    house = House.objects.create(
        house_number=data.house_number,
        parent_house_id=data.parent_house_id,
        veng_id=data.veng_id,
        street=data.street,
        landmarks=data.landmarks,
        is_owner=data.is_owner,
        lsc_number=data.lsc_number,
        awmtan_kum=data.awmtan_kum,
        pem_luh_chhan=data.pem_luh_chhan,
        have_tenant=data.have_tenant,
        household_size=data.household_size,
        is_tenant=data.is_tenant,
        landlord_name=data.landlord_name,
        landlord_phone=data.landlord_phone,
        landlord_veng=data.landlord_veng,
        latitude=data.latitude,
        longitude=data.longitude,
    )
    return {"id": house.id, "message": "House created successfully"}


@router.put("/update/{house_id}", summary="Update a house")
def update_house(request, house_id: int, data: HouseUpdate):
    try:
        house = House.objects.get(id=house_id)
    except House.DoesNotExist:
        raise Http404("House not found")

    update_data = data.dict(exclude_unset=True)

    if "parent_house" in update_data:
        parent_id = update_data.pop("parent_house")
        house.parent_house = House.objects.get(id=parent_id) if parent_id else None

    if "veng" in update_data:
        veng_id = update_data.pop("veng")
        house.veng = Veng.objects.get(id=veng_id) if veng_id else None

    for attr, value in update_data.items():
        setattr(house, attr, value)

    house.save()
    return {"message": "House updated successfully"}


@router.delete("/delete/{house_id}", summary="Delete a house")
def delete_house(request, house_id: int):
    try:
        house = House.objects.get(id=house_id)
        house.delete()
        return {"message": "House deleted successfully"}
    except House.DoesNotExist:
        raise Http404("House not found")
