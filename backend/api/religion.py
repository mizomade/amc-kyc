from ninja import Router
from kyc.models import Religion

router = Router(tags=["Religion"]) 
@router.get("/", summary="Get list of Religions for dropdown")
def list_religions(request):
    return [{"id": r.id, "name": r.name} for r in Religion.objects.all()]
