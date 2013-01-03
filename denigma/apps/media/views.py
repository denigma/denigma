"""Uploads photos to S3.
TODO:
- Instead of transferring the upload contents to the server the to S3,
  have user's browser directly upload to S3.
  See: http://developer.amazonwebservices.com/connect/entry!default.jspa?categoryID=139&externalID=1434&fromSearchPage=true
- Access control: Granting different users with different access.
  See: http://docs.amazonwebservices.com/AmazonS3/latest/dev/UsingAuthAccess.html
"""
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render
from django.conf import settings

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import mimetypes

try:
    from data import get
except ImportError:
    pass

from data.views import View
from add.forms import handlePopAdd

from models import Image
from forms import UploadForm, ArtistForm


bucket = "dgallery"

def store_in_s3(filename, content, bucket=bucket):
    conn = S3Connection(settings.ACCESS_KEY, settings.PASS_KEY)
    b = conn.create_bucket(bucket) # Bucket name
    # if it doesn't exist it creates a new one, otherwise it retrieves it.
    mime = mimetypes.guess_type(filename)[0] # Determines file type.
    k = Key(b)
    k.key = filename
    k.set_metadata('Content-Type', mime)
    k.set_contents_from_string(content)
    k.set_acl('public-read')

def index(request, template='./gallery/index.html'):
    entry = get("Gallery")

    if 'gallery' in request.POST and request.POST['gallery']:
        artist = User.objects.get(pk=request.POST['gallery'])
        photos = Image.objects.filter(artist=artist).order_by('-uploaded')
    else:
        photos = Image.objects.all().order_by('-uploaded')

    if not request.method == "POST" or ('gallery' in request.POST and request.POST['gallery']):
        f = UploadForm()
        af = ArtistForm(request.POST)
        ctx = {'entry': entry, 'form': f, 'photos': photos, 'artist': af}
        return render(request, template, ctx)

    f = UploadForm(request.POST, request.FILES)
    af = ArtistForm(request.POST)


    if not f.is_valid() and not request.FILES['file'].name.endswith('.svg'):
        ctx = {'entry': entry, 'form': f, 'photos': photos, 'artist': af}
        return render(request, template, ctx)

    file = request.FILES['file']
    #print type(file)
    #print dir(file)
    #for k,v in file.items(): print k, v
    #filename = file._get_name() #['filename']
    #content = file['content']
    store_in_s3(file.name, file.read())
    p = Image(url="http://%s.s3.amazonaws.com/%s" % (bucket, file.name))
    print request.user, type(request.user)
    if isinstance(request.user, AnonymousUser):
         p.user = User.objects.get(username="Anonymous")
    else:
        p.user = User.objects.get(username=request.user)
    if f.cleaned_data['artist']:
        p.artist = User.objects.get(username=f.cleaned_data['artist'])
    p.save()
    photos = Image.objects.all().order_by('-uploaded')
    ctx = {'entry': entry, 'form': f, 'photos': photos, 'artist': af}
    return render(request, template, ctx)



class Slides(View):
    def get_context_data(self, **kwargs):
        context = super(Slides, self).get_context_data(**kwargs)
        import re
        #context['slides'] = re.find

def newImage(request):
    return handlePopAdd(request, UploadForm,  'images')

#234567891123456789212345678931234567894123456789512345678961234567897123456789

