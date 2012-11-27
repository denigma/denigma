"""Interactomics classes."""
import os

from gen import Gene


def Taxid(t): # Make function name lowercase
    st = t.split(':')
    if st[0] == "taxid":
        if "(" in st[1]:
            sst = st[1].split('(')
            return sst[0]
        else:
            return sst[1]
    else:
        #print "Taxid unknown! ", t
        return ""

unsortedIDInteractor = []
InteractionDetectionMethodList = {}
##physicalInteractionDetectionMethods = []
##geneticInteractionDetectionMethods = []
Dic = {}

class Interactions(list):
    """Wrapper for interactions. Allows to save collected interactions to unifyied text file format."""
    def __init__(self, load=False):
        self.i = {}
        if load:
            input = file('D:/Interactions/IntegratedInteractions/IntMerged.txt').read().split('\n')
            L = len(input); n = 0; PB = 0 #Start Counter

            for i in input:
                        
                n += 1; PA = 100*n/L #Continue Counter
                if PA != PB: print PA,
                PB = PA

                if i != input[0] and i != "":
                    s = i.split('\t')
                    #self.append(
                    i = Interaction(s[0], s[1],
                                            s[2].split('; '),
                                            s[3].split('; '),
                                            s[4].split('; '),
                                            s[5].split('; '),
                                            s[6].split('; '),
                                            s[7].split('; '),
                                            s[8], s[9],
                                            s[10].split('; '),
                                            s[11].split('; '),
                                            s[12])
                    if i.a not in self.i:
                        #I[idA] = {idB:s[2:]}
                        self.i[i.a] = {i.b:i}

                    else:
                        #I[idA][idB] = s[2:]
                        self.i[i.a][i.b] = i

    def partners(self, id):
        """Retrieves all interaction partners of an identifier."""
        res = {}
        for a in self.i:
            if id == a:
                res.update(self.i[a])
            for b, i in self.i[a].items():
                if id == b:
                    res[a] = i
        return res
    
    def get(self, ida, idb=None):
        """Retrieves all interactions for a gene by its identifier."""
        res = []
        if not idb:
            for a in self.i:
                for b, i in self.i[a].items():
                    if ida == a or ida == b:
                        res.append(i)     
        else:
            for a in self.i:
                for b, i in self.i[a].items():
                    if (a == ida and b == idb) or (a == idb and b == ida):
                        res.append(i)
        return res

            
    def save(self, path='.', name='interactions.txt', id=False, header=False):
        """Saves interactions to text file format."""
        if id: slots = Interaction.__slots__[0:]
        else: slots = Interaction.__slots__[2:]
        output = open(os.path.join(path, name), 'wb')
        if header: output.write('\t'.join(slots)+'\n')
        #L = len(self); PB = 0; n = 0
        for interaction in self:
            #n += 1; PA = 100*n/L
            #if PA != PB: print PA
            #PB = PA
            outputList = []
            if not id and interaction.a: interaction.aliasA.append(interaction.a)
            if not id and interaction.b: interaction.aliasB.append(interaction.b)
            for attribute in slots:
                value = eval('interaction.'+attribute)
                if type(value) == list: value = '; '.join(map(str, value))
                elif type(value) != str: value = str(value or '')
                outputList.append(value or '')
            output.write('\t'.join(outputList)+'\n')
        output.close()

    def __repr__(self):
        string = []
        for interaction in self:
            print interaction
            print
        return "\n".join(string)

    def batch(self, data, info):
        """Adds interaction data in batch."""
        for i in data:
            interaction = Interaction()
            if hasattr(self, 'taxid'):
                interaction.taxidA = interaction.taxidB = self.taxid
            if hasattr(self, 'db'):
                interaction.db = self.db
            if info:
                for k, v in info.items():
                    if isinstance(v, (int, list)): exec('interaction.'+k+'='+str(v))
                    elif isinstance(v, str): exec('interaction.'+k+'="'+v+'"')
                    #elif isinstance(v, list): exec('interaction.'+k+'='+v)
##                if 'taxid' in info: interaction.taxid = info['taxid']
##                if 'db' in info: interaction.db = info['db']
##                if 'method' in info
            keep = False
            for k, v in i.items():
                k = k.replace(' ', '_').lower()
                if k in Interaction.mapping:
                    k = Interaction.mapping[k]
                #print k, v
                if k in Interaction.__slots__ and v:
                   attr = eval('interaction.'+k)
                   if isinstance(attr, list):
                       if '; ' in v:
                           v = v.split('; ')
                           for i in v:
                               exec('interaction.'+k+'.append("'+i+'")')
                       else:
                           exec('interaction.'+k+'.append("'+v+'")')
                   else:
                       exec('interaction.'+k+'="'+v+'"')
                   keep = True
            if not keep:
                self.pop()
            
                            
                    
                
            
interactions = Interactions()

class Interaction():
    __slots__ = ['a', 'b', 'aliasA', 'aliasB', 'system', 'method', 'type', 'modification', 'taxidA', 'taxidB', 'pmid', 'db']
    
    keys = {'aliasA':['enzyme_catalyzing_modification', 'bait_short_name', 'bait_name', 'bait_nucl_gl', 'bait_protein_gl'],
            'aliasB':['protein_name', 'prey_short_name', 'prey_nucl_gi', 'prey_prot_gi'],
            'modification':['modification_type'],
            'type':['stimulates_or_inhibits']
            }
    mapping = {}
    for k,v in keys.items():
        for i in v:
            mapping[i] = k
            
    def __init__(self, a=0, b=0, aliasA=None, aliasB=None, system=None, method=None, type=None, modification=None, taxidA=0, taxidB=0, pmid=None, db=None, score=None):
        self.a = int(a)
        self.b = int(b)
        self.aliasA = aliasA or []
        self.aliasB = aliasB or []
        self.system = system or []
        self.method = method or []
        self.type = type or []
        self.modification = modification or []
        self.taxidA = int(taxidA)
        self.taxidB = int(taxidB)
        self.pmid = pmid or []
        if db and isinstance(db, list): self.db = db
        elif db: self.db = [db]
        else: self.db = []
        self.score = score
        if method:
            for m in method:
                if m in physicalInteractionTypes or m in physicalInteractionDetectionMethods:
                    if 'direct' not in system: system.append('system')
                    if 'physical' not in system: system.append('physical')
                elif m in geneticInteractionTypes or m in geneticInteractionDetectionMethods:
                    if 'direct' not in system: system.append('system')
                    if 'genetic' not in system: system.append('physical')
                else:
                    if m not in InteractionDetectionMethodList: InteractionDetectionMethodList[m] = self
        interactions.append(self)

    def add(self, **args):
        """Takes parameters of attributes and checks whether they are valied (i.e. not '-' or '')
        and maps them to their corresponding attributes."""
        if (self.taxidA or ('taxidA' in args and args['taxidA'] and args['taxidA'] != '-'))\
           and (self.taxidB or ('taxidB' in args and args['taxidB'] and args['taxidB'] != '-')): # Ensures that only interaction between entities of known species are used.
            for attribute, value in args.items():
                if attribute in vars(self):
                    Attribute = eval('self.'+attribute)
                    if isinstance(value, list):
                        for item in value:
                            if item and item != '-' and item not in Attribute:
                                exec('self.%s.append(item)' % attribute)
                    elif isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                        if value and value != '-' and not Attribute:
                            exec('self.%s=value' % (attribute))
        else:
            interactions.pop()
          
    def AddMethod(self):
        pass
    def AddType(self):
        pass
    def AddMod(self):
        pass

    def __repr__(self):
        string = []
        for k, v in vars(self).items():
            if v:
                string.append("%s: %s" % (k, v))
        return "\n".join(string)
        
