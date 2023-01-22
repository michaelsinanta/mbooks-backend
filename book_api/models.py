from django.db import models
# from django.conf import settings
from users.models import MyUser
from django.core.validators import MaxValueValidator, MinValueValidator
    
# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=100)
    description = models.TextField()
    number_of_pages = models.IntegerField()
    publish_date = models.DateField()
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    image_url = models.ImageField(upload_to='MBooks', blank=True, null=True)