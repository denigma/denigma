"""Genomics classes."""
import os
import copy
import time
import shelve
import marshal
import cPickle as pickle

try:
    from eva import msg
except:
    def msg(message): print message

from taxonomy import organisms, species_translation
from utils import evalu, roman_to_int

if os.name == 'posix':
    try:
        from django.conf import settings
        base = os.path.join(settings.PROJECT_ROOT, 'apps')
    except:
        base = '/media/SDATA1/'
else:
    base = 'D:/'


class Genes(dict):
    '''This represents a Wrapper for all gene-related information.
    It can store and retrieve gene information from different database types
    Usage:
    1. for id, gene in genes.mapped.items(): print id, gene
    2. for id, gene in genes.discontinued.items(): print id, gene'''
    #__slots__ = ['discontinued', 'mapped', 'ignored', 'table_schema']
    def __init__(self, name='genes'):
        self.key = "id"         # The unique primary key used for the directory#
        self.name = name
        self.discontinued = {}  # Contains a dictionary of discontinued genes with if any new continued id.
        self.mapped = {}        # Contains gene objects successfully mapped and integrated.
        self.ignored = []
        self.table_schema = [
        '''Discontinued(models.Model):
        entrez_gene_id
        discontinued_id
        symbol
        Entrez_Ensembl ManyToMany table
        ''']
        self.taxid = None
        self.taxids = {}

        if self.name == 'genes': pass
        elif self.name == 'Entrez':
            self.load()
        elif self.name == 'WormBase':
            self.load(path=base+'/annotations/WormBase/', name='wormbase.mrl')
        else:
            self.load(path=base+'annotations/'+self.name, name=self.name.lower()+'.mrl')

        self.building = self.mapping # Depricated! Use mapping directly!

    def add(self, D, key='id'):
        id = None
        List = []
        taxid = False
        for attribute, value in D.items():
            if not value or value == "null": continue # Ignore attributes without values.
            attribute = attribute.lower().replace(' ', '_')
            if "(" in attribute: attribute = attribute.split('(')[0] #omit bracket information.
            if attribute in Gene.mapping: attribute = Gene.mapping[attribute]
            #print "%s: %s" % (attribute, value)
            if attribute == key:
                try: id = value = int(value)
                except: id = value
            elif attribute == 'taxid' and int(value) in species_translation:
                taxid = species_translation[int(value)]
                value = taxid
            elif attribute == 'chromosome': value = roman_to_int(value)
            List.append((attribute, value))
        if taxid or id in self:                                                   #int(Dict['taxid']) in Taxids:     #and Dict['symbol'] != 'NEWENTRY':
            #if int(taxid) == 559292: taxid = 4932
            #print id
            if id not in self: self[id] = eval('Gene('+key+'=id)')
            #List.append(('taxid', taxid))
            for attribute, value in List:
                if attribute in Gene.keys and value:
                    if attribute == 'dbxrefs': 
                        values = value.split('|')
                        for value in values:
                            s = value.split(':')
                            if len(s) == 2:
                                attribute, value = s[0].lower(), s[1]
                                self[id].add(value, attribute)
                    elif '|' in attribute: # It is string containing a | seperated list.
                        values = value.split('|')
                        for value in values:
                            self[id].add(v, attribute)
                    elif isinstance(value, list): 
                        for v in value: self[id].add(v, attribute)
                    else: self[id].add(value, attribute)
                    
                else:   # Called the ignored attributes.
                    if attribute not in self.ignored: self.ignored.append(attribute)

    def addData(self, data, key=None, taxid=None):
        """Add genes in a batch.
        Optional pass in a taxid for all genes."""
        if not key: key = self.key
        if self.taxid: taxid = self.taxid
        if taxid:
            for i in data:
                i['taxid'] = taxid
                self.add(i, key=key)
        else:
            for i in data:
                self.add(i, key=key)


    def include(self, **arg):
        pass 
        
    def update_names(self):
        for id, gene in self.items(): gene.update()

    def update_ratios(self):
        for id, gene in self.items(): gene.update_ratio()
            
    def mapping(self, key, value, save=False):
        """Builds a mapping between a key to a value."""
        if not save:
            mapping = {}
            def comp(x): return x
        else:
            self.folder = os.path.join(base,'annotations', self.name)
            print os.path.join(self.folder, key.capitalize()+'To'+value.capitalize())
            mapping = shelve.open(os.path.join(self.folder, key.capitalize()+'To'+value.capitalize()), 'c')
            def comp(x): return str(x) # Integer values are not allowed as indices for shelves.
        for id, gene in self.items():
            From = eval('gene.'+key)
            To = eval('gene.'+value)
            if From and To:
                if type(From) != list:
                    mapping[comp(From)] = To
                elif type(From) == list and type(To) != list:
                    for i in From:
                        mapping[comp(i)] = To
                elif type(From) == list and type(To) == list:
                    for iF in From:
                        for iT in To:
                            mapping[comp(iF)] = iT
        if save: mapping.close()
        else: return mapping

    def buildMappings(self):
        """Trickers the creation of the AliasToId and IdToAlias
        as well as IdToEntrez and EntrezToId mappings.
        Depriciated!"""
        self.alias() # Exchanged aliases by alias
        self.folder = os.path.join(base, 'annotations', self.name)

        self.mapping(self.key, 'id', save=True)
        self.mapping('id', self.key, save=True)
        
        # Ectopic approach with customized file names:
