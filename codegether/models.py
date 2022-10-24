import datetime as dt

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE)
    pfp = models.ImageField(upload_to='pfp', null=True)
    bio = models.TextField(blank=True)
    github_url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('profile', args=[str(self.user.username)])

    def get_absolute_url_edit(self):
        return reverse('profile_edit', args=[str(self.user.username)])

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Project(models.Model):
    slug = models.SlugField(max_length=100, null=False, unique=True)
    name = models.CharField(max_length=50)
    desc = models.TextField()
    requirements = models.TextField(blank=True)
    github_url = models.CharField(max_length=100, blank=True)
    creator = models.ForeignKey(User,blank=True,on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(UserProfile, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.name)
            self.slug = f"{self.slug}-{dt.datetime.now().strftime('%H%M%S%d%m%Y')}"
        return super().save(*args, **kwargs)