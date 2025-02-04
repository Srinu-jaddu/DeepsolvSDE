from django.db import models
from django.utils import timezone

class SocialMediaUser(models.Model):
    facebook_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    profile_pic_url = models.URLField()
    profile_pic_s3_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Page(models.Model):
    username = models.CharField(max_length=100, unique=True)
    facebook_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    profile_pic_url = models.URLField()
    profile_pic_s3_url = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=100)
    followers_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    last_scraped = models.DateTimeField(default=timezone.now)
    
    followers = models.ManyToManyField(SocialMediaUser, related_name='followed_pages')
    following = models.ManyToManyField(SocialMediaUser, related_name='following_pages')

    def __str__(self):
        return self.name

class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    facebook_id = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    posted_at = models.DateTimeField()
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    media_urls = models.JSONField(default=list)
    media_s3_urls = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.page.name} - {self.posted_at}"
