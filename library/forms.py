from dataclasses import fields
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

# class PersonForm(forms.Form):
#     first_name = forms.CharField(max_length=50)
#     last_name = forms.CharField(max_length=50)


class AuthorForm(UserCreationForm):
    email = forms.EmailField()
    age = forms.IntegerField()
    
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','password1','password2')

class PublisherForm(ModelForm):

    class Meta:
        model = Publisher
        fields = '__all__'

class LibraryUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','password1','password2')


# Login form
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
        }

# Book form
class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = ('title', 'authors','publisher','publisher_date','book')

        widgets = {
            'authors': forms.CheckboxSelectMultiple()
        }

    