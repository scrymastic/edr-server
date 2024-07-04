

from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = ['/api/receive_events/']
        websockets = '/ws/'
        # print('request.path_info:', request.path_info)
        if not request.user.is_authenticated \
            and request.path_info not in [reverse('login')] \
            and not any([request.path_info.startswith(url) for url in exempt_urls]) \
            and not request.path_info.startswith(websockets):
            return redirect('login')
        return self.get_response(request)