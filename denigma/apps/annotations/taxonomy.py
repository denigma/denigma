"""Taxonomy module for species-related data. It responsibility is identifying and naming species
as well as arranging them into a classification.
Consider to include Zebrafish
"""
import os
import cPickle as pickle
import marshal

taxid_list = [4932, 6239, 7227, 10090, 9606]
taxids = [4896, 4932, 6239, 7227, 7955, 10090, 10116, 9544, 9606]


class Organisms(dict):
        
    def __init__(self, load=False, id='taxid', name='taxonomy', path=None):
        self.taxids = []
        if load == 'anage':
            self.load(name='anage.pkl', path='D:/Annotations/AnAge/')
        self.name = name
        if path:
            self.load(path=path)
        
    def addOn(self, taxid, attribute, value):
        #taxid = int(taxid)
        attribute = attribute.lower().replace(' ', '_').replace('-', '_').replace('/', '_').replace('(', '_').replace(')', '').replace('__', '_')
        if attribute in self.mapping: attribute = self.mapping[attribute]
        attr = eval('self['+taxid+'].'+attribute)

        if isinstance(attr, dict):
            if isinstance(value, dict):
                for k, v in value.items():
                    if k not in attr: exec('self.'+attribute+'["'+k+'"]=v')
            elif isinstance(value, list):
                for i in value:
                    if i not in attr: exec('self.'+attribute+'["'+i+'"]="'+i+'"') 
            elif isinstance(value, str):
                if value not in attr: exec('self.'+attribute+'["'+value+'"]="'+value+'"')
                
        elif isinstance(attr, list):
            if value not in attr: exec('self.'+attribute+'.append("'+value+'")')
        elif not attr:
            try:
                if '.' in value:
                    try: exec('self.'+attribute+'=float('+value+')')
                    except: exec('self.'+attribute+'="'+value+'"')
                else:
                    try: exec('self.'+attribute+'=int('+value+')')
                    except: exec('self.'+attribute+'="'+value+'"')
            except: print repr('self.'+attribute+'="'+value+'"')

        elif attr != value: print "Discripance: %s, %s, %s" % (attribute, attr, value)

    def add(self, attribute, value, id=None, type='taxid'):
        if id:
            try: id = int(id)
            except: pass
            if id not in self:
                self[id] = eval('Species('+type+'=id)')
            self[id].add(attribute, value)
        else: "No taxid defined"

    def adding(self, data, id='taxid'):
        key = None
        for k, v in data.items():
            if k == id:
                try: key = int(v)
                except: key = v
            if k == 'source':
                v = [str(v)]
            if k == 'reference':
                v = v.split(',')
        if key:
            for k, v in data.items(): self.add(k, v, id=key, type=id)
        else: print "No taxid defined"

    def find(self, term):
        res = {}
        term = term.lower()
        for taxid, species in self.items():
            for k, v in vars(species).items():
                if isinstance(v, dict) or isinstance(v, list):
                    for i in v:
                        if isinstance(i, str) and term in i.lower():
                            res[taxid] = species
                elif isinstance(v, str):
                    if term in v.lower():
                        res[taxid] = species
        return res

    def save(self, name='taxonomy.pkl', path='.'):
        if name.endswith('.pkl'): pickle.dump(self, open(os.path.join(path, name), 'wb'))
        elif name.endswith('.mrl'):
            data_file = open(os.path.join(path, name), 'wb', 5)
            D = {}
            for id, species in self.items():
                D[id] = {}
                for key, value in vars(species).items():
                    if value:
                        if isinstance(value, dict):
                            D[id][key] = value.keys() # zip(value.keys(), value.values())
                        else:
                            D[id][key] = value
            marshal.dump(D, data_file)
            data_file.close()
        
    def load(self, name='taxonomy.mrl', path='D:/Annotations/Taxonomy/'):
        if name.endswith('.pkl'):
            genes = pickle.load(open(os.path.join(path, name), 'rb'))
            self.update(genes)
        elif name.endswith('.mrl'):
            data_file = open(os.path.join(path, name), 'rb')
            D = marshal.load(data_file)
            data_file.close()
            for id, attribute in D.items():
                self[id] = Species(id=id)
                for key in attribute: setattr(self[id], str(key), attribute[key])
            
    def identify(self, attribute, value):
        res = {}
        value = value.lower()
        for taxid, species in self.items():
            attr = eval('species.'+attribute)
            #if isinstance(attr, str):
            if value in attr:
                res[taxid] = species
        return res
        
    def identity(self, other):
        res = {}
        for k, v in vars(other).items():
            if v:
                if isinstance(v, dict) or isinstance(v, list):
                    for i in v:
                        if i.lower() in self.alias:
                            if self.alias[i.lower()] not in res:
                                res[self.alias[i.lower()]] = 1
                            else:
                                res[self.alias[i.lower()]] += 1
                elif isinstance(v, str):
                    if v.lower() in self.alias:
                        if self.alias[v.lower()] not in res:
                            res[self.alias[v.lower()]] = 1
                        else:
                            res[self.alias[v.lower()]] += 1
        print res              
        result = dict((v,k) for k, v in res.iteritems())    # inverse mapping (assumes that values in dict are unique)  # http://stackoverflow.com/questions/483666/python-reverse-inverse-a-mapping
        key = result.keys()
        key.sort()

        return self[result[key[-1]]]
                                      
        #for taxid, species in self.items(): pass


    def __repr__(self):
        #L = []
        for taxid in self:
            #L.append(str(self[taxid]))
            print str(self[taxid])
            print
        #return '\n'.join(L)

    def __str__(self):
        return self.__repr__()
    

    def alias(self, all=False):
        """{name:[taxid]}"""
        self.alias = {}
        
        if all:
            L = len(self); n = 0; PB = 0
            for taxid, species in self.items():

                n += 1; PA = 100*n/L
                if PA != PB:
                    print PA
                    PB = PA
                
                for k, v in vars(species).items():
                    if v:
                        if isinstance(v, dict) or isinstance(v, list):
                            for i in v:
                                self.alias[i.lower()] = taxid
                        elif isinstance(v, str):
                            self.alias[v.lower()] = taxid
                            
        else:
            for taxid, species in self.items():
                self.alias[species.scientific_name.lower()] = taxid
                if species.genbank_common_name: self.alias[species.genbank_common_name.lower()] = taxid
                for common_name in species.common_names:
                    self.alias[common_name.lower()] = taxid

    def switchId(self, id):
        keys = self.keys()
        for key in keys:
            exec('self[self[key].'+id+'] = self[key]')
            exec('del self[key]')
            
