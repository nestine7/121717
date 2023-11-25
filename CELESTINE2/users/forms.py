from django import forms
from django.forms import ModelForm
from .models import *


class studentsForm(ModelForm):
    class Meta:
        model=Students
        #fields="__all__"
        fields=('name','units','clubs','email','phone_no')
class studentsUpdateForm(ModelForm):
    class Meta:
        model=Python
        #fields="__all__"
        fields=('name','reg','cat1','cat2','cat3')
class pyattendaceForm(ModelForm):
    class Meta:
        model=pythonAttendance

        fields=('reg','name','From_hrs','To_hrs','present','date')
class jsattendaceForm(ModelForm):
    class Meta:
        model=jsAttendance
        fields=('reg','name','From_hrs','To_hrs','present','date')
class sqlattendaceForm(ModelForm):
    class Meta:
        model=sqlAttendance
        fields=('reg','name','From_hrs','To_hrs','present','date')
class phpattendaceForm(ModelForm):
    class Meta:
        model=phpAttendance
        fields=('reg','name','From_hrs','To_hrs','present','date')