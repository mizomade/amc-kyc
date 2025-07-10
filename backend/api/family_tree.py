from ninja import Router
from django.http import Http404
from kyc.models import Person
from django.db import models

router = Router(tags=['Deep Family Tree'])

def build_family_tree(person, request, depth=5, visited=None, target_house_id=None, show_spouse=True, show_children=True):
    if visited is None:
        visited = set()

    if not person or person.id in visited:
        return None  # Return None to skip rendering duplicates

    visited.add(person.id)

    node = {
        "id": person.id,
        "first_name": person.first_name,
        "hnam_hming": person.hnam_hming,
        "dob": person.dob,
        "gender": person.gender,
        "photo": request.build_absolute_uri(person.photo.url) if person.photo else None,
    }

    if show_spouse and person.spouse and person.spouse.id not in visited:
        spouse_subtree = build_family_tree(
            person.spouse,
            request,
            depth,
            visited,
            target_house_id,
            show_spouse=False,
            show_children=False
        )
        if spouse_subtree:
            node["spouse"] = spouse_subtree

    if depth > 1 and show_children:
        children_qs = Person.objects.select_related('father', 'mother', 'spouse').filter(
            house_id=target_house_id
        ).filter(
            models.Q(father=person) | models.Q(mother=person)
        ).distinct()

        children = []
        for child in children_qs:
            if child.id not in visited:
                subtree = build_family_tree(
                    child,
                    request,
                    depth - 1,
                    visited,
                    target_house_id,
                    show_spouse=True,
                    show_children=True
                )
                if subtree:
                    children.append(subtree)

        if children:
            node["children"] = children

    return node


@router.get("/{person_id}/deep-family-tree/", summary="Get full family tree for house")
def deep_family_tree(request, person_id: int):
    try:
        person = Person.objects.get(id=person_id)
        target_house_id = person.house_id  # use .house_id_id for raw id

        # Find root persons in same house (no parents)
        root_persons = Person.objects.filter(
            house_id=target_house_id,
            father__isnull=True,
            mother__isnull=True,
        )

        # If no root persons found, fallback to person searched
        if not root_persons.exists():
            root_persons = Person.objects.filter(id=person_id)

        trees = []
        visited = set()
        for root in root_persons:
            tree = build_family_tree(root, request, depth=5, target_house_id=target_house_id, visited=visited)
            if tree:
                trees.append(tree)

        if len(trees) == 1:
            return trees[0]

        return trees

    except Person.DoesNotExist:
        raise Http404("Person not found")
