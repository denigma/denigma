"""Gene Ontology Terms"""
import os
import cPickle as pickle
#from biosystem import *


def xstr(s):
    if s is '-': return None
    else: return s
    

class GOs(dict):
    """Gene Ontologies"""
    def __init__(self, name=None):
        super(GOs, self).__init__()
        self.name = name or 'GO'
        if name and name != 'GO':
            self.load()

    def __repr__(self):
        ontologies = [] # '%s:\n' % (self.name)
        for id in self:
            #if go and id: print id, go
            ontologies.append(self[id].__repr__())
            #yield self[id].__repr__()
        return "\n".join(ontologies)
    
    def add(self, data):
        if isinstance(data, dict):
            go = GO() # gos=self)
            for attribute, value in data.items():
                if attribute == 'id' and isinstance(value, str) and "GO:" in value:
                    #value = value.split('GO:')[1])
                    value = int(value.split('GO:')[1])

                elif attribute == 'replaced_by':
                    value = value.split('GO:')[1]
                elif value == 'true':
                    value = True
                elif value == 'false':
                    value = False
                
                setattr(go, attribute, value)
            if go.id not in self:
                self[go.id] = go
                

    def list(self):
        for go in self.values():
            print('\n'+str(go))

    def save(self, path='D:\\Annotations\\GO', name='go.pkl'):
        pickle.dump(self, open(os.path.join(path, name), 'wb'))

    def load(self, path='D:\\Annotations\\GO', name='go.pkl'):
        gos = pickle.load(open(os.path.join(path, name), 'rb'))
        for go in gos.values():
            if go.id in self:
                self[go.id].__dict__.update(go.__dict__)
            else: self[go.id] = go

    def retrieve(self, term):
        """Retrieves all terms which contain the inout word."""
        results = []
        for k, v in self.items():
            if v.name and term in v.name:
                results.append(v)
        return results

    def findGenes(self, term, taxid):
        """Prints all genes belonging to a certain term."""
        if "genes" not in globals():
            from bioentities import genes
            genes.load() 
        res = self.retrieve(term)
        for i in res:
            print i.name
            for gene in i.genes:
                    if genes[gene].taxid == 9606:
                            print " ", genes[gene].symbol, genes[gene].name, genes[gene].description


class GO():
    """Gene Ontology"""
    keys = {'definition': ['def'],
            'category': ['namespace'],
            'name':['term']}
    mapping = {}
    for k, v in keys.items():
        for i in v:
            mapping[i] = k
    categories = {'P':'molecular process', 'F':'molecular function', 'C': 'cellular component'}
    def __init__(self, id=None, name=None, category=None, evidence=None, description=None, source=None, pmid=None, genes=None,
                 synonyms=None, exact_synonyms=None, related_synonyms=None, is_a=None, part_of=None, positively_regulates=None,
                 gos=False):
        if isinstance(id, str) and "GO:" in id:
            id = int(value.split('GO:')[1])
        self.id = id                    # GO-ID
        self.name = name
        if category in GO.categories:
            category = GO.categories[category]
        self.category = category        # P=Process; F=Function; C=Component (a.k.a. namespace)
        self.description = description
        self.source = source or []
        self.pmid = pmid or []
        self.synonyms = synonyms or []
        self.exact_synonyms = exact_synonyms or []
        self.related_synonyms = related_synonyms or []
        self.is_a = is_a or []
        self.part_of = part_of or []
        self.positively_regulates = positively_regulates or []
        self.genes = genes or []              #{taxid:[] for taxid in Taxids}

        if gos != False:
            gos[id] = self
        
    def __repr__(self):
        attributes = []
        for k, v in self.__dict__.items():
            if v: attributes.append(str(k)+' = '+str(v))   #print v, #'%s: %s' % (k,)
        return "\n".join(attributes)

    def add(self):
        pass


class Terms(GOs):
    pass


class Term(GO):
    pass


gos = GOs()


