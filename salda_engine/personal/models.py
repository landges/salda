from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.

class Review(models.Model):
	user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
	mark = models.IntegerField()
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username + str(self.mark)