'''forms file for users app'''
from django import forms
from . models import Profile
from django.forms.widgets import DateInput, Textarea

'''class CustomUserCreationForm'''
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture', 'about', 'age']
        labels = {'picture': 'Profile Pic:',
                  'about': 'Tell us a bit about yourself',
                  'age': 'Your D.O.B'}
        widgets = {'age': DateInput(attrs={'type': 'date'}),
                   'about': Textarea(attrs={'height': 30, 'width': 30})}