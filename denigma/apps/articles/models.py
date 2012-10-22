from django.db import models
from django.utils.translation import ugettext_lazy as _


class Article(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    year = models.PositiveIntegerField(_("Year"), max_length=4, null=False, blank=False)
    #thumbnail = ImageWithThumbsField(_("thumbnail"), upload_to"images/",
    #    blank=True, null=True, sizes=((250,250),))

    class Meta:
        ordering = ['-year']

    def __unicode__(self):
        return "'%s' - '%s'" % (self.title, self.year)


class Page(models.Model):
    article = models.ForeignKey('Article')#, to_field='publication'
    #page = ImageWithThumbsField(_("page"), upload_to="images/",
    #    blank=True, null=True, sizes=((250,250),))
    number = models.PositiveSmallIntegerField(null=False, blank=False)

    class Meta:
        ordering = ['number']

    def __unicode__(self):
        return '%s' '%s' % (self.article, self.number)