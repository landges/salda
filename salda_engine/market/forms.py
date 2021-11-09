from django import forms
from .models import *


class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields  = ("customer_name","customer_email","customer_phone","customer_address","delivery","payment","confirm","comments")