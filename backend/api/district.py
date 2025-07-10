from ninja import Router
from kyc.models import District

router = Router(tags=["District"])

@router.get("/", summary="Get list of Districts for dropdown when registering House")
def list_districts(request):
    return [{"id": d.id, "name": d.name} for d in District.objects.all()]
