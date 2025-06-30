from django.db import models

class House(models.Model):
    house_number = models.CharField(max_length=20,unique=True)
    #foreugn key
    parent_house = models.ForeignKey('self',null = True,blank= True,on_delete=models.SET_NULL, related_name= 'rented_units')    
   
    veng = models.ForeignKey('Veng',null = True,blank=True,on_delete=models.SET_NULL,related_name='in_veng')
    
    street = models.CharField(max_length=100,blank=True,null=True)
    landmarks = models.CharField(max_length=100,null=True,blank=True)
    is_owner = models.BooleanField(default=True)            #mahni in a cheng nge chenglo
    lsc_number = models.CharField(max_length=100,blank=True,null=True)
    awmtan_kum = models.PositiveBigIntegerField(null=True,blank=True)
    pem_luh_chhan = models.CharField(max_length=255, null=True,blank=True)
    have_tenant = models.BooleanField(default=False)                #inluahtu nei nge neilo
    household_size = models.PositiveBigIntegerField(null=True,blank=True)       #chhungkaw engzat in nge luah
    is_tenant = models.BooleanField(default=False)                  #mi luah nge luah lo
    
    landlord_name = models.CharField(max_length=100,null=True,blank=True)
    landlord_phone = models.CharField(max_length=20,null=True,blank=True)
    landlord_veng = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.house_number


class Veng(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Person(models.Model):
    first_name = models.CharField(max_length=100)
    hnam_hming = models.CharField(max_length=100,null=True,blank=True)

    gender_choice = [('Male','Male'),
                     ('Female','Female'),
                     ('Transgender','Transgender'),
                     ('Other','Other'),
                     ]
    gender = models.CharField(max_length=15,choices=gender_choice)
    
    dob = models.DateField(null=True,blank=True)
    blood_group = models.CharField(max_length=5,null=True,blank=True)
    mobile = models.CharField(max_length=20,blank=True,null=True)
    epic_number = models.CharField(max_length=20,unique=True,null=True,blank=True)
    aadhar_number = models.CharField(max_length=20,unique=True,null=True,blank=True)
    marital_status = models.CharField(max_length=20,blank=True)
    occupation = models.CharField(max_length=50,blank=True)

    #pa/nu in link kualna
    father = models.ForeignKey('self',null=True,blank=True,on_delete=models.SET_NULL,related_name='children_by_father')
    mother = models.ForeignKey('self',null=True,blank=True,on_delete=models.SET_NULL,related_name='children_by_mother')
    spouse = models.ForeignKey('self',null=True,blank=True,on_delete=models.SET_NULL,related_name='spouse_of')

    #foreign keys
    house = models.ForeignKey('House',null=True,blank=True,on_delete=models.SET_NULL)
    education = models.ForeignKey('Education',null=True,blank=True, on_delete=models.SET_NULL)
    religion = models.ForeignKey('Religion', null=True,blank=True,on_delete=models.SET_NULL)
    denomination = models.ForeignKey('Denomination',null=True,blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} ({self.hnam_hming})"




class Education(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Religion(models.Model):
    name = models.CharField(max_length=100 , unique=True)

    def __str__(self):
        return self.name


class Denomination(models.Model):
    name = models.CharField(max_length=100)
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, related_name='denominations')

    class Meta:
        unique_together = [['name', 'religion']] 

    def __str__(self):
        return f"{self.name} ({self.religion.name})"


class HouseMaid(models.Model):
    name = models.CharField(max_length=100)
    veng = models.CharField(max_length=100)
    epic_number = models.CharField(max_length=20, blank=True,null =True)
    aadhar_number = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True , null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)

    house = models.ForeignKey('House', on_delete=models.CASCADE, related_name='maids')

    def __str__(self):
        return self.name
