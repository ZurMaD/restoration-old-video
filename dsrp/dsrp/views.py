import ibm_boto3
from ibm_botocore.client import Config
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
###########################################################
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
###########################################################


# from .models import ProductoHijoCompra
# from .models import ProductoPadre
# from .models import Proveedor
# from .models import BoletaCompra
# ###########################################################
# from .models import ProductoPlato
# from .models import PlatoPadre
# from .models import PlatoHijoVenta
# from .models import BoletaVentaRestaurante
# from .models import ProductoHijoTransaccion


###########################################################
from django.utils.timezone import get_current_timezone
import datetime
##########################################################
from django.db.models import Count
from django.db.models import Sum
from django.db.models import F

##########################################################
# Allow iFrame
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin

##########################################################
# ALLOW REST_FRAMEWORK LOGIN
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
# from .models import AuthtokenToken
# from .models import AuthUser
# from .models import ApiMedicKitPerUser
from .forms import SignUpForm
from django.contrib import messages

##########################################################
# ALLOW WEBHOOK GRAFANA
# from .models import ApiMedicNotifications
from django.utils import timezone
from rest_framework.utils import json


##########################################################
# ALLOW MONGODB
import pymongo
from pymongo import MongoClient
from bson import objectid
from bson.objectid import ObjectId
from datetime import datetime
import pprint
##################################
from .forms import VideoForm
import os
import subprocess

##################################
import numpy as np


# -------------------- INICIO CREDENTIALS -----------------
from .credentials import *

credentials = key_1
cos_credentials = key_2

auth_endpoint = str(os.environ.get('IBM_AUTH_ENDPOINT'))
service_endpoint = str(os.environ.get('SERVICE_ENDPOINT'))


cos = ibm_boto3.client('s3',
                       ibm_api_key_id=cos_credentials['apikey'],
                       ibm_service_instance_id=cos_credentials['resource_instance_id'],
                       ibm_auth_endpoint=auth_endpoint,
                       config=Config(signature_version='oauth'),
                       endpoint_url=service_endpoint)


def upload_file_cos(credentials, local_file_name, key):
    cos = ibm_boto3.client(service_name='s3',
                           ibm_api_key_id=credentials['IBM_API_KEY_ID'],
                           ibm_service_instance_id=credentials['IAM_SERVICE_ID'],
                           ibm_auth_endpoint=credentials['IBM_AUTH_ENDPOINT'],
                           config=Config(signature_version='oauth'),
                           endpoint_url=credentials['ENDPOINT'])
    try:
        res = cos.upload_file(Filename=local_file_name,
                              Bucket=credentials['BUCKET'], Key=key)
    except Exception as e:
        print(Exception, e)
    else:
        print('File Uploaded')


def download_file_cos(credentials, local_file_name, key):
    cos = ibm_boto3.client(service_name='s3',
                           ibm_api_key_id=credentials['IBM_API_KEY_ID'],
                           ibm_service_instance_id=credentials['IAM_SERVICE_ID'],
                           ibm_auth_endpoint=credentials['IBM_AUTH_ENDPOINT'],
                           config=Config(signature_version='oauth'),
                           endpoint_url=credentials['ENDPOINT'])
    try:
        res = cos.download_file(
            Bucket=credentials['BUCKET'], Key=key, Filename=local_file_name)
    except Exception as e:
        print(Exception, e)
    else:
        print('File Downloaded')

# cos.upload_file(Filename='results/frames_out_fastdvdnet.zip',Bucket=credentials['BUCKET'],Key='frames_out_fastdvdnet.zip')
# cos.download_file(Bucket=credentials['BUCKET'],Key='frames_out.zip',Filename='frames_out.zip')

# -------------------- FIN CREDENTIALS -----------------


# ------------------------  INICIO LOGIN ------------------
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(
                request, 'Nueva cuenta registrada satisfactoriamente.')
            return redirect('signup')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

# ------------------------  FIN LOGIN ------------------

# ------------------------ INICIO INDEX ------------------


def index_view(request):

    # Variables de reporte mensual

    return render(request, 'index/index.html', locals())

# -------------------------- FIN INDEX -------------------

# -------------------- INICIO DASHBOARD -----------------


