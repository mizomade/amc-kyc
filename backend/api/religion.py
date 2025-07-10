from ninja import Router
from core.models import Religion, Denomination  # adjust based on your model location

router = Router(tags=["Religion & Denomination"])

@router.get("/religions/", summary="Get list of Religions for dropdown")
def list_religions(request):
    return [{"id": r.id, "name": r.name} for r in Religion.objects.all()]

@router.get("/denominations/", summary="Get list of Denominations for dropdown (optionally filtered by religion_id)")
def list_denominations(request, religion_id: int = None):
    qs = Denomination.objects.all()
    if religion_id:
        qs = qs.filter(religion_id=religion_id)
    return [{"id": d.id, "name": d.name, "religion_id": d.religion_id} for d in qs]
