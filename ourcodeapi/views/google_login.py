# views.py

from social_django.utils import psa
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponse


def google_login(request):
    return HttpResponse("Google login test!")

