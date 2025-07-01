from ninja import Router
from django.http import Http404
from typing import List

from certificates.models import CertificateType, Certificate, CertificateTemplate

router = Router(tags=["Certificates"])


# =============================
# CertificateType endpoints
# =============================

@router.post("/types/", summary="Create a certificate type")
def create_certificate_type(request):
    data = request.POST
    cert_type = CertificateType.objects.create(
        name=data.get('name'),
        description=data.get('description')
    )
    return {"id": cert_type.id, "message": "Certificate type created successfully"}


@router.get("/types/", summary="List all certificate types")
def list_certificate_types(request):
    return [
        {
            "id": ct.id,
            "name": ct.name,
            "description": ct.description
        }
        for ct in CertificateType.objects.all()
    ]


@router.put("/types/{type_id}", summary="Update a certificate type")
def update_certificate_type(request, type_id: int):
    try:
        ct = CertificateType.objects.get(id=type_id)
        data = request.POST
        ct.name = data.get('name', ct.name)
        ct.description = data.get('description', ct.description)
        ct.save()
        return {"message": "Certificate type updated successfully"}
    except CertificateType.DoesNotExist:
        raise Http404("Certificate type not found")


@router.delete("/types/{type_id}", summary="Delete a certificate type")
def delete_certificate_type(request, type_id: int):
    try:
        ct = CertificateType.objects.get(id=type_id)
        ct.delete()
        return {"message": "Certificate type deleted successfully"}
    except CertificateType.DoesNotExist:
        raise Http404("Certificate type not found")


# =============================
# CertificateTemplate endpoints
# =============================

@router.post("/templates/", summary="Create a certificate template")
def create_certificate_template(request):
    data = request.POST
    template = CertificateTemplate.objects.create(
        certificate_type_id=data.get('certificate_type_id'),
        name=data.get('name'),
        body=data.get('body'),
        is_active=data.get('is_active', 'true').lower() in ['true', '1']
    )
    return {"id": template.id, "message": "Certificate template created successfully"}


@router.get("/templates/{type_id}", summary="List templates for a certificate type")
def list_certificate_templates(request, type_id: int):
    templates = CertificateTemplate.objects.filter(certificate_type_id=type_id)
    return [
        {
            "id": t.id,
            "certificate_type_id": t.certificate_type_id,
            "name": t.name,
            "body": t.body,
            "is_active": t.is_active,
            "created_at": t.created_at,
            "updated_at": t.updated_at,
        }
        for t in templates
    ]


@router.put("/templates/{template_id}", summary="Update a certificate template")
def update_certificate_template(request, template_id: int):
    try:
        t = CertificateTemplate.objects.get(id=template_id)
        data = request.POST
        t.name = data.get('name', t.name)
        t.body = data.get('body', t.body)
        if 'is_active' in data:
            t.is_active = data.get('is_active', 'true').lower() in ['true', '1']
        t.save()
        return {"message": "Certificate template updated successfully"}
    except CertificateTemplate.DoesNotExist:
        raise Http404("Certificate template not found")


@router.delete("/templates/{template_id}", summary="Delete a certificate template")
def delete_certificate_template(request, template_id: int):
    try:
        t = CertificateTemplate.objects.get(id=template_id)
        t.delete()
        return {"message": "Certificate template deleted successfully"}
    except CertificateTemplate.DoesNotExist:
        raise Http404("Certificate template not found")


# =============================
# Certificate endpoints
# =============================

@router.post("/", summary="Create a certificate")
def create_certificate(request):
    data = request.POST
    cert = Certificate.objects.create(
        person_id=data.get('person_id'),
        certificate_type_id=data.get('certificate_type_id'),
        citizen_locality_id=data.get('citizen_locality_id') or None,
        details=data.get('details'),
        issue_date=data.get('issue_date') or None,
        certificate_number=data.get('certificate_number'),
        issued_by=data.get('issued_by'),
        remarks=data.get('remarks'),
        is_approved=data.get('is_approved', 'false').lower() in ['true', '1'],
    )
    return {"id": cert.id, "message": "Certificate created successfully"}


@router.get("/person/{person_id}", summary="List certificates for a person")
def list_certificates(request, person_id: int):
    certs = Certificate.objects.filter(person_id=person_id)
    return [
        {
            "id": c.id,
            "certificate_number": c.certificate_number,
            "certificate_type_id": c.certificate_type_id,
            "citizen_locality_id": c.citizen_locality_id,
            "details": c.details,
            "application_date": c.application_date,
            "issue_date": c.issue_date,
            "issued_by": c.issued_by,
            "remarks": c.remarks,
            "is_approved": c.is_approved,
            "approved_at": c.approved_at,
        }
        for c in certs
    ]


@router.get("/{certificate_id}", summary="Get single certificate")
def get_certificate(request, certificate_id: int):
    try:
        c = Certificate.objects.get(id=certificate_id)
        return {
            "id": c.id,
            "certificate_number": c.certificate_number,
            "certificate_type_id": c.certificate_type_id,
            "citizen_locality_id": c.citizen_locality_id,
            "details": c.details,
            "application_date": c.application_date,
            "issue_date": c.issue_date,
            "issued_by": c.issued_by,
            "remarks": c.remarks,
            "is_approved": c.is_approved,
            "approved_at": c.approved_at,
        }
    except Certificate.DoesNotExist:
        raise Http404("Certificate not found")


@router.put("/{certificate_id}", summary="Update a certificate")
def update_certificate(request, certificate_id: int):
    try:
        c = Certificate.objects.get(id=certificate_id)
        data = request.POST
        c.citizen_locality_id = data.get('citizen_locality_id') or c.citizen_locality_id
        c.details = data.get('details') or c.details
        c.issue_date = data.get('issue_date') or c.issue_date
        c.certificate_number = data.get('certificate_number') or c.certificate_number
        c.issued_by = data.get('issued_by') or c.issued_by
        c.remarks = data.get('remarks') or c.remarks
        if 'is_approved' in data:
            c.is_approved = data.get('is_approved', 'false').lower() in ['true', '1']
        c.save()
        return {"message": "Certificate updated successfully"}
    except Certificate.DoesNotExist:
        raise Http404("Certificate not found")


@router.delete("/{certificate_id}", summary="Delete a certificate")
def delete_certificate(request, certificate_id: int):
    try:
        c = Certificate.objects.get(id=certificate_id)
        c.delete()
        return {"message": "Certificate deleted successfully"}
    except Certificate.DoesNotExist:
        raise Http404("Certificate not found")
