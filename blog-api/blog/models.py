
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


# QuerySet Reference
# https://docs.djangoproject.com/en/4.0/ref/models/querysets/



# QuerySet Manager
# https://docs.djangoproject.com/en/4.0/topics/db/managers/
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


# Model Reference
# https://docs.djangoproject.com/en/4.0/ref/models/fields/
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    TAG_CHOICES = (
        ('mundo', 'Mundo'),
        ('esportes','Esportes'),
        ('tecnologia','Tecnologia'),
        ('natureza','Natureza'),
        ('cultura','Cultura'),
        ('dinheiro','Dinheiro'),
        ('política','Política'),
        ('saúde','Saúde'),
        ('turismo','Turismo'),
        ('games','Games'),
    )

    title = models.CharField(max_length=250, unique = True,)
    slug = models.SlugField(max_length=250, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='1') #related_name='blog_posts'
    body = models.TextField(max_length=5000)

    #https://docs.djangoproject.com/en/4.0/ref/models/fields/#datefield
    publish = models.DateTimeField(default=timezone.now)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default='mundo')


    #https://docs.djangoproject.com/en/4.0/topics/db/managers/
    #objects serve para obter tanto as publicações published ou draft
    objects = models.Manager() # The default manager.
    #serve apenas para obter as publicações published
    published = PublishedManager()


# Class Meta reference
# https://docs.djangoproject.com/en/4.0/ref/models/options/
    class Meta:
        ordering = ('-created_date',)
    
    def __str__(self):
        return self.title

    # Gerar SLUG
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse ('blog:post_detail', args=[self.slug])
        # return f'blog/{self.slug}/'



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, )
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=80)
    body = models.TextField(max_length=100)
    publish = models.DateTimeField(default=timezone.now)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('publish',)


    def __str__(self):
        return f'Comment by {self.name} on {self.post}'