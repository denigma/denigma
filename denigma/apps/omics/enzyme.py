"""Integrating enzyme data: http://steveasleep.com/"""
try:
    from collections import OrderedDict
    Dict = OrderedDict
except ImportError:
    Dict = dict

    
class Enzyme():
    keys = dict(id=['ID'],
                description=['DE'],
                names=['AN'],
                activities=['CA'],
                cofactors=['CF'],
                comments=['CC'],
                prosites=['PR'],
                swiss_prots=['DR'])
    mapping = {}
    for k, v in keys.items():
        for i in v:
            mapping[i] = k
    def __init__(self, id=None, substrates=None, products=None,
                 ec_numbers=None, description=None, names=None,
                 activities=None, cofactors=None, prosites=None,
                 swiss_prots=None, comments=None, *args, **kwargs):
        self.id = id                        # Identification (ID).
        self.substrates = substrates or []
        self.products = products or []
        self.ec_numbers = ec_numbers or []
        self.description = description or []# Official name (DE). Contains the NC_IUB recommanded name for an enzyme.
        # = self.name = name
        self.names = names or []            # alternate name(s) (AN).Other than the NC-IUBMB recommanded name, that are used in the literature to describe an enzyme.
        self.activities = activities or []  # Catalytic activity (CF) indicates the reaction(s) catalysed by an enzyme. The majority of reactions are described using a standard chemical reaction format.
        self.cofactors = cofactors or []    # (CF).
        self.prosites = prosites or []      # Cross-reference to PROSITE (PR). PROSITE document entry accession number.
        self.swiss_prots = swiss_prots or []# Cross-reference to Swiss-Prot (DR). Database references are sued as pointers to the UniProtKB/Swiss-Prot entries that corresponds to the enzyme being described.
        self.comments = comments or []      # (CC). Free text comments on the entry, and may be used to convey any useful information.

    def __repr__(self):
        L = []
        for k,v in vars(self).items():
            if v:
                L.append('{0} = {1}'.format(k,v))
        return "\n".join(L)


class Enzymes(Dict):
    def __repr__(self):
        L = []
        for i in self:
            L.append(str(self[i])+'\n')
        return "\n".join(L)
#234567891123456789212345678931234567894123456789512345678961234567897123456789                
