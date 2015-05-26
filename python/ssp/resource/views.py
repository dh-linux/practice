#!coding:utf-8
from django.http import HttpResponse
from django.shortcuts import redirect, render
from resource.models import Device, Domain
from django import forms

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device

def device_list(request):
    return render(request, 'resource/device/device.html')

def index(request):
    return render(request, 'log/langshou.html')

def app(request,appname):
#   devices = Device.objects.filter(app=appname)
    device = Device()
    devices = device.app_list(appname)
    return render(request, 'resource/device/device.html', {'devices':devices})

def edit_device(request):
    if request.method == "POST":
        df = DeviceForm(request.POST)
        if df.is_valid():
            i_ip = df.cleaned_data['i_ip']
            o_ip = df.cleaned_data['o_ip']
            hostname = df.cleaned_data['hostname']
            serial_number = df.cleaned_data['serial_number']
            cpu_num = df.cleaned_data['cpu_num']
            mem_size = df.cleaned_data['mem_size']
            disk_size = df.cleaned_data['disk_size']
            rack = df.cleaned_data['rack']
            app = df.cleaned_data['app']
            role = df.cleaned_data['role']
            local = df.cleaned_data['local']
            status = df.cleaned_data['status']
            Device.objects.create(i_ip=i_ip, o_ip=o_ip, hostname=hostname, serial_number=serial_number, cpu_num=cpu_num, mem_size=mem_size, disk_size=disk_size, rack=rack, app=app, role=role, local=local, status=status)
            return redirect('/resource/device/')
    else:
        df = DeviceForm()
        return render(request, 'resource/device/edit.html', {'df':df})

