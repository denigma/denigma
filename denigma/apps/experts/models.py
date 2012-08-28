from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Day(models.Model): #sOfWeek:
    """The day of the week."""
    name = models.CharField(max_length=32)

    def __iter__(self):
        return self

    def next(self):
        for entry in self.objects.all():
            return (entry.id, entry.name)
        

class BusinessHour(models.Model):
    """Working hours in a business day."""
    day = models.ForeignKey(Day) #sOfWeek
    #days = models.CharField(max_length=32, choices=Day)#sOfWeek
    start = models.TimeField()
    end = models.TimeField()


class WorkingHour(models.Model):
    profile = models.ForeignKey("Profile") #User
    day = models.ForeignKey("Day")
    from_time = models.TimeField()
    to_time = models.TimeField()


class OpeningTime(models.Model):
    """The time where an institition is open."""
    day = models.CharField(max_length=10)
    start = models.TimeField()
    end = models.TimeField()


class Institute(models.Model):
    """An academic institution such as a university."""
    name = models.CharField(max_length=250)


class Profile(models.Model): # User
    """The profile of a user.
    dude = int(User.objects.get(username='godric').pk)
    # first get user:
    me = Profile.objects.get(user=myuser)
    friends = me.friend1_set.all()
    """
    GENDER_CHOICES=(
        (1, _('Male')),
        (2, _('Female')),)
    working_hours = models.ManyToManyField("Day", through="WorkingHour", blank=True)
    user = models.ForeignKey(User, blank=True, null=True, unique=True, # user = models.OneToOneField(User, unique=True)
                             verbose_name=_('user'),
                             related_name='data')
    user_name = models.CharField(_('username'), max_length=30, unique=True, blank=True) #
    password = models.CharField(max_length=128, blank=True)
    first_name = models.CharField(_('first_name'), max_length=30) # models.TextField(max_length=50)
    last_name = models.CharField(_('last name'),max_length=30, blank=True) # models.TextField(max_length=50)
    gender = models.PositiveSmallIntegerField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=60, blank=True) #primary_email = models.EmailField(max_length=60, blank=True)
    msn = models.EmailField(max_length=60, blank=True) 
    
    birthday = models.DateField(_('birth date'), blank=True, null=True)

    # For professional Account
    affliation = models.CharField(max_length=250, blank=True, null=True) #instituition_name
    street = models.CharField(max_length=75, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    zip_code = models.IntegerField(max_length=7, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True)
    business_hours = models.ManyToManyField(BusinessHour, blank=True)
    work = models.TextField(blank=True, null=True)
    website = models.URLField(_('website'), blank=True, verify_exists=True)
    
    def __unicode(self):
        name = self.first_name + self.last_name
        return name

    def get_absolute_url(self):
        return "/experts/%s/" % self.user_name.replace(' ', '_')
