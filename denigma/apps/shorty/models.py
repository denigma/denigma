from django.conf import settings
from django.db import models


ALPHABET = "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"

def alphabet_encode(num, alphabet=ALPHABET):
    base = len(alphabet)
    num += base

    arr = []

    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def alphabet_decode(string, alphabet=ALPHABET):
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num - base

class SourceURL(models.Model):
    url = models.URLField(verify_exists=False, max_length=250)
    email = models.EmailField()
    admin_key = models.CharField(max_length=40, db_index=True, editable=False, unique=True)

class ShortyURL(models.Model):
    source = models.ForeignKey('SourceURL', related_name='shorty_urls', editable=False)
    label = models.CharField(max_length=50)
    notify = models.BooleanField(default=True)

    @classmethod
    def id_for_key(self, key):
        return alphabet_decode(key)

    @property
    def key(self):
        return alphabet_encode(self.id)

    @property
    def url(self):
        return settings.BASE_URL + "/url/" + self.key

class Visit(models.Model):
    when = models.DateTimeField(auto_now_add=True)
    shorty = models.ForeignKey('ShortyURL', related_name='visits')
    user_agent_string = models.TextField()
