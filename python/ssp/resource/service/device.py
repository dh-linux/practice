#!coding:utf-8
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from django.conf import settings
from resource.models import Device
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
import types, json

def app_list(request,appname):
    device = Device()
    devices = device.get_all_host(appname)
    page_devices = Paginator(devices, 10)
    page_arg = request.GET.get('page')
    if page_arg:
        page = int(page_arg)
    else:
        page = 1
    page_device = page_devices.page(page)
    device_count = page_devices.count
    page_count = range(1,page_devices.num_pages+1)
    return render(request, 'resource/device/device.html', {'appname':appname,'page':page,'page_device':page_device,'device_count':device_count,'page_count':page_count})

def search_list(request):
    if request.method == "POST":
        search_field_post = request.POST.get('search', 'NONE')
        search_field = search_field_post.strip()
        device = Device()
        search_devices = device.search_host(search_field)
        #print search_devices
        page_devices = Paginator(search_devices, 10)
        page_device = page_devices.page(1)
        device_count = page_devices.count
        page_count = range(1,page_devices.num_pages+1)
        return render(request, 'resource/device/device.html', {'appname':'search','page':1,'page_device':page_device,'device_count':device_count,'page_count':page_count})


def device_add(request):
    devices_obj = request.POST
    keys_list = ['app', 'cpu_num', 'disk_size', 'hostname', 'i_ip', 'local', 'm_room', 'mem_size', 'o_ip', 'role', 'serial_number', 'status']
    post_keys_list = devices_obj.keys()
    if keys_list == sorted(post_keys_list):
        i_ip = devices_obj.get('i_ip')
        o_ip = devices_obj.get('o_ip')
        hostname = devices_obj.get('hostname')
        serial_number = devices_obj.get('serial_number')
        cpu_num = devices_obj.get('cpu_num')
        mem_size = devices_obj.get('mem_size')
        disk_size = devices_obj.get('disk_size')
        m_room = devices_obj.get('m_room')
        app = devices_obj.get('app')
        role = devices_obj.get('role')
        local = devices_obj.get('local')
        status = devices_obj.get('status')
        Device.objects.create(i_ip=i_ip, o_ip=o_ip, hostname=hostname, serial_number=serial_number, cpu_num=cpu_num, mem_size=mem_size, disk_size=disk_size, m_room=m_room, app=app, role=role, local=local, status=status)
        return HttpResponse("SUCEESS!!")
    else:
        return HttpResponse("Post data ERROR!!")
