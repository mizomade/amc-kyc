from ninja import Router
from kyc.models import Role

router = Router(tags=["Role"]) 
@router.get("/", summary="Get list of Roles for dropdown")
def list_roles(request):
    return [{"id": r.id, "name": r.name} for r in Role.objects.all()]
