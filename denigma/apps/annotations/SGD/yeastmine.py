"""Retrieving annotation data from YeastMine."""
import os
import shelve

from django.conf import settings

from intermine.webservice import Service


def main():
    """Connects to yeastmine and creates a dictionary of annotation data.
    Data is saved into shelve as well as returned."""
    #print("annotations.SGD.yeastmine.main:")
    service = Service("http://yeastmine.yeastgenome.org/yeastmine")

    query = service.new_query()

    query.add_view(
        "SequenceFeature.primaryIdentifier", "SequenceFeature.featureType",
        "SequenceFeature.secondaryIdentifier", "SequenceFeature.description",
        "SequenceFeature.sgdAlias", "SequenceFeature.name", "SequenceFeature.symbol",
        "SequenceFeature.chromosome.name", "SequenceFeature.chromosome.featAttribute",
        "SequenceFeature.locations.start", "SequenceFeature.locations.end", "SequenceFeature.locations.strand"
        )
    query.add_constraint("SequenceFeature.organism.name", "=", "Saccharomyces cerevisiae", "A")
    query.add_constraint("SequenceFeature.featureType", "=", "ORF", "B")
    query.set_logic("(A and B)")

    annotation = {}
    #print("settins.PROJECT_ROOT: %s" % settings.PROJECT_ROOT)
    #print("os.path.join: %s" % os.path.join(os.path.join(settings.PROJECT_ROOT, 'apps', 'annotations', 'SGD', 'yeastmine')))
    db = shelve.open(os.path.join(settings.PROJECT_ROOT, 'apps', 'annotations', 'SGD', 'yeastmine'), 'c')
    for row in query.rows():
        data = {}
        for x in xrange(0, len(row.views)):
            attribute = row.views[x].split('.')[-1]
            value = row.data[x]['value']
            if attribute == 'name' and not value: continue
            data[attribute] = value
        if 'name' not in data: data['name'] = None
        annotation[data['secondaryIdentifier']] = data
        db[str(data['secondaryIdentifier'])] = data
    db.close()
    return annotation

def retrieve(orf):
    """Retrieves the annotation data for a single orf."""
    db = shelve.open(os.path.join(settings.PROJECT_ROOT, 'apps', 'annotations', 'SGD', 'yeastmine'), 'r')
    annotation = db[orf]
    db.close()
    return annotation

if __name__ == '__main__':
    annotation = main()
    printing = raw_input('Annotation completed, do you want to check them? (Yes or No): ')
    if printing.lower() == 'yes':
        for k,v  in annotation.items():
            print v['secondaryIdentifier'], v['symbol'], v['name']
