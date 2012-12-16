import re
import unicodedata

from django.conf import settings


IP_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

def get_ip(request):
    """Retrieves the remote IP address from the request data."""

    # If neither header conatin a value, just use local loopback
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR',
                                  request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        # Make sure we have only only on IP:
        try:
            ip_address = IP_RE.match(ip_address)
            if ip_address:
                ip_address = ip_address.group(0)
            else:
                # No IP, probaly from some dirty proxy or other device
                # Throw in some bogus IP
                ip_address = '10.0.0.1'
        except IndexError:
            pass
    return ip_address

def get_timeout():
    """Gets any specified timeout from the settings file, or use 10 minutes by default."""
    return getattr(settings, 'TRACKING_TIMEOUT', 10)

def get_cleanup_timeout():
    """Gets any specified visitor clean-up timeout from the settings file,
    or use 24 hours by default."""
    return getattr(settings, 'TRACKING_CLEANUP_TIMEOUT', 24)

def u_clean(s):
    """A strange attempt at celaning up unicode."""
    uni = ''
    try:
        # Try this first
        uni = str(s).decode('iso-8859-1')
    except UnicodeDecodeError:
        try:
            # Try utf-8 next
            uni = str(s).decode('utf-8')
        except UnicodeError:
            # Last resort method... one chracter at a time
            if s and type(s) in (str, unicode):
                for c in s:
                    try:
                        uni += unicodedata.normalize('NFKC', unicode(c))
                    except UnicodeDecodeError:
                        uni += '-'
    return uni.encode('ascii', 'xmlcharrefreplace')