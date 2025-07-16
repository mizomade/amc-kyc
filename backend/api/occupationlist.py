from ninja import Router
from core.models import Occupation
from kyc.schema import OccupationOut

router = Router()

@router.get("/", summary="Get all education options")
def list_educations(request):
    Occupations = Occupation.objects.all().values('id', 'name')
    return list(Occupations)


