from ninja import Router
from kyc.models import Denomination

router = Router(tags=["Denomination"]) 

@router.get("/", summary="Get list of Denominations for dropdown")
def list_denominations(request, religion_id: str = None):
    if religion_id == "":
        religion_id = None

    qs = Denomination.objects.all()
    if religion_id:
        qs = qs.filter(religion_id=religion_id)
    return [{"id": d.id, "name": d.name} for d in qs]
