from djongo import models

# Create your models here.

class Person(models.Model):
    _id = models.ObjectIdField()
    index = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    age = models.SmallIntegerField()
    eyeColor = models.CharField(max_length=20)
    balance = models.CharField(max_length=50)
    tags = models.JSONField()
    friends = models.JSONField()
    greeting = models.CharField(max_length=100)
    favoriteFruit = models.CharField(max_length=30)
    objects = models.DjongoManager()
