from ninja import Router
from core.models import DocumentType

router = Router()

@router.get("/", summary="Get all document options")
def list_educations(request):
    Documnents = DocumentType.objects.all().values('id', 'name')
    return list(Documnents)

