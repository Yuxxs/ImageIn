from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_list_or_404, redirect
import datetime
# Create your views here.
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

import mainapp
from mainapp.models import *

from mainapp.serializers import *
from mainapp.forms import *
from mainapp.filters import *

def index(request):
    return HttpResponse("Hello World. First Django Project. PythonCircle.Com")