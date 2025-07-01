from django.db import models
from django.contrib.auth.models import AbstractUser


# -----------------------------------
# LOCATION STRUCTURE
# -----------------------------------

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Veng(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='vengs', null=True, blank=True)

    def __str__(self):
        return self.name


# -----------------------------------
# MASTER TABLES
# -----------------------------------

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Religion(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Denomination(models.Model):
    name = models.CharField(max_length=100)
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, related_name='denominations')

    class Meta:
        unique_together = [['name', 'religion']]

    def __str__(self):
        return f"{self.name} ({self.religion.name})"


class Education(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Occupation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    
class DocumentType(models.Model):
    """
    E.g. 'Aadhar Card', 'Voter ID', 'Birth Certificate', 'Utility Bill'
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Hnam(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    details = models.TextField(blank=True, null=True)

    is_verified = models.BooleanField(default=True)  # Optional, if you do phone/email verification

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role.name if self.role else 'No Role'})"
