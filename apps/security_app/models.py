from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User

today = datetime.now()

class Sharer(models.Model):
    user = models.ForeignKey( User, on_delete = models.CASCADE )
    code = models.CharField( max_length = 128, blank=True )
    limit_visits = models.IntegerField( default = 7 )
    limit_datetime = models.DateTimeField( default = today + timedelta(days = 7) )
    public = models.BooleanField( default = True )
    def __str__(self):
        return self.user.username