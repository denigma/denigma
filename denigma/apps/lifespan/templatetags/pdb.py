"""http://www.uniprot.org/faq/28#id_mapping_examples"""
import urllib, urllib2


def fetch_pdb(id):
    url = 'http://www.rcsb.org/pdb/files/%s.pdb' % id
    return urllib.urlopen(url).read()

def entrez_id_to_pdb(id):
    acc = mapit(id)
    pdb = mapit(acc, fr='ACC', to='PDB_ID')
    return pdb[:-1].replace('\n', '; ')

def mapit(ids='856399', fr='P_ENTREZGENEID', to='ACC'):
    url = 'http://www.uniprot.org/mapping/'

    params = {
        'from': fr,
        'to': to,
        'format': 'list',
        'query': ids
    }

    data = urllib.urlencode(params)
    request = urllib2.Request(url,data)
    contact = 'age@liv.ac.uk'
    request.add_header('User-Agent', 'Python %s' % contact)
    response = urllib2.urlopen(request)
    page = response.read(200000)
    return(page)

def mapping():
    from lifespan.models import Factor
    factors = Factor.objects.all()
    for factor in factors:
        if factor.entrez_gene_id:
            pdb = entrez_id_to_pdb(factor.entrez_gene_id)
            print("%s: %s" % (factor.symbol, pdb))
            factor.pdb = pdb.split(';')[0]
            if len(pdb) < 250:
                try: factor.save()
                except Exception as e: print e, pdb, factor.pdb

if __name__ == '__main__':
    print(entrez_id_to_pdb('856399'))
    #fetch_pdb()#
    #print(mapit())
    #print(type(mapit()))
    #print(mapit('P00447', fr='ACC', to='PDB_ID'))