##    def __str__(self):
##        return str(vars(self))

    def string(self):
        return '\t'.join(map(str, ['; '.join(map(str,self.system)), '; '.join(map(str,self.method)),
                                   '; '.join(map(str,self.type)), '; '.join(map(str,self.pmid)),
                                   '; '.join(map(str,self.db)), self.score]))

    def Print(self):
        """Depriciated."""
        return '\t'.join(['; '.join(self.a.alsoKnownAs()), '; '.join(self.b.alsoKnownAs()),
                          '; '.join(self.system), '; '.join(self.method),
                          '; '.join(self.type), '; '.join(self.modification),
                          self.taxidA, self.taxidB,
                          '; '.join(map(str, self.pmid)), '; '.join(self.db)])+'\n'
    def output(self):
        """Returns a string output representation of an interaction."""
        return '\t'.join(['; '.join(map(str, self.a)), '; '.join(map(str, self.b)),
                          '; '.join(self.system), '; '.join(self.method),
                          '; '.join(self.type), '; '.join(self.modification),
                          self.taxidA, self.taxidB,
                          '; '.join(map(str, self.pmid)), '; '.join(self.db)])+'\n'

    def Solve(id, s):
        ss = s[n].split(':')
        A.uniprotkbAC = ss[1]

    def MiTAB(self, interaction):
        "this is an new interaction"
        if self.db in ["iRefIndex", "DIP"] and Dic == {}:
            Input = file('./DIP/fasta20101010.seq').read().split('\n')
            for line in Input:
                if ">" in line:
                    split = line.split('|')
                    for item in split:
                        if '>dip:' in item:
                            DIP = item.split('>dip:')
                            Dic[DIP[1]] = [DIP[1]]
                        if 'refseq:' in item:
                            RefSeq = item.split('refseq:')
                            Dic[DIP[1]].append(RefSeq[1])
                        if 'uniprot:' in item:
                            UniProt = item.split('uniprot:') 
                            Dic[DIP[1]].append(UniProt[1])

        #if Database == 'IntAct' or Database == 'MINT' or Database == 'DIP' or Database == 'Reactome' or (Database == 'BioGRID' and FileName =='BIOGRID-ALL-3.0.64.mitab.txt') or Database == "iRefIndex":   
            #Data = file(FileName).read().split('\n')
            #for Interaction in Data:
        #if Interaction == "": return ""
        field = interaction.split('\t')
        self.taxidA = Taxid(field[9])
        self.taxidB = Taxid(field[10])
        self.a = Gene(taxid=self.taxidA)
        self.b = Gene(taxid=self.taxidB)

