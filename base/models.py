from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Language_Category(models.Model):
    lang = models.CharField(max_length=200)

    def __str__(self):
        return self.lang


class Language(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lang = models.CharField(max_length=50)
    extension = models.CharField(max_length=20)
    source = models.TextField()
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-updated']

    def first_two_letters(self):
        return self.user.username[0:2]

    def title_length(self):
        if len(self.title) >= 20:
            return self.title[0:20] + '..'
        else:
            return self.title

    def description_length(self):
        if len(self.description) >= 50:
            return self.description[0:50] + '..'
        else:
            return self.description
