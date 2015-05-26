# -*- coding:utf-8 -*-

# django library
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.utils.translation import ugettext_lazy as _
import simplejson
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# our own code
from authority.models import Permission
from log.models import Log
from authority.decorators import permission_required
from utils.constants import permission_type_dict


# 显示用户列表
@permission_required('authority_manage')
def index(request):
    return render_to_response('authority/index.html',{}, context_instance=RequestContext(request))

@permission_required('authority_manage')
def search(request):
    retdir = {}
    if request.POST:
        permissions = Permission.objects.order_by('type')
        if 'query' in request.POST and request.POST['query']:
            query = request.POST['query'].strip()
            retdir['query'] = query
            permissions = permissions.filter(Q(codename__icontains = query) | Q(desc__icontains = query))
        
        paginator = Paginator(permissions, 10)
        currentPage = request.POST.get('pageNum', 1)
        try:
            pager = paginator.page(currentPage)
        except InvalidPage:
            pager = paginator.page(1)
        
        return render_to_response('authority/search.html', {'permission_list':pager, 'permission_type_dict':permission_type_dict, 'auth_set':request.session["authority_set"]})
    else:
        return  HttpResponseBadRequest("错误请求")

    
# 删除记录
@permission_required('authority_manage')
def delete(request, authority_id):
    permission = None
    try:
        permission = Permission.objects.get(id = int(authority_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400,"message":u'此权限不存在!'}), mimetype='application/json')
    # 删除此权限
    permission.delete()
    # 日志
    Log(username=request.user.username,log_type=1,relate_id=authority_id,content="execute delete permission " + permission.codename + " success!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/authority/index", "message":u'删除成功'}), mimetype='application/json')


@permission_required('authority_manage')
def add(request):
    if request.POST:
        codename = request.POST.get("codename")
        desc = request.POST.get("desc")
        type = request.POST.get("type")
        # 验证重复的codename
        permissions = Permission.objects.filter(codename__iexact=codename)
        if permissions:
            return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'此权限已经存在不能添加'}), mimetype='application/json')
        
        permission = Permission(codename=codename, desc=desc, type=type)
        permission.save()
        
        # 日志
        Log(username=request.user.username,log_type=1,relate_id=permission.id,content="execute add permission " + permission.codename + " success!", level=1).save()
        
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/authority/index", "message":u'添加成功'}), mimetype='application/json')
    
    return render_to_response('authority/add.html', {'permission_type_dict':permission_type_dict}, context_instance=RequestContext(request))


# 编辑
@permission_required('authority_manage')
def edit(request, authority_id):
    permission = None
    try:
        permission = Permission.objects.get(id = int(authority_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400,"message":u'此权限不存在!'}), mimetype='application/json')
    if not permission:
        return HttpResponseBadRequest(u"错误请求")
    if request.POST:
        permission.codename = request.POST.get("codename")
        permission.desc = request.POST.get("desc")
        permission.type = request.POST.get("type")
        permission.save()
        
        # 日志
        Log(username=request.user.username,log_type=1,relate_id=authority_id,content="execute edit permission " + permission.codename + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/authority/index", "message":u'编辑成功'}), mimetype='application/json')  
    return render_to_response('authority/edit.html', {'permission':permission, 'permission_type_dict':permission_type_dict}, context_instance=RequestContext(request))