##        idToEntrez = shelve.open(os.path.join(self.folder, 'KeyToEntrez'), 'c')
##        idToEntrez.update(self.mapping(self.key, 'id', save=True))
##        idToEntrez.close()
##        entrezToId = shelve.open(os.path.join(self.folder, 'EntrezToKey'), 'c')
##        entrezToId.update(self.mapping('id', self.key, save=True))
##        entrezToId.close()

    def save(self, path='.', name=None, direct=False):
        """Serializes the entites in diverse formats.""
        pickle = '.pkl'
        text = '.txt'
        marshal = '.mrl'
        relational = .sql
        shelve = .shl"""
        if not name and self.name:
            path = os.path.join(base, 'annotations', self.name)
            name = self.name.lower()+'.mrl'
        start = time.time()
        if name[-4:] == '.pkl':
            pickle.dump(self, open(os.path.join(path, name), 'wb'))   # pickle

        elif name[-4:] == '.mrl' and not direct:
            data_file = open(os.path.join(path, name), 'wb', 5)
            D = {}
            for id, gene in self.items():
                D[id] = {}
                for key, value in gene.__dict__.items():
                    if value: D[id][key] = value
            marshal.dump(D, data_file)
            data_file.close()

            # Meta data:
            meta = {'name':self.name, 'key':self.key}
            data = open(os.path.join(path, 'meta.mrl'), 'wb', 5)
            marshal.dump(meta, data)
            data.close()
            
            if self.discontinued:
                data_file = open(os.path.join(path, 'discontinued.mrl'), 'wb', 5)
                marshal.dump(self.discontinued, data_file)
                data_file.close()

        elif name[-4:] == '.mrl' and direct:
            data_file = open(os.path.join(path, name), 'wb', 5)
            marshal.dump(self, data_file)
            data_file.close()
            
        elif name[-4:] == '.sql':        #elif name.endswith('.sql'):
            import MySQLdb
            db = MySQLdb.connect('localhost', 'root', '', 'd')             # Connect to SQL database
            cur = db.cursor()
            cur.execute('''DROP TABLE IF EXISTS %s''' % name[:-4])
            cur.execute('''CREATE TABLE %s (id int NOT NULL primary key,
                                      symbol varchar(255) NOT NULL,
                                      name varchar(255) NOT NULL,
                                      description text,
                                      taxid int NOT NULL)''' % name[:-4])     

            for id, gene in self.items():

                sql = '''INSERT INTO %s (id, symbol, name, description, taxid) ''' % name[:-4]
                sql += '''VALUES ("%(id)s", "%(symbol)s", "%(name)s", "%(description)s", "%(taxid)s")''' % gene.__dict__
                cur.execute(sql)
                
                #for key, value in gene:

            # Determine the schema ( fields, types, length)
                #ids
                #attributes = database fields
                    #Boolean-, Float-, Integer-, Char-, Text-, OneToMany-, ManyToMany-Fields, maxlength?
            #Attributes = []
##            if eval('self.'+attribute) and eval('self.'+attribute) != list #ManyToMany
##            attributes = self.__dict__
##            for attribute in attributes:
##                if eval('self.'+attribute) != list #ManyToMany
##                    Attributes.append((attribute,type(eval('self.'+attribute))))

        elif nam[-4:] == '.shl':
            pass


        msg("Saved data on %s genes to %s in %s seconds" % (len(self), name, round(time.time() - start, 0)))
        
        #end = time.time()
        #difference = end - start
       # print difference, 'seconds'
        
                #gene.save(name=name)
        #shelve
        #sql