##    def update(self):
##        for taxid in self: self.taxids

        
class Species():
    keys = {'synonyms':['synonym'],
            'authorities':['authorities'],
            'misspellings':['misspelling'],
            'in_parts':['in_part'],
            'authorities':['authority'],
            'common_names':['common_name'],
            'equivalent_names':['equivalent_name'],
            'anamorphs':['anamorph'],
            'misnomers':['misnomer'],
            'acronyms':['akronym', 'acronym'],
            'unpublished_names':['unpublished_name'],
            'classis':['class'],
            'mrdt':['mrdt_yrs'],
            'imr':['imr_per_yr'],
            'metabolic_rate':['metabolic_rate_w'],
            'gestation':['gestation_incubation_days'],
            'weaning_weight':['weaning_weight_g'],
            'adult_weight':['adult_weight_g'],
            'birth_weight':['birth_weight_g'],
            'body_mass':['body_mass_g'],
            'litters_size':['litter_clutch_size'],
            'litter_rate':['litters_clutches_per_year'],
            'inter_litters':['inter_litter_interbirth_interval'], # Inter-litter/Interbirth interval
            'female_maturity':['female_maturity_days'],
            'male_maturity':['male_maturity_days'],
            'maximum_longevity':['maximum_longevity_yrs'],
            'temperature':['temperature_k'],
            'growth_rate':['growth_rate_1_days'],
            'reference':['references'],
            'ordo':['order']}
    
    mapping = {}
    for key, values in keys.items():
        for value in values:
            mapping[value] = key

    #__slots__ = ['kingdom', 'taxid', 'name', 'latin_name', 'short_latin_name', 'organisms']
    def __init__(self, taxid=None, latin_name=None,common_names=None, name=None, shortcut=None, lineage=None,  short_name=None, 
                 genome_name=None, genome_build=None,scientific_name=None, includes=None, blast_name=None, equivalent_names=None,
                 synonyms=None, authorities=None, misspellings=None, in_parts=None, genbank_common_name=None, genbank_synonym=None, genbank_acronym=None, genbank_anamorph=None, anamorphs=None, misnomers=None, acronyms=None, teleomorph=None, unpublished_names=None,

                 superkingdom=None, kingdom=None, subkingdom=None,
                 superphylum=None, phylum=None, subphylum=None,
                 superclass=None, classis=None, subclass=None, infraclass=None,
                 superorder=None, ordo=None, suborder=None, infraorder=None,  parvorder=None,
                 superfamily=None, family=None, subfamily=None,
                 genus=None, subgenus=None,
                 species=None, subspecies=None, species_group=None, species_subgroup=None,
                 forma=None, tribe=None, subtribe=None,varietas=None, no_rank=None, 

                 female_maturity=None, male_maturity=None, gestation=None, weaning_weight=None, weaning_days=None, litters_size=None, litter_rate=None, inter_litters=None,
                 birth_weight=None, adult_weight=None, growth_rate=None, maximum_longevity=None, source=None, specimen_origin=None, sample_size=None, data_quality=None, imr=None, mrdt=None,
                 metabolic_rate=None, body_mass=None, temperature=None, reference=None,
                 add=False, id='taxid'):


        #if isinstance(add, dict) and taxid in add:
            

        try: self.taxid = int(taxid)
        except: self.taxid = taxid
        self.latin_name = latin_name
        if latin_name: self.short_latin_name = latin_name.split()[0][:1]+'. '+latin_name.split()[1] #self.short_latin_name = self.latin_name.split(' ')[0][1:]+'.'+self.latin_name.split(' ')[1]
        else: self.short_name = short_name
        if common_names: self.common_names = common_names
        else: self.common_names = []
        self.name = name
        self.genome_name = genome_name
        self.genome_build = genome_build
        self.organisms = []
        self.shortcut = shortcut
        self.lineage = lineage
        if synonyms: self.synonyms = synonyms
        else: self.synonyms = []
        self.scientific_name = scientific_name
        if includes: self.includes = includes
        else: self.includes = []
        self.blast_name = blast_name
        if in_parts: self.in_parts = in_parts
        else: self.in_parts = []
        if equivalent_names: self.equivalent_names = equivalent_names
        else: self.equivalent_names = []
        if authorities: self.authorities = authorities
        else: self.authorities = []
        if misspellings: self.misspellings = misspellings
        else: self.misspellings = []
        self.genbank_common_name = genbank_common_name
        self.genbank_acronym = genbank_acronym
        self.genbank_synonym = genbank_synonym
        self.genbank_anamorph = genbank_anamorph
        if anamorphs: self.anamorphs = anamorphs
        else: self.anamorphs = []
        if misnomers: self.misnomers = misnomers
        else: self.misnomers = []
        if acronyms: self.acronyms = acronyms
        else: self.acronyms = []
        self.teleomorph = teleomorph
        if unpublished_names: self.unpublished_names = unpublished_name
        else: self.unpublished_names = []

##        if superkingdom: self.superkingdom = superkingdom
##        else: superkingdom = {}
##        if kingdom: self.kingdom = kingdom
##        else: self.kingdom = {}
##        if subkingdom: self.subkingdom = subkingdom
##        else: self.subkingdom = {}
##        if superphylum: self.superphylum = superphylum
##        else: self.superphylum = {}
##        if phylum: self.phylum = phylum
##        else: self.phylum = {}
##        if subphylum: self.subphylum = subphylum
##        else: self.subphylum = {}
##        if superclass: self.superclass = superclass
##        else: self.superclass = {}
##        if self.classis = classis
##        else: self.classis = {}
##        if subclass: self.subclass = subclass
##        else: self.subclass = {}
##        if infraclass: self.infraclass = infraclass
##        else: self.infraclass = {}
##        if superorder: self.superorder = superorder
##        else: self.superorder = {}
##        if order: self.order = order
##        else: self.order = {}
##        if self.suborder = suborder
##        else: self.suborder = {}
##        if self.infraorder = infraorder
##        else: self.infraorder = {}
##        if parvorder: elf.parvorder = parvorder
##        else: self.parvorder = {}
##        if superfamily: self.superfamily = superfamily
##        else: self.superfamily = {}
##        if family: self.family = family
##        else: self.family = {}
##        if subfamily: self.subfamily = subfamily
##        else: self.subfamily = {}
##        if genus: self.genus = genus
##        else: self.genus = {}
##        if subgenus: self.subgenus = subgenus
##        else: self.subgenus = {}
##        if self.species = species
##        else: self.species = {}
##        if subspecies: self.subspecies = subspecies
##        else: subspecies = {}
##        if species_group: self.species_group = species_group
##        else: self.species_group = {}
##        if species_sub_group: self.species_subgroup = species_subgroup
##        else: self.species_sub_group = {}
##        if forma: self.forma = forma
##        else: self.forma = {}
##        if tribe: self.tribe = tribe
##        else: self.stribe = {}
##        if subtribe: self.subtribe = subtribe
##        else: self.subtribe = {}
##        if self.varietas = varietas
##        else: self.varietas = {}
##        if no_rank: self.no_rank = no_rank
##        else: self.no_rank = {}

##        self.superkingdom = superkingdom
##        self.kingdom = kingdom
##        self.subkingdom = subkingdom
##        self.superphylum = superphylum
##        self.phylum = phylum
##        self.subphylum = subphylum
##        self.superclass = superclass
##        self.classis = classis
##        self.subclass = subclass
##        self.infraclass = infraclass
##        self.superorder = superorder
##        self.order = order
##        self.suborder = suborder
##        self.infraorder = infraorder
##        self.parvorder = parvorder
##        self.superfamily = superfamily
##        self.family = family
##        self.subfamily = subfamily
##        self.genus = genus
##        self.subgenus = subgenus
##        self.species = species
##        self.subspecies = subspecies
##        self.species_group = species_group
##        self.species_subgroup = species_subgroup,
##        self.forma = forma
##        self.tribe = tribe
##        self.subtribe = subtribe
##        self.varietas = varietas
##        self.no_rank = no_rank

        self.superkingdom = {}
        self.kingdom = {}
        self.subkingdom = {}
        self.superphylum = {}
        self.phylum = {}
        self.subphylum = {}
        self.superclass = {}
        self.classis = {}
        self.subclass = {}
        self.infraclass = {}
        self.superorder = {}
        self.ordo = {}
        self.suborder = {}
        self.infraorder = {}
        self.parvorder = {}
        self.superfamily = {}
        self.family = {}
        self.subfamily = {}
        self.genus = {}
        self.subgenus = {}
        self.species = {}
        self.subspecies = {}
        self.species_group = {}
        self.species_subgroup = {}
        self.forma = {}
        self.tribe = {}
        self.subtribe = {}
        self.varietas = {}
        self.no_rank = {}
        
        self.female_maturity = female_maturity
        self.male_maturity = male_maturity
        self.gestation = gestation
        self.weaning_weight = weaning_weight
        self.weaning_days = weaning_days
        self.litters_size = litters_size
        self.litter_rate = litter_rate
        self.inter_litters = inter_litters
        self.birth_weight = birth_weight
        self.adult_weight = adult_weight
        self.growth_rate = growth_rate
        try: self.maximum_longevity = float(maximum_longevity)
        except: self.maximum_longevity = maximum_longevity
        if source: self.source = [source]#int(source)
        else: self.source = []
        self.specimen_origin = specimen_origin
        self.sample_size = sample_size
        self.data_quality = data_quality
        self.imr = imr
        self.mrdt = mrdt
        self.metabolic_rate = metabolic_rate
        self.body_mass = body_mass
        self.temperature = temperature
        if reference: self.reference = reference
        else: self.reference = []
        
        if isinstance(add, dict):
            id = eval('self.'+id)
            if id not in add: add[id] = self
            else: pass #print "%s already in %s" % (taxid, add)
            
##    def __setitem__(self, species):
##        self.taxids.append(species.taxid)

    def add(self, attribute, value):
        #taxid = int(taxid)
        attribute = attribute.lower().replace(' ', '_').replace('-', '_').replace('/', '_').replace('(', '_').replace(')', '').replace('__', '_').replace('\n', '')
        if isinstance(value, str):
            value = value.replace('"', '').replace('\n', '')
        if attribute in self.mapping: attribute = self.mapping[attribute]
        attr = eval('self.'+attribute)

        if isinstance(attr, dict):
            if isinstance(value, dict):
                for k, v in value.items():
                    if k not in attr: exec('self.'+attribute+'["'+k+'"]=v')
            elif isinstance(value, list):
                for i in value:
                    if i not in attr: exec('self.'+attribute+'["'+i+'"]="'+i+'"') 
            elif isinstance(value, str):
                if value not in attr: exec('self.'+attribute+'["'+value+'"]="'+value+'"')              

        elif isinstance(attr, list):
            if value not in attr: exec('self.'+attribute+'.append("'+value+'")')
        elif not attr:
            try:
                if '.' in value:
                    try: exec('self.'+attribute+'=float('+value+')')
                    except: exec('self.'+attribute+'="'+value+'"')
                else:
                    try: exec('self.'+attribute+'=int('+value+')')
                    except: exec('self.'+attribute+'="'+value+'"')
            except: print repr('self.'+attribute+'="'+value+'"')
            
        elif attr != value: print "Discripance: %s, %s, %s" % (attribute, attr, value)


    def __repr__(self):
        L = []
        for k, v in vars(self).items():
            if v: L.append('%s = %s' % (k, v))           #, (%s) type(v)))
        return '\n'.join(L)     #self.taxid #str(self.__dict__) #self.taxid, self.name, self.latin_name, self.short_latin

    def __str__(self):
        return self.__repr__()

#Current organisms under investigation

#self, taxid=None, latin_name=None,common_names=None, name=None, shortcut=None, lineage=None,  short_name=None, 
species, organisms = [  (4932, 'Saccharomyces cerevisiae', 'Budding yeast', 'Yeast', 'YEAST'),
                        (559292, 'Saccharomyces cerevisiae', 'Budding yeast', 'Yeast', 'YEAST'),
                        (4896, 'Saccharomyces pombe', 'Fission yeast', 'Yeast', '?'),                        
                        (6239, 'Caenorhabditis elegans', 'Nematode', 'Worm', 'CAEEL'),
                        (7227, 'Drosophila melanogaster', 'Fruit fly', 'Fly', 'DROME'),
                        (10090, 'Mus musculus', 'House mouse', 'Mouse', 'MOUSE'),
                        (7955, 'Danio rerio', 'Zebrafish', 'Fish', 'DANR'),
                        (10116, 'Rattus norvegicus', 'Norway rat', 'Rat', 'RAT'),
                        (9544, 'Macaca mulatta', 'Rhesus monkey', 'Monkey', 'MONKEY'),
                        (9606, 'Homo sapiens', 'Human', 'Human', 'HUMAN')], {}

species_translation = {4932:4932,559292:4932,4896:4896,6239:6239,7227:7227,7955:7955, 10090:10090,10116:10116,9544:9544,9606:9606}   # This mapping corrects the budding yeast discripancy.

organisms = Organisms() #Creates organisms instances
for s in species: organisms[s[0]] = Species(s[0], s[1], s[2], s[3], s[4])

#lifeforms = LifeForms()
#for s in species: lifeforms[s[0]] = Species(s[0], s[1], s[2], s[3], s[4])

if __name__ == "__main__":
    for taxid, species in organisms.items(): print species.__dict__
    species = Species()
