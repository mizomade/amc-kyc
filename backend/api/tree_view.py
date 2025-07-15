from ninja import Router, Schema
from typing import List, Optional
from kyc.models import Person
from django.db.models import Q

router = Router(tags=['Deep Family Tree'])


# === Output Schemas ===

class PersonOut(Schema):
    id: int
    name: str

class PersonSummary(Schema):
    id: int
    name: str

class TreeNodeOut(Schema):
    id: int
    name: str
    father: Optional['TreeNodeOut'] = None
    mother: Optional['TreeNodeOut'] = None
    spouse: Optional['TreeNodeOut'] = None
    siblings: Optional[List[PersonSummary]] = None
    children: Optional[List['TreeNodeOut']] = None

TreeNodeOut.update_forward_refs()


# === Search ===

@router.get("/citizens/search", response=List[PersonOut])
def search_citizens(request, name: str):
    qs = Person.objects.filter(first_name__icontains=name)[:10]
    return [{"id": p.id, "name": p.first_name} for p in qs]


# === Build Tree ===

def build_tree(person: Person, visited: set = None) -> Optional[dict]:
    if person is None:
        return None

    if visited is None:
        visited = set()

    # If already processed, return a leaf node to stop recursion
    if person.id in visited:
        return {
            "id": person.id,
            "name": person.first_name,
            "father": None,
            "mother": None,
            "spouse": None,
            "siblings": None,
            "children": None,
        }

    visited.add(person.id)

    # Siblings remain as summaries to prevent horizontal explosion and complex recursion
    sibling_qs = Person.objects.none()
    q_filter = Q()
    if person.father:
        q_filter |= Q(father=person.father)
    if person.mother:
        q_filter |= Q(mother=person.mother)
    
    if q_filter:
        sibling_qs = Person.objects.filter(q_filter).exclude(id=person.id).distinct()
    
    siblings = [{"id": sib.id, "name": sib.first_name} for sib in sibling_qs]

    # Children: Recurse fully
    children_qs = Person.objects.filter(Q(father=person) | Q(mother=person)).distinct()
    children = [build_tree(child, visited) for child in children_qs]

    # Recurse for parents and spouse
    father_node = build_tree(person.father, visited)
    mother_node = build_tree(person.mother, visited)
    spouse_node = build_tree(person.spouse, visited)

    return {
        "id": person.id,
        "name": person.first_name,
        "father": father_node,
        "mother": mother_node,
        "spouse": spouse_node,
        "siblings": siblings if siblings else None,
        "children": [c for c in children if c] if children else None,
    }


# === Tree View Endpoint ===

@router.get("/citizens/{person_id}/tree", response=TreeNodeOut)
def get_family_tree(request, person_id: int):
    try:
        # Eager load relationships to reduce DB queries inside the recursion
        person = Person.objects.select_related('father', 'mother', 'spouse').get(id=person_id)
    except Person.DoesNotExist:
        return router.create_response(request, {"detail": "Not found"}, status=404)

    # The visited set is created inside the first call if not provided
    return build_tree(person)
