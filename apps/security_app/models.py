from django.db import models
from datetime import timedelta, date
from django.contrib.auth.models import User

class Sharer(models.Model):
    user = models.OneToOneField( User, on_delete = models.CASCADE)
    code = models.CharField( max_length = 128, blank=True, unique = True )
    limit_visits = models.IntegerField( default = 7 )
    limit_datetime = models.DateField( default = date.today() + timedelta(days = 7) )
    public = models.BooleanField( default = True )
    password = models.CharField( max_length = 128, blank=True )
    def __str__(self):
        return self.user.username
