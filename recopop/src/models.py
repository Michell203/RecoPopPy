from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Track(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    trackName = models.CharField(max_length=100, default='unknowntrack')
    trackId = models.CharField(max_length=25)

    def __str__(self):
        return self.trackName
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_pass = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    collections = models.ForeignKey(Collection, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.user.username    
    

