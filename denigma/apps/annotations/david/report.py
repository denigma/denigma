import os

from suds.client import Client


def authenticate():
    from suds.client import Client
    import os
    client = Client('http://david.abcc.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl')
    print 'User Authentication:', client.service.authenticate('age@liv.ac.uk')


def enrich(ids, idType=None, listName='test'):
    client = Client('http://david.abcc.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl')
    #print 'User Authentication:', \
    client.service.authenticate('age@liv.ac.uk')
    listF = listName
    inputListIds = ",".join(map(str, ids))
    listType = 0
    #print 'Percentage mapped(list):',
    client.service.addList(inputListIds, idType, listName, listType)
    flagBg = False
    thd = 0.1
    ct = 2
    category = 'abcd,BBID,BIOCARTA,COG_ONTOLOGY,INTERPRO,KEGG_PATHWAY,OMIM_DISEASE,PIR_SUPERFAMILY,SMART,SP_PIR_KEYWORDS,UP_SEQ_FEATURE'
    #print "Use categories",
    client.service.setCategories(category)
    chartReport = client.service.getChartReport(thd, ct)
    #chartRow = len(chartReport)
    #print 'Total chart records:', chartRow
    results = Results(chartReport)
    results.header = 'Category\tTerm\tCount\t%\tPvalue\tList Total\tPop Total\tFold Enrichment\tBonferri\tBenjamini\tFDR'.split('\t')
    resF = listF + '.chartReport'
    return results


class Result(object):
    def __init__(self, row):
        rowDict = dict(row)
        self.categoryName = str(rowDict['categoryName'])
        self.termName = str(rowDict['termName'])
        self.listHits = str(rowDict['listHits'])
        self.percent = str(rowDict['percent'])
        self.ease = str(rowDict['ease'])
        self.genes = str(rowDict['geneIds'])
        self.listTotals = str(rowDict['listTotals'])
        self.popHits = str(rowDict['popHits'])
        self.popTotals = str(rowDict['popTotals'])
        self.foldEnrichment = str(rowDict['foldEnrichment'])
        self.bonferroni = str(rowDict['bonferroni'])
        self.benjamini = str(rowDict['benjamini'])
        self.FDR = str(rowDict['afdr'])

    def __str__(self):
        return self.termName


class Results(list):
    def __init__(self, chartReport):
        for row in chartReport:
            self.append(Result(row))

    def columns(self):
        return vars(self[0]).keys()

    def data(self):
        rows = []
        for result in self:
            rows.append(vars(result))
            #print vars(result)
        return rows

