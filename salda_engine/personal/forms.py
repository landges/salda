from django.forms import fields, widgets
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from market.models import *


class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('first_name','last_name','username','password1','password2')


class CancelOrderForm(forms.Form):
	class Meta:
		model = Order
		fields = ("cancel",)

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ('mark','text')