##        print self
        #print "Genes:", self.a, self.b
        #print field[:6]
        for pos in xrange(0,6):
            s = field[pos].split('|')
            
            if s != "" and s != "-" and s != " -":
                x = len(s)
                n = 0

                if pos % 2:
                    X = self.b

                    #print "X is now self.b"
                        
                else: X = self.a
                    #print "X is now self.a"
                if pos == 0 or pos == 1:
                    X.alias = []
                    X.probe = []
                    X.intact = []
                    X.pdb = []
                    X.short_label = []
                    X.name_synonym = []
                    X.locus_name = []
                    X.emb = []
                    X.uniprotkb_ac = []
                    X.uniprotkb_id = []
                    X.refseq = []
                    X.dbj_embl_genbank = []
                    X.tigr = []
                    X.mint = []
                    X.prf = []
                    X.genbank_protein_gi = []
                    X.cygd = []
                while n != x:
                    #for i in ids:
                        #if i in s[n]
 
                    ss = ''
                    zz = ''
                    sss = ''
                    ss = s[n].split(':')
                    zz = s[n].split('"')
                    if len(ss) > 1:
                        if "(" in ss[1]: sss = ss[1].split('(')

                    if "uniprotkb" in s[n] and "_" in s[n]:   #multiple assigninments in iRefIndex
                        #if X.uniprotkb_id and ss[1] != X.uniprotkb_id: print "X.uniprotkb_id", X.uniprotkb_id, ss[1], field[pos].split('|')[n]
                        try:
                            if sss[0] not in X.uniprotkb_id: X.uniprotkb_id.append(sss[0])
                        except:
                            if ss[1] not in X.uniprotkb_id: X.uniprotkb_id.append(ss[1])

                    elif 'uniprotkb' in s[n] and 'gene name' in s[n]:
                        try: 
                            if sss[0] not in X.symbols: X.symbols.append(sss[0])
                        except:
                            if ss[1] not in X.symbols: X.symbols.append(ss[1])

                    elif 'uniprotkb' in s[n] and 'gene name synonym' in s[n]:
                        try: 
                            if sss[0] not in X.names: X.names.append(sss[0])
                        except:
                            if ss[1] not in X.names: X.names.append(ss[1])

                    elif 'uniprotkb' in s[n] and 'orf name' in s[n]:
                        try: 
                            if not X.ensembl_gene: X.ensembl_gene = sss[0]
                        except:
                            #raise "Error"
                            print s[n], ss[1], 
                            #if ss[1] not in X.ensembl_gene: X.ensembl_gene.append(ss[1])
                            
                            
                    elif "uniprotkb" in s[n] and "_" not in s[n]:
                        #if X.uniprotkb_ac: print "uniprotkb_ac should be list"
                        try: 
                            if sss[0] not in X.uniprotkb_ac: X.uniprotkb_ac.append(sss[0])
                        except:
                            if ss[1] not in X.uniprotkb_ac: X.uniprotkb_ac.append(ss[1])
                            

                    
                    elif "uniprotkb" in s[n] or "uniprot:" in s[n]:   #uniprotkb can be like P38276 or YBY7_YEAST in iRefIndex
                        #if X.uniprotkb_ac and ss[1] != X.uniprotkb_ac: print "uniprotkb_ac should be list", X.uniprotkb_ac, ss[1], field[pos].split('|')[n]
                        if ss[1] not in X.uniprotkb_ac:
                            X.uniprotkb_ac.append(ss[1])
                            
                    elif "uniprotkb" in s[n] and ("_" or "gene name" or "locus name" or "gene name synonym" or "orf name") not in s[n]:
                        if X.uniprotkb_gn: print "uniprotkb_gn", X.uniprotkb_gn, sss[0], field[pos].split('|')[n]
                        X.uniprotkb_gn = sss[0]

                    elif "Swiss-Prot:" in s[n]:
                        if ss[1] not in X.uniprotkb_ac: X.uniprotkb_ac.append(ss[1])
                        
                    elif "TREMBL:" in s[n]:
                        if X.trembl: print "trembl", X.trembl, ss[1]
                        X.trembl == ss[1]
                    elif "UniProtKB/TrEMBL:" in s[n]:       #trange    uniprotkb_trembl: O45054 -1
                        if X.uniprotkb_trembl: print"uniprotkb_trembl:", X.uniprotkb_trembl, ss[1]
                        X.uniprotkb_trembl = ss[1]
                        
                    #elif "refseq" in s[n]: X.refseq = ss[1] 
                    elif "refseq" in s[n] or "RefSeq" in s[n]:
                        #if X.refseq: print "refseq", X.refseq, ss[1]
                        try:
                            if sss[0] not in X.refseq: X.refseq.append(sss[0])
                        except:
                            if ss[1] not in X.refseq: X.refseq.append(ss[1])

                    elif "gb:" in s[n] or "GB:" in s[n]:
                        try:
                            int(sss[0])
                            if X.genbank_nucl_gi: print "GB genbank_nucl_gi sss[0]", X.genbank_nucl_gi, sss[0]
                            X.genbank_nucl_gi = int(sss[0])
                        except:
                            try:
                                #if X.genbank_protein_gi: print "GB genbank_protein_gi sss[0]", X.genbank_protein_gi, sss[0]
                                if sss[0] not in X.genbank_protein_gi: X.genbank_protein_gi.append(sss[0])                      #List in iRefIndex
                            except:
                                try:
                                    int(ss[1])
                                    if X.genbank_nucl_gi: print "GB genbank_nucl_gi ss[1]", X.genbank_nucl_gi, ss[1]
                                    X.genbank_nucl_gi = int(ss[1])
                                except:
                                    #if X.genbank_protein_gi: print "GB genbank_protein_gi ss[1]", X.genbank_protein_gi, ss[1]
                                    if ss[1] not in X.genbank_protein_gi: X.genbank_protein_gi.append(ss[1])                      #List in iRefIndex
                                    
                    elif "genbank_nucl_gi" in s[n]:
                        if X.genbank_nucl_gi: print "genbank_nucl_gi", X.genbank_nucl_gi, ss[1]
                        X.genbank_nucl_gi = ss[1]
                        
                    elif "genbank_protein_gi" in s[n]:
                        #if X.genbank_protein_gi: print "genbank_protein_gi", X.genbank_protein_gi, ss[1]
                        #X.genbank_protein_gi = ss[1]
                        if ss[1] not in X.genbank_protein_gi: X.genbank_protein_gi.append(ss[1])
                        
                    elif "entrez gene/locuslink" in s[n] or "entrezgene/locuslink" in s[n]:
                        try:
                            int(sss[0])
                            if X.id:
                                #print "entrez gene/locuslink", X.id, sss[0]
                                if sss[0] not in X.alias: X.alias.append(sss[0])
                            X.id = int(sss[0])
                        except:
                            try:
                                sss[0]
                                if X.symbol:
                                    #print "entrez gene/locuslink", X.symbol, ss[1]
                                    if sss[0] not in X.alias: X.alias.append(sss[0])
                                X.symbol = sss[0]
                            except:
                                try:
                                    int(ss[1])
                                    if X.id:
                                        #print "entrez gene/locuslink", X.id, ss[1]
                                        if ss[1] not in X.alias: X.alias.append(ss[1])
                                    X.id = int(ss[1])
                                except:
                                    if X.symbol:
                                        #print "entrez gene/locuslink", X.symbol, ss[1]
                                        if ss[1] not in X.alias: X.alias.append(ss[1])
                                    X.symbol = ss[1]
                        
                    elif "entrez gene/locuslink" in s[n]:
                        ss = s[n].split('k:')
                        #if 'locuslink:"'  in splitAltIDInteractorA[n]and 'locuslink:""' not in splitAltIDInteractorA[n]:
                            #print splitAltIDInteractorA[n]
                        if 'locuslink:"' in s[n]: # and 'locuslink:""' not in splitAltIDInteractorA[n]:
                            sss = ss[1].split('"')
                            print sss[2]
                            X.symbol.append(sss[2])  #wrong
                        else:
                            sss = ss[1].split('(')
                            print sss[0]
                            X.symbol.append(sss[0])     #wrong
                    elif "cygd" in s[n]:
                        #if X.cygd: print "X.cygd:", X.cygd
                        #X.cygd = ss[1]
                        if ss[1] not in X.cygd: X.cygd.append(ss[1])    #List in iRefIndex
                    elif "wormbase" in s[n]:
                        if X.wormbase: print "wormbase", X.wormbase, ss[1]
                        X.wormbase = ss[1]
                    elif "flybase" in s[n] or "FlyBase" in s[n]:
                        if X.flybase: print "flybase", X.flybase, ss[1] 
                        X.flybase = ss[1]
                    elif "ensembl" in s[n] or "Ensembl" in s[n]:
                        if X.ensembl: "ensembl", X.ensembl, ss[1]
                        X.ensembl = ss[1]
                    elif "dbj/embl/genbank" in s[n] or "dbj:" in s[n]:
                        #if X.dbj_embl_genbank: print "dbj_embl_genbank", X.dbj_embl_genbank, ss[1]
                        #X.dbj_embl_genbank = ss[1]
                        if ss[1] not in X.dbj_embl_genbank: X.dbj_embl_genbank.append(ss[1])
                    elif "uniparc" in s[n]:
                        if X.uniparc: print "uniparc", X.uniparc, ss[1]
                        X.uniparc = ss[1]
                    elif "interpro" in s[n]:
                        if X.interpro: print "interpro", X.interpro, ss[1]
                        X.interpro = ss[1]

                    elif "chebi" in s[n]:
                        if X.chebi: "chebi", X.chebi, ss[1]
                        X.chebi = ss[1]
                    elif "pubchem" in s[n]:
                        if X.pubchem: print "pubchem", X.pubchem, ss[1]
                        X.pubchem = zz[1]
                    elif "ipi:" in s[n]:
                        if X.ipi: print "ipi", X.ipi, ss[1]
                        X.ipi = ss[1]
                    elif "rgd:" in s[n]:
                        if X.rgd: print "rgd", X.rgd, ss[1]
                        X.rgd = s[1]
                    elif "newt:" in s[n]:
                        if X.newt: print "newt", X.newt, ss[1]
                        X.newt = ss[1]
                    elif "sgd:" in s[n]:
                        if X.sgd: print "sgd", X.sgd, ss[1]
                        X.sgd = ss[1]
                    elif "intact" in s[n]: X.intact.append(ss[1])  #print "intact should be list, because of three exception"
                    elif "DIP-" in s[n]:
                        if X.dip: print "dip", X.dip, ss[1]
                        X.dip = s[n]
                        if X.dip in Dic:
                            for item in Dic[X.dip]: X.alias(item)
                    elif "GRID" in s[n]:
                        if X.grid: print "grid", X.grid, ss[1]
                        X.grid = ss[1]
                    elif "mint:" in s[n]:
                        #if X.mint: print "mint", X.mint, ss[1]
                        #X.mint = ss[1]
                        if ss[1] not in X.mint: X.mint.append(ss[1])    #List in iRefIndex
                    elif "HPRD:" in s[n]:
                        if X.hprd: print "hprd", X.hprd, ss[1]
                        X.hprd = ss[1]
                    elif "irefindex" in s[n]:
                        if "irefindex": print "irefindex", X.irefindex, sss[0]
                        X.irefindex = sss[0]
                    #elif "irefindex:" in s[n]: irefindexComplex += 1    #What the hell is this?                        
                    elif 'xx:' in s[n]:
                        if X.Id: print "Id", X.Id, ss[1]
                        X.Id = ss[1]
                    elif "(isoform synonym)" in s[n]:
                        if X.isoform_synonym: print "isoform_synonym", X.isoform_synonym, sss[0]
                        X.isoform_synonym = sss[0]
                    elif "(shortlabel)" in s[n]:
                        #if X.short_label: print "short_label", X.short_label, sss[0]
                        X.short_label.append(sss[0])
                        print "short_label is used"
                        if len(X.short_label) > 1: print "short_label should be list"                        
                    elif "(gene name synonym)" in s[n]:
                        X.name_synonym.append(sss[0])
                        print "name_synonym is used"
                        if len(X.name_synonym) > 1: print "name_synonym should be list"                        
                    elif "(locus name)" in s[n]:
                        X.locus_name.append(sss[0])
                        print "locus name is used"                        
                        if len(X.locus_name) > 1: print "locus_name should be list"                           
                    elif "(orf name)" in s[n]:
                        X.orf_name.append(sss[0])
                        print "orf_name is used" 
                        if len(X.orf_name) > 1: print "orf_name should be list"  
                    elif "(gene name)" in s[n]:
                        if X.name: print "name", X.name, sss[0]
                        X.name = sss[0]
                    elif "emb:" in s[n]:                        #print "emb should be list"
                        try:
                            X.emb.append(sss[0])
                            print "emb try is used"
                        except: X.emb.append(ss[1]) #print "emb except is used in iRefIndex"
                        
                    elif "PDB:" in s[n]:
                        try:
                            X.pdb.append(sss[0])    #"pdb should be list" 
                            print "try: pdb should be there"     
                        except: X.pdb.append(ss[1])    #"pdb should be list and is used in iRefIndex" 
                    elif "prf:" in s[n]:
                        #if X.prf: print "prf", X.prf, ss[1]
                        #X.prf = ss[1]
                        if ss[1] not in X.prf: X.prf.append(ss[1])

                    elif "KEGG:" in s[n]:       #strange kegg sce:YNL335W sce:YFL061W   kegg sce:YNL335W sce:YFL061W    kegg hsa:440733 hsa:650283
                        if X.kegg:
                            print "kegg", X.kegg, ss[1] + ':' + ss[2]
                            if ss[2] not in X.alias: X.alias.append(ss[2])
                        else:
                            X.kegg = ss[2]#ss[1] + ':' + ss[2]

                    elif "pir:" in s[n] or "PIR:" in s[n]:
                        if X.pir: print "pir", X.pir, ss[1]
                        X.pir = ss[1]

                    elif "afcs:" in s[n]:
                        if X.afcs: print "afcs", X.afcs, ss[1]
                        X.afcs = ss[1]
                    elif "tpg:" in s[n]:
                        if X.tpg: print "tpg", X.tpg, ss[1]
                        X.tpg = ss[1]
                    elif "TIGR:" in s[n]:
                        #if X.tigr: print "tigr", X.tigr, ss[1]
                        #X.tigr = ss[1]
                        if ss[1] not in X.tigr: X.tigr.append(ss[1])    #List in iRefIndex
                    elif "pubmed:" in s[n]:
                        if X.pmids: print "pmids", X.pmids, ss[1]
                        X.pmids = ss[1]
                    elif "other:" in s[n]:
                        if X.other: print "other", X.other, ss[1]
                        X.other = ss[1]
                    elif "icrogid:" in s[n]:
                        if X.icrogid: print "icrogid", X.icrogid, ss[1]
                        X.icrogid = ss[1]
                    elif "crogid:" in s[n]:
                        if X.crogid: print "crogid", X.crogid, ss[1]
                        X.crogid = ss[1]
                    elif "irogid:" in s[n]:
                        if X.irogid: print "irogid", X.irogid, ss[1]
                        X.irogid = ss[1]
                    elif "rogid:" in s[n]:
                        if X.rogid and ss[1] != X.rogid: print "rogid", X.rogid, ss[1]  #Multiple assignments in iRefIndex
                        X.rogid = ss[1]
                    elif "complex:" in s[n]:
                        if X.complex: print "complex", X.complex, ss[1]
                        X.complex == ss[1]

                    elif "camjedb:" in s[n]:
                        if X.camjedb: print "camjedb", X.camjedb, ss[1]
                        X.camjedb = ss[1] 
                    elif "-" == s[n]: pass
                    else:
                        unsortedIDInteractor.append(s)
                        print "symbol/name/id missed! ", field[pos]
                    n += 1

        m = field[6]
        if m != "-":
            sm = m.split('|')
            x = len(sm)
            n = 0
            while n != x:
                if sm[n] != "-":
                    ssm = sm[n].split('(')
                    sssm = ssm[1].split(')')
                    if sssm[0] != "-" and sssm[0] not in self.method:
                        self.method.append(sssm[0])
