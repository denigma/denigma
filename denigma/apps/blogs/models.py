"""This is ane experimental module to modelling mutliple author blogging.

The djangopject weblog is an inspiration of this:
https://www.djangoproject.com/weblog/

For exisitng approaches see:
http://www.djangopackages.com/grids/g/blogs/"""


from django.db import models
##from djangotoolbox.fields import ListField
##
##class Post(models.Model):
##    title = models.CharField(max_lenth=100)
##    text = models.TextField()
##    tags = ListField()
##    comments = ListField()
##      created = models.DateTimeField(auto_now_add=True)
##      updated = models.DateTomeField(auto_now=True)

##class Entry(models.Model):
##    published = models.BooleanField(db_index=True, default=True)
##    created = models.DateField(auto_now_add=True)
##    updated = models.DateField(auto_now=True)
##    title = models.CharField(max_length=64)
##    text = models.TextField()
##
##    def __unicode__(self):
##        return u"%s - %s" % (self.title, self.created)


class Blog(models.Model):
    title = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    #entry = models.ManyToManyField(Entry)

    def __unicode__(self):
       return self.title


"""Once user logs in, s/he can write a new comment (insert into comment table)
or alternatively select the comment of some other user and give his feedback
(insert into comment_feedback)
Select a comment and write his/er own comment with a feedback on the original comment
(inserted into comments table with root_comment as the orignal comment
and inserted into the comment_feedback table for the original comment)"""

#FEEDBACK_CHOICES = {
#    (1, 'FOR'),
#    (-1, 'AGAINST'),
#    (0, 'NEUTRAL'),
#}
#
#class User(models.Model): name = models.CharField(max_length=150)
#from django.contrib.auth.models import User
#
#
#class Comment(models.Model):
#    text = models.CharField(max_length=1000)
#    root_comment = models.ForeignKey('self', null=True, blank=True, related_name="children")
#    written_by = models.ForeignKey(User)
#
#
#class Comment_feedback(models.Model):
#    feedback_user_id = models.ForeignKey(User)
#    comment_id = models.ForeignKey(Comment)
#    feedback_type_id = models.CharField(max_length=20, choices=FEEDBACK_CHOICES)
#
#    class Meta:
#        unique_together = [("feedback_user_id", "info_id")]

