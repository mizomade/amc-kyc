from django.contrib import admin
from .models import CertificateType, IssuedCertificate

# Register your models here.
admin.site.register(CertificateType)
admin.site.register(IssuedCertificate)




