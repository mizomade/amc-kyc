from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, District, Veng, Role, Religion, Denomination, Education, Occupation, DocumentType, Hnam


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'role', 'details')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'role', 'details')}),
    )


admin.site.register(District)
admin.site.register(Veng)
admin.site.register(Role)
admin.site.register(Religion)
admin.site.register(Denomination)
admin.site.register(Education)
admin.site.register(Occupation)
admin.site.register(DocumentType)
admin.site.register(Hnam)
