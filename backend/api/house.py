from ninja import Router
from kyc.models import House, Veng, Person, HouseMaid, PersonalQualification, PersonalOccupation, Attachment, Religion, Denomination, Role, Education, Occupation, DocumentType
from kyc.schema import HouseCreate, HouseUpdate, PersonOut, HouseOut, HouseMaidOut, PersonalQualificationOut, PersonalOccupationOut, AttachmentOut, VengOut, ReligionOut, DenominationOut, RoleOut, EducationOut, OccupationOut, DocumentTypeOut, PersonRelationOut
from django.http import Http404
from typing import List, Optional, get_origin, get_args
from django.shortcuts import get_object_or_404
from datetime import date, datetime

router = Router(tags=['House'])

def serialize_model_instance(instance, schema):
    if not instance:
        return None

    data = {}
    for field_name, field_info in schema.model_fields.items(): # field_info is a FieldInfo object
        value = None
        django_attr_name = field_name # Default mapping

        # Specific mappings for Django RelatedManagers to Pydantic list fields
        if field_name == 'members':
            django_attr_name = 'person_set'
        elif field_name == 'tenants':
            django_attr_name = 'rented_units'
        elif field_name == 'maids':
            django_attr_name = 'maids' # This one already matches

        if hasattr(instance, django_attr_name):
            value = getattr(instance, django_attr_name)

        # Handle RelatedManager (for lists of related objects)
        if hasattr(value, 'all') and callable(value.all()):
            item_schema = None
            if field_name == 'members':
                item_schema = PersonOut
            elif field_name == 'tenants':
                item_schema = HouseOut
            elif field_name == 'maids':
                item_schema = HouseMaidOut
            elif field_name == 'qualifications':
                item_schema = PersonalQualificationOut
            elif field_name == 'occupations':
                item_schema = PersonalOccupationOut
            elif field_name == 'attachments':
                item_schema = AttachmentOut

            if item_schema:
                data[field_name] = [serialize_model_instance(item, item_schema) for item in value.all()]
            else:
                # If it's a RelatedManager but no specific item_schema, default to empty list
                data[field_name] = []
        # Direct value types (str, int, float, bool, None)
        elif isinstance(value, (str, int, float, bool, type(None))):
            data[field_name] = value
        # ImageFieldFile to URL
        elif hasattr(value, 'url') and field_name == 'photo':
            data[field_name] = value.url if value else None
        # Nested Model Instances (single related objects)
        elif isinstance(value, (Person, House, Veng, Religion, Denomination, Role, Education, Occupation, DocumentType, HouseMaid)):
            nested_schema = None
            if field_name == 'house':
                nested_schema = HouseOut
            elif field_name == 'veng':
                nested_schema = VengOut
            elif field_name in ['father', 'mother', 'spouse']:
                nested_schema = PersonRelationOut
            elif field_name == 'religion':
                nested_schema = ReligionOut
            elif field_name == 'denomination':
                nested_schema = DenominationOut
            elif field_name == 'role':
                nested_schema = RoleOut
            elif field_name == 'education':
                nested_schema = EducationOut
            elif field_name == 'occupation':
                nested_schema = OccupationOut
            elif field_name == 'document_type':
                nested_schema = DocumentTypeOut
            elif field_name == 'parent_house':
                nested_schema = HouseOut

            if nested_schema:
                data[field_name] = serialize_model_instance(value, nested_schema)
            else:
                data[field_name] = None
        # Date and DateTime objects to ISO format strings
        elif isinstance(value, (date, datetime)):
            data[field_name] = value.isoformat() if value else None
        # Fallback for other types
        else:
            # Check if the Pydantic schema field is a list type
            field_annotation = field_info.annotation
            if get_origin(field_annotation) is list or get_origin(field_annotation) is List:
                data[field_name] = [] # Ensure list fields are always lists
            else:
                data[field_name] = value
    return data

@router.get("/{house_id}", response=HouseOut, summary="Get a single house by ID")
def get_house(request, house_id: int):
    house = get_object_or_404(
        House.objects.select_related(
            'veng',
            'parent_house'
        ).prefetch_related(
            'person_set__qualifications__education',
            'person_set__occupations__occupation',
            'person_set__attachments__document_type',
            'person_set__house__veng',
            'person_set__religion',
            'person_set__denomination',
            'person_set__role',
            'person_set__father',
            'person_set__mother',
            'person_set__spouse',
            'rented_units__veng',
            'rented_units__person_set',
            'rented_units__maids',
            'maids'
        ),
        id=house_id
    )

    serialized_house_data = serialize_model_instance(house, HouseOut)
    return HouseOut.model_validate(serialized_house_data)

@router.get("/details/{house_id}", response=HouseOut, summary="Get detailed house information by ID")
def get_house_details(request, house_id: int):
    house = get_object_or_404(
        House.objects.select_related(
            'veng',
            'parent_house'
        ).prefetch_related(
            'person_set__qualifications__education',
            'person_set__occupations__occupation',
            'person_set__attachments__document_type',
            'person_set__house__veng',
            'person_set__religion',
            'person_set__denomination',
            'person_set__role',
            'person_set__father',
            'person_set__mother',
            'person_set__spouse',
            'rented_units__veng',
            'rented_units__person_set',
            'rented_units__maids',
            'maids'
        ),
        id=house_id
    )

    serialized_house_data = serialize_model_instance(house, HouseOut)
    return HouseOut.model_validate(serialized_house_data)

@router.get("/", summary="Get list of all houses")
def list_houses(request):
    return [{"id": h.id, "house_number": h.house_number} for h in House.objects.all()]

@router.get("/{house_id}/members", response=List[PersonOut], summary="Get all persons in a house")
def list_house_members(request, house_id: int):
    try:
        house = House.objects.get(id=house_id)
        return Person.objects.filter(house=house)
    except House.DoesNotExist:
        raise Http404("House not found")

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
        household_head_id=data.household_head_id,
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
