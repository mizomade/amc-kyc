from ninja import Router
from kyc.models import Veng

router = Router(tags=["Veng"]) 
@router.get("/", summary="Get list of Vengs for dropdown when registering Veng")
def list_vengs(request):
    return [{"id": v.id, "name": v.name} for v in Veng.objects.all()]
