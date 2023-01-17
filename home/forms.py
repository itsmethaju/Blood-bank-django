from django import forms
from django.contrib.auth.models import User
from . models import *


class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class PersonForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ('date_of_birth','phone','state', 'district', 'city','address','blood_group','gender','image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['district'].queryset = District.objects.none()

        
        #city
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.country.city_set.order_by('name')
        #vanue
        self.fields['city'].queryset = District.objects.none()
        if 'city' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['city'].queryset = City.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            #self.fields['vanue'].queryset = self.instance.country.city.vanue_set.order_by('name')
            self.fields['city'].queryset = self.instance.district.city_set.order_by('name')
        #area
     



class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ('date_of_birth','phone','state', 'district', 'city','address','blood_group','gender','image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['district'].queryset = District.objects.none()

        
        #city
          
        #city
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.state.district_set.order_by('name')
        #vanue
        self.fields['city'].queryset = District.objects.none()
        if 'city' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['city'].queryset = City.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            #self.fields['vanue'].queryset = self.instance.country.city.vanue_set.order_by('name')
            self.fields['city'].queryset = self.instance.district.city_set.order_by('name')
        #area
     

     





class RequestBloodForm(forms.ModelForm):
    class Meta:
        model = RequestBlood
        fields = ('name','email','state', 'district', 'city','address','blood_group','date','phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['district'].queryset = District.objects.none()

        
        #city
          
        #city
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.country.city_set.order_by('name')
        #vanue
        self.fields['city'].queryset = District.objects.none()
        if 'city' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['city'].queryset = City.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            #self.fields['vanue'].queryset = self.instance.country.city.vanue_set.order_by('name')
            self.fields['city'].queryset = self.instance.district.city_set.order_by('name')
        #area
     
