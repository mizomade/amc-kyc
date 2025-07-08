from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Certificate)
admin.site.register(CertificateType)
admin.site.register(CertificateTemplate)