##        for gene in self:
##            gene.save()

    

    def load(self, path=base+'annotations/Entrez/', name='entrez.mrl', direct=False):
        """Loads data on genes."""
        start = time.time()
        key = self.key
        if not os.path.split(path)[0]:
            self.name = path; path = base+'annotations/%s/' % path; name = self.name+'.mrl'
        if name == 'entrez.mrl': self.name = "Entrez" # Entrez is the default annotation.
        print(os.path.join(path, name))
        if name[-4:] == '.pkl':
            genes = pickle.load(open(os.path.join(path, name), 'rb'))
            print type(genes)
            if 'discontinued' in vars(genes): self.discontinued = genes.discontinued
            self.update(genes)
            #print "Loaded %s genes" % len(genes)

        elif name[-4:] == '.mrl' and not direct:
            data_file = open(os.path.join(path, name), 'rb')
            D = marshal.load(data_file)
            data_file.close()
            
            for id, attribute in D.items():
                self[id] = eval('Gene('+key+'=id)') # Exchanged here id by key.
                for k in attribute: setattr(self[id], str(k), attribute[k])

            try:
                # Meta data:
                meta = open(os.path.join(path, 'meta.mrl'), 'rb')
                data = marshal.load(meta)
                self.key = data['key'] 
                meta.close()
            except: print("Couldn't load meta data.")

            try:
                data_file = open(os.path.join(path, 'discontinued.mrl'), 'rb')
                self.discontinued = marshal.load(data_file)
                data_file.close()
            except: print "Did not load discontinued gene ids."

        elif name[-4:] == '.mrl' and direct:
            data_file = open(os.path.join(path, name), 'rb')
            genes = marshal.load(data_file)
            data_file.close()
            self.update(genes)
            
        msg("Loaded %s genes from %s in %s seconds" % (len(self), name, round(time.time() - start, 0)))

        #end = time.time()
        #difference = end - start
        #print difference, 'seconds'

    def shelveIt(self, path=os.path.join(base, 'annotations', 'Entrez'), name='entrez.shl'):
        """Connects to a shelve."""
        import shelve
        output = shelve.open(os.path.join(path, name))
        output.update(self)
        output.close()

    def deshelve(self, path=os.path.join(base, 'annotations', 'Entrez'), name='entrez.shl'):
        import shelve
        input = shelve.open(os.path.join(path, name))
        self.update(input)

    def aliasList(self, folder=None):
        """Creates a `id to alias` and a `alias to id file list.""" 
        if self.name == 'WormBase':
            folder = os.path.join(base, 'annotations', 'WormBase')
        elif self.name == 'Entrez':
            folder = os.path.join(base, 'annotations', 'Entrez')
        else:
            folder = os.path.join(base, 'annotations', self.name)
        IdToAlias = shelve.open(os.path.join(folder, 'IdToAlias'), 'c')
        PreAliasToId = {}
        for taxid in organisms: PreAliasToId[str(taxid)] = {}
        for id, gene in self.items():
            alias = gene.alsoKnownAs() # aliasSynonym() Depricated!
            IdToAlias[str(id)] = alias
            #if str(gene.taxid) not in ReMap: ReMap[str(gene.taxid)] = {}
            if id:
                for synonym in alias:
                    if isinstance(synonym, str):
                        synonym = synonym.lower()
                        if synonym not in PreAliasToId[str(gene.taxid)]:
                            PreAliasToId[str(gene.taxid)][synonym] = [id]
                        else:
                            PreAliasToId[str(gene.taxid)][synonym].append(id)
        IdToAlias.close()
        AliasToId = shelve.open(os.path.join(folder+'AliasToId'), 'c')
        AliasToId.update(PreAliasToId)
        AliasToId.close()

    def alias(self, folder=None):
        """Creates `id to alias` and `alias to id` list as well as species-specific `alias to id` lists
        for each species defined in taxonomy."""
        if not folder:
            folder = os.path.join(base, 'annotations', self.name)
        try: idToAlias = shelve.open(os.path.join(folder,'IdToAlias'))
        except: print os.path.join(folder, 'IdToAlias')
        for taxid in organisms:
            taxid = str(taxid) # necessary?
            exec("aliasToId_"+taxid+" = shelve.open(os.path.join('"+folder+"', 'AliasToId_"+taxid+"'))")
        aliasToId = shelve.open(os.path.join(folder,'AliasToId'))
        for id, gene in self.items():
            alias = gene.alsoKnownAs()
            idToAlias[str(id)] = alias
            aliasToIdTaxid = eval("aliasToId_%s" % gene.taxid)
            for synonym in alias:
                if not isinstance(synonym, str):
                    synonym = str(synonym)
                synonym = synonym.lower()
                if synonym not in aliasToIdTaxid:
                     aliasToIdTaxid[synonym] = [id]
                else:
                    aliasToIdTaxid[synonym].append(id)
                if synonym not in aliasToId:
                    aliasToId[synonym] = [id]
                else:
                    aliasToId[synonym].append(id)

        idToAlias.close()
        aliasToId.close()
        for taxid in organisms:
            exec('aliasToId_%s.close' % taxid)

    
    def categories(self):
        catgories = {}
        for id, gene in self.items(): categories[gene.category] = None
        return categories.keys()

    def filterCategory(self, category='protein_coding', taxid=None):
        res = []
        for id, gene in self.items():
            if gene.category == category:
                if taxid:
                    if gene.taxid == int(taxid): res.append(id)
                else: res.append(id)
        return res
    
    def switchId(self, id='ensembl_gene'):
        "Switch the primary id fo the genes to another identifier"
        D = {}
        for identifier, gene in self.items():
            try: exec('D[gene.'+id+'] = gene')
            except:
                ids = eval('gene.'+id)
                for i in ids: D[i] = gene
        self.clear()
        self.update(D)
        #for id in self: print id
        self.primary_identifier = id

    def identify(self, aliases, taxid=None):
        """Given any alias it will mapped to an id"""
        if self.name == 'WormBase':
            folder = os.path.join(base, 'annotations', 'WormBase')
        elif self.name == 'Entrez':
            folder = os.path.join(base, 'annotations', 'Entrez')
        else:
            folder = 'D:/Annotations/%s/' % self.name
        if taxid:
            AliasToId = shelve.open(os.path.join(folder+'AliasToId_%s' % taxid), 'c')
        else:
            AliasToId = shelve.open(os.path.join(folder+'AliasToId'), 'c')
        def find(self, alias, taxid, AliasToId):
            if isinstance(alias, str):
                alias = alias.lower()
                if alias in AliasToId: return AliasToId[alias]
                else: pass# print "Could not map %s to id!" % alias
            else:
                ids = [] 
                for taxid, aliases in AliasToId.items():
                    if alias in aliases:
                        ids.append(aliases[alias])
                return ids

        if type(aliases) == list or type(aliases) == dict:
            res = {}
            for alias in aliases: res[alias] = find(self, alias, taxid, AliasToId)
            return res
        else: return find(self, aliases, taxid, AliasToId)

        AliasToId.close()

    def get(self, aliases, taxid=None):
        """Given any alias the genes matching them will be returned."""
        res = identify(self, aliases, taxid=None)
        genes = Genes()
        for alias, id in res.items(): genes[id] = self.genes[id]
        return genes
                
    def aliases(self, id):
        """Given any id it will mapped to an its alias and synonyms"""
        if id in self: return self[id].aliasSynonym()
        #folder = 'D:/Annotations/Entrez/'
        #IdToAlias = shelve.open(os.path.join(folder+'IdToAlias'), 'c')
        #id = str(id)
        #if id in IdToAlias: return IdToAlias[id]
        else: print("Could not map id to alias!")

    def count(self):
        for id, gene in self.items():
            if gene.taxid not in self.taxids: self.taxids[gene.taxid] = [id]
            else: self.taxids[gene.taxid].append(id)
        for taxid, genes in self.taxids.items(): print taxid, len(genes)

    def tell(self, gene, taxid):
        """Takes a gene symbol, name or identifier and
        returns the corresponding gene object if exists."""
        id = genes.identify(gene, taxid)
        return genes[id]

    def search(self, term):
        """Searches for a term in all attributes for each gene and retrieves the genes as a dictionary."""
        res = {}
        for id, gene in self.items():
            for attr, value in vars(gene).items():
                if value:
                    if term == value: res[id] = gene
                    elif isinstance(value, str) and term in value: res[id] = gene
                    elif isinstance(value, list):
                        for item in value:
                            if term == item: res[id] = gene
                            elif term in item: res[id] = gene
        return res                               

    def go(self, gene, category, term, data=None):
        """Takes a gene id, a category as well as term and adds it to the respective go list."""
        #categories = {'P':'go_process', 'F':'go_function', 'C':'go_component'}
        category = category.lower()
        if category in Gene.mapping: category = Gene.mapping[category]
        terms = eval('self[gene].'+category)
        if term not in terms:
            try: exec('self[gene].'+category+'.append("'+term+'")')
            except: exec('self[gene].'+category+'["'+term+'"] =' + '"' + data + '"')

    def __add__(self, other):
        """Combines to gene annotations."""
        # Create an alias list of self and other
        self.alias()
        other.alias()
        L = len(other); n = 0; PB = 0
        for id, gene in other.items():
            n += 1; PA = 100*n/L
            if PA != PB:
                print PA,
                PB = PA
            aliases = other.aliases(id)
            identified = {}
            for alias in aliases:
                finding = self.identify(alias, taxid=gene.taxid)
                if finding:
                    if finding not in identified:
                        identified[finding] = [alias]
                    else:
                        identified[finding].append(alias)
            if len(identified) == 1:
                self[identified.keys()[0]].mergeIt(gene)
            elif len(identified) > 1:
                print "\nFound more than id mapping to this gene:", id, identified, gene, 

    def merge(self):
        pass

    def find(self, name, taxid=None):
        """Given a symbol, name or identify it returns the gene.
        A default taxid can be set via genes.taxid."""
        if not taxid and self.taxid:
            taxid = self.taxid
        identified = self.identify(name, taxid)
        if not isinstance(identified, list):
            return self[identified]
        else:
            results = []
            for i in identified:
                result.append(str(i))
            return "\n".join(results)

    def check(self):
        """Subsquently, prints out all ids and genes.
        Used as quick integrity check."""
        for k,v in self.items():
            print k
            print v
            print

    def keep(self, attr, value):
        """Removes all genes except for those which the defined attribute is true."""
        for id, gene in self.items():
            attribute = eval('gene.'+attr)
            if attribute != value:
                del self[id]

    def remove(self, attr, value, contains=False):
        """Removes all genes for which the attribute has the given value."""
        if contains:
            for id, gene in self.items():
                attribute = eval('genes.'+attr)
                if value in attribute:
                    del self[id]
        else:
            for id, gene in self.items():
                attribute = eval('gene.'+attr)
                if attribute == value:
                    del self[id]


