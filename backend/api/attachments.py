from ninja import Router, File,Form
from ninja.files import UploadedFile
from kyc.models import Attachment
from kyc.schema import AttachmentCreate, AttachmentUpdate
from django.http import Http404
from typing import List

router = Router(tags=['Attachments'])

@router.post("/", summary="Create a new attachment")
def create_attachment(
    request,
    person_id: int = Form(...),
    document_type_id: int = Form(...),
    remarks: str = Form(None),
    file: UploadedFile = File(None),   
):
    attachment = Attachment.objects.create(
        person_id=person_id,
        document_type_id=document_type_id,
        remarks=remarks,
    )

    if file:
        attachment.file = file
        attachment.save()

    return {"id": attachment.id, "message": "Attachment created successfully"}


@router.get("/{person_id}", summary="Get all attachments for a person", response=List[AttachmentCreate])
def get_attachments(request, person_id: int):
    return Attachment.objects.filter(person_id=person_id)

@router.put("/{attachment_id}", summary="Update an attachment")
def update_attachment(request, attachment_id: int, data: AttachmentUpdate):
    try:
        attachment = Attachment.objects.get(id=attachment_id)
        for attr, value in data.dict().items():
            setattr(attachment, attr, value)
        attachment.save()
        return {"message": "Attachment updated successfully"}
    except Attachment.DoesNotExist:
        raise Http404("Attachment not found")

@router.delete("/{attachment_id}", summary="Delete an attachment")
def delete_attachment(request, attachment_id: int):
    try:
        attachment = Attachment.objects.get(id=attachment_id)
        attachment.delete()
        return {"message": "Attachment deleted successfully"}
    except Attachment.DoesNotExist:
        raise Http404("Attachment not found")
