"""A mechanized Browser.
Inspired by:
http://stockrt.github.com/p/emulating-a-browser-in-python-with-mechanize/
http://palewi.re/posts/2008/04/20/python-recipe-grab-a-page-scrape-a-table-download-a-file/
http://stackoverflow.com/questions/4250061/using-python-mechanize-to-login-on-webpage-with-javascript-md5-hashing-function"""

import mechanize
import cookielib


br = mechanize.Browser() # Browser

cj = cookielib.LWPCookieJar() # Cookiejar
br.set_cookiejar(cj)

# Browser options:
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Debugging:
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

# Agent:
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linuz i686; en-US; rv:1.9.0.1)'\
                                'Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#return br

if __name__ == '__main__':
    pass
    r = br.open('http://google.com')
    #html = r.read()

    # Show source:
    #print html # or:
    #print br.response().read()

    # Show html title:
    print br.title()

    # Show the repsonse headers:
    #print r.info() # or:
    #print br.response().info()

    # Show the available forms:
    #for f in br.forms(): print f

    # Show the first (index zero) form:
    br.select_form(nr=0)

    # Let's search:
    br.form['q']='pyglet'
    br.submit()
    #print br.response().read()

    # Looking at some results in link format
    #for l in br.links(url_regex="opengl"): print l

    # Downloading a file:
    f = br.retrieve('http://www.google.com.br/intl/pt-BR_br/images/logo.gif', 'logo.gif')[0]
    #print f
    #fh = open(f)

  

#br.set_allreadonly(False)
##session = br['session']
##for form in br.forms():
##    req = form.click()
##req = mechanize.urlopen(req)
##print req.geturl()
#print br.response().read()