class Gene(object):
    #__slots__ = [id, ensembl_gene, ensembl_transcript, symbol, synonyms, name, alias, refseq, probe, unigene, function, taxid, exp, ctr, log3, fold_change, ratio, classification, p_value, zscore, binding, site_score]
    keys = {  #'age', 'strain', 'tissue', 'cell_type', 'diet', 'gene'
    'id':['entrez_gene_id', 'entrezgene', 'entrezgeneid', 'entrez_gene', 'entrez_id', 'geneid', 'locuslink', 'locusid'],
    'taxid':['tax_id'],
    'symbol':['gene_symbol', 'public_name', 'approved_symbol', 'marker_symbol', 'current_symbol', '##gene_symbol', 'nearest_gene'], #current_symbol(flybase), ##gene_symbol(flybase), #nearest_gene('Epigenome-Wide Scans Identify Differentially Methylated Regions for Age')
    'symbols':['symbol_from_nomenclature_authority', 'previous_symbols', 'synonyms', 'marker_synonyms', 'marker_synonyms_', 'uniprot_genename', 'symbol_synonym'], # uniprot_genename(ensembl), symbol_synonym(s)(flybase)
    'synonyms':[],
    'name':['gene_name','gene_title', 'full_name_from_nomenclature_authority', 'approved_name', 'marker_name', 'current_fullname'], # current_fullname(flybase) 'description':'name',    #Description does not necessary be the gene name
    'names':['other_designations', 'sgdAlias', 'uniprot_genename', 'fullname_synonym(s)'],# uniprot_genename(ensembl), fullname_synonym(s)(flybase)
    'alias':['wormbase_locus', ' flybasename_transcript', 'flybasename_translation', 'flybasecgid_transcript', 'flybasecgid_gene', 'secondary_bggn#', 'annotation_id', 'secondary_annotation_id'], #  flybasename_transcript(ensembl) wormbase_locus(ensembl), FlyBaseName_translation(ensembl), flybasecgid_transcript(ensembl) Better place>?, secondary_FBgn#(flybase), annotation_id(flybase), secondary_annotation_id(flybase)
    'locustag':['locus_tag', 'locustag'],
    'ensembl_gene':['ensembl_gene_identifier','ensembl_gene_id', 'ensembl_id', 'orf', 'orf_name', 'secondaryIdentifier', 'platform_cloneid', 'gene_id'], # gene_id was ensemble gene id in one tissue-specific DR effect signature.
    'ensembl_transcript':['ensembl_rna_identifier', 'ensembl_transcript_id', 'wormbase_transcript', 'seq_id'], #wormbase_transcript(ensembl)
    'ensembl_protein':['ensembl_protein_identifier', 'ensembl_protein_id'], # Corrected a mistake here: 'esembl_protein_identifier'
    'probe':['probe_id','probe_set','probe_set_id','affymetrix_probe_set_id','affy id'],
    'refseq':['ref_seq', 'refseqid', 'ref_seq_ids', 'rna_nucleotide_accession_version', 'protein_accession.version', 'genomic_nucleotide_accession.version', 'refseq_protein_id', 'refseq_peptide', 'refseq_mrna', 'refseq_dna', 'refseq_ncrna', 'refseq_mrna_predicted'], #refseq_peptide(ensembl), refseq_mrna(ensembl), refseq_dna(ensembl), refseq_ncrna(ensembl)  #http://www.ncbi.nlm.nih.gov/RefSeq/RSfaq.html#rsgbdiff #refseqid('Epigenome-Wide Scans Identify Differentially Methylated Regions for Age')
    'genbank':['genbank_accession_no.','gene_bank_accession_no.','genbank_id'],
    'genbank_nucl_gi':['rna_nucleotide_gi', 'genomic_nucleotide_gi'],
    'genbank_protein_gi':['protein_gi'],
    'unigene':['unigene_id'],
    'uniprotkb_id':['uniprot_id', 'uniprot/swissprot'],  #'uniprot/swissprot'(ensembl)  
    'uniprotkb_ac':['uniprotkb_protein_accession'],   
    'uniprotkb_gn':[],
    'trembl':['trembl_id'],
    'uniprot_trembl':['uniprot/sptrembl'], # uniprot/sptrembl(ensembl)
    'wormbase':['wormbase_id', 'wormbase_gene'], #wormbase_gene(ensembl)
    'flybase':['flybase_id', '##primary_fbid', 'primary_fbgn#'], ###primary_FBid(flybase), primary_fbgn#(flybase)
    'imgt_gene_db':['imgt/gene-db'],
    'mim':[],
    'mirbase':['mirbase_gene_id'],
    'mgi':['mouse_genome_database_id', 'mgi_marker_accession_id', 'mgi_accession_id'],
    'vega':['vega_ids', 'vega_gene_id'],
    'hgnc':['hgnc_id'],
    'sgd':['sgd_gene', 'sgd_transcript'],  # sgd_gene = sgd_transcript (ensembl)
    'hprd':[],
    'ucsc':['ucsc_id'],
    'omim':['omim_id'],
    'ec_numbers':['enzyme_ids', 'ec_number'],
    'classification':['changes_in_cr', 'changes_in_aging', 'exclusive category'],
    'exp':[],
    'ctr':[],
    'fold_change':['fc'],
    'log2':[],
    'ratio':['ratio(cy3/cy5))'],
    'zscore':[],
    'binding':[],
    'site_score':[],
    'marked':[],
    'pvalue':['pvaluelogratio','bootstrap_adjusted_p-value','parametric_p-value', 'p_value'],
    'qvalue':['q_value'],
    'fdr':[],
    'chromosome':['chr'],
    'chromosomal_location':[],
    'start':['start_position', 'start position', 'genome_coordinate_start'],
    'stop':['end', 'end_position', 'end position', 'genome_coordinate_end'],
    'strand':['orientation', 'genome_strand'],
    'function':[],
    'description':['concise_descriptor', 'descriptions'],
    'dbxrefs':[],
    'category':['type_of_gene','locus_type', 'marker_type', 'type'],
    'processes':['go_process', 'p', 'molecular_process', 'molecular process', 'gene_ontology_biological_process', "Gene Ontology Biological Process"],
    'functions':['go_function', 'f', 'molecular_function', 'molecular function', 'gene_ontology_molecular_function', "Gene Ontology Molecular Function"],
    'components':['go_component', 'c', 'cellular_component', 'cellular component', 'gene_ontology_cellular_component', "Gene Ontology Cellular Component"],
    'go_slim':['goslim_goa'],
    'pmids':['pmid', 'pubmed_id', 'pubmed_ids',],
    'observation':[],
    'reference':[],
    'expressions':[],
    'expression':['avg_expr'],
    'exp_variance':[],
    'ctr_varaince':[],
    'keywords':[],
    'cg':[],
    }
    mapping =  {}               # Creating an inverse mapping.     
    for k, v in keys.items():   # http://stackoverflow.com/questions/483666/python-reverse-inverse-a-mapping
        for i in v:             # dict(zip(map.values(), map.keys()))
            mapping[i] = k      # dict(v,k) for k,v in map.iteritems()
    akas = """symbol name unigene wormbase flybase mirbase imgt_gene_db genbank Id vega name_ids ensembl rgd newt sgd irefindex
              orf_name kegg pir afcs tpg other icrogid crogid irogid rogid complex camjedb uniprotkb_gn trembl uniprotkb_trembl
              uniparc interpro chebi ipi grid isoform_synonym ratmap probe alias refseq synonyms uniprotkb_id uniprotkb_ac dbj_embl_genbank
              intact mint short_label name_synonym locus_name pdb prf emb tigr cygd discontinued_ids ensembl_gene ensembl_transcript
              ensembl_protein symbols names locustag embl uniprotkb_ac refseq probe""".split()
    # Parsing Mint results in this: uniprotkb_ac: ['Q99590', 'SIP1', 'CASP11', 'SFRS2IP', '"Splicing factor, arginine/serine-rich 2-interacting protein"', 'SC35-interacting protein 1', 'CTD-associated SR protein 11', 'Splicing regulatory protein 129', 'Renal carcinoma antigen NY-REN-40']
    snis = akas + ['id', 'genbank_protein_gi', 'genbank_nucl_gi']
    def __init__(self, id=None,
                 ensembl=None,
                 ensembl_gene=None,
                 ensembl_transcript=None,
                 ensembl_protein=None,
                 symbol=None,
                 symbols=None,
                 alias=None,
                 name=None,
                 names=None,
                 locustag=None,
                 refseq=None,     
                 probe=None,
                 unigene=None,
                 function=None,
                 taxid=None,

                 exp=None,
                 ctr=None,
                 exp_variance=None,
                 ctr_variance=None,
                 log2=None,
                 fold_change=None,
                 ratio=None,
                 ratios=None,
                 expressions=None,
                 expression=None,
  
                 classification=None,
                 pvalue=None,
                 zscore=None,
                 fdr=None,
                 binding=None,
                 site_score=None,
                 marked=None,
                 genbank=None,
                 qvalue=None,
                 wormbase=None,
                 flybase=None,
                 pdb=None,
                 intact=None, 
                 uniprotkb_id=None,
                 uniprotkb_ac=None,
                 uniprotkb_gn=None,
                 trembl=None,
                 uniprotkb_trembl=None,
                 embl=None, # European Nucleotide Archive (e.g. in Ensembl)
                 genbank_nucl_gi=None,
                 genbank_protein_gi=None, 
                 Id=None,
                 dbj_embl_genbank=None,
                 uniparc=None,
                 interpro=None,
                 chebi=None,
                 pubchem=None,
                 ipi=None,
                 rgd=None,
                 newt=None,
                 sgd=None,
                 cygd=None,
                 dip=None,
                 grid=None,
                 hprd=None,
                 mint=None,
                 isoform_synonym=None,
                 short_label=None,
                 name_synonym=None, 
                 locus_name=None,
                 irefindex=None,
                 prf=None,
                 emb=None,
                 kegg=None,
                 pir=None,
                 afcs=None,  
                 tpg=None,
                 tigr=None,   
                 pmids=None,
                 other=None,
                 name_ids=None,
                 orf_name=None,
                 icrogid=None,
                 crogid=None,
                 irogid=None,
                 rogid=None,
                 complex=None,
                 camjedb=None,
                 discontinued_ids=None,
                 discontinued=False,

                 hgnc=None,
                 mim=None,              
                 ratmap=None,
                 mirbase=None,             
                 imgt_gene_db=None,             
                 vega=None,         
                 mgi=None,
                 synonyms=None,
                 ec_numbers=None,    
                 description=None,
                 
                 go_process=None,
                 go_function=None,
                 go_component=None,
                 go_slim=None,
                 processes=None,       
                 functions=None,
                 components=None,
                 keywords=None,

                 category=None,
                 
                 cpg=None,
                 name_clone=None,
                 position=None,
                 promoter_number=None,
                 chromosome=None,
                 chromosomal_location=None,
                 cg=None,
                 
                 start=None,
                 stop=None,
                 strand=None,
                 map_location=None,

                 observation=None,
                 reference=None
                 ):
        # Synonyms:
        try: id = int(id)
        except: pass
        self.id = id            #Entrez gene id
        self.symbol = symbol    #Gene symbol
        self.symbols = symbols or []
        self.name = name        #Gene name
        self.names = names or []
        self.locustag = locustag
        #self.ensembl_gene = [ensembl_gene] or []
        self.ensembl = ensembl
        self.ensembl_gene = ensembl_gene
        #if ensembl_gene: self.ensembl_gene = [ensembl_gene]
        #else: self.ensembl_gene = []
        if ensembl_transcript: self.ensembl_transcript = [ensembl_transcript]
        else: self.ensembl_transcript = []
        if ensembl_protein: self.ensembl_protein = [ensembl_protein]
        else: self.ensembl_protein = []
        #self.refseq = [refeseq] or []
        if refseq: self.refseq = [refseq]     #List in iRefindex
        else: self.refseq = []
        self.unigene = unigene     #Is this right a list?
        self.genbank = genbank or [] # Add a [] here on 09/06/2012
        self.wormbase = wormbase
        self.flybase = flybase  #"flybase" or "FlyBase"; e.g.FBgn0053472
        self.name_ids = name_ids
        if uniprotkb_id: self.uniprotkb_id = [uniprotkb_id]
        else: self.uniprotkb_id = []                              # List in iRefIndex
        if uniprotkb_ac: self.uniprotkb_ac = [uniprotkb_ac]
        else: self.uniprotkb_ac = []                        # List in iRefIndex
        self.uniprotkb_gn = uniprotkb_gn
        self.trembl = trembl or []                                # looks like and unprot protein identifer; better a list? Jep in MGI it is a list.
        self.uniprotkb_trembl = uniprotkb_trembl
        self.embl = embl or []
        self.genbank_nucl_gi = genbank_nucl_gi
        if genbank_protein_gi: self.genbank_protein_gi = [genbank_protein_gi] # "gb:" or "GB:"; e.g. AAH24185.1
        else: self.genbank_protein_gi = []                                       # List in iRefIndex
        self.Id = Id                               #Whats this?
        if dbj_embl_genbank: self.dbj_embl_genbank = [dbj_embl_genbank] # "dbj" or "dbj/embl/genbank"; e.g. BAA09221.1
        else: self.dbj_embl_genbank = []                                     # List in iRefIndex
        self.uniparc = uniparc
        self.interpro = interpro
        self.chebi = chebi
        self.pubchem = pubchem
        self.ipi = ipi
        self.rgd = rgd
        self.newt = newt
        self.sgd = sgd
        if intact: self.intact = [intact]     # e.g.EBI-1190365 
        else: self.intact = []              # List in iRefIndex     What is this?
        self.dip = dip
        self.grid = grid
        self.hprd = hprd    #integer e.g. 07260
        if mint: self.mint = [mint]   # e.g. MINT-7385512
        else: self.mint = []        # List in iRefIndex
        self.irefindex = irefindex
        self.isoform_synonym = isoform_synonym
        if short_label: self.short_label = short_label
        else: self.short_label = []     # List in iRefIndex
        if name_synonym: self.name_synonym = [name_synonym]
        else: self.name_synonym = []
        self.orf_name = orf_name
        if locus_name: self.locus_name = [locus_name]
        else: self.locus_name = []
        if pdb: self.pdb = [pdb]
        else: self.pdb = []
        if prf: self.prf = [prf]  #e.g. 0706243A
        else: self.prf = []    #List in iRefIndex
        if emb: self.emb = [emb]
        else: self.emb = []
        self.kegg = kegg    #e.g. hsa:64396
        self.pir = pir
        self.afcs = afcs  
        self.tpg = tpg
        if tigr: self.tigr = [tigr]   # "TIGR"; e.g. ATA1235 or NTL02ATA0611
        else: self.tigr = []        # List in iRefIndex
        self.pmids = [pmids] or []
        self.other = other
        if cygd: self.cygd = [cygd]       # "cygd"; e.g. GALd3RPTaY2Occygd4iZTPZ3sSA83333
        else: self.cygd = []            # List in iRefIndex
        self.icrogid = icrogid    #int
        self.crogid = crogid
        self.irogid = irogid      #int e.g. 11789984
        self.rogid = rogid        #e.g. Z2H+9BGmjlTDAESXmB/nhR9CIHc197
        self.complex = complex
        self.camjedb = camjedb  #e.g.Cj0290c
        if discontinued_ids: self.discontinued_ids = [discontinued_ids]
        else: self.discontinued_ids = [] # Entrez gene ids discontinued from gene_history
        self.discontinued = discontinued
        self.hgnc = hgnc                            # HGNC:7              (int in entrez_gene_info)
        self.mim = mim                              # MIM:103950    (int in entrez_gene_info)
        self.vega = vega         # Vega:OTTHUMG00000150267  (Entrez)
        self.mirbase = mirbase # Entrez
        self.mgi = mgi
        self.imgt_gene_db = imgt_gene_db    # Entrez
        self.ratmap = ratmap    # Entrez
        if synonyms: self.synonyms = [synonyms]
        else: self.synonyms = []
        if probe: self.probe = [probe]
        else: self.probe = []
        if alias:
            if type(alias) == list: self.alias = alias
            else: self.alias = [alias]
        else: self.alias = []
  
        #self.alias = [self.id, self.symbol, self.name, self.unigene, self.wormbase, self.flybase, self.mim,self.mirbase, self.imgt_gene_db, self.mgi, self.genbank_nucl_gi,self.Id,self.hgnc,self.vega, self.name_ids,self.ensembl,self.ensembl_protein,self.rgd,self.newt, self.sgd,self.irefindex,self.orf_name,self.kegg, self.pir, self.afcs, self.tpg,self.pmid, self.other,self.icrogid, self.crogid, self.irogid,self.rogid, self.complex, self.camjedb]+self.probe+self.alias+self.refseq+self.synonyms+self.ensembl_gene+self.ensembl_transcript+self.uniprotkb_id+self.genbank_protein_gi+self.ensembl_gene+self.ensembl_transcript+self.dbj_embl_genbank+self.intact+self.mint+self.short_label+self.name_synonym+ self.locus_name+self.pdb+self.prf+self.emb+self.tigr+self.cygd+self.discontinued_ids
        #while None in self.alias: self.alias.remove(None)

        # Annotations:
        try: self.taxid = int(taxid)
        except: self.taxid = taxid
        if ec_numbers: self.ec_numbers = [ec_numbers] # SGD_features
        else: self.ec_numbers = []              
        self.description = description
        if go_process: self.go_process = [go_process]
        else: self.go_process = []
        if go_function: self.go_function = [go_function]
        else: self.go_function = []
        if go_component: self.go_component = [go_component]
        else: self.go_component = []
        if go_slim: self.go_slim = [go_slim]
        else: self.go_slim = []
        self.category = category     # from entrez_gene_info, e.g. protein-coding
        self.keywords = keywords or []

        # Associated terms:
        if processes:
            if isinstance(processes, dict): self.processes = processes
            elif isinstance(processes, str): self.processes = {processes:None}
        else: self.processes = {}
        if functions:
            if isinstance(functions, dict): self.functions = functions
            elif isinstance(functions, str): self.functions = {functions:None}
        else: self.functions = {}
        if components:
            if isinstance(components, dict): self.components = components
            elif isinstance(components, str): self.components = {components:None}
        else: self.components = {}
        
        self.observation = observation
        self.pmids = pmids or []
        self.function = function or None
        self.reference = reference or None
    
        # Signatures:
        if exp: self.exp = float(exp)
        else: self.exp = None
        if ctr: self.ctr = float(ctr)
        else: self.ctr = None
        if fold_change: self.fold_change = float(fold_change)
        else: self.fold_change = None
        if ratio == None and fold_change != None: # ratio stores the average ratio.
            if fold_change < 0: ratio = 1./(abs(fold_change)+1)
            else: ratio = fold_change + 1 #self.ratio = -1/fold_change #http://bitesizebio.com/questions/how-do-you-convert-a-decimal-fold-change-value-into-a-negative-number/
        elif ratio == None and log2 != None: self.ratio = 2**log2
        elif ratio: self.ratio = float(ratio)
        else: self.ratio = None
        self.ratios = ratios or [] # Stores all ratios, if multiple are given.
        if exp_variance: self.exp_variance = exp_variance
        else: self.exp_variance = None
        if ctr_variance: self.ctr_variance = ctr_variance
        else: self.ctr_variance = None

        if expressions:
            if isinstance(expressions, list):   self.expressions = int(expression)
            else:                               self.expressions = [int(expressions)]
        else:                                   self.expressions = []
        if expression: self.expression = float(expression)
        else: self.expression = None
        
        self.variance = None

        self.classification = classification

        self.pvalue = pvalue
        self.qvalue= qvalue
        self.zscore = zscore
        if fdr:
            try: self.fdr = float(fdr)
            except ValueError: self.fdr = None
        else: self.fdr = None
        self.binding = binding

        self.cpg = cpg
        self.name_clone = name_clone
        self.position = position
        self.promoter_number = promoter_number
        self.cg = cg

        self.marked = marked
        self.site_score = site_score

        self.molecule = None # For Cellularity
        self.chromosome = chromosome
        if start: self.start = int(start)
        else: self.start = None
        if stop: self.stop = int(stop)
        else: self.stop = None