##                        if sssm[0] not in InteractionDetectionMethodList:
##                            InteractionDetectionMethodList[sssm[0]] = FileName
##                            print sssm[0]
                        if sssm[0] in physicalInteractionDetectionMethods:
                            if "direct" not in self.system: self.system.append("direct")
                            if "physical" not in self.system: self.system.append("physical")
                        elif sssm[0] in geneticInteractionDetectionMethods:
                            if "direct" not in self.system: self.system.append("direct")
                            if "genetic" not in self.system: self.system.append("genetic")
                        else:
                            InteractionDetectionMethodList[sssm[0]] = interaction
                        if sssm[0] in PTMs:
                            if PTMs[sssm[0]] not in self.modification: self.modification.append(PTMs[sssm[0]])
                n += 1
                
        pmid = field[8]
        if pmid != "-":
            spmid = pmid.split('|')
            x = len(spmid)
            n = 0
            while n != x:
                if spmid[n] != "-":
                    sspmid = spmid[n].split(':')
                    if sspmid[1] not in self.pmid and sspmid[1] != "-": #Here was initial not this command, but this lead in combination without the command below to redundancy in Entry. I don't know if it worse to keep the InteractionType sorted to PMID in the cost of redundancy.
                        self.pmid.append(sspmid[1])
                n += 1
        else:
            self.pmid.append("")

        if self.db != "PINA":
            type = field[11]
            if type != "" and type != "-":
                stype = type.split('(')
                sstype = stype[1].split(')')
                if sstype[0] != "-" and sstype[0] not in self.type: #Here was initial not the command " and splitsplitINTERACTIONTYPE[0] not in InteractionType", but this lead to redundancy in Entry
                    self.type.append(sstype[0])
                    if sstype[0] not in self.type:
                        InteractionTypeList[sstype[0]] = FileName
                if sstype[0] in physicalInteractionTypes:
                    if "physical" not in self.system:
                        self.system.append("physical")
                        #print  splitsplitINTERACTIONTYPE[0]
                    if sstype[0] in  PTMs and PTMs[sstype[0]] not in self.modification:
                        self.modification.append(PTMs[sstype[0]])
                        #print Modification
                if sstype[0] in geneticInteractionTypes:
                    if "genetic" not in self.system:
                        self.system.append("genetic")

        if self.db == ['iRefIndex']:
            #print "searching source db"
            db = field[12]
            sdb = db.split('|')
            x = len(sdb)
            n = 0
            while n != x:
                if sdb[n] != "-":
                    ssdb = sdb[n].split('(')
                    sssdb = ssdb[1].split(')')
                    if sssdb[0] not in self.db and sssdb[0] != "irefindex":
                        if sssdb[0] == "mint":
                            sssdb[0] = "MINT"
                            if "direct" not in self.system: self.system.append("direct")                            
                            if "physcial" not in self.system: self.system.append("physical")                        
                        elif sssdb[0] == "grid":
                            sssdb[0] = "BioGRID"
                            if "direct" not in self.system: self.system.append("direct")
                        elif sssdb[0] == "bind":
                            sssdb[0] = "BIND"
                            if "direct" not in self.system: self.system.append("direct")
                            if "physcial" not in self.system: self.system.append("physical")  
                        elif sssdb[0] == "intact":
                            sssdb[0] = "IntAct"
                            if "direct" not in self.system: self.system.append("direct")                            
                            if "physcial" not in self.system: self.system.append("physical")  
                        elif sssdb[0] == "dip":
                            sssdb[0] = "DIP"
                            if "direct" not in self.system: self.system.append("direct")
                            if "physcial" not in self.system: self.system.append("physical")                              
                        elif sssdb[0] == "BIND_Translation":
                            sssdb[0] = "BIND"
                            if "direct" not in self.system: self.system.append("direct")                            
                            if "physcial" not in self.system: self.system.append("physical")  
                        elif sssdb[0] == "ophid":
                            sssdb[0] = "OPHID" #Mine!
                            if "predicted" not in self.system: self.system.append("predicted")
                            if "physcial" not in self.system: self.system.append("physical")  
                        elif sssdb[0] == "CORUM":
                            if "direct" not in self.system: self.system.append("direct")                            
                            if "physcial" not in self.system: self.system.append("physical")  
                        elif sssdb[0] == "MPACT":
                            if "direct" not in self.system: self.system.append("direct")                            
                            if "physcial" not in self.system: self.system.append("physical")  
                        elif sssdb[0] == "HPRD":
                            if "direct" not in self.system: self.system.append("direct")
                            if "physcial" not in self.system: self.system.append("physical")                              
                        elif sssdb[0] == "mpiimex": pass #Mine!
                        elif sssdb[0] == "InnateDB": pass #Mine!
                        elif sssdb[0] == "mpilit": pass #Mine!
                        elif sssdb[0] == "MPPI":    #Mine!
                            if "direct" not in self.system: self.system.append("direct")
                            if "physcial" not in self.system: self.system.append("physical")  
                        elif sssdb[0] == "MatrixDB":    #Mine!
                            if "direct" not in self.system: self.system.append("direct")                         
                            if "physcial" not in self.system: self.system.append("physical")  
                        else: print "Database not reqconized", sssdb[0]    #Utilize a controlled vacubulary for database names
                        self.db.append(sssdb[0])
                n += 1

        # In order to presever memory gene instances will be unpacked to sets of aliases:
        #for i in [self.a, self.b]
        a = tuple(self.a.sni())
        if not a:
            print self.a
        self.a = a
        b = tuple(self.b.sni())
        if not b:
            print self.b
        self.b = b



