from django.shortcuts import redirect    
from django.http import JsonResponse
from django.contrib.sessions.models import Session

class IPAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    
    def __call__(self, request):
        print('middlware called')
        if request.META['REMOTE_ADDR'] == '127.0.0.1' and request.META['SERVER_PORT'] == '8000':
            print(f"Local Development Server Access from IP: {request.META['REMOTE_ADDR']}")
          
        response = self.get_response(request)
        return response
    
    # request.META contains all the metadata of the HTTP request that is coming to your Django server, it can contain the user agent, ip address, content type, and so on.




class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        print('middlware Login')
        allow_url = ['/login/', '/register/']
        if request.path not in allow_url:
                if request.session.session_key:

                    allow = validate_seesion(request, request.session.session_key)
                    if allow:
                       response = self.get_response(request)
                       
                    else:
                            response = {'error':'Please provide valid session'}
                            return JsonResponse(response)

                else:
                    response = {'error':'Not Provide Session Key'}
                    return JsonResponse(response)
        else:
            response = self.get_response(request)   # view ke pas jane ke liye
        return response
    


def validate_seesion(request,session_key):
        session_data = Session.objects.filter(session_key=session_key).first()
        uid = session_data.get_decoded()
        if session_data:
            return True
        else:
            return False







  