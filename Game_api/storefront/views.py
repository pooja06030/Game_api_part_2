from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response
from django.http.response import JsonResponse
from Game_app.models import GameMaker
from Game_app.serializers import GameMakerSerializer
from Game_app.serializers import DeveloperSerializer
from Game_app.serializers import device_frantSerializer
from storefront.serializers import categorySerializer
from storefront.serializers import make_and_ModelsSerializer
from Game_app.models import Developer
from Game_app.models import device_frant
from rest_framework import status
from rest_framework import viewsets
from storefront.models import store_frant
from storefront.models import category
from storefront.models import make_and_Models_mapping
from rest_framework.decorators import api_view, permission_classes
from django.db import connections, reset_queries
from storefront.models import Storemap
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
import logging
logger = logging.getLogger(__name__)
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.decorators import login_required


import json
# Create your views here.


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def test(request):
    if request.method == 'GET':
        store_id = request.GET.get('id')
        logger.info('Received a GET request with store_id:', store_id)

        if store_id:
            store_data = store_frant.objects.filter(
                id=store_id).select_related('Game', 'Game__developer', 'device', 'category')
            logger.debug('Store data ', store_data)
        else:
            store_data = store_frant.objects.all().select_related(
                'Game', 'Game__developer', 'device', 'category')
            logger.debug('All store data: ', store_data)

        datas = []
        for data in store_data:
            if data.Game:
                GameMaker_data = GameMakerSerializer(data.Game).data

            if data.Game.developer:
                developer_data = DeveloperSerializer(data.Game.developer).data

            if data.device:
                device_data = device_frantSerializer(data.device).data

            if data.category:
                category_data = categorySerializer(data.category).data
                datas.append(
                    {'game': GameMaker_data, 'devloper': developer_data, 'device': device_data, 'category': category_data})

        return Response(datas)

# esme only game type pr filter lgaya he mujhe age html ke game chahiye to sare html game cloud ke sare game chahiye to sare cloud game mil jayenge
@api_view(['GET'])
def Game_type_all(request):
    if request.method == 'GET':
        disp_game_type = request.GET.get('display_game_type')
        developer_id__name = request.GET.get('developer_id__name')
        device_id__name = request.GET.get('device_id__name')
        
        logger.debug('@@@@@@@ ', disp_game_type)
        logger.debug('****** ', device_id__name)
        logger.debug('&&&&&&&&& ', developer_id__name)

        if disp_game_type:
            game_makers = GameMaker.objects.filter(
                game_type=disp_game_type, developer_id__name=developer_id__name, device_id__name=device_id__name).values('game_type', 'device_id__name', 'developer_id__name', 'id', 'short_description', 'is_active', 'include_ads', 'game_name',  'game_price')
            logger.debug('^^^^^^^^^ ', game_makers)
            return Response(game_makers)
        else:
            game_makers = GameMaker.objects.all().select_related('developer', 'device')
            logger.debug('%s$$$$$', game_makers)
            datas = []
            for data in game_makers:
                logger.debug('!!!!!!!!!!!!! ', data)
                if data.developer:
                    GameMaker_data = GameMakerSerializer(data).data
                    developer_data = DeveloperSerializer(data.developer).data

                if data.device:
                    device_data = device_frantSerializer(data.device).data
                    datas.append({'game': GameMaker_data, 'devloper': developer_data, 'device': device_data})
            return Response(datas)



@api_view(['GET'])
def make_and_modal_data(request):
    if request.method == 'GET':
        mobile_id = request.GET.get('id')
        Make_and_modle_id_make = request.GET.get('Make_and_modle_id_make')
        Make_and_modle_id_model = request.GET.get('Make_and_modle_id_model')
        Game_id_game_name = request.GET.get('Game_id_game_name')

        if mobile_id:
            data = make_and_Models_mapping.objects.filter(id=mobile_id)
            logger.debug(f"Data for mobile_id :{data}")

        if Make_and_modle_id_make:
            filtered_mobile = make_and_Models_mapping.objects.filter(
                Make_and_modle__make=Make_and_modle_id_make,
                Make_and_modle__model=Make_and_modle_id_model,
                Game__game_name=Game_id_game_name
            ).values('Game__game_name', 'Game__game_price', 'Game__game_type', 'Game__include_ads', 'Game__is_active', 'Make_and_modle__make', 'Make_and_modle__model')
            logger.debug(f"Filtered data: {filtered_mobile}")
            return Response(filtered_mobile)

        else:
            datas = make_and_Models_mapping.objects.all().select_related('Make_and_modle', 'Game')
            dev_data = []
            for data in datas:

                if data.Game:
                    GameMaker_data = GameMakerSerializer(data.Game).data
                    logger.debug(f"GameMaker data: {GameMaker_data}")

                if data.Make_and_modle:
                    make_modal_data = make_and_ModelsSerializer(
                        data.Make_and_modle).data
                    logger.debug(f"Make and Model data: {make_modal_data}")

                    dev_data.append(
                        {'game': GameMaker_data, 'Make_and_modle': make_modal_data})

            logger.debug(f"Final dev_data: {dev_data}")

        return JsonResponse(dev_data, safe=False)

# Create your views here.
