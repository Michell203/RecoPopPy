from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

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
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    # collections = models.ForeignKey(Collection, on_delete=models.CASCADE, default='') 

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    track_name = models.CharField(max_length=100)
    track_id = models.CharField(max_length=100)
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)


    def __str__(self):
        return self.user
    

