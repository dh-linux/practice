from django.http import HttpResponse
from django.shortcuts import render_to_response, render

def search_form(request):
	return render_to_response('search_form.html')

def search(request):
	if 'q' in request.GET:
		message = 'You search : %s' % request.GET['q']
	else:
		message = 'You submitted an empty form.'
	return HttpResponse(message)

def ua(request):
	ua = request.META.get('HTTP_USER_AGENT', 'unknown')
	return HttpResponse("Your brower is %s" % ua)