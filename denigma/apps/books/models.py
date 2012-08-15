from django.db import models #(the database tables)


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField('e-mail', blank=True)
    last_accessed = models.DateField(blank=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class BookManager(models.Manager):
    def title_count(self, keyword):
        return self.filter(title__icontains=keyword).count()


class DanielBookManager(models.Manager):
    def get_query_set(self):
        return super(DanielBookManager, self).get_query_set().filter(author='Daniel Wuttke')


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, blank=True)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    publication_date = models.DateField(blank=True,null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    objects = models.Manager()          # The default manager.
    count_objects = BookManager()       # A counter manager.
    daniel_objects = DanielBookManager()  # The Daniel-specific manager (allows .all(), .filter(), .count())
    #name = models.CharField(max_length=50)
    #pub_date = models.DateField()
    
    def __unicode__(self):
        return self.title


class PersonManager(models.Manager):
    def first_names(self, last_name):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT DISTINCT first_name
        FROM book_person
        WHERE last_name = %s""", [last_name])
        return [row[0] for row in cursor.fetchone()]


class MaleManager(models.Manager):
    def get_query_set(self):
        return super(MaleManager, self).get_query_set().filter(sex='M')


class FemaleManager(models.Manager):
    def get_query_set(self):
        return super(FemaleManager, self).get_query_set().filter(sex='F')


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    birth_date = models.DateField(null=True)
    adress = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50) # No, this is not U.S.-centric... wtf?
    people = models.Manager()
    objects = PersonManager()
    men = MaleManager()
    women = FemaleManager()

    def baby_boomer_status(self):
        """Returns the person;s baby-boomer status."""
        import datetime
        if datetime.date(1945, 8, 1) <= self.birth_date <= datetime.date(1964, 12, 31):
            return "Baby boomer"
        if self.birt_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        return "Post-boomer"

    def is_midwester(self):
        """Returns True if this person is from the Midwest."""
        return self.state in ('IL', 'WI', 'MI', 'IN', 'OH', 'IA', 'MO')

    def _get_full_name(self):
        """Returns the person's full name."""
        return u'%s %s' % (self.first_name, self.last_name)
    full_name = property(_get_full_name)    # This is not a method, it is treated as an attribute.


class Group(models.Model):
    name = models.CharField(max_length=128)
    membrs = models.ManyToManyField(Person, through='Membership')

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)


if __name__ == '__main__':
    pass
