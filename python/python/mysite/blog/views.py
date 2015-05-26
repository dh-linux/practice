from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import models

# Create your views here.

def index(request):
	blog_list = models.Blog.objects.all()
	linux_blog = models.Blog.objects.filter(category_name__name="linux")
	python_blog = models.Blog.objects.filter(category_name__name="python")
	return render_to_response('index.html', {'blog_list':blog_list, 'linux_blog':linux_blog, 'python_blog':python_blog})

def blog_detail(request, blog_id):
	blog = models.Blog.objects.get(id=blog_id)
	return render_to_response('blog_detail.html', {'blog_obj':blog})