##        if strand: self.strand = int(strand)
        if strand:
            try: self.strand = int(strand)
            except: self.strand = strand
        else: self.strand = None
        self.map_location = map_location

    def update_name(self):
        if not self.name: self.name = self.description

    def update_ratio(self):
        self.ratio = self.exp/self.ctr

    def add(self, value, attribute=None):
        '''Assigns a gene symbol, name or identifier to its respective attribute
        It decides whether it has to already present and whether it assigns it to its attrubute value or appends it to the attrubite list'''
        seperators = ['|', ', ', '; ', ',', ';', ' /// '] # ' /// ' is in GPL files.
        if attribute:
            if attribute in Gene.mapping: attribute = Gene.mapping[attribute]
            #print attribute, value
            
            if not hasattr(self, attribute):
                setattr(self, attribute, [value])
                return None
                
            attr = eval('self.'+attribute)  # Still None?
            #Type = type(attr)                # list or integer/string
            if isinstance(attr, dict): pass     #Type == dict: pass # Add an functio to include for instance functional terms.
            elif isinstance(attr, list):    #Type == list:
                if value != "" and value != "-" and value != "null" and value not in attr:
                    seperated = False
                    for seperator in seperators:
                        if seperator in value:
                            values = value.split(seperator)
                            for value in values:
                                #if ':' in value: s = value.split(':')[1]
                                if value not in attr: exec('self.'+attribute+'.append(evalu(value))')
                            seperated = True
                    if not seperated: exec('self.'+attribute+'.append(evalu(value))')
            else: # Probaly string or digit
                if not attr and value != "" and value != "-":
                    
                    if isinstance(value, str):  #type(value) == str:# or type(value) == int or type:
                        #print value, attribute     ##### is this actually funcitonal #### When will it be triggered??
                        if ":" in value and ": " not in value and attribute != "description" and attribute != 'synonyms' and attribute != "other designation" and attribute != "symbol" and attribute != "name" and attribute[:3] != 'go_'  and attribute != 'observation' and attribute != 'function':
                            attribute, value = value.split(':')
                            if attribute in Gene.mapping: attribute = Gene.mapping[attribute]
                        try:
                            exec('self.'+attribute+'=evalu(value)')
                        except:
                            print attribute, value
                            print 'self.'+attribute+'=evalu(value)'
                            exec('self.'+attribute+'=evalu(value)')
                    else:
                        exec('self.'+attribute+'=evalu(value)')

        else:
            if isinstance(value, str):  # type(value) == str:
                if ":" in value and ": " not in value and ": " not in value and attribute != "description" and attribute != "synonyms" and attribute != "other designation":
                    attribute, value = value.split(':')
                    if attribute in Gene.mapping: attribute = Gene.mapping[attribute]
                    exec('self.'+attribute+'=evalu(value)')


    def merge(self, other):
