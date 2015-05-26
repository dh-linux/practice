#!coding:utf-8
# from django.http import HttpResponse
# from django.shortcuts import redirect, render
# from resource.models import Device, Domain
# from django import forms
# from django.template import RequestContext
# from django.template import loader
import StringIO
import pycurl
import urllib

#解析url
def opreq(requrl):
    mybuf = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEFUNCTION,mybuf.write)
    c.setopt(pycurl.URL,str(requrl))
    c.setopt(pycurl.HTTPHEADER, ["Accept:application/json"])
    c.perform()
    return mybuf.getvalue()

def opreq_post(requrl, post_dic):
    rs = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.CONNECTTIMEOUT, 3)
    c.setopt(pycurl.WRITEFUNCTION,rs.write)
    c.setopt(pycurl.URL,str(requrl))
    c.setopt(pycurl.HTTPHEADER, ["Accept:application/json"])
    c.setopt(c.POSTFIELDS, str(post_dic))
    c.perform()
    return rs.getvalue()
