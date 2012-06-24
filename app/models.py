from django.db import models

class Entry(models.Model):
    title = models.CharField(max_length=1000)
    # A cleaned up version of the title for use in a URL. "Blog Title" gets turned into "blog-title" in post.py.
    normalized_title = models.CharField(max_length=1000)
    tagline = models.CharField(max_length=300)
    body = models.TextField()
    # Set the date upon saving the model.
    date = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'title: %s, tagline: %s, date: %s, body: %s...' % (self.title,
                                                                self.tagline,
                                                                self.date,
                                                                self.body[:30])

# A member of the Apatapateam.
class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # A little blurb about this member, i.e., Luke is infinite.
    tagline = models.CharField(max_length=1000)
    bio = models.TextField()
    # To be done when I figure out what the deal is with ImageFields.
    # image = models.ImageField(upload_to='')

# The number of beads that we've got. There should only be one of these models.
class BeadCount(models.Model):
    beadcount = models.IntegerField()

# The reason why we got beads.
class BeadEntry(models.Model):
    # Automatically set the date to the date which this bead entry was created.
    date = models.DateField(auto_now=True)
    text = models.TextField()
