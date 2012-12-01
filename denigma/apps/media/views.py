"""Uploads photos to S3.
TODO:
- Instead of transferring the upload contents to the server the to S3,
  have user's browser directly upload to S3.
  See: http://developer.amazonwebservices.com/connect/entry!default.jspa?categoryID=139&externalID=1434&fromSearchPage=true
- Access control: Granting different users with different access.
  See: http://docs.amazonwebservices.com/AmazonS3/latest/dev/UsingAuthAccess.html
"""
from django import forms
from django.shortcuts import render
from django.conf import settings

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import mimetypes

from models import Image

try:
    from data import get
except ImportError:
    pass


class UploadForm(forms.Form):
    file = forms.ImageField(label='Select photo to upload')


bucket = "dgallery"

def index(request, template='./gallery/index.html'):
    entry = get("Gallery")
    def store_in_s3(filename, content):
        conn = S3Connection(settings.ACCESS_KEY, settings.PASS_KEY)
        b = conn.create_bucket(bucket) # Bucket name
        # if it doesn't exist it creates a new one, otherwise it retrieves it.
        mime = mimetypes.guess_type(filename)[0] # Determines file type.
        k = Key(b)
        k.key = filename
        k.set_metadata('Content-Type', mime)
        k.set_contents_from_string(content)
        k.set_acl('public-read')
        
    photos = Image.objects.all().order_by('-uploaded')
    if not request.method == "POST":
        f = UploadForm()
        ctx = {'entry': entry, 'form': f, 'photos': photos}
        return render(request, template, ctx)

    f = UploadForm(request.POST, request.FILES)
    if not f.is_valid():
        ctx = {'entry': entry, 'form': f, 'photos': photos}
        return render(request, template, ctx)

    file = request.FILES['file']
    #print type(file)
    #print dir(file)
    #for k,v in file.items(): print k, v
    #filename = file._get_name() #['filename']
    #content = file['content']
    store_in_s3(file.name, file.read())
    p = Image(url="http://%s.s3.amazonaws.com/%s" % (bucket, file.name))
    p.save()
    photos = Image.objects.all().order_by('-uploaded')
    ctx = {'entry': entry, 'form': f, 'photos': photos}
    return render(request, template, ctx)

#234567891123456789212345678931234567894123456789512345678961234567897123456789