##        print "Collecting Genes and Interactions in Lists...",
##        Data = file(FileName).read().split('\n')
##        print "Loaded File..",
##        for Interaction in Data:
##            if Database == "MPACT" or Database == "BIND" and FileName != './BIND/BIND10090.txt':
##                split = Interaction.split('|')
##            elif Database == "CORUM":
##                split = Interaction.split(';')
##            else:
##                split = Interaction.split('\t')
##            if "ID interactor A" not in Interaction and "#ID(s) interactor A" not in Interaction and "#ID Interactor A" not in Interaction and "unique id A" not in Interaction and "FBGN_GENE1_BD" not in Interaction and "FLY_GENE1" not in Interaction and "BioGRID Interaction ID" not in Interaction and "#uidA" not in Interaction and "CST catalog number" not in Interaction and "Dataset" not in Interaction and len(split) > 1 and split[0] != "A" and split[0] != "pmid1" and "unique interactions" not in Interaction and "PDZ name" not in Interaction and split[0] != "Complex id" and split[0] != '"ID(s) interactor A"' and split[0] != "ID(s) interactor A" and split[0] != "pmid": #or (Database == "PhosphoGRID" and  (len(split) > 1) and (split[0] != "A") and ((split[9] or split[10]) or (split[13] or split[14])) != "-")     
##                #print Interaction

#InteractionTypes: 90
physicalInteractionTypes = [
'direct interaction',
'physical association',
'association',
'colocalization',
'gtpase reaction',
'phosphorylation reaction',
'protein cleavage',
'methylation reaction',
'enzymatic reaction',
'acetylation reaction',
'physical interaction',
'adp ribosylation reaction',
'cleavage reaction',
'ubiquitination reaction',
'dephosphorylation reaction',
'covalent binding',
'palmitoylation reaction',
'dna strand elongation',
'neddylation reaction',
'disulfide bond',
'sumoylation reaction',
'demethylation reaction',
'phosphotransfer reaction',
'atpase reaction',
'deacetylation reaction',
'rna cleavage',
'deubiquitination reaction',
'genetic interaction defined by inequality',
'nucleic acid cleavage',
'amidation reaction',
'glycosylation reaction',
'hydroxylation reaction',
'deneddylation reaction',
'deformylation reaction',
'aggregation',
'phosphorylation',
'methylation',
'acetylation',
'ubiquitination',
'dephosphorylation',
'cleavage',
'neddylation',
'deacetylation',
'amidation',
'sumoylation',
'demethylation',
'elongation',
'adp ribosylation',
'palmitoylation',
'glycosylation',
'deneddylation',
'deubiquitination',
'acts_on',
'bidirectional',
'Two-hybrid',
'Affinity Capture-Western',
'Affinity Capture-MS',
'Reconstituted Complex',
'Co-localization',
'Co-purification',
'Co-fractionation',
'Protein-peptide',
'complex',
'indirect_complex',
'reaction',
'FRET',
'Biochemical Activity',
'Far Western',
'Affinity Capture-RNA',
'Co-crystal Structure',
'Protein-RNA',
'in vivo',
'in vitro',
'targetsChip',
'targetsCore',
'oxidoreductase activity electron transfer assay',
'phosphotransfer',
'redox reaction',
'hydroxylation',
'post-translational modification']