##        if g.ensembl_gene == None: g.ensembl_gene = self.ensembl_gene
##        if g.ensembl_transcript == None: g.ensembl_transcript = self.ensembl_transcript
##        if g.symbol == None: g.symbol = self.symbol
##        if g.name == None: g.name = self.name
##        if g.refseq == None: g.ref_seq = self.ref_seq
##        if g.taxid == None: g.taxid = self.taxid
##        if g.cpg == None: g.cpg = self.cpg
##        if g.name_clone == None: g.name_clone = self.name_clone
##        if g.position == None: g.position = self.position
##        if g.promoter_number == None: g.promoter_number = self.promoter_number
##        if g.fold_change == None:
##            self.fold_change = self.fold_change
##        for probe in self.probe:
##            if self.probe and self.probe not in g.probe: g.probe.append(self.probe)
##        g.alias = list(set.union(set(self.alias), set(g.alias)))    # self.#[self.id, self.ensembl_gene_id, self.ensembl_transcript_id, self.symbol, self.name, self.ref_seq] + self.probe_id
        if not self.ensembl_gene: self.ensembl_gene = other.ensembl_gene
        if not self.ensembl_transcript: self.ensembl_transcript = self.ensembl_transcript
        if not self.symbol: self.symbol = self.symbol
        if not self.name: other.name = self.name
        if not self.refseq: other.refseq = self.refseq
        if not self.taxid: other.taxid = self.taxid
        if not self.cpg: other.cpg = self.cpg
        if not self.name_clone: other.name_clone = self.name_clone
        if not self.position: other.position = self.position
        if not self.promoter_number: other.promoter_number = self.promoter_number
        if not self.fold_change:
            self.fold_change = other.fold_change
        for probe in self.probe:
            if self.probe and self.probe not in other.probe: other.probe.append(self.probe)
        other.alias = list(set.union(set(self.alias), set(other.alias)))    # self.#[self.id, self.ensembl_gene_id, self.ensembl_transcript_id, self.symbol, self.name, self.ref_seq] + self.probe_id
        if other.expressions: self.expressions.extend(other.expressions)
        #self.__dict__.update({k:v for k,v in g.__dict__.items() if v})  # http://stackoverflow.com/questions/6354436/python-dictionary-merge-by-updating-but-not-overwrting-if-value-exists
        #The above statement does not work in 2.6 but in 2.7 - find alterntive formulation!

    def mergeIt(self, other):
        otherAttributes = vars(other).items()
        for attr, value in otherAttributes:
            if attr != "id":
                if value:
                    selfAttribute = getattr(self, attr)
                    if not selfAttribute:
                        setattr(self, attr, value)
                    elif value == selfAttribute:
                        pass
                    elif isinstance(value, list):
                        for item in value:
                            if item not in selfAttribute:
                                selfAttribute.append(item)
                        if selfAttribute != getattr(self, attr):
                            setattr(self, attr, selfAttribute)
                    else:                                               # Catch here all exceptions:
                            #try:
                            if attr == "description":
                                if self.description == self.name: # Entrez description for 6239 are identical with the gene names
                                    self.description = value
                                elif self.description == 'hypothetical protein':
                                    self.description = other.description
                                    self.alias.remove('hypothetical protein')
                                
                            elif attr == "symbol":
                                if other.symbol == other.ensembl_gene[0]:
                                    pass
                                elif self.symbol in self.synonyms: # Rename it to self.locus_tag
                                    self.symbol = other.symbol
                            elif attr == "name":
                                if "Record to support submission of GeneRIFs " in self.name:
                                    self.name = other.name
                            elif attr == "wormbase":
                                self.wormbase = other.wormbase
                                self.symbol = other.symbol
                            elif attr == 'strand':
                                if self.strand == '?':
                                    self.strand = other.strand
                            elif attr == 'chromosome':
                                self.chromosome = other.chromosome
                            else:
                                print "-"*20
                                print "Discrepancy regarding:", attr, "for:"
                                print self
                                print "="*20
                                print other
                            #except:
                                #print "Raised exception:", attr, value, selfAttribute
