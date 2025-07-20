from ninja import Router
from django.shortcuts import get_object_or_404
from kyc.models import Person

family_tree_router = Router(tags=["Family Tree v3"])


def build_family_tree(person, include_parents=True, include_children=True, depth=0):
    if not person:
        return None

    # Prepare children from both parents
    children_set = set()
    children = []
    for child in list(person.children_by_father.all()) + list(person.children_by_mother.all()):
        if child.id not in children_set:
            children.append(child)
            children_set.add(child.id)

    # Siblings
    siblings = set()
    if person.father and person.mother:
        father_children = set(person.father.children_by_father.all())
        mother_children = set(person.mother.children_by_mother.all())
        siblings = (father_children & mother_children) - {person}

    return {
        "id": person.id,
        "name": person.full_name,
        "gender": person.gender,
        "photo": person.photo.url if person.photo else None,
        "spouse": {
            "id": person.spouse.id,
            "name": person.spouse.full_name,
        } if person.spouse else None,
        "parents": [
            build_family_tree(person.father, include_parents=True, include_children=False),
            build_family_tree(person.mother, include_parents=True, include_children=False)
        ] if include_parents else [],
        "children": [
            build_family_tree(child, include_parents=False, include_children=True)
            for child in children
        ] if include_children else [],
        "siblings": [
            {
                "id": sib.id,
                "name": sib.full_name
            }
            for sib in siblings
        ]
    }


@family_tree_router.get("/tree/{person_id}", summary="Get full family tree")
def get_family_tree(request, person_id: int):
    person = get_object_or_404(Person, id=person_id)
    tree = build_family_tree(person)
    return tree
