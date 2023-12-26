from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response
from .models import GameMaker
from .models import Developer
from .models import custom_user
from Game_app.datavalidator import validate_User
from .serializers import GameMakerSerializer
from .serializers import DeveloperSerializer
from .serializers import verifyAccountSerilizer
from rest_framework import status
from rest_framework import viewsets
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import redirect
import re
from django.contrib.sessions.models import Session
# from django.core.serializers import Serializer
# from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
import random
from Game_app.models import User
from django.db.utils import IntegrityError
from storefront.middleware.main import LoginMiddleware 
import logging

logger = logging.getLogger(__name__)


# Create your views here.


class GameMakerSerializerViewSet(viewsets.ViewSet):
    def list(self, request):
        stu = GameMaker.objects.all()
        logger.debug('@@@@@@@@@@@@@@@@@@@@@@@@ ', stu)
        serializer = GameMakerSerializer(stu, many=True)
        return Response(serializer.data)

class DeveloperSerializerViewSet(viewsets.ViewSet):
    def list(self, request):
        stu = Developer.objects.all()
        serializer = DeveloperSerializer(stu, many=True)
        return Response(serializer.data)


# values to ho gya ab mujhe count lgana he jese id 3 wale ne 2 game bnaye to id=3 hit kru postman se to 2 count aana chahiye id=1 wale ne ek game bnaya to count 1 aana chahiye
# means game ki id ko count krna
# loop ke under count nhi lgana he kyki loop me count replace ho jayega mtlab count ka alg se function bnaya us count function ko men function me loop ke uper call kro us function ki key bnakr ek list me appned kr do
class Developer_games_SerializerViewSet(viewsets.ViewSet):
    def list(self, request):
        # if request.session.get('user'):
        #     print('&&&&&&&&&&&&',request.session)
            dev_id = request.data.get('id')
            if dev_id:
                game_makers = GameMaker.objects.filter(
                developer_id=dev_id).select_related('developer')
            else:
                game_makers = GameMaker.objects.all().select_related('developer')

            d = {}
            datas = []
            count_dat = count_data(game_makers)
            d['count_data'] = count_dat
            datas.append(d)
            del_key = 'device'

            for data in game_makers:
                if data.developer:
                    logger.debug('########## ', data.developer)
                    GameMaker_data = GameMakerSerializer(data).data
                    logger.debug('game_dta ', GameMaker_data)
                    developer_data = DeveloperSerializer(data.developer).data
                    logger.debug('developer_data ', developer_data)
                    datas.append({'game': GameMaker_data, 'developer': developer_data})
                    if datas:
                        for items in datas:
                            if del_key in items:
                                del items[del_key]
                    logger.debug('##########@@@@ ', datas)

            return Response(datas)
            


def count_data(game_makers):
    count = 0
    for game_maker in game_makers:
        if game_maker.id:
            count += 1
    return count


@api_view(['POST'])
def register_user(request):
    data = {}
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    user = {'username': username, 'password': password, 'email': email}
    error_message = validate_User(user)
    logger.debug('&&&&&&&& ', error_message)
    if not error_message:
        user = custom_user.objects.create(
            username=username, password=password, email=email)
        user.save()
        datas=send_otp_via_email(email)
        data['email']=datas
        data['message'] = 'User registered successfully'
        return Response(data)
    else:
        return Response(error_message)



def post_decorator(login_user):
    def display(request, *args, **kwargs):
        if request.method == 'POST':
            logger.info(f"Received a POST request: {request}")
            return login_user(request, *args, **kwargs)
        else:
            logger.warning("GET method is not allowed")
            return JsonResponse({'message': 'GET method is not allowed'}, status=405)
    return display



@api_view(['POST'])  #Asseration error
@post_decorator
def login_user(request):
    logger.debug('call this function====>')
    data = {}
    error = None
    username = request.POST.get('username')
    password = request.POST.get('password')
    logger.debug('username: %s', username)
    logger.info('username: %s', password)

    try:
        user = custom_user.objects.filter(username=username, password=password).first()
        # Generate and set(session key)
        if user:
            request.session['user'] = user.username
            request.session['email'] = user.email
            data['login'] = 'login successfully'
            logger.debug('login success @#######################', data)
            return Response(data)
        else:
            error = {'login': 'invalid creditional'}
            logger.error('%s####', error)
            return Response(error, status=400)
    except Exception as e:
        error = {'login': 'invalid creditional'}
        logger.error('#####', error)
        return Response(error, status=400)
  

    
   
    
def send_otp_via_email(email):
    subject = 'your account verification email'
    otp = random.randint(1000,9999)
    message = f'your otp is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    user=User.objects.create(email=email,otp=otp)
    user.save()
    val='send mail otp succesfully'
    return val


@api_view(['POST'])
@post_decorator
def verify_otp(request):
    email = request.POST.get('email')
    otp = request.POST.get('otp')
    logger.debug('Verifying email: %s', email)
    logger.debug('Verifying OTP : %s', otp)

    if not email:
        logger.error('Email not found in request')
        return JsonResponse({'message': 'something went wrong', 'data': 'email not found'})

    user = User.objects.filter(email=email, otp=otp).first()

    if not user:
        user_v = User.objects.filter(email=email, is_verified=True).first()
        if user_v:
            logger.info('User email already verified: ###', email)
            return JsonResponse({'message': 'already verified ', 'data': 'already verified USER Email'})
        
        logger.error('Invalid OTP or Email: #####', otp, email)
        return JsonResponse({'message': 'something went wrong ', 'data': 'invalid otp or Email'})

    user.is_verified = True
    user.otp = int(otp) + 1
    user.save()

    logger.debug('Account verified for email: %s&&&&&&&&', email)
    return JsonResponse({'message': 'Account verified'})





# Create your views here.
