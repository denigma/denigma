"""A high effective mapping algorithm for gene symbols, names and identifiers.
TODO:
- use dynamic programming to increase performance on large datasets.
  Memorize the mapped aliases as well as individual alias and also incorporate taxid information.
- Prevent too many dereferences, by creating a local variables e.g. for instance ids[taxid][query]
  Use profiling techniques as described in Performance python to measure effectiveness of this change.
- Use better relative platform independent paths (e.g. os.path.join).
- Allow retrieval of a gene instance with all annotations instantly (function `mg` for map gene).
  Create shelve with id, gene instances and key, values.
- Incorporate String, FlyBase and Probe-ids.
- Xref DB related data should be in Denigma.
- Create a django view which can accesses mappings.
- Intelligent mapping with EVA strategy. Use synonyms type consensus sequences, etc.
- Test whether E-Queries can increase coverage
  (e.g. from Bio import Entrez #Entrez.email = ...)."""
import os
import shelve
import marshal
import urllib2
from operator import itemgetter, attrgetter

if os.name == 'posix':
    try:
        import development
        PATH = '/media/SDATA1/annotations'
    except:
        try:
            import annotations
            PATH = annotations.__path__[0]
        except Exception as e:
            print("annotations.mapper: Could not set path. %s" % e)
            #PATH = '/home/daniel/denigma/denigma/apps/annotations'
            PATH = '/home/denigma/denigma/apps/annotations'

    import sys
    sys.path.append('/media/SDATA1')
    sys.path.append('/media/SDATA1/scripts')
elif os.name == 'nt':
    PATH = 'D://annotations'

try:
    from taxonomy import organisms
except:
    organisms = {4932:'Budding yeast',
                 4896: 'Fission yeast',
                 6239:'Nematode',
                 7227:'Fruit fly',
                 10090: 'House mouse',
                 10116: 'Rat',
                 7955: 'Zebra fish',
                 9544: 'Rhesus monkey',
                 9606: 'Human',
                 }
    print("annotations.mapper: Could not load taxonomy.")

try:
    from files import File # For testing purposes
except:
    print("annotations.mapper: Could not load file.")


