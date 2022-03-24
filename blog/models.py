from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from django import forms

class Day(models.Model):
    number = models.IntegerField(verbose_name="Day Number", unique=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.number)
    
    class Meta:
        ordering = ['number']
    

class Post(models.Model):
    title = models.CharField(max_length=100)
    datetime_posted = models.DateTimeField(default=timezone.now)
    url = models.URLField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    postpic = models.ImageField( upload_to='post_pics',blank=True, null=True)
    postvideo = EmbedVideoField(blank=True, null=True)
    post_text = models.TextField(blank=True, null=True)
    alt_text = models.CharField(max_length=600, default=None, null=True, blank=True)
    is_private = models.BooleanField(default=False)
    anything_else = models.CharField(max_length=250, default=None, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
    
    def __str__(self):
        return ("Post " + str(self.id) + " " + str(self.title))

    def clean(self):
        super().clean()
        if (not self.postpic) and (not self.url) and (not self.postvideo) and (not self.post_text):
            raise forms.ValidationError("You must specify an image to upload, a webpage URL, a soundcloud/youtube/vimeo link or a Text post!")

def auto_generate_day_pages(sender,**kwargs):
    """
    Automatically creates all 30 days pages. If the pages already exists, it will not run.  
    """
    for i in range(1,31):
        try:
            Day.objects.create(number=i)
            print('Day {} added!'.format(i))
            Day.save
        except:
            if len(Day.objects.all()) == 30:
                print('All 30 days already exist')
                return
            print('Day {} already exists'.format(i))
    print('All 30 days now exist!')
    
        