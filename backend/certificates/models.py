from django.db import models
from core.models import Veng
from kyc.models import Person

# Create your models here.
class CertificateType(models.Model):
    """
    Master list of certificate categories issued by AMC, including the template for the certificate.
    Example: Residential Certificate, Income Certificate, NOC, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    # Rich text template with placeholders like {{ person.name }}, {{ person.permanent_address }}
    template = models.TextField(help_text="Use placeholders like {{ person.name }}, {{ person.permanent_address }}", default='')
    variables = models.JSONField(default=dict, help_text="List of variables used in the template", blank=True, null=True)

    def __str__(self):
        return self.name

class IssuedCertificate(models.Model):
    """
    Stores each issued certificate, generated from a CertificateType template.
    """
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='issued_certificates')
    certificate_type = models.ForeignKey(CertificateType, on_delete=models.CASCADE, related_name='issued_certificates')
    

    # The final, rendered content of the certificate after replacing placeholders
    content = models.TextField()
    variables = models.JSONField(default=dict, help_text="Variables used in the certificate content", blank=True, null=True)

    application_date = models.DateField(auto_now_add=True)
    issue_date = models.DateField(null=True, blank=True)

    certificate_number = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Optional: auto generate for print/export

    issued_by = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.certificate_number} - {self.person} - {self.certificate_type}"
