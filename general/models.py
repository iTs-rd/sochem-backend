from django.db import models
from django.contrib.auth.models import User


class ForumPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField(max_length=500)
    body = models.TextField()
    date = models.DateTimeField(auto_now=True)
    author_name = models.TextField(max_length=50, default = "no_name")


class ForumComment(models.Model):
    parent_post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(auto_now_add=True)
    author_name = models.TextField(max_length=50, default = "no_name")


class ForumReply(models.Model):
    parent_comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE)
    reply = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(auto_now_add=True)


def upload_path(instance, filename):
    return '/'.join(['covers', str(instance.title), filename])


def upload_profile_photo(instance, filename):
    return '/'.join(['profile-photo', str(instance.user), str(instance.user)+'.jpeg'])

class Events(models.Model):
    title = models.CharField(max_length=150, blank=False)
    description = models.TextField()
    date = models.DateField()
    venue = models.CharField(max_length=50)
    cover1 = models.ImageField(blank=True, null=True, upload_to=upload_path)
    cover2 = models.ImageField(blank=True, null=True, upload_to=upload_path)
    file1 = models.FileField(upload_to='files', blank=True)
    file2 = models.FileField(upload_to='files', blank=True)

class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, default="No Bio Added")
    batch = models.CharField(max_length=10)
    profile_photo = models.TextField()
