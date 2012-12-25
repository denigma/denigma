from urllib2 import urlopen, Request
import re ##socket
#try:
#    raise
#    from django.conf import settings
#except Exception:
#    class settings:
#        BASE_URL = 'http://google.com'
#
#domain_re = re.compile('^(http|https):\/\/?([^\/]+)')
#domain = domain_re.match(settings.BASE_URL).group(2)
#
#def getUserCountry(ip):
#    url = "http://api.wipmania.com/" + ip + "?" + domain
#    socket.setdefaulttimeout(5)
#    headers = {'Type': 'django', 'Ver': '1.4.3', 'Connection': 'Close'}
#    try:
#        req = Request(url, None, headers)
#        urlfile = urlopen(req)
#        land = urlfile.read()
#        return land[:2]
#    except Exception as e:
#        return e

city_re = re.compile('<meta name="city" content="(.+)">')
country_re = re.compile('<meta name="country" content="(.+)">')

def locate(ip):
    url = "http://www.geobytes.com/IpLocator.htm?GetLocation&template=php3.txt&IpAddress=%s" % ip
    try:
        req = Request(url, None)
        urlfile = urlopen(req)
        data = urlfile.read()
        #print(data)
        country = re.findall(country_re, data)[0]
        city = re.findall(city_re, data)[0]
    except Exception as e:
        print(e)
        country = city = '?'
    return "%s/%s" % (country, city)


if __name__ == "__main__":
    #print getUserCountry("66.249.75.199")
    print locate("129.12.232.198") #")127.0.0.1