geneticInteractionTypes = [
'suppressive genetic interaction defined by inequality',
'additive genetic interaction defined by inequality',
'synthetic genetic interaction defined by inequality',
'genetic interference',
'ECrel',
'Synthetic Lethality',
'Dosage Rescue',
'Phenotypic Enhancement',
'Dosage Lethality',
'Phenotypic Suppression', 
'Synthetic Growth Defect',
'Synthetic Rescue', 
'neighbouring_reaction',
'Dosage Growth Defect',
'GErel',
'suppressive interaction',
'synthetic interaction',
'additive interaction',
'genetic inequality']
#InteractionDetectionMethods: 312
physicalInteractionDetectionMethods = [
'two hybrid',
'affinity chromatography technology',
'pull down',
'enzymatic study',
'x-ray crystallography',
'far western blotting',
'fluorescent resonance energy transfer',
'imaging technique',
'protein complementation assay',
'biochemical',
'anti tag coimmunoprecipitation',
'tandem affinity purification',
'bimolecular fluorescence complementation',
'confocal microscopy',
'coimmunoprecipitation',
'anti bait coimmunoprecipitation',
'dihydrofolate reductase reconstruction',
'gtpase assay',
'two hybrid pooling approach',
'surface plasmon resonance',
'enzyme linked immunosorbent assay',
'two hybrid fragment pooling approach',
'two hybrid array',
'ion exchange chromatography',
'adenylate cyclase complementation',
'affinity technology',
'filter binding',
'cross-linking study',
'chromatography technology',
'molecular sieving',
'fluorescence microscopy',
'cosedimentation through density gradient',
'beta galactosidase complementation',
'protein cross-linking with a bifunctional reagent',
'experimental interaction detection',
'peptide array',
'protease assay', 'inferred by author',
'fluorescence polarization spectroscopy',
'circular dichroism',
'electron microscopy',
'electrophoretic mobility shift assay',
'protein array',
'cosedimentation',
'nuclear magnetic resonance',
'methyltransferase radiometric assay',
'fluorescence-activated cell sorting',
'isothermal titration calorimetry',
'yeast display',
'in-gel kinase assay',
'protein kinase assay',
'phage display',
'classical fluorescence spectroscopy',
'immunodepleted coimmunoprecipitation',
'polymerization',
'biophysical',
'transcriptional complementation assay',
'fluorescence correlation spectroscopy',
'electrophoretic mobility supershift assay',
'phosphatase assay',
'mass spectrometry studies of complexes',
'saturation binding',
'scintillation proximity assay',
'ubiquitin reconstruction',
'comigration in non denaturing gel electrophoresis',
'3 hybrid method',
'chromatin immunoprecipitation assay',
'footprinting', 'one hybrid',
'methyltransferase assay',
'blue native page',
'cosedimentation in solution',
'fluorescence technology',
'mammalian protein protein interaction trap',
'kinase homogeneous time resolved fluorescence',
'rna directed rna polymerase assay',
'bioluminescence resonance energy transfer',
'homogeneous time resolved fluorescence',
'competition binding',
'lex-a dimerization assay',
'x ray scattering',
'dynamic light scattering',
'tox-r dimerization assay',
'lambda phage display',
'deacetylase assay',
'systematic evolution of ligands by exponential enrichment',
'green fluorescence protein complementation assay',
'protein tri hybrid',
't7 phage display',
'light scattering',
'gal4 vp16 complementation',
'electron tomography',
'antibody array',
'demethylase assay',
'static light scattering',
'reverse phase chromatography',
'array technology',
'dna directed dna polymerase assay',
'comigration in sds page',
'solid phase assay',
'atpase assay',
'reverse two hybrid',
'comigration in gel electrophoresis',
'ribonuclease assay',
'phosphotransfer assay',
'enzymatic footprinting',
'light microscopy',
'reverse ras recruitment system',
'DNase I footprinting',
'luminescence based mammalian interactome mapping',
'acetylation assay',
'lambda repressor two hybrid',
'nucleic acid uv cross-linking assay',
'interaction detection method',
'chromatin immunoprecipitation array',
'surface plasmon resonance array',
'experimental knowledge based',
'colocalization by immunostaining',
'gst pull down',
'copurification',
'colocalization/visualisation technologies',
'tap tag coimmunoprecipitation',
'beta lactamase complementation',
'colocalization by fluorescent probes cloning',
'his pull down',
'filamentous phage display',
'cytoplasmic complementation assay',
'atomic force microscopy',
'membrane bound complementation assay',
'protease accessibility laddering',
'neutron diffraction',
'electron paramagnetic resonance',
'transmission electron microscopy',
'x-ray fiber diffraction',
'gdp/gtp exchange assay',
'intermolecular force',
'mass spectrometry study of hydrogen/deuterium exchange',
'2 hybrid',
'coip',
'experimental interac',
'density sedimentation',
'elisa',
'crosslink',
'fret',
'emsa',
'x-ray diffraction',
'spr',
'detection by mass spectrometry',
'fps',
'in vivo',
'yeast 2-hybrid',
'in vitro',
' in vivo',
'invitro',
'reconstituted complex',
'affinity capture-western',
'chromatography techniques',
'anti bait coip',
'anti tag coip',
'glutathione S-tranferase pull down',
'co-fractionation',
'imaging techniques',
'fluorescence imaging',
'co-purification',
'Library Array',
'fluorescence techniques',
'affinity capture-ms',
'affinity chromatography',
'solution sedimentation',
'enzymatic studies',
'cross-linking studies',
'in gel kinase assay',
'affinity techniques',
'dhfr reconstruction',
'two-hybrid-test',
'2h fragment pooling',
'two hybrid pooling',
'tap',
'three-dimensional-structure',
'solution sedimentati',
'fluorescence',
'affinity-chromatography',
'coip_ coimmunoprecipitation',
'immunoprecipitation',
'ub reconstruction',
'tap tag coip',
'nmr',
'fluorescence spectr',
'affinity chrom',
'coloc fluoresc probe',
'chromatography',
'sucrose-gradient-sedimentation',
'bn-page',
'ms of complexes',
'x-ray',
'colocalization by im',
'immunostaining',
'elisa_ enzyme-linked immunosorbent assay',
'cross-linking',
'far-western',
'surface-plasmon-resonance-chip',
'competition-binding',
'resonance-energy-transfer',
'itc',
'ion exchange chrom',
'gel-retardation-assays',
'bifc',
'radiolabeled methyl',
'gel-filtration-chromatography',
'density sedimentatio',
'colocalization',
'beta galactosidase',
'comig non denat gel',
'protein crosslink',
'colocalization-visua',
'gfp complementation',
'beta lactamase',
't7 phage',
'electron-microscopy',
'phage-display',
'complementation',
'adenylate cyclase',
'reverse phase chrom',
'bret',
'gallex',
'cd',
'filamentous phage',
'methyltransferase as',
'gal4 vp16 complement',
'electron resonance',
'mappit',
'fluorescence-anisotropy',
'facs',
'immunoblotting',
'dls',
'transcription compl',
'lambda phage',
'transient-coexpression',
'kinase spa',
'comigration in gel',
'epr',
'sem',
'mass-spectrometry',
'comigration in sds',
'enzymatic footprint',
'tem',
'monoclonal-antibody-blockade',
'fcs',
'spa',
'htrf',
'saxs',
'sls',
'autoradiography',
'toxcat',
'light-scattering',
'kinase htrf',
'phosphotransfer assa',
'reverse rrs',
'atomic force microsc',
'hybridization',
'interaction-adhesion-assay',
'immunodepletion',
'emsa supershift',
'lumier',
'affinity chromatography technologies',
'cosedimentation through density gradients',
'chromatography technologies',
'fluorescence technologies',
'chromatin immunoprecipitation assays',
' scintillation proximity assay',
'enzyme-linked immunosorbent assay',
'affinMI:0030',
'proteinchip(r) on a surface-enhanced laser desorption/ionization',
'Two-hybrid',
'Affinity Capture-Western',
'Affinity Capture-MS',
'Reconstituted Complex',
'Co-localization',
'Co-purification',
'Co-fractionation',
'FRET',
'Far Western',
'Affinity Capture-RNA',
'Co-crystal Structure',
'targetsChip',
'targetsCore',
'display technology',
'proximity enzyme linked immunosorbent assay',
'p3 filamentous phage display',
'bead aggregation assay',
'electron diffraction',
'small angle neutron scattering',
'coloc by immunost',
'cytoplasmic compl',
'Gal4 proteome-wide y2h',
'LexA yeast two-hybrid system',
'targetsCore',
'two-hybrid',
'co-localization',
'biochemical activity',
'colocalization technologies',
'co-crystal structure',
'invivo',
'western blotting',
'transcription assay',
'gel retardation assay',
'in vitro binding',
'interaction adhesion assay',
'alanine scanning',
'filter overlay assay',
'knowledge based',
'experimental',
'ch-ip',
'immunofluorescence',
'protein complex',
'surface plasmo resonance',
'Interologs mapping',
'protein-peptide',
'experimental detection',
'yeast two-hybrid',
'far western',
'Literature curated yeast protein physical interactions',
'Protein complexes from affinity purification/mass spectrometry (multiple datasets)',
'Literature curated yeast protein interactions',
'amplified luminescent proximity homogeneous assay',
'kinase scintillation proximity assay',
'Protein interactions inferred from tertiary structures of complexes',
'Fly protein physical interactions',
'Literature curated human protein physical interactions',
'coip  coimmunoprecipitation',
'structure based prediction',
'predict from struct',
'Yeast protein complexes from affinity purification/mass spectrometry',
'2H',
'OPHID Predicted Protein Interaction',
'High-throughput yeast 2-hybrid assays (multiple datasets)',
'lambda two hybrid',
'Yeast protein interactions inferred from tertiary structures of complexes',
'interactome parallel affinity capture',
'High-throughput yeast 2-hybrid assays among human genes',
'High-throughput yeast 2-hybrid assays among worm genes',
'Literature curated worm protein physical interactions',
'elisa  enzyme-linked immunosorbent assay',
'Y2H',
'human protein complexes from affinity purification/mass spectrometry'
]

geneticInteractionDetectionMethods = [
'genetic interference',
'ECrel',
'Synthetic Lethality',
'Dosage Rescue',
'Phenotypic Enhancement',
'Dosage Lethality',
'Phenotypic Suppression',
'Synthetic Growth Defect',
'Synthetic Rescue',
'neighbouring_reaction',
'Dosage Growth Defect',
'GErel',
'phenotypic suppression',
'phenotypic enhancement',
'genetic',
'Worm genetic interactions',
'Yeast genetic interactions',
'Yeast genetic interactions (multiple datasets)'
]

otherInteractionDetectionMethods = [
'unspecified method',
'inferred by author',
'inferred by curator',
'experimental knowledge based',
'interaction prediction',
'not-specified',
'NA',
'None',
'other',
'',
'interologs mapping',
'confirmational text mining',
'predicted interac',
'experimental info',
'predictive text mining',
'text mining',
'prediction',
'not specified']

PTMs = {
'phosphorylation':'Phosphorylation', 
'phosphorylation reaction':'Phosphorylation',
'protein kinase assay': 'Phosphorylation',
'kinase homogeneous time resolved fluorescence':'Phosphorylation',
'kinase spa':'Phosphorylation',
'kinase htrf':'Phosphorylation',
'in gel kinase assay':'Phosphorylation',
'phosphotransfer assa':'Phosphorylation',
'phosphotransfer assay':'Phosphorylation',
'phosphotransfer reaction':'Phosphorylation',
'dephosphorylation':'Dephosphorylation',
'dephosphorylation reaction':'Dephosphorylation',
'phosphatase assay':'Dephosphorylation',
'acetylation':'Acetylation',
'acetylation assay':'Acetylation',
'acetylation reaction':'Acetylation',
'deacetylation':'Deacetylation',
'deacetylase assay':'Deacetylation',
'methylation reaction':'Methylation',
'methylation':'Methylation', 
'methyltransferase assay':'Methylation',
'methyltransferase radiometric assay':'Methylation',
'methyltransferase as':'Methylation',
'radiolabeled methyl':'Methylation',
'demethylation':'Demethylation',
'demethylase assay':'Demethylation',
'demethylation reaction':'Demethylation',
'ubiquitination':'Ubiquitination',
'ubiquitination reaction':'Ubiquitination',
'deubiquitination':'Deubiquitination',
'deubiquitination reaction':'Deubiquitination',
'sumoylation':'Sumoylation',
'sumoylation reaction':'Sumoylation',
'neddylation':'Neddylation',
'neddylation reaction':'Neddylation',
'deneddylation':'Deneddylation',
'deneddylation reaction':'Deneddylation',
'deformylation reaction':'Deformylation',
'protein cleavage':'Cleavage',
'cleavage':'Cleavage',
'cleavage reaction':'Cleavage',
'protease assay':'Cleavage',
'amidation':'Amidation',
'hydroxylation reaction':'Hydroxylation',
'adp ribosylation':'Adp ribosoylation',
'adp ribosylation reaction':'Adp ribosylation',
'covalent binding':'Covalent binding',
'palmitoylation':'Palmitoylation',
'palmitoylation reaction':'Palmitoylation',
'glycosylation':'Glycosylation',
'disulfide bond':'Disulfide bond',
}


