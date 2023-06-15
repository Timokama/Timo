import datetime
from django.db import models
from django.utils import timezone
class Person(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50)
    #person = models.ForeignKey(Person, on_delete=models.CASCADE)
    members = models.ManyToManyField(Person, through="Membership")

    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)    
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField('date published')
    invite_reason = models.CharField(max_length=64)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_joined <= now