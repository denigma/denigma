from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required


from data import get


def index(request, template='about/index.html'):
    entry = get("Denigma")
    return render(request, template, {'entry': entry})

def what_next(request, template='about/what_next.html'):
    """Presents what's next to do after registration."""
    entry = get("What's Next")
    return render(request, template, {'entry': entry})

@login_required
def matrix(request, number, template='about/matrix.html'):
    """Welcome in the matrix!"""
    try: 
       if int(number) == 0: 
          path = get("Paths of Truth")
    except:
       path = get(title__startswith="Path of Truth %s:" % number)
    return render(request, template, {'path': path, 'number': number})

def choice(request, number, color, template='about/choice.html'):
    """The choice of a path."""
    if color == "red": 
       path = "Truth"
    elif color == "blue":
       path = "Lie"
    print "Path of Truth %s %s" % (number, color)
    result = get("Path of Truth %s %s" % (number, color))

    ASPECTS = {'I':'rank', 'II':'grade', 'III':'title', 'IV':'role'}
    aspect = ASPECTS[number]

    if request.user.is_authenticated:
        promoted = request.user.profile_set.all()[0].promote(aspect=aspect,
                                                                        level=1)
        if promoted:
            messages.add_message(request,
                messages.SUCCESS, ugettext("You got promoted!"))
        else:
            messages.add_message(request,
                messages.WARNING, ugettext("You were not further promoted."))

    ctx = {'number': number,
           'color': color,
           'result': result,
           'promoted': promoted}
    return render(request, template, ctx)



#234567891123456789212345678931234567894123456789512345678961234567897123456789