#InteractionTypes: 90
physicalInteractionTypes = [
'direct interaction',
'physical association',
'association',
'colocalization',
'gtpase reaction',
'phosphorylation reaction',
'protein cleavage',
'methylation reaction',
'enzymatic reaction',
'acetylation reaction',
'physical interaction',
'adp ribosylation reaction',
'cleavage reaction',
'ubiquitination reaction',
'dephosphorylation reaction',
'covalent binding',
'palmitoylation reaction',
'dna strand elongation',
'neddylation reaction',
'disulfide bond',
'sumoylation reaction',
'demethylation reaction',
'phosphotransfer reaction',
'atpase reaction',
'deacetylation reaction',
'rna cleavage',
'deubiquitination reaction',
'genetic interaction defined by inequality',
'nucleic acid cleavage',
'amidation reaction',
'glycosylation reaction',
'hydroxylation reaction',
'deneddylation reaction',
'deformylation reaction',
'aggregation',
'phosphorylation',
'methylation',
'acetylation',
'ubiquitination',
'dephosphorylation',
'cleavage',
'neddylation',
'deacetylation',
'amidation',
'sumoylation',
'demethylation',
'elongation',
'adp ribosylation',
'palmitoylation',
'glycosylation',
'deneddylation',
'deubiquitination',
'acts_on',
'bidirectional',
'Two-hybrid',
'Affinity Capture-Western',
'Affinity Capture-MS',
'Reconstituted Complex',
'Co-localization',
'Co-purification',
'Co-fractionation',
'Protein-peptide',
'complex',
'indirect_complex',
'reaction',
'FRET',
'Biochemical Activity',
'Far Western',
'Affinity Capture-RNA',
'Co-crystal Structure',
'Protein-RNA',
'in vivo',
'in vitro',
'targetsChip',
'targetsCore',
'oxidoreductase activity electron transfer assay',
'phosphotransfer',
'redox reaction',
'hydroxylation',
'post-translational modification']

geneticInteractionTypes = [
'suppressive genetic interaction defined by inequality',
'additive genetic interaction defined by inequality',
'synthetic genetic interaction defined by inequality',
'genetic interference',
'ECrel',
'Synthetic Lethality',
'Dosage Rescue',
'Phenotypic Enhancement',
'Dosage Lethality',
'Phenotypic Suppression', 
'Synthetic Growth Defect',
'Synthetic Rescue', 
'neighbouring_reaction',
'Dosage Growth Defect',
'GErel',
'suppressive interaction',
'synthetic interaction',
'additive interaction',
'genetic inequality']
#InteractionDetectionMethods: 312
physicalInteractionDetectionMethods = [
'two hybrid',
'affinity chromatography technology',
'pull down',
'enzymatic study',
'x-ray crystallography',
'far western blotting',
'fluorescent resonance energy transfer',
'imaging technique',
'protein complementation assay',
'biochemical',
'anti tag coimmunoprecipitation',
'tandem affinity purification',
'bimolecular fluorescence complementation',
'confocal microscopy',
'coimmunoprecipitation',
'anti bait coimmunoprecipitation',
'dihydrofolate reductase reconstruction',
'gtpase assay',
'two hybrid pooling approach',
'surface plasmon resonance',
'enzyme linked immunosorbent assay',
'two hybrid fragment pooling approach',
'two hybrid array',
'ion exchange chromatography',
'adenylate cyclase complementation',
'affinity technology',
'filter binding',
'cross-linking study',
'chromatography technology',
'molecular sieving',
'fluorescence microscopy',
'cosedimentation through density gradient',
'beta galactosidase complementation',
'protein cross-linking with a bifunctional reagent',
'experimental interaction detection',
'peptide array',
'protease assay', 'inferred by author',
'fluorescence polarization spectroscopy',
'circular dichroism',
'electron microscopy',
'electrophoretic mobility shift assay',
'protein array',
'cosedimentation',
'nuclear magnetic resonance',
'methyltransferase radiometric assay',
'fluorescence-activated cell sorting',
'isothermal titration calorimetry',
'yeast display',
'in-gel kinase assay',
'protein kinase assay',
'phage display',
'classical fluorescence spectroscopy',
'immunodepleted coimmunoprecipitation',
'polymerization',
'biophysical',
'transcriptional complementation assay',
'fluorescence correlation spectroscopy',
'electrophoretic mobility supershift assay',
'phosphatase assay',
'mass spectrometry studies of complexes',
'saturation binding',
'scintillation proximity assay',
'ubiquitin reconstruction',
'comigration in non denaturing gel electrophoresis',
'3 hybrid method',
'chromatin immunoprecipitation assay',
'footprinting', 'one hybrid',
'methyltransferase assay',
'blue native page',
'cosedimentation in solution',
'fluorescence technology',
'mammalian protein protein interaction trap',
'kinase homogeneous time resolved fluorescence',
'rna directed rna polymerase assay',
'bioluminescence resonance energy transfer',
'homogeneous time resolved fluorescence',
'competition binding',
'lex-a dimerization assay',
'x ray scattering',
'dynamic light scattering',
'tox-r dimerization assay',
'lambda phage display',
'deacetylase assay',
'systematic evolution of ligands by exponential enrichment',
'green fluorescence protein complementation assay',
'protein tri hybrid',
't7 phage display',
'light scattering',
'gal4 vp16 complementation',
'electron tomography',
'antibody array',
'demethylase assay',
'static light scattering',
'reverse phase chromatography',
'array technology',
'dna directed dna polymerase assay',
'comigration in sds page',
'solid phase assay',
'atpase assay',
'reverse two hybrid',
'comigration in gel electrophoresis',
'ribonuclease assay',
'phosphotransfer assay',
'enzymatic footprinting',
'light microscopy',
'reverse ras recruitment system',
'DNase I footprinting',
'luminescence based mammalian interactome mapping',
'acetylation assay',
'lambda repressor two hybrid',
'nucleic acid uv cross-linking assay',
'interaction detection method',
'chromatin immunoprecipitation array',
'surface plasmon resonance array',
'experimental knowledge based',
'colocalization by immunostaining',
'gst pull down',
'copurification',
'colocalization/visualisation technologies',
'tap tag coimmunoprecipitation',
'beta lactamase complementation',
'colocalization by fluorescent probes cloning',
'his pull down',
'filamentous phage display',
'cytoplasmic complementation assay',
'atomic force microscopy',
'membrane bound complementation assay',
'protease accessibility laddering',
'neutron diffraction',
'electron paramagnetic resonance',
'transmission electron microscopy',
'x-ray fiber diffraction',
'gdp/gtp exchange assay',
'intermolecular force',
'mass spectrometry study of hydrogen/deuterium exchange',
'2 hybrid',
'coip',
'experimental interac',
'density sedimentation',
'elisa',
'crosslink',
'fret',
'emsa',
'x-ray diffraction',
'spr',
'detection by mass spectrometry',
'fps',
'in vivo',
'yeast 2-hybrid',
'in vitro',
' in vivo',
'invitro',
'reconstituted complex',
'affinity capture-western',
'chromatography techniques',
'anti bait coip',
'anti tag coip',
'glutathione S-tranferase pull down',
'co-fractionation',
'imaging techniques',
'fluorescence imaging',
'co-purification',
'Library Array',
'fluorescence techniques',
'affinity capture-ms',
'affinity chromatography',
'solution sedimentation',
'enzymatic studies',
'cross-linking studies',
'in gel kinase assay',
'affinity techniques',
'dhfr reconstruction',
'two-hybrid-test',
'2h fragment pooling',
'two hybrid pooling',
'tap',
'three-dimensional-structure',
'solution sedimentati',
'fluorescence',
'affinity-chromatography',
'coip_ coimmunoprecipitation',
'immunoprecipitation',
'ub reconstruction',
'tap tag coip',
'nmr',
'fluorescence spectr',
'affinity chrom',
'coloc fluoresc probe',
'chromatography',
'sucrose-gradient-sedimentation',
'bn-page',
'ms of complexes',
'x-ray',
'colocalization by im',
'immunostaining',
'elisa_ enzyme-linked immunosorbent assay',
'cross-linking',
'far-western',
'surface-plasmon-resonance-chip',
'competition-binding',
'resonance-energy-transfer',
'itc',
'ion exchange chrom',
'gel-retardation-assays',
'bifc',
'radiolabeled methyl',
'gel-filtration-chromatography',
'density sedimentatio',
'colocalization',
'beta galactosidase',
'comig non denat gel',
'protein crosslink',
'colocalization-visua',
'gfp complementation',
'beta lactamase',
't7 phage',
'electron-microscopy',
'phage-display',
'complementation',
'adenylate cyclase',
'reverse phase chrom',
'bret',
'gallex',
'cd',
'filamentous phage',
'methyltransferase as',
'gal4 vp16 complement',
'electron resonance',
'mappit',
'fluorescence-anisotropy',
'facs',
'immunoblotting',
'dls',
'transcription compl',
'lambda phage',
'transient-coexpression',
'kinase spa',
'comigration in gel',
'epr',
'sem',
'mass-spectrometry',
'comigration in sds',
'enzymatic footprint',
'tem',
'monoclonal-antibody-blockade',
'fcs',
'spa',
'htrf',
'saxs',
'sls',
'autoradiography',
'toxcat',
'light-scattering',
'kinase htrf',
'phosphotransfer assa',
'reverse rrs',
'atomic force microsc',
'hybridization',
'interaction-adhesion-assay',
'immunodepletion',
'emsa supershift',
'lumier',
'affinity chromatography technologies',
'cosedimentation through density gradients',
'chromatography technologies',
'fluorescence technologies',
'chromatin immunoprecipitation assays',
' scintillation proximity assay',
'enzyme-linked immunosorbent assay',
'affinMI:0030',
'proteinchip(r) on a surface-enhanced laser desorption/ionization',
'Two-hybrid',
'Affinity Capture-Western',
'Affinity Capture-MS',
'Reconstituted Complex',
'Co-localization',
'Co-purification',
'Co-fractionation',
'FRET',
'Far Western',
'Affinity Capture-RNA',
'Co-crystal Structure',
'targetsChip',
'targetsCore',
'display technology',
'proximity enzyme linked immunosorbent assay',
'p3 filamentous phage display',
'bead aggregation assay',
'electron diffraction',
'small angle neutron scattering',
'coloc by immunost',
'cytoplasmic compl',
'Gal4 proteome-wide y2h',
'LexA yeast two-hybrid system',
'targetsCore',
'two-hybrid',
'co-localization',
'biochemical activity',
'colocalization technologies',
'co-crystal structure',
'invivo',
'western blotting',
'transcription assay',
'gel retardation assay',
'in vitro binding',
'interaction adhesion assay',
'alanine scanning',
'filter overlay assay',
'knowledge based',
'experimental',
'ch-ip',
'immunofluorescence',
'protein complex',
'surface plasmo resonance',
'Interologs mapping',
'protein-peptide',
'experimental detection',
'yeast two-hybrid',
'far western',
'Literature curated yeast protein physical interactions',
'Protein complexes from affinity purification/mass spectrometry (multiple datasets)',
'Literature curated yeast protein interactions',
'amplified luminescent proximity homogeneous assay',
'kinase scintillation proximity assay',
'Protein interactions inferred from tertiary structures of complexes',
'Fly protein physical interactions',
'Literature curated human protein physical interactions',
'coip  coimmunoprecipitation',
'structure based prediction',
'predict from struct',
'Yeast protein complexes from affinity purification/mass spectrometry',
'2H',
'OPHID Predicted Protein Interaction',
'High-throughput yeast 2-hybrid assays (multiple datasets)',
'lambda two hybrid',
'Yeast protein interactions inferred from tertiary structures of complexes',
'interactome parallel affinity capture',
'High-throughput yeast 2-hybrid assays among human genes',
'High-throughput yeast 2-hybrid assays among worm genes',
'Literature curated worm protein physical interactions',
'elisa  enzyme-linked immunosorbent assay',
'Y2H',
'human protein complexes from affinity purification/mass spectrometry'
]

