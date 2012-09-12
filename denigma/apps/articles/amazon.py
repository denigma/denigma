"""An Amozone API to retrieve book informations.
Inpsired by:
https://github.com/mutaku/PyAmazon
http://weblog.bluepenguin.us/2002/07/diveintomark-search-amazon-fro.html
https://bitbucket.org/basti/python-amazon-product-api/issue/29/11-1-2011-new-requirement-associatetag
"""
from itertools import count
import webbrowser
from xml.dom import minidom as xml

import bottlenose
from amazonproduct import API

from denigma.key import AWS_KEY, SECRET_KEY


LOG = dict(AWS_KEY = AWS_KEY,
           SECRET_KEY = SECRET_KEY,
           ASSOC_TAG = 'Hevok',
           LOCAL = 'us')


def search(title=''):
    """Amazon quick search function."""
    api = API(LOG['AWS_KEY'], LOG['SECRET_KEY'], LOG['LOCAL'], LOG['ASSOC_TAG'])
    node = api.item_search('Books', Title=title, Publisher=publisher)
    for page in node:
        for book in page.Items.Item:
            print '%s' % (book.ASIN)
            #print dir(book)
##total_results = root.Items.TotalResults.pyval
##print len(total_results)



class Search():
    """Integration with Amazon API to show search results and so forth.

    TODO:
     - better parsing for output as dictionary or std out
     - error container to report bach any issues

    USAGE:
    import webbrowser
    from amazon import Search

    result = Search(title="The Idea of America", author="Gordon Wood", style="xml")
    link = result.parsedXML[0]['URL']

    webbrowser.open(link)
     """
    def __init__(self, title='', author='', keywords='', style='xml', output='detailed'):
        # Setup the search terms from args:
        self.title = title
        self.author = author
        self.keywords = keywords
        self.rawstyle = style
        self.rawoutput = output

        # Setup the result data type ---> defaults to json the xml2json stylesheet
        styles = {
            "xml": "XML",
            "json": "xml2json.xslt"
            }
        self.style = styles[self.rawstyle]

        # We will fire up a parsing precodure if we have XML style:
        if self.style == "XML":
            self.parse = True
        else:
            self.parse = False

        # Search result type ---> defaults to ItemAttributes (most detailed)
        outputTypes = {
            "images": "Images",
            "detailed": "ItemAttributes"
            }

        self.outputMethod = outputTypes[self.rawoutput]

        # Setup the API access - these are temporarily filled in wtih affilate id
        keys = {'access_key':LOG['AWS_KEY'],
                'secret_key':LOG['SECRET_KEY'],
                'local':LOG['LOCAL'],
                'affiliate_id':LOG['ASSOC_TAG']} #associated_tag'
        self.amazon = bottlenose.Amazon(keys['access_key'], keys['secret_key'], keys['local'], keys['affiliate_id'])

        # Run the search to populate self.results with an xml string:
        self.search()

    def search(self):
        """Do the search."""
        self.results = self.amazon.ItemSearch(
            SearchIndex = "Books",
            Style = self.style,
            ResponseGroup = self.outputMethod,
            Sort = "relevancerank",
            Title = self.title,
            Author = self.author,
            Keywords = self.keywords)
        print self.results
##        for i in self.results:
##            print i

        # If we set Parse=True whne instatiating, we will print out a nice parsed version as well.
        if self.parse:
            self.parser()
        else:
##            import simplejson as json
##            self.results = json.loads(self.results)
            return self.results

    def parser(self):
        """Parse XML results"""
        # pipe the results into the xml dom
        r = xml.parseString(self.results)
        self.parsedXML = {}

        # Setup some Attributes that will be grapped and print out:
        attrs = ['Title', 'Author', 'FormattedPrice', 'URL', 'PublicationDate', 'Publisher', 'Studio', 'ISBN', 'NumberOfPages', 'Edition']

        #iterate through by Item and if we can find the attribute we print it out
        x = count(0)
        for i in r.getElementsByTagName('Item'):
            item = next(x)
            self.parsedXML[item] = {}
            parsedItem = self.parsedXML[item]
            for attr in attrs:
                parsedItem[attr] = ""
                try:
                    if len(i.getElementsByTagName(attr)) == 1:
                        parsedItem[attr] = i.getElementsByTagName(attr)[0].childNodes[0].data
                    else:
                        parsedItem[attr] = []
                        for item in i.getElementsByTagName(attr):
                            parsedItem[attr].append(item.childNodes[0].data)
                except:
                    pass
        return self.parsedXML

    def result(self):
        d = {}
        print self.parsedXML[0]['Author']
        d['authors'] = self.parsedXML[0]['Author']
        d['authors'] = [', '.join([d['authors'].split(' ')[1], d['authors'].split(' ')[0]])]
        d['date'] = self.parsedXML[0]['PublicationDate']
        d['year'] = int(d['date'].split('-')[0])
        d['title'] = self.parsedXML[0]['Title']
        d['publisher'] = self.parsedXML[0]['Publisher']
        d['pages'] = self.parsedXML[0]['NumberOfPages']
        d['isbn'] = self.parsedXML[0]['ISBN']
        d['edition'] = self.parsedXML[0]['Edition']
        d['links'] = self.parsedXML[0]['URL']
        d['link'] = d['links'][0]
        del d['links'] # Not necessary to have to many links for now.
        #studio = result.parsedXML[0]['Studio']
        return d
    result = property(result)
    

if __name__ == '__main__':
    query = "Wolfe RR, Chinkes DL (2005) Isotope Tracers in Metabolic Research: Principles and Practice of Kinetic Analysis. Hoboken NJ: Wiley."
    #search = Search(title=query.split(')')[1].split('.')[0])
    search = Search(title="Python Cookbook")
    print search.result
    #result = Search(keywords=query)
    #webbrowser.open(link) 