def handle_uploaded_file(f, codigo, current_user_id):

    current_user_id = current_user_id
    filename_temp = ''
    filename_cos = ''
    static_file_dir = ''
    temp_file_dir2 = ''
    static_file_dir2 = ''

    try:
        temp_file_dir = 'dsrp/static/temp_upload/' + \
            str(datetime.now().strftime('%Y%m%d%H%M%S')) + \
            "-"+str(current_user_id)+"-" + f.name

        static_file_dir = '/temp_upload/' + \
            str(datetime.now().strftime('%Y%m%d%H%M%S')) + \
            "-"+str(current_user_id)+"-" + f.name

        with open(temp_file_dir, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        name_file_cos = str(datetime.now().strftime('%Y%m%d%H%M%S')) + \
            "-"+str(current_user_id)+"-"+codigo + '.mp4'

        cos.upload_file(Filename=temp_file_dir,
                        Bucket=credentials['BUCKET'], Key=name_file_cos)

        print("File uploaded to IBM COS")

    except Exception as e:  # Exclusive for Heroku

        temp_file_dir2 = 'static/temp_upload/' + \
            str(datetime.now().strftime('%Y%m%d%H%M%S')) + \
            "-"+str(current_user_id)+"-" + f.name

        static_file_dir2 = '/temp_upload/' + \
            str(datetime.now().strftime('%Y%m%d%H%M%S')) + \
            "-"+str(current_user_id)+"-" + f.name

        with open(temp_file_dir2, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        name_file_cos = str(datetime.now().strftime('%Y%m%d%H%M%S')) + \
            "-"+str(current_user_id)+"-"+codigo + '.mp4'

        cos.upload_file(Filename=temp_file_dir2,
                        Bucket=credentials['BUCKET'], Key=name_file_cos)

        print("File uploaded to IBM COS")

    client = MongoClient(key_3)
    db = client.galeria
    collection = db.videos

    data = {'current_user_id': str(current_user_id),
            'filename_temp': str(temp_file_dir),
            'filename_cos': str(name_file_cos),
            'static_file_dir': str(static_file_dir),
            'temp_file_dir2': str(temp_file_dir2),
            'static_file_dir2': str(static_file_dir2),
            'models': {'processing_sequence': ['FastDVDNet', 'RRIN', 'DeOldify', 'Deflickering', 'Speech Enhancement'],
                       # Can be priority also
                       'order_sequence': [1, 3, 2, 0, 4],
                       'status': 'Creating/Running/Completed/Failed/Rechazed',
                       'download_links': {'0': '0'},
                       }
            }
    print(data)

    collection.insert_one(data)


@csrf_exempt
@login_required(login_url='/accounts/login')
@permission_classes((AllowAny,))
def dashboard_upload_view(request):

    if request.method == "POST":

        video = VideoForm(request.POST, request.FILES)
        if video.is_valid():
            current_user_id = request.user.id
            handle_uploaded_file(
                request.FILES['video'], request.POST.get('codigo'), current_user_id)
            print("File uploaded successfuly")
            HttpResponse("File uploaded successfuly")
            return redirect('../choose/')

    elif request.method == "GET":
        video = VideoForm()
        return render(request, 'dashboard/pipeline/upload.html', {'form': video, 'user_name': str(request.user.username)})


@login_required(login_url='/accounts/login')
def dashboard_choose_view(request):

    if request.method == "POST":

        return redirect('../status/')

        # video = VideoForm(request.POST, request.FILES)
        # if video.is_valid():
        #     current_user_id = request.user.id
        #     handle_uploaded_file(request.FILES['video'], request.POST.get('codigo'), current_user_id)
        #     print("File uploaded successfuly")
        #     HttpResponse("File uploaded successfuly")
        #     return redirect('../choose/')

    elif request.method == "GET":
        # Variables de dashboard
        user_name = str(request.user.username)
        client = MongoClient(key_3)
        db = client.galeria
        collection = db.videos

        list_filename_temp = []
        current_user_id = request.user.id
        myvideos = collection.find({'current_user_id': str(current_user_id)})

        for myvid in myvideos:
            list_filename_temp.append(myvid['static_file_dir'])
        try:
            last_video = list_filename_temp[-1]
        except Exception as e:
            last_video = str(e)

        # list_filename_temp

        # # GET CHUNKS OF THE FILE WITH ID
        # print("GET CHUNKS OF THAT FILE")
        # files_id = ObjectId('5f67ee7920bfdaf148938ccd')
        # thefile = []
        # for chunk in cluster_db['uploaded_videos']['chunks'].find({"files_id": files_id}):
        #     thefile.append(chunk['data'])
        #     pprint.pprint(chunk['_id'])

        with open("models.json", encoding='utf-8', errors='ignore') as json_data:
            myjson = json.load(json_data, strict=False)

        return render(request, 'dashboard/pipeline/choose.html', locals())

import time

@login_required(login_url='/accounts/login')
def dashboard_status_view(request):

    if request.method == "POST":

        return redirect('../results/')
            

    elif request.method == "GET":

        client = MongoClient(key_3)
        db = client.galeria
        collection = db.videos
        user_id = str(request.user.id)
        lista_videos = collection.find_one({"current_user_id": str(user_id)})
        array_results = [lista_videos['models']['order_sequence'],
                        lista_videos['models']['processing_sequence'],
                         ['Cargando...']*len(lista_videos['models']['order_sequence'])]
        array_results = np.array(array_results).T

        user_name = str(request.user.username)

        return render(request, 'dashboard/pipeline/status.html', locals())


@login_required(login_url='/accounts/login')
def dashboard_results_view(request):

    if request.method == "POST":
        pass
        # return redirect('../results/')

    elif request.method == "GET":

        user_name = str(request.user.username)

        return render(request, 'dashboard/pipeline/results.html', locals())


@login_required(login_url='/accounts/login')
def dashboard_utils_view(request):

    myCmd = "ls"
    listoffiles = str(subprocess.check_output(
        myCmd, shell=True).decode("utf-8"))

    myCmd2 = "ls ../"
    listoffiles2 = str(subprocess.check_output(
        myCmd2, shell=True).decode("utf-8"))

    try:
        myCmd3 = "ls ./static/"
        listoffiles3 = str(subprocess.check_output(
            myCmd3, shell=True).decode("utf-8"))
    except Exception as e:
        listoffiles3 = str(e)
        print(e)

    try:
        myCmd4 = "ls ./static/temp_upload/"
        listoffiles4 = str(subprocess.check_output(
            myCmd4, shell=True).decode("utf-8"))
    except Exception as e:
        listoffiles4 = str(e)
        print(e)

    return render(request, 'dashboard/pipeline/utils.html', locals())

# ----------------------- FIN DASHBOARD -----------------

# -------------------- INICIO LOGIN REST_FRAMEWORK -----------------

# -------------------- FIN LOGIN REST_FRAMEWORK -----------------
