"""Model data transfer."""

def transfer(a, b, mapping=None):
    """transfers the attributes from one model to another one."""
    moduleA, modelA = a.split('.')
    moduleB, modelB = b.split('.')
    print "from %(moduleA)s.models import %(modelA)s as mA" % locals()
    print "from %(moduleB)s.models import %(modelB)s as mB" % locals()
    exec("from %(moduleA)s.models import %(modelA)s as mA" % locals())
    exec("from %(moduleB)s.models import %(modelB)s as mB" % locals())
    
    mAs = mA.objects.all()
    mBs = mB.objects.all()

    attrsA = mA.__doc__.split('(')[1].split(')')[0].split(', ')
    attrsB = mB.__doc__.split('(')[1].split(')')[0].split(', ')
        
    for a in mAs:
        b = mB()
        for attr in attrsA:
            if attr == 'id': continue

            if attr in attrsB:
                attribute = getattr(a, attr)

                setattr(b, attr, attribute)
            elif attr in mapping:
                attribute = getattr(a, attr)
                setattr(b, mapping[attr], attribute)

        b.save()

def main():
    a = "blogs.Blog"
    b = "blog.Post"
    return transfer(a,b, {'date':'created'})


if __name__ == '__main__':
    names = main()
