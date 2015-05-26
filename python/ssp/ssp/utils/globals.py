#!coding:utf-8
# from django.http import HttpResponse
# from django.shortcuts import redirect, render
# from resource.models import Device, Domain
# from django import forms
# from django.template import RequestContext
# from django.template import loader
from django.conf import settings

def configs(request):
    context = {
        'SIDEBAR':settings.SIDEBAR,
        'REQ_PATH':request.path,
        'URL_ROOT':'http://' + request.get_host(),
    }
    return context