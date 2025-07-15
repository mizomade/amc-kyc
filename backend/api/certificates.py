from ninja import Router, Schema
from django.http import Http404
from typing import List, Optional
from datetime import date, datetime
from pydantic import ConfigDict

from certificates.models import CertificateType, IssuedCertificate
from kyc.models import Person

router = Router(tags=["Certificates"])

# =============================
# Schemas
# =============================

class CertificateTypeSchema(Schema):
    id: int
    name: str
    description: Optional[str] = None
    template: str

class IssuedCertificateSchema(Schema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    person_first_name: str
    certificate_type: str
    content: str
    application_date: date
    issue_date: Optional[date] = None
    certificate_number: Optional[str] = None
    issued_by: Optional[str] = None
    remarks: Optional[str] = None
    is_approved: bool
    approved_at: Optional[datetime] = None

class IssueCertificateSchema(Schema):
    person_id: int
    certificate_type_id: int

# =============================
# CertificateType endpoints
# =============================

@router.get("/types/", response=List[CertificateTypeSchema], summary="List all certificate types")
def list_certificate_types(request):
    return CertificateType.objects.all()

@router.post("/types/", summary="Create a certificate type")
def create_certificate_type(request, payload: CertificateTypeSchema):
    cert_type = CertificateType.objects.create(**payload.dict())
    return {"id": cert_type.id, "message": "Certificate type created successfully"}

# =============================
# IssuedCertificate endpoints
# =============================

@router.get("/issued/", response=List[IssuedCertificateSchema], summary="List all issued certificates")
def list_issued_certificates(request):
    issued = IssuedCertificate.objects.select_related("person", "certificate_type")
    return [
        {
            "id": cert.id,
            "person_first_name": cert.person.first_name,
            "certificate_type": cert.certificate_type.name,
            "content": cert.content,
            "application_date": cert.application_date,
            "issue_date": cert.issue_date,
            "certificate_number": cert.certificate_number,
            "issued_by": cert.issued_by,
            "remarks": cert.remarks,
            "is_approved": cert.is_approved,
            "approved_at": cert.approved_at,
        }
        for cert in issued
    ]

@router.post("/issue/", summary="Issue a new certificate")
def issue_certificate(request, payload: IssueCertificateSchema):
    try:
        person = Person.objects.get(id=payload.person_id)
        cert_type = CertificateType.objects.get(id=payload.certificate_type_id)

        # Render the template
        content = cert_type.template
        for field in person._meta.fields:
            placeholder = f"{{{{ person.{field.name} }}}}"
            if placeholder in content:
                content = content.replace(placeholder, str(getattr(person, field.name)))

        # Create the issued certificate
        issued_cert = IssuedCertificate.objects.create(
            person=person,
            certificate_type=cert_type,
            content=content,
            application_date=date.today(),
            is_approved=False,
        )
        return {"id": issued_cert.id, "content": content}

    except Person.DoesNotExist:
        raise Http404("Person not found")
    except CertificateType.DoesNotExist:
        raise Http404("Certificate type not found")
