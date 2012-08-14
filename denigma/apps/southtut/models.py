from django.db import models
import sha


class Knight(models.Model):
    name = models.CharField(max_length=100, unique=True)
    of_the_round_table = models.BooleanField()
    dances_whenever_able = models.BooleanField()
    shrubberies = models.IntegerField(null=False)


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    facebook_page_id = models.CharField(max_length=255)


class User(models.Model):
    username = models.CharField(max_length=255)
    #password = models.CharField(max_length=60)
    password_salt = models.CharField(max_length=8, null=True)
    password_hash = models.CharField(max_length=40, null=True)
    name = models.TextField()
    
    def check_password(self, password):
        return sha.sha(self.password_salt + password).hexdigest() == self.password_hash
