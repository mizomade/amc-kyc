from ninja import Router
from .schemas import UserSchema

router = Router()

@router.get("/me/", response=UserSchema)
def me(request):
    return request.user
