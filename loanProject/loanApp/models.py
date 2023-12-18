from django.db import models
from django.contrib.auth.models import AbstractUser
import shortuuid


class CustomUser(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_customer = models.BooleanField('Is customer', default=False)
    image = models.FileField(upload_to='', null=True, blank=True)


class SavedModel(models.Model):
    name = models.CharField(max_length=50)
    file_path = models.CharField(max_length=255)
    
    

class UserDetail(models.Model):
    userID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    job = models.CharField(max_length=30, null=True)
    salary = models.FloatField(null=True)
    image = models.FileField(upload_to='profile', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True) 
    
    def __str__(self):
        return self.firstName + " " + self.lastName

class LoanApplicant(models.Model):
    LoanID = models.CharField(max_length=12, primary_key=True, default=shortuuid.uuid)
    Age = models.IntegerField() 
    Income = models.FloatField()
    LoanAmount = models.FloatField()
    CreditScore = models.IntegerField()
    MonthsEmployed = models.IntegerField()
    LoanTerm = models.IntegerField()
    DTIRatio = models.FloatField()
    EmploymentType = models.CharField(max_length=50, choices=[('Full time', 'Full-time'), ('Part time', 'Part-time'), ('Self employed', 'Self-employed'), ('unemployed', 'Unemployed')])
    Default = models.IntegerField(null=True, blank=True)
    
class Applicant(models.Model):
    id = models.AutoField(primary_key=True)
    loan_id = models.IntegerField(unique=True, null=True, blank=True) 
    income = models.BigIntegerField()
    age = models.IntegerField()
    experience = models.IntegerField()
    marital_status = models.CharField(max_length=10, choices=[('single', 'Single'), ('married', 'Married')])
    house_ownership = models.CharField(max_length=10, choices=[('rented', 'Rented'), ('owned', 'Owned')])
    car_ownership = models.CharField(max_length=10, choices=[('no', 'No'), ('yes', 'Yes')])
    profession = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    current_job_years = models.IntegerField()
    current_house_years = models.IntegerField()
    risk_flag = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.profession} from {self.city}, {self.state}"  
    
    def get_profession(self):
        return self.profession

    def get_income(self):
        return self.income

    def get_city(self):
        return self.city

    def get_state(self):
        return self.state   
    


