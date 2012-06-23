from django.db import models

class Entry(models.Model):
    title = models.CharField(max_length=1000)
    normalized_title = models.CharField(max_length=1000)
    tagline = models.CharField(max_length=300)
    body = models.TextField()
    date = models.DateTimeField()
    
    def __unicode__(self):
        return u'title: %s, tagline: %s, date: %s, body: %s...' % (self.title,
                                                                self.tagline,
                                                                self.date,
                                                                self.body[:30])