geneticInteractionDetectionMethods = [
'genetic interference',
'ECrel',
'Synthetic Lethality',
'Dosage Rescue',
'Phenotypic Enhancement',
'Dosage Lethality',
'Phenotypic Suppression',
'Synthetic Growth Defect',
'Synthetic Rescue',
'neighbouring_reaction',
'Dosage Growth Defect',
'GErel',
'phenotypic suppression',
'phenotypic enhancement',
'genetic',
'Worm genetic interactions',
'Yeast genetic interactions',
'Yeast genetic interactions (multiple datasets)'
]

otherInteractionDetectionMethods = [
'unspecified method',
'inferred by author',
'inferred by curator',
'experimental knowledge based',
'interaction prediction',
'not-specified',
'NA',
'None',
'other',
'',
'interologs mapping',
'confirmational text mining',
'predicted interac',
'experimental info',
'predictive text mining',
'text mining',
'prediction',
'not specified']

PTMs = {
'phosphorylation':'Phosphorylation', 
'phosphorylation reaction':'Phosphorylation',
'protein kinase assay': 'Phosphorylation',
'kinase homogeneous time resolved fluorescence':'Phosphorylation',
'kinase spa':'Phosphorylation',
'kinase htrf':'Phosphorylation',
'in gel kinase assay':'Phosphorylation',
'phosphotransfer assa':'Phosphorylation',
'phosphotransfer assay':'Phosphorylation',
'phosphotransfer reaction':'Phosphorylation',
'dephosphorylation':'Dephosphorylation',
'dephosphorylation reaction':'Dephosphorylation',
'phosphatase assay':'Dephosphorylation',
'acetylation':'Acetylation',
'acetylation assay':'Acetylation',
'acetylation reaction':'Acetylation',
'deacetylation':'Deacetylation',
'deacetylase assay':'Deacetylation',
'methylation reaction':'Methylation',
'methylation':'Methylation', 
'methyltransferase assay':'Methylation',
'methyltransferase radiometric assay':'Methylation',
'methyltransferase as':'Methylation',
'radiolabeled methyl':'Methylation',
'demethylation':'Demethylation',
'demethylase assay':'Demethylation',
'demethylation reaction':'Demethylation',
'ubiquitination':'Ubiquitination',
'ubiquitination reaction':'Ubiquitination',
'deubiquitination':'Deubiquitination',
'deubiquitination reaction':'Deubiquitination',
'sumoylation':'Sumoylation',
'sumoylation reaction':'Sumoylation',
'neddylation':'Neddylation',
'neddylation reaction':'Neddylation',
'deneddylation':'Deneddylation',
'deneddylation reaction':'Deneddylation',
'deformylation reaction':'Deformylation',
'protein cleavage':'Cleavage',
'cleavage':'Cleavage',
'cleavage reaction':'Cleavage',
'protease assay':'Cleavage',
'amidation':'Amidation',
'hydroxylation reaction':'Hydroxylation',
'adp ribosylation':'Adp ribosoylation',
'adp ribosylation reaction':'Adp ribosylation',
'covalent binding':'Covalent binding',
'palmitoylation':'Palmitoylation',
'palmitoylation reaction':'Palmitoylation',
'glycosylation':'Glycosylation',
'disulfide bond':'Disulfide bond',
}



##    def __init__(aliasA=[], aliasB=[], system=[], method=[], type=[], taxidA=None, taxidB=None, modification=[], pmid=[], database=[]):
##        self.aliasA = aliasA
##        self.aliasB = aliasB
##        self.system =  system
##        self.method = method
##        self.type = type
##        self.taxidA = taxidA
##        self.taxidB = taxidB
##        self.modification = modification
##        self.pmid = pmid
##        self.db = database
