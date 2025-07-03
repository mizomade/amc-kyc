from django.db import models
from core.models import Veng
from kyc.models import Person

# Create your models here.
class CertificateType(models.Model):
    """
    Master list of certificate categories issued by AMC.
    Example: Residential Certificate, Income Certificate, NOC, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name



class Certificate(models.Model):
    """
    Stores each issued certificate.
    """
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='certificates')
    certificate_type = models.ForeignKey(CertificateType, on_delete=models.CASCADE, related_name='certificates')

    citizen_locality = models.ForeignKey(Veng, null=True, blank=True, on_delete=models.SET_NULL)
    details = models.TextField(null=True, blank=True)  # Rich text body for the certificate’s content

    application_date = models.DateField(auto_now_add=True)
    issue_date = models.DateField(null=True, blank=True)

    certificate_number = models.CharField(max_length=100, unique=True)  # Optional: auto generate for print/export

    issued_by = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.certificate_number} - {self.person} - {self.certificate_type}"




class CertificateTemplate(models.Model):
    """
    Stores reusable templates for each certificate type.
    Example: Standard format for Residential Certificate, Income Certificate, etc.
    """
    certificate_type = models.ForeignKey(
        'CertificateType',
        on_delete=models.CASCADE,
        related_name='templates'
    )
    name = models.CharField(max_length=100)
    body = models.TextField(help_text="Use placeholders like {{ citizen_name }}, {{ address }}")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['certificate_type', 'name']]

    def __str__(self):
        return f"{self.name} ({self.certificate_type.name})"
