"""Uitility middlewares."""
import re
from threading import current_thread


"""Middleware to redirect users.
Alternatively simply memecache or redix (in case of large data) can eb used to do that."""
class LastSiteUrl(object):
    """Records th last url the user visited.
    Can be used to return user back to the last app page they were at,
    from the admin page, no matter how deep into admin they were."""
    def is_admin_url(self, url):
        if re.search('^(http:\/\/.*){0,1}\/admin\/', url) is None:
            return False

    def process_request(self, request):
        if self.is_admin_url(request.path) and \
            not self.is_admin_url(request.META['HTTP_REFERER']):
            request.session['last_site_url'] = request.META['HTTP_REFERER']


"""Middlewars can be used to put attributes on a request.
Alternativly if django-s UserMiddlerware is active, it can always be done request.user.get_profiler()
without the need of a cusomt middleware"""
class ProfileMiddleware(object):
    """Enables to accesses the user's profile on request."""
    def process_request(request):
        request.profile = None
        if request.user.is_authenticated():
            request.profile = request.user.get_profile()


class GlobalRequest(object):
    """"A middleware for the cases when it is very inconvenient to make the
    `request` object depp in the call stack."""
    _request = {}

    @staticmethod
    def get_request():
        try:
            return GlobalRequest._request[current_thread()]
        except KeyError:
            return None

    def process_request(self, request):
        GlobalRequest._requests[current_thread()] = request

    def process_response(self, request, response):
        # Cleanup
        thread = current_thread()
        try:
            del GlobalRequest._request[thread]
        except KeyError:
            pass
        return response

def get_request():
    return GlobalRequest.get_request()