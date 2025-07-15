from ninja import Router
from kyc.models import Denomination

router = Router(tags=["Denomination"]) 
@router.get("/", summary="Get list of Denominations for dropdown")
def list_denominations(request):
    return [{"id": d.id, "name": d.name} for d in Denomination.objects.all()]
