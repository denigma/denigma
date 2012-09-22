from django.shortcuts import render_to_response
from django.template import RequestContext

from blog.models import Post


def matrix(request, number):
    """Welcome in the matrix!"""
    try: 
       if int(number) == 0: 
          path = Post.objects.get(title="Paths of Truth")
    except:
       path = Post.objects.get(title__startswith="Path of Truth %s:" % number)
    return render_to_response('about/matrix.html', {'path': path, 'number': number},
                             context_instance=RequestContext(request))

def choice(request, number, color):
    """The choice of a path."""
    if color == "red": 
       path = "Truth"
    elif color == "blue":
       path = "Lie"
    print "Path of Truth %s %s" % (number, color)
    result = Post.objects.get(title="Path of Truth %s %s" % (number, color))

   # if request['user'].is_authenticated:
    #   user.profile.promote(aspect=number, level=0)

    return render_to_response('about/choice.html', {'number': number,
                                                    'color': color,
                                                    'result': result},
                              context_instance=RequestContext(request))
#234567891123456789212345678931234567894123456789512345678961234567897123456789
