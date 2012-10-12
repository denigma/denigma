"""Uploads photos to S3.
TODO:
- Instead of transferring the upload contents to the server the to S3,
  have user's browser directly upload to S3.
  See: http://developer.amazonwebservices.com/connect/entry!default.jspa?categoryID=139&externalID=1434&fromSearchPage=true
- Access control: Granting different users with different access.
  See: http://docs.amazonwebservices.com/AmazonS3/latest/dev/UsingAuthAccess.html
"""
from django import forms
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import mimetypes

from models import Image


class UploadForm(forms.Form):
    file = forms.ImageField(label='Select photo to upload')

bucket = "dgallery"

def index(request):
    def store_in_s3(filename, content):
        pass
        conn = S3Connection(settings.ACCESS_KEY, settings.PASS_KEY)
        b = conn.create_bucket(bucket) # Bucket name
        # if it doens't exist it creates a new one, otherweise it retrives it.
        mime = mimetypes.guess_type(filename)[0] # Determines filetype.
        k = Key(b)
        k.key = filename
        k.set_metadata('Content-Type', mime)
        k.set_contents_from_string(content)
        k.set_acl('public-read')
        
    photos = Image.objects.all().order_by('-uploaded')
    if not request.method == "POST":
        f = UploadForm()
        return render_to_response('./gallery/index.html', {'form':f, 'photos':photos},
                                  context_instance=RequestContext(request))

    f = UploadForm(request.POST, request.FILES)
    if not f.is_valid():
        return render_to_response('./gallery/index.html', {'form':f, 'photos':photos},
                                  context_instance=RequestContext(request))
    
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
    return render_to_response('./gallery/index.html', {'form':f, 'photos':photos},
                              context_instance=RequestContext(request))
