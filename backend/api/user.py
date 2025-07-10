from ninja import Router
from .schemas import UserSchema

router = Router()

@router.get("/me/", response=UserSchema)
def me(request):
    
    user = request.user
    print("user", user)
    return {"username": user.username, "groups": user.groups.all()}
