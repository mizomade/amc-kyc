from ninja import Router
from django.http import Http404
from kyc.models import Person
from typing import Set


router = Router(tags=['Deep Family Tree'])


def build_family_tree(person, depth=2, visited: Set[int] = None):
    """
    Recursive tree builder for Person
    """
    if visited is None:
        visited = set()

    if not person:
        return None

    if person.id in visited:
        return {"id": person.id, "first_name": person.first_name, "note": "cycle detected"}

    visited.add(person.id)

    # Base structure
    node = {
        "id": person.id,
        "first_name": person.first_name,
        "hnam_hming": person.hnam_hming,
        "dob": person.dob,
        "gender": person.gender,
    }

    # Parents
    if depth > 0:
        node["father"] = build_family_tree(person.father, depth - 1, visited) if person.father else None
        node["mother"] = build_family_tree(person.mother, depth - 1, visited) if person.mother else None

    # Spouse (only one)
    if depth > 0 and person.spouse:
        node["spouse"] = build_family_tree(person.spouse, depth - 1, visited)
    else:
        node["spouse"] = None

    # Children by father/mother (combine & unique)
    if depth > 0:
        children_qs = person.children_by_father.all().union(person.children_by_mother.all()).distinct()
        children_list = []
        for child in children_qs:
            if child.id not in visited:
                children_list.append(build_family_tree(child, depth - 1, visited))
        node["children"] = children_list
    else:
        node["children"] = []

    # Siblings (same parents)
    siblings_qs = Person.objects.filter(
        (models.Q(father=person.father) | models.Q(mother=person.mother))
    ).exclude(id=person.id).distinct()
    node["siblings"] = [
        {
            "id": s.id,
            "first_name": s.first_name,
            "gender": s.gender
        } for s in siblings_qs
    ]

    return node


@router.get("/{person_id}/deep-family-tree/", summary="Get a multi-gen family tree")
def deep_family_tree(request, person_id: int):
    try:
        p = Person.objects.select_related('father', 'mother', 'spouse').get(id=person_id)
        tree = build_family_tree(p, depth=3)  # Customize depth here
        return tree
    except Person.DoesNotExist:
        raise Http404("Person not found")
