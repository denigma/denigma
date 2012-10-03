import re
import math

try:
    from django.http import HttpResponse
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from django import forms
    from django.contrib import messages
    from django.translation import ugettext

    from data import get
except ImportError as e:
    print e

try:
    from browser import br
except ImportError:
    pass


class Input(forms.Form):
    #text = forms.Textarea()
    search = forms.CharField()


class Word(object):
    def __init__(self, key, Nw, IDF, ndw, TF_IDF):
        self.key = key
        self.Nw = Nw
        self.IDF = IDF
        self.ndw = ndw
        self.TF_IDF = TF_IDF


def hits(keyword):
    url = "http://www.google.com/search?q=%s"
    content  = br.open(url % keyword)
    html = content.read()
    regex = "resultStats>About (.+) results<nobr>"
    match = int(re.findall('resultStats>About (.{5,50}?) results', html)[0].replace(',', ''))

    return int(match)

def index(request):
    entry = get('EVA')
    return render_to_response('eva/index.html', {'entry': entry},
        context_instance=RequestContext(request))

def tf_idf(request, keyword="a"):
    form = Input(request.POST or None)
    if request.POST and form.is_valid():
        keyword = request.POST['keyword']
    if 'keyword' in request.POST:
        keyword = request.POST['keyword']
    if 'text' in request.POST:
        text = request.POST['text'].lower()
    else:
        text = keyword.lower()

    N = hits("the")
    words = text.replace('.', ' ').replace(', ', '').split(' ')

    def calculate_tf_idf(keyword):
        Nw = hits(keyword)
        IDF = math.log(1.*N/Nw, 2)
        ndw= 1.*text.count(keyword.lower())/len(words)
        TF_IDF = ndw * IDF
        print "Text", text
        print "Words:", words
        print "TF_IDF", TF_IDF
        return Nw, IDF, ndw, TF_IDF

    def keywords(words):
        result = []
        for word in words:
            if not word: continue
            result.append(Word(word, *calculate_tf_idf(word)))
        return result

    Nw, IDF, ndw, TF_IDF = calculate_tf_idf(keyword)
    words = keywords(words)

    ctx = { 'title': 'TF-IDF',
            'keyword': keyword,
            'N': N,
            'Nw': Nw,
            'IDF': IDF,
            'ndw': ndw,
            'TF_IDF': TF_IDF,
            'words': words,
            'form': form,
    }
    if __name__ == '__main__':
        return match
    else:
        #return HttpResponse(str(match))
        return render_to_response('eva/tf_idf.html', ctx,
            context_instance=RequestContext(request))

if __name__ == '__main__':
    print tf_idf("request")