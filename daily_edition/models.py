from django.contrib.auth.models import User
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=30)
    followers = models.ManyToManyField(User, through='OrderedFollow',
                                       related_name='influencers')

    class Meta:
        verbose_name_plural = 'people'

    def __unicode__(self):
        return self.name

class Alias(models.Model):
    name = models.CharField(max_length=30)
    person = models.ForeignKey(Person, related_name='aliases')

    class Meta:
        verbose_name_plural = 'aliases'

    def __unicode__(self):
        return self.name

class Site(models.Model):
    KIND_CHOICES = [
        (u'feed', u'Feed'),
        (u'flickr', u'Flickr'),
        (u'linkedin', u'LinkedIn'),
        (u'twitter', u'twitter'),
        (u'identica', u'Identica'),
        (u'delicious', u'Delicious'),
        (u'vimeo', u'Vimeo'),
        (u'youtube', u'YouTube'),
        (u'picasa', u'Picasa')
    ]

    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    title = models.CharField(max_length=60, null=True)
    url = models.URLField()
    feed = models.URLField(null=True)
    person = models.ForeignKey(Person, related_name='sites')
    last_update = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.title or self.url

class OrderedFollow(models.Model):
    user = models.ForeignKey(User)
    person = models.ForeignKey(Person)
    priority = models.IntegerField()

class Article(models.Model):
    url = models.URLField(unique=True)
    site = models.ForeignKey(Site, related_name='articles')
    title = models.CharField(max_length=40)
    body = models.TextField()
    published = models.DateTimeField(null=True)
    received = models.DateTimeField(null=True)

class Issue(models.Model):
    user = models.ForeignKey(User)
    articles = models.ManyToManyField(Article)
    published = models.DateTimeField()
