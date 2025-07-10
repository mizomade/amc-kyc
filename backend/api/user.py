from ninja import Router
from .schemas import UserSchema, UserInSchema, UserUpdateSchema, GroupSchema,MeSchema
from core.models import User
from django.contrib.auth.models import Group
from typing import List
from django.shortcuts import get_object_or_404

router = Router()

@router.get("/", response=List[UserSchema])
def list_users(request):
    users = User.objects.all()
    return users

@router.post("/", response=UserSchema)
def create_user(request, user_in: UserInSchema):
    user = User.objects.create_user(
        username=user_in.username,
        email=user_in.email,
        password=user_in.password
    )
    if user_in.role:
        group, created = Group.objects.get_or_create(name=user_in.role)
        user.groups.add(group)
    user.save()
    return user

@router.put("/{user_id}/", response=UserSchema)
def update_user(request, user_id: int, user_in: UserUpdateSchema):
    user = get_object_or_404(User, id=user_id)
    if user_in.username:
        user.username = user_in.username
    if user_in.email:
        user.email = user_in.email
    if user_in.password:
        user.set_password(user_in.password)
    if user_in.role:
        # Clear existing groups and add the new one
        user.groups.clear()
        group, created = Group.objects.get_or_create(name=user_in.role)
        user.groups.add(group)
    user.save()
    return user

@router.delete("/{user_id}/")
def delete_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return {"success": True}

@router.get("/getch/me/", response=MeSchema)
def me(request):
    
    user = request.user
    print("user", user)
    return {"username": user.username, "groups": user.groups.all()}

@router.get("/getch/groups/", response=List[GroupSchema])
def list_groups(request):
    groups = Group.objects.all()
    return groups

