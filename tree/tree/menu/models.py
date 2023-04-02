from django.db import models
from django.urls import reverse

# Create your models here.

class Base(models.Model):
    title = models.CharField(max_length=50)
    level = models.PositiveIntegerField(default=0)


class Menu(Base):
    slug = models.SlugField(max_length=200, null=True)
    named_url = models.CharField(max_length=200, blank=True)

    def full_path(self):
        if self.named_url:
            url = reverse(self.named_url)
        else:
            url = f'/{self.slug}/'
        return url
    
    def __str__(self):
        return self.title

class Item(Base):
    menu = models.ForeignKey(Menu, blank=True, null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='items', on_delete=models.CASCADE)
    named_url = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title
    
    def get_url(self):
        if self.named_url:
            url = self.named_url
        elif self.url:
            url = self.url
        else:
            url = '/'
        return url
