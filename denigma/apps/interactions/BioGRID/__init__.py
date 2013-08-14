""" Download BioGRID File
Check for already downloaded files"""
import os
import os.path
import urllib
import datetime

from files import File, Folder


def main(generator=False):
    os.chdir(path)
    # Version:
    url = 'http://thebiogrid.org/'
    f = urllib.urlopen(url)
    contents = f.read()
    f.close()
    lines = contents.split('\n')
    for line in lines:
        if '<div class="newspost-title">BioGRID Version' in line:
            print line
            VERSION = line.split('<div class="newspost-title">BioGRID Version ')[1].split(' Release ')[0]
            break
    print VERSION

    # Urlsexi:
    url = 'http://thebiogrid.org/downloads/archives/Release%20Archive/BIOGRID-'
    tab2url = url+VERSION+'/BIOGRID-ALL-'+VERSION+'.tab2.zip'
    mitaburl = url+VERSION+'/BIOGRID-ALL-'+VERSION+'.mitab.zip'

    # Files:
    folder = Folder()
    folder.get([tab2url, mitaburl])

    tab2 = folder.contains('tab2')[0].parse(printing=False, seperator=None)
    mitab = folder.contains('mitab')[0].parse(printing=False, seperator=None)

    # Parsing:
    header = tab2[0].split('\t')
    D = {}
    output = open(os.path.join(path, 'interactions.txt'), 'w')

    for x in xrange(0, len(tab2)):
        line = tab2[x]
        if "#BioGRID Interaction ID" not in line and line != "":
            columns = line.split('\t')
            if int(columns[0]) not in D: D[int(columns[0])] = {}
            systematic_name_intactor_a = columns[5]
            systematic_name_intactor_b = columns[6]
            official_gene_symbol_a = columns[7]
            official_gene_symbol_b = columns[8]
            synonymns_interactor_a = columns[9].split('|')
            synonymns_interactor_b = columns[10].split('|')
            
            AliasA, AliasB = [columns[1]], [columns[2]]

            if systematic_name_intactor_a != '-' and systematic_name_intactor_a not in AliasA: AliasA.append(systematic_name_intactor_a)
            if systematic_name_intactor_b != '-' and systematic_name_intactor_b not in AliasB: AliasB.append(systematic_name_intactor_b)
            if official_gene_symbol_a != '-' and official_gene_symbol_a not in AliasA: AliasA.append(official_gene_symbol_a)
            if official_gene_symbol_b != '-' and official_gene_symbol_b not in AliasB: AliasB.append(official_gene_symbol_b)
            for i in synonymns_interactor_a:
                if i != "-" and i not in AliasA: AliasA.append(i)
            for i in synonymns_interactor_b:
                if i != "-" and i not in AliasB: AliasB.append(i)

            experimental_system_type = [columns[12], 'direct']
            experimental_system = columns[11]

            type = mitab[x].split('\t')[11].split('(')[1].split(')')[0]
            
            pmid = int(columns[14])
            taxid_a = int(columns[15])
            if taxid_a == 559292: taxid_a = 4932
            taxid_b = int(columns[16])
            if taxid_b == 559292: taxid_b = 4932
            throughput = columns[17].split('|')
            if columns[19] != '-':
                modification = columns[19]
                #print modification
            else: modification =  ''
            source = columns[23]   #'BioGRID'

            r = '\t'.join(['; '.join(AliasA), '; '.join(AliasB), '; '.join(experimental_system_type), experimental_system, type,  modification, str(taxid_a), str(taxid_b), str(pmid), source+'\n'])
            output.write(r)
                    
            D[int(columns[0])][int(columns[1])] = {'source':source,
                                       'experimental_system':experimental_system,
                                       'experimental_system_type':experimental_system_type,
                                       'taxid_a':taxid_a,
                                       'taxid_b':taxid_b,
                                       'pmid':pmid,
                                       'throughput':throughput}
    output.close()
    new_entry = '\n%s %s' % (VERSION, datetime.datetime.now())
    version_file = open(os.path.join(path, 'version.txt'), 'a')
    version_file.write(new_entry)
    version_file.close()

    #Cleaning up:
    filenames = os.listdir(path)
    for filename in filenames:
        if "BIOGRID" in filename:
            print("Deleting %s" % filename)
            #os.remove(os.path.join(filename))
            
if __name__ == '__main__': path = '.'; main()
else: path = os.path.join(os.path.split(__file__)[:-1])[0]

