from django.contrib import admin
from .models import House, Person, Education, Religion, Denomination, HouseMaid,Veng

admin.site.register(House)
admin.site.register(Veng)
admin.site.register(Person)
admin.site.register(Education)
admin.site.register(Religion)
admin.site.register(Denomination)
admin.site.register(HouseMaid)
