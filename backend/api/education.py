from ninja import Router
from core.models import Education

router = Router(tags=["Education"])

@router.get("/", summary="Get all education options")
def list_educations(request):
    educations = Education.objects.all().values('id', 'name')
    return list(educations)
