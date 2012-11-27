import re
import urllib2


class HTML(object):
    def __init__(self, url):
        self.url = url
        self.content = self.get(url)

    def get(self, url):

        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),    # Automatically follows redirects.
                                      urllib2.HTTPHandler(debuglevel=0))# Will read any web pages that are returned.
        opener.addheaders = [                                           # User-agent-string: Pretend to be Internet Explorer 7 running on Windows XP.
            ('User-agent',
            "Mozilla/4.0 (compatible; MSIE 7.0; "
            "Windows NT 5.1; .NET CLR 2.0.50727; "
            ".NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)")
            ]
        response = opener.open(url)
        return ''.join(response.readlines())

    def find_quote_section(self, element):
        from BeautifulSoup import BeautifulSoup
        soup = BeautifulSoup(self.content)      # Parsing the html to get an beautiful soup object
        self.quote = soup.find('div',                # Find returns another soup object.
                          attrs={'class':element})
        return self.quote

    def parse(self, ticker_name):
        if not hasattr(self, 'quote'): self.quote = self.find_quote_section()
        result = {}
        tick = ticker_name.lower()

        # <h2>Google Inc.</h2>
        result['stock_name'] = self.quote.find('h2').contents[0]

        ### After hours values:
        # <span id="yfs_l91_goog">329.94</span>
        result['ah_price'] = self.quote.find('span',
                                        attrs={'id': 'yfs_l91_'+tick}).string

        # <span id="yfs+z08_goog">
        #  < span class="yfi-price-change-down">0.22</span>
        result['ah_change'] = (selfquote.find('span',
                                          attrs={'id': 'yfs_l91_'+tick}).contents[1])

        ### Current values
        # < span id="yfs_l10_goog">330.16</span>
        result['last_trade'] = self.quote.find('span', attrs={'id': 'yfs_l10_'+tick}).string

        # <span id="yfs_c10_goog" class="yfi_quote_price">
        #  <span class='yfi-price-change-down">1.06</span>
        def is_price_change(value):
            return (value is not None and
                    value.strip().lower().startswith('yfi-price-change'))

        result['change'] = (
            quote.find(attrs={'id': 'yfs_c10_'+tick})
                 .find(attrs={'class': is_price_change}.string))

        return result

    def find(self, term):
        """Find lines contening a defined term."""
        result = []
        content = self.content.split('\n')
        for line in content:
            #print line
            if term in line:
                result.append(line)
        return result

    def find_follows(self, term):
        result = []
        findings = self.find(term)
        for finding in findings:
            follows = finding.split(term)[1]
            result.append(follows)
        return result

    def single_between(self, after, before):
        finding = self.find_follows(after)[0]
        between = finding.split(before)[0]
        return between

    def find_between(self, after, before, discard=None, all=False):
        """Gets all strings which are between after and before."""
        betweens = []
        if all:
            findings = self.get_follows(after)
        else:
            findings = self.find_follows(after)
        for finding in findings:
            if discard:
                if isinstance(discard, str):
                    if discard in finding.split(before)[0]:
                        continue
                else:
                    ignore = False
                    between = finding.split(before)[0]
                    for dis in discard:
                        if dis in between:
                            ignore = True
                    if ignore:
                        continue
            between = finding.split(before)[0]
            if not between:
                continue # If it found an empty string, ignore it.
            betweens.append(between)
        return betweens

    def get_follows(self, term):
        result = []
        findings = self.find(term)
        for finding in findings:
            follows = finding.split(term)
            if len(follows) > 2:
                for i, follow in enumerate(follows):
                    if i: #Odd
                        result.append(follow)
        return result

    def all_between(self, after, before, discard=None):
         """Gets absolutly all strings which are inbetween after and before
         even if there multipe occurence in the same line
         via the use of regular expression!
         Depriciated as it is too complicated."""
         betweens = []
         pattern = r'%s(.*?)%s' % (after, before)
         i
         prog = re.compile(pattern)
         for line in self.content:pass

    def write_csv(self, ticker_name):
        self.field_order = ['date', 'last_trade', 'change', 'ah_price', 'ah_change']
        self.fields = {'date': 'Date',
                  'last_trade': 'Last Trade',
                  'change': 'Change',
                  'ah_price': 'After Hours Price',
                  'ah_change': 'After Hours Change'}

        stock = parse()
        stock['date'] = time.sftrtime("%Y-%m-%d %H:%M")
        self.write_row(ticker_name, stock)
        
    def write_row(ticker_name, stock_values):
        fiel_name = 'html-' + ticker_name + '.csv'
        if os.access(file_name, os.F_OK):
            file_mode = 'ab'
        else:
            file_mode =  'wb'

        csv_writer = csv.DictWriter(
            open(file_name, file_mode),
            fieldnames=self.field_order,
            extrasaction='ignore')

        if file_mode == 'wb':
            csv_writer.writerow(self.fields)
        csv_writer.writerow(stock_values)