class Map:
    # Defines databases used for mapping:
    dbs = {'Entrez':'id', 'Ensembl':'ensembl_gene', 'UniProt':'uniprotkb_ac',
           'SGD':'ensembl_gene', 'WormBase':'wormbase', 'FlyBase':'flybase', 'MGI':'mgi', 'HGNC':'hgnc'}
    primary_db = 'Entrez'
    # Establish connections to mapping tables:

    aliasTo = {}
    idToAlias = {}
    idTo = {}
    fromId = {} # 

    for db, id in dbs.items():
        try:
            exec(db+"ToAlias= shelve.open(os.path.join('"+PATH+"', '"+ db+"', 'IdToAlias'))")
            exec("aliasTo['%(db)s'] = {}" % locals())
            exec("fromId['%(db)s'] = {}" % locals())
            for taxid in organisms:
                exec("aliasTo['%(db)s']['%(taxid)s'] = {}" % locals())
                exec("aliasTo['"+db+"']['"+str(taxid)+"'] = shelve.open(os.path.join('"+PATH+"', '"+db+"', 'AliasToId_"+str(taxid)+"'))")
                exec("idToAlias['"+db+"'] = shelve.open(os.path.join('"+PATH+"', '"+db+"', 'idToAlias'))")
            exec("aliasTo['"+db+"']['None'] = shelve.open(os.path.join('"+PATH+"','"+db+"', 'AliasToId'))")
            if db != primary_db:
                exec("idTo['"+db+"'] = shelve.open(os.path.join('"+PATH + "', '" + db + "', 'idTo"+id+"'))")
                exec("fromId['"+db+"'] = shelve.open(os.path.join('"+PATH+ "', '" + db + "', '" + id+"ToId'))")
            else:
                exec("discontinued = open(os.path.join('"+PATH+"', '"+db+"', 'discontinued.mrl'), 'rb')")
                discontinued = marshal.load(discontinued)
        except Exception as e:
            print("annotations.mapper: %s %s %s" % (db, id, e))

    ids = dict(zip(map(str, organisms.keys()),[{} for i in organisms.keys()] ))
    ids.update({'None':{}}) # Mapped ids.
    uncertainUniqueIDs = {} # Unmapped/Uncertain ids.

    @staticmethod
    def it(aliases, taxid=None):
        """Takes either a symbol/name/id or a list of those and maps it
        to a unique primary identifiers as well as all found synonyms."""
        #print("aliases %s & taxid %s" % (aliases, taxid))
        if isinstance(aliases, (int, str)): aliases = [aliases]
        if not aliases: return None

        # Form query and perform dynamic programming:
        taxid = str(taxid)
        ids = Map.ids
        query = ", ".join(map(str, aliases))
        if query in ids[taxid]: # False: Exchange this to enforce not using dynamic programming.
            #print("Used dynamic pogramming.")
            return (ids[taxid][query]['ID'], ids[taxid][query])
        else:
            ids[taxid][query] = {'id':'', 'ID':'', 'synonyms':[]} # MUST BE IN THE FIRST

        # Restrict database selection arcording to species:

        if not taxid: #print "Taxid not given. Query other tables! Not yet implimented!!"
            dbs = {'Entrez':'id', 'Ensembl':'ensembl_gene', 'UniProt':'uniprotid_kb',
                   'SGD':'ensembl_gene', 'WormBase':'wormbase', 'FlyBase':'flybase', 'MGI':'mgi', 'HGNC':'hgnc'}
        if taxid == '4932':
            dbs = {'Entrez':'id', 'Ensembl':'ensembl_gene', 'UniProt':'uniprotkb_ac',
                   'SGD':'sgd'}
        elif taxid == '6239':
            dbs = {'Entrez':'id', 'Ensembl':'ensembl_gene', 'UniProt':'uniprotkb_ac',
                   'WormBase':'wormbase'}
        elif taxid == '7227':
            dbs = {'Entrez':'id', 'Ensembl':'ensembl_gene', 'UniProt':'uniprotkb_ac',
                   'FlyBase':'flybase'}
        elif taxid == '10090': #print("its mouse")
            dbs = {'Entrez':'id', 'Ensembl':'ensembl_gene', 'UniProt':'uniprotkb_ac',
                   'MGI':'mgi'}
        elif taxid == '9606':
            dbs = {'Entrez':'id', 'Ensembl':'ensembl_gene', 'UniProt':'uniprotkb_ac',
                   'HGNC':'hgnc'}
        else: # All other species except common model organisms:
            dbs = {'Entrez':'id', 'Ensembl':'ensembl_gene', 'UniProt':'uniprotkb_ac'} #print("no taxid!")

        # Prepares local look-ups:
        aliasTo = Map.aliasTo
        idTo = Map.idTo
        fromId = Map.fromId
        uncertainUniqueIDs = Map.uncertainUniqueIDs
        primary_db = Map.primary_db
        discontinued = Map.discontinued

        # Resets secondary scoring (consensus of all db mapping tables):
        secondaryScoring = {}
        secondaryScoringList = []
        foundSecondaryUniqueID = False
        uniqueID = ''

        for db, id in dbs.items():
            #print("DB, id:", db, id)

            # Resets scoring:
            ids[taxid][query][id] = ''
            foundUniqueID = False
            scoring = {}
            scoringList = []

            # Get for each alias the id if avaiable:
            for alias in aliases:
                if alias not in ids[taxid][query]['synonyms']:
                    ids[taxid][query]['synonyms'].append(alias)

                alias = alias.lower()
                if alias in aliasTo[db][taxid]:    #Removed "upper" as EntrezAliasList genes are not upper letter.
                    #if printing: print "\n", db, "found", aliasTo[db][taxid][alias]
                    x = len(aliasTo[db][taxid][alias]) #Removed "upper" as EntrezAliasList genes are not upper letter.
                    y = 0
                    while x != y:
                        uniqueID = aliasTo[db][taxid][alias][y]
                        y += 1
                        foundUniqueID = True
                        if uniqueID not in scoring:
                            scoring[uniqueID] = 1
                        elif uniqueID in scoring:
                            scoring[uniqueID] += 1

            # Get highest scoring id:
            if foundUniqueID == True:
                for uniqueID, score in scoring.items():
                    t = (score, uniqueID) # t = tuple
                    #print(t)
                    scoringList.append(t)
                sortedScoringList = sorted(scoringList, key=itemgetter(0,1))
                sortedScoringList.reverse()
                uniqueID = sortedScoringList[0][1]
                ids[taxid][query][id] = uniqueID #print "id ids[taxid][query][id]", id, ids[taxid][query][id]

                #print "Convert non primary id to primary id:"
                if db != primary_db:
                    struniqueID = str(uniqueID)
                    #print struniqueID, struniqueID in fromId[db], len(fromId[db])
                    if struniqueID in fromId[db]:
                        uniqueID = fromId[db][str(uniqueID)] #[0]
                else: struniqueID = str(uniqueID) #print uniqueID

                # Increase secondary scoring for found id:
                foundSecondaryUniqueID = "A"
                if uniqueID not in secondaryScoring:
                    secondaryScoring[uniqueID] = 1
                elif uniqueID in secondaryScoring:
                    secondaryScoring[uniqueID] += 1

                # Get synonyms for id:
                try:
                    for synonym in Map.idToAlias[db][struniqueID]:

                        if synonym and synonym not in ids[taxid][', '.join(aliases)]['synonyms']:
                            ids[taxid][query]['synonyms'].append(synonym)

                    if not ids[taxid][query]['id']:
                        ids[taxid][query]['id'] = uniqueID

                    elif ids[taxid][query]['id'] and ids[taxid][query]['id'] != uniqueID:
                        if query not in uncertainUniqueIDs:
                            uncertainUniqueIDs[query] = [ids[taxid][query]['id'], uniqueID]
                        else:
                            uncertainUniqueIDs[query].append(uniqueID)
                except Exception as e:
                    pass
                    #print e

        # Secondary Scoring:
        if foundSecondaryUniqueID == "A":
            #print "found secondary unique id."
            for uniqueID, secondaryScore in secondaryScoring.items():
                t = (secondaryScore, uniqueID)
                secondaryScoringList.append(t)
            sortedScoringList = sorted(secondaryScoringList, key=itemgetter(0,1))
            sortedScoringList.reverse()
            #print sortedScoringList
            uniqueID = sortedScoringList[0][1]
            #print SortedScoringList, Aliases
        ##            else: print ", ".join(Aliases)
        #print uniqueID
        ##        try:
        ##            uniqueID = int(uniqueID)
        ##        except: pass
        if isinstance(uniqueID, int):
            ids[taxid][query]['ID'] = uniqueID # Secondary defined ID.

        for db, id in dbs.items():
            #print(db, id)
            if not ids[taxid][query]['ID']:

                foundUniqueID = False
                scoring.clear()
                scoringList = []
                for alias in ids[taxid][query]['synonyms']:
                    #print "alias", alias
                    alias = str(alias).lower()          # AttributeError: 'int' object has no attribute 'lower'
                    if alias in aliasTo[db][taxid]:
                        #print "successe, found %s in %s" % (alias, db)
                        x = len(aliasTo[db][taxid][alias])
                        y = 0
                        uniqueID = aliasTo[db][taxid][alias][0]          #This is not neccessary, right? Removed upper.
                        #print alias, uniqueID
                        while x != y:
                            uniqueID = aliasTo[db][taxid][alias][y]
                            y +=1
                            foundUniqueID = True
                            if uniqueID not in scoring:
                                scoring[uniqueID] = 1
                            elif uniqueID in scoring:
                                scoring[uniqueID] += 1

                # Get highest scoring id:
                if foundUniqueID == True:
                    for uniqueID, score in scoring.items():
                        t = (score, uniqueID) # t = tuple
                        scoringList.append(t)
                    sortedScoringList = sorted(scoringList, key=itemgetter(0,1))
                    sortedScoringList.reverse()
                    uniqueID = sortedScoringList[0][1]
                    ids[taxid][query][id] = uniqueID

                    #print "Convert non primary id to primary id:"
                    if db != primary_db:
                        struniqueID = str(uniqueID)
                        #print struniqueID, struniqueID in fromId[db], len(fromId[db])
                        if struniqueID in fromId[db]:
                            uniqueID = fromId[db][str(uniqueID)] #[0]
                            #print "got it damwiid"
                    else: struniqueID = str(uniqueID)
                    #print uniqueID


                    if ids[taxid][query]['id'] == "":
                        ids[taxid][query]['id'] = uniqueID

                    ##                    if ids[taxid][query]['ID'] == "":
                    ##                        ids[taxid][query]['ID'] = uniqueID

                    elif ids[taxid][query]['id'] != "" and ids[taxid][query]['ID'] != uniqueID:
                        #print  ids[taxid][query]['id'], ids[taxid][query]['ID'], uniqueID
                        #uncertainUniqueIDs[query].append('['+uniqueID+']')
                        ids[taxid][query]['ID'] = ids[taxid][query]['id'] #= uniqueID
                        if query not in uncertainUniqueIDs:
                            uncertainUniqueIDs[query] = [ids[taxid][query]['id'], uniqueID]
                        else:
                            uncertainUniqueIDs[query].append(uniqueID)

        if not ids[taxid][query]['ID']: ids[taxid][query]['ID'] = ids[taxid][query]['id'] # Consider using also non-primary db unique ids

        if ids[taxid][query]['ID'] in discontinued: ids[taxid][query]['ID'] = discontinued[ids[taxid][query]['ID']]
        return (ids[taxid][query]['ID'], ids[taxid][', '.join(aliases)])

    @staticmethod
    def reset():
        """Resets the dynamic programming memory."""
        Map.ids.clear()
        Map.uncertainUniqueIDs.clear()


def main():
    """Testing suits here:"""
    #print Map.dbs
    #print Map.it('zbtb16', 9606)
    #print m("ZBTB16")
    ##    res = m("eat-1", 6239)
    ##    print res
    ##    return res
    print m('chico', 7227)

    f = File(name='MappedIDs.txt')
    data = f.parse(header=True, printing=False)
    for i in data:
        if not i: continue # correct this.
        #print i
        id = i['Input Id']
        print id, m([id], 6239)[0],
        try: print mo([id], 6239)#[0]
        except: print
        #print data[1]
    print m("cha-1", 6239)
    print m("unc-17", 6239)

m = Map.it

if __name__ == '__main__':
    main()
    #print m("ZBTB16", 10090)

#234567891123456789212345678931234567894123456789512345678961234567897123456789

    
