from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    profile_pic = models.ImageField(upload_to='profile_pic',blank=True)
    profile_URL = models.URLField(blank=True)

    def get_absolute_url(self):
        return reverse('home')

    def __str__(self):
        return self.user.username

STATUS = (
    (0,'Draft'),
    (1,'Publish')
)
class Post(models.Model):
    title = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    content = models.TextField()
    image = models.ImageField(upload_to='post', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def save(self, *args,**kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('details',{slug:self.slug})

    def __str__(self):
        return self.title
