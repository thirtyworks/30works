import uuid

from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.

class UserProfile(models.Model):
    '''
    Extend default model to contain profile photo
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    bio = models.TextField(default='', blank=True, null=True)
    contact_info = models.TextField(default='', blank=True, null=True)
    blocked = models.BooleanField(default=False)
    insta_handler = models.TextField(default='', blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    date_blocked = models.DateField(blank=True, null=True)
    user_uuid = models.UUIDField(default=None, blank=True, null=True)
    acount_id = models.CharField(default=None,max_length=4, blank=True, null=True, unique=True)

    def __str__(self):
        return '{} Profile'.format(self.user.username)

    def save(self, *args, **kwargs):
        '''
        Overriding default save to implement image downsampling for disk space saving
        '''
        if self.user_uuid is None:
            self.user_uuid = str(uuid.uuid4())

        if self.acount_id is None:
            self.acount_id = str(self.user.id).zfill(4)

        if self.blocked == True:
            User.objects.filter(username=self.user.username).update(is_active=False)
        else:
            User.objects.filter(username=self.user.username).update(is_active=True)

        super(UserProfile, self).save(*args, **kwargs)