from.models import *
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'is_admin', 'is_customer')

class LoanForm(forms.Form):
    Age = forms.IntegerField()
    Income = forms.FloatField()
    LoanAmount = forms.FloatField(label= "Loan Amount")
    CreditScore = forms.IntegerField(label= "Credit Score")
    MonthsEmployed = forms.IntegerField(label= "Months Employed")
    LoanTerm = forms.IntegerField(label= "Loan Term")
    DTIRatio = forms.FloatField(label= "Debt To Income Ratio")
    EmploymentType = forms.ChoiceField(choices=[('----', '----'), ('full time','Full time' ), ('part time', 'Part time'), ('self employed', 'Self employed'), ('unemployed', 'Unemployed')], required=True)
    

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

# mute for now

# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self):
#         cleaned_data = super().clean()
#         username = cleaned_data.get('username')
#         password = cleaned_data.get('password')

#         user = authenticate(username=username, password=password)

#         if user is None or not user.is_active:
#             raise ValidationError("Invalid login credentials")



class NewUserForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields='__all__'
        
       
class ApplicantForm(ModelForm):
    class Meta:
        model=Applicant
        fields='__all__'

class UserForm(ModelForm):
    class Meta:
        model=CustomUser
        fields='__all__'

class UpdateUserForm(forms.Form):
    fname = forms.CharField(label="First name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lname = forms.CharField(label= "Last name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    uname = forms.CharField(label= "User name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label= "Email", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label="Image", widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model=CustomUser
        fields = "__all__"

class DeleteUser(forms.Form):
    confirm = forms.BooleanField(label="Are you sure?")