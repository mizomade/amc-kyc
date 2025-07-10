# api.py
from ninja import NinjaAPI, Schema, Router
from typing import List, Optional
from kyc.models import Person

router = Router(tags=['Deep Family Tree'])

class PersonOut(Schema):
    id: int
    name: str

class TreeNodeOut(Schema):
    id: int
    name: str
    father: Optional['TreeNodeOut'] = None
    mother: Optional['TreeNodeOut'] = None
    children: Optional[List['TreeNodeOut']] = None

TreeNodeOut.update_forward_refs()

@router.get("/citizens/search", response=List[PersonOut])
def search_citizens(request, name: str):
    qs = Person.objects.filter(first_name__icontains=name)[:10]
    return [{"id": p.id, "name": p.first_name} for p in qs]

def build_full_tree(person, visited=None):
    if visited is None:
        visited = set()

    if person.id in visited:
        return None  # Prevent cycles

    visited.add(person.id)

    children_qs = Person.objects.filter(father=person) | Person.objects.filter(mother=person)
    children = []
    for child in children_qs:
        child_node = build_full_tree(child, visited)
        if child_node:
            children.append(child_node)

    father_node = build_full_tree(person.father, visited) if person.father else None
    mother_node = build_full_tree(person.mother, visited) if person.mother else None

    return {
        "id": person.id,
        "name": person.first_name,
        "father": father_node,
        "mother": mother_node,
        "children": children if children else None
    }

@router.get("/citizens/{person_id}/tree", response=TreeNodeOut)
def get_family_tree(request, person_id: int):
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        return router.create_response(request, {"detail": "Not found"}, status=404)

    return build_full_tree(person)
