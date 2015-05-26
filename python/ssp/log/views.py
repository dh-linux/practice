#!coding:utf-8
from django.http import HttpResponse
from django.shortcuts import redirect, render
from log.models import CRoom

def index(request):
    return render(request, 'log/langshou.html')

def app(request, appname):
	return render(request, 'log/langshou.html')