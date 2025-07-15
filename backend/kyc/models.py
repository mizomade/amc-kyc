from django.db import models
from core.models import *

class House(models.Model):
    house_number = models.CharField(max_length=20, unique=True)

    parent_house = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='rented_units'
    )

    veng = models.ForeignKey(
        Veng,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='houses'
    )

    street = models.CharField(max_length=100, null=True, blank=True)
    landmarks = models.CharField(max_length=100, null=True, blank=True)

    is_owner = models.BooleanField(default=True)
    have_tenant = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)

    lsc_number = models.CharField(max_length=100, null=True, blank=True)
    awmtan_kum = models.PositiveBigIntegerField(null=True, blank=True)
    pem_luh_chhan = models.CharField(max_length=255, null=True, blank=True)
    household_size = models.PositiveBigIntegerField(null=True, blank=True)

    landlord_name = models.CharField(max_length=100, null=True, blank=True)
    landlord_phone = models.CharField(max_length=20, null=True, blank=True)
    landlord_veng = models.CharField(max_length=100, null=True, blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # household_head = models.ForeignKey(
    #     'Person',
    #     null=True, blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='head_of_house'
    # )

    is_verified = models.BooleanField(default=False)
    verified_by = models.CharField(max_length=100, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    rent_start_date = models.DateField(null=True, blank=True)
    rent_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.house_number


class Person(models.Model):
    photo = models.ImageField(upload_to='person_photos/', null=True, blank=True)

    first_name = models.CharField(max_length=100)
    hnam_hming = models.CharField(max_length=100, null=True, blank=True)

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Transgender', 'Transgender'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)

    dob = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    epic_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    aadhar_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    marital_status = models.CharField(max_length=20, null=True, blank=True)

    father = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='children_by_father'
    )
    mother = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='children_by_mother'
    )
    spouse = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='spouse_of'
    )

    house = models.ForeignKey(House, null=True, blank=True, on_delete=models.SET_NULL)
    religion = models.ForeignKey(Religion, null=True, blank=True, on_delete=models.SET_NULL)
    denomination = models.ForeignKey(Denomination, null=True, blank=True, on_delete=models.SET_NULL)
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)

    is_househead = models.BooleanField(default=False,null=True)
    
    is_verified = models.BooleanField(default=False)
    verified_by = models.CharField(max_length=100, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return f"{self.first_name} ({self.house.house_number if self.house else 'No House'})"


# -----------------------------------
# RELATED ENTITIES
# -----------------------------------

class HouseMaid(models.Model):
    name = models.CharField(max_length=100)
    veng = models.CharField(max_length=100)
    epic_number = models.CharField(max_length=20, null=True, blank=True)
    aadhar_number = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)

    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='maids')
    is_verified = models.BooleanField(default=False)
    verified_by = models.CharField(max_length=100, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)



    def __str__(self):
        return self.name


class PersonalQualification(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='qualifications')
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='holders')

    year_of_passing = models.PositiveIntegerField(null=True, blank=True)
    institution_name = models.CharField(max_length=255, null=True, blank=True)
    grade_or_marks = models.CharField(max_length=50, null=True, blank=True)
    certificate_number = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    class Meta:
        unique_together = [['person', 'education']]

    def __str__(self):
        return f"{self.person} - {self.education}"


class PersonalOccupation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='occupations')
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE, related_name='holders')

    employer_name = models.CharField(max_length=255, null=True, blank=True)
    position_title = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)  # Null = current
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    
    class Meta:
        unique_together = [['person', 'occupation', 'employer_name']]

    def __str__(self):
        return f"{self.person} - {self.occupation} at {self.employer_name or 'N/A'}"


class Attachment(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='attachments')
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='kyc_documents/')
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person} - {self.document_type.name}"