#synonyms: ['F56H1.6', 'NEWENTRY']
# introduce an orf or locus_tag attribute for keeping sequence names
# ensembl_gene is a list of gene models mapping to one sequence name/ entrez gene id


    def __add__(self, g):
        c = copy.deepcopy(self)
        for attribute, value in vars(g).items():
            if value:
                if isinstance(value, list):
                    exec('c.'+attribute+'=list(set(c.'+attribute+'+value))')
                    #exec('c.'+attribute+'=list(set(c.'+attribute+'.extend(value)))')
                else:
                    attr = eval('c.'+attribute)
                    if attr: exec('c.'+attribute+' = value')
        return c
    
    def annot(self, g):
        #PyGr Seq infos
        self.start = g.sequence.start
        self.stop = g.sequence.stop
        self.orientation = g.sequence.orientation
        self.chrom = g.chrom
        return self
            
    def __repr__(self):
        #return '\t'.join(map(str,self.alias))
        Attributes = []
        attributes = self.__dict__
        for attribute in attributes:
            #if eval('self.'+attribute): Attributes.append((attribute,eval('self.'+attribute)))
            if eval('self.'+attribute): Attributes.append(attribute+': '+str(eval('self.'+attribute)))
        return '\n'.join(map(str,Attributes))

    def Print(self):
        return '\t'.join(map(str, [''.join(self.ensembl_gene), self.taxid, self.description, self.chromosome, self.start, self.stop, self.strand]))
                
    def __eq__(self, g):             
        return self.__dict__ == g.__dict__

    def aliasSynonym(self):
        self.alias = [self.id, self.symbol, self.name, self.unigene, self.flybase, self.mirbase, self.imgt_gene_db, self.genbank,
                      self.Id, self.vega, self.name_ids, self.ensembl, self.rgd, self.newt, self.sgd, self.irefindex, self.orf_name,
                      self.kegg, self.pir, self.afcs, self.tpg, self.other, self.icrogid, self.crogid, self.irogid, self.rogid,
                      self.complex, self.camjedb, self.uniprotkb_gn, self.trembl, self.uniprotkb_trembl, self.uniparc,
                      self.interpro, self.chebi, self.ipi, self.grid, self.isoform_synonym, self.ratmap]\
                      +self.probe+self.alias+self.refseq+self.synonyms+self.uniprotkb_id+self.uniprotkb_ac+self.dbj_embl_genbank\
                      +self.intact+self.mint+self.short_label+self.name_synonym+self.locus_name+self.pdb+self.prf+self.emb+self.tigr\
                      +self.cygd+self.discontinued_ids+self.ensembl_gene+self.ensembl_transcript+self.ensembl_protein+self.symbols+self.names
                      # self.dip, is integer
        if self.wormbase and self.wormbase != self.id:
            self.alias.append(self.wormbase)
        while None in self.alias: self.alias.remove(None)
        #self.pubchem, self.pmids, self.hgnc, self.hprd, self.mim,  self.mgi, self.genbank_nucl_gi +self.genbank_protein_gi
##        self.alias = [self.id, self.symbol, self.name, self.ensembl_gene, self.ensembl_transcript, self.ensembl_protein, self.ensembl, self.unigene, self.uniparc, 
##                           self.genbank, self.genbank_nucl_gi, 
##                           self.sgd, self.wormbase, self.flybase, self.hprd,
##                           self.uniprotkb_gn, self.trembl, self.uniprotkb_trembl,
##                           self.Id, self.interpro, self.chebi, self.pubchem, self.ipi, self.rgd, self.newt, self.pir, self.afcs, self.camjedb,
##                           self.name_ids, self.orf_name, self.tpg, self.pmid, self.other,
##                           self.dip, self.grid, self.irefindex, self.kegg,
##                           self.isoform_synonym, self.isoform_synonym, self.rogid] + self.alias + self.probe + self.intact + self.pdb  + self.short_label + self.name_synonym + self.locus_name + self.emb + self.uniprotkb_ac + self.uniprotkb_id + self.refseq + self.dbj_embl_genbank +  self.tigr +  self.mint + self.prf + self.genbank_protein_gi + self.cygd + self.discontinued_id
##        while None in self.alias: self.alias.remove(None)
        return self.alias#';'.join(map(str,self.alias))

    def sni(self):
        """Retrieves all symbols/names and identifiers."""
        snis = []
        for sni in Gene.snis: #sni = symbol/name/identifier
            #if sni == "uniprotkb_ac": print "sni == uniprotkb_ac"
            attr = getattr(self, sni)
            if attr:
                if isinstance(attr, list):
                    snis.extend(attr)
                else:
                    snis.append(attr)
        return set(snis)
        
    def alsoKnownAs(self):
        """Retrieves all symbols and names and entrez identifier of the gene."""
        self.aka = []
        for aka in Gene.akas:
            attr = getattr(self, aka)
            if attr:
                if isinstance(attr, list):
                    self.aka.extend(attr)
                elif isinstance(attr, str):
                    self.aka.append(attr)
        if self.id: self.aka.append(self.id) # Not sure if this is wise.
        return set(self.aka) # Eleminates duplicates.

    def save(self, name):
        if name[-4:] == '.mrl':
            data_file = open(name, 'wb', 5)
            for key, value in self.__dict__.items():
                marshal.dump(value, data_file)
            
    def load(self, name):
        if name[-4:] == '.mrl':
            marshal.load(value, name)

    def averageExpression(self):
        """Calculates the average expression from the expression values, if present."""
        try: self.expression = 1.*sum(self.expressions)/len(self.expressions)   # Need to be of type float (1.*).
        except ZeroDivisionError: self.expression = 0

    def calcVariance(self):
        """Calculates the variance in its expression."""
        try:
            #self.variance = naiveVariance(self.expressions)
            if not self.expression: self.expression = 1.*sum(self.expressions)/len(self.expressions)
            for i in self.expressions: self.variance = (self.expression-i)**2
        except ZeroDivisionError: self.variance = 0


    def pValue(self):
        """Calculates the p-value of expression change.
        Not yet implemented here."""
        if self.variance:
            pass
            #ttest(self.sfdd)
        

class GenomeGene:
    def __init__(self, name, id, start, stop, orientation):
        self.name = name
        self.id = id
        self.chrom = id
        if orientation == -1:
            self.start = -stop
            self.stop = -start
        else:
            self.start = start
            self.stop = stop  
        self.orientation = orientation

        self.exp = None
        self.ctr = None
        self.fold_change = None
        self.symbol = None
        self.probe_id = None

    def annot(self, g):
        self.exp = g.exp
        self.ctr = g.ctr
        self.fold_change = g.ratio  # Remove this when possible
        self.ratio = g.ratio
        self.symbol = g.symbol
        self.probe = g.probe


genes = Genes()

if __name__ == '__main__':
    genes.load()
