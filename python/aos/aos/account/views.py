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
from account.models import UserProfile 
from account.models import getUser,user2Extend
from role.models import Role 
from log.models import Log
from authority.decorators import permission_required


# 显示用户列表
@permission_required('user_manage')
def index(request):
    return render_to_response('account/index.html',{}, context_instance=RequestContext(request))

@permission_required('user_manage')
def search(request):
    retdir = {}
    if request.POST:
        users = User.objects.order_by('-id')
        if 'query' in request.POST and request.POST['query']:
            query = request.POST['query'].strip()
            retdir['query'] = query
            users = users.filter(Q(username__icontains = query) | Q(userprofile__realname__icontains = query))
        
        paginator = Paginator(users, 10)
        currentPage = request.POST.get('pageNum', 1)
        try:
            pager = paginator.page(currentPage)
        except InvalidPage:
            pager = paginator.page(1)
        
        pager.object_list = user2Extend(pager.object_list)
        
        return render_to_response('account/search.html', {'user_list':pager,'auth_set':request.session["authority_set"]})
    else:
        return  HttpResponseBadRequest("错误请求")

    
# 删除记录
@permission_required('user_manage')
def delete(request, user_id):
    user = None
    try:
        user = User.objects.get(id = int(user_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400,"message":u'此用户不存在!'}), mimetype='application/json')
    # 删除用户对应的扩展表 UserProfile 中的记录
    UserProfile.objects.get(user_id = user.id).delete()
    # 删除此用户与角色的关联关系
    user.role_set.clear()
    # 删除此用户与权限的关联关系
    user.permission_set.clear()
    # 删除此用户
    user.delete()
    # 日志
    Log(username=request.user.username,log_type=1,relate_id=user_id,content="execute delete user " + user.username + " success!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/account/index", "message":u'删除成功'}), mimetype='application/json')

@permission_required('user_manage')
def add(request):
    role_list = Role.objects.all()
    if request.POST:
        username = request.POST.get("username")
        realname = request.POST.get("realname")
        email = request.POST.get("email")
        roles = request.POST.getlist("role")
        department = request.POST.get("department")
        phone = request.POST.get("phone")
        
        # 审批领导信息
        leader_username = request.POST.get("leader_username")
        leader_realname = request.POST.get("leader_realname")
        leader_email = request.POST.get("leader_email")
        leader_phone = request.POST.get("leader_phone")
        leader_roles = request.POST.getlist("leader_role")
        
        # 验证重复的帐号名
        usernames = User.objects.filter(username__iexact=username)
        # 验证重复的邮件地址
        emails = User.objects.filter(email__iexact=email)
        
        if usernames:
            return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'用户名已经存在不能添加'}), mimetype='application/json')
        if emails:
            return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'邮件地址已经存在不能添加'}), mimetype='application/json')
        
        # 验证审批领导用户名是否存在
        if leader_username != None and leader_username != '':
            # 验证审批领导真实姓名或邮件是否为空
            if leader_realname == None or leader_realname == '' or leader_email == None or leader_email == '' or leader_phone == None or leader_phone == '':
                return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'审批领导中真实姓名/邮件/联系方式为空不能添加'}), mimetype='application/json')
            # 判断审批领导是否已经存在于当前系统中
            leader_users = User.objects.filter(username__iexact=leader_username)
            if leader_users:
                leader_user = leader_users[0]
                # 验证重复的邮件地址
                leader_emails = User.objects.filter(email__iexact=leader_email).exclude(id=int(leader_user.id))
                if leader_emails:
                    return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'审批领导邮件地址已经存在不能添加'}), mimetype='application/json')
                leader_user.email = leader_email
                leader_user.save()
                userprofile = UserProfile.objects.get(user_id = leader_user.id)
                userprofile.realname = leader_realname
                userprofile.phone = leader_phone
                userprofile.save()
            else:
                # 验证重复的邮件地址
                leader_emails = User.objects.filter(email__iexact=leader_email)
                if leader_emails:
                    return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'审批领导邮件地址已经存在不能添加'}), mimetype='application/json')
                leader_password = make_password(leader_username, salt=None, hasher='default')
                leader_user = User(username=leader_username, email=leader_email, password=leader_password)
                leader_user.save()
                leader_userprofile = UserProfile(user=leader_user, realname=leader_realname, phone=leader_phone)
                leader_userprofile.save()
            
            # 审批领导用户保存角色信息
            for leader_item in leader_roles:
                leader_user.role_set.add(int(leader_item))
            
            # 日志
            Log(username=request.user.username,log_type=1,relate_id=leader_user.id,content="execute add leader_user " + leader_user.username + " success!", level=1).save()
        
        # 保存用户信息
        # 密码由用户名单向散列得到,实际登录时使用LADP 验证真正的用户名和密码
        password = make_password(username, salt=None, hasher='default')
        
        user = User(username=username, email=email, password=password)
        user.save()
        userprofile = UserProfile(user=user, department=department, phone=phone, realname=realname, 
                                  leader_username=leader_username, 
                                  leader_realname=leader_realname, 
                                  leader_email=leader_email, 
                                  leader_phone=leader_phone)
        userprofile.save()
        
        # 保存角色信息 
        for item in roles:
            user.role_set.add(int(item))
        
        # 日志
        Log(username=request.user.username,log_type=1,relate_id=user.id,content="execute add user " + user.username + " success!", level=1).save()
        
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/account/index", "message":u'添加成功'}), mimetype='application/json')
    
    return render_to_response('account/add.html',{'role_list':role_list},context_instance=RequestContext(request))

# 编辑
@permission_required('user_manage')
def edit(request, user_id):
    user = getUser(int(user_id));
    role_list = Role.objects.all()
    if not user:
        return HttpResponseBadRequest(u"错误请求")
    if request.POST:
        department = request.POST.get("department")
        realname = request.POST.get("realname")
        phone = request.POST.get("phone")
        roles = request.POST.getlist("role")
        
        # 审批领导信息
        leader_username = request.POST.get("leader_username")
        leader_realname = request.POST.get("leader_realname")
        leader_email = request.POST.get("leader_email")
        leader_phone = request.POST.get("leader_phone")
        leader_roles = request.POST.getlist("leader_role")
        
        # 验证审批领导用户名是否为空
        if leader_username != None and leader_username != '':
            # 验证审批领导真实姓名或邮件是否为空
            if leader_realname == None or leader_realname == '' or leader_email == None or leader_email == '' or leader_phone == None or leader_phone == '':
                return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'审批领导中真实姓名/邮件/联系方式为空不能修改'}), mimetype='application/json')
            # 判断审批领导是否已经存在于当前系统中
            leader_users = User.objects.filter(username__iexact=leader_username)
            if leader_users:
                leader_user = leader_users[0]
                # 验证重复的邮件地址
                leader_emails = User.objects.filter(email__iexact=leader_email).exclude(id=int(leader_user.id))
                if leader_emails:
                    return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'审批领导邮件地址已经存在不能修改'}), mimetype='application/json')
                leader_user.email = leader_email
                leader_user.save()
                userprofile = UserProfile.objects.get(user_id = leader_user.id)
                userprofile.realname = leader_realname
                userprofile.phone = leader_phone
                userprofile.save()
            else:
                # 验证重复的邮件地址
                leader_emails = User.objects.filter(email__iexact=leader_email)
                if leader_emails:
                    return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'审批领导邮件地址已经存在不能添加'}), mimetype='application/json')
                leader_password = make_password(leader_username, salt=None, hasher='default')
                leader_user = User(username=leader_username, email=leader_email, password=leader_password)
                leader_user.save()
                leader_userprofile = UserProfile(user=leader_user, realname=leader_realname, phone=leader_phone)
                leader_userprofile.save()
            
            # 审批领导用户重置角色信息
            leader_user.role_set.clear()
            for leader_item in leader_roles:
                leader_user.role_set.add(int(leader_item))
            
            # 日志
            Log(username=request.user.username,log_type=1,relate_id=leader_user.id,content="execute edit leader_user " + leader_user.username + " success!", level=1).save()
        
        
        userprofile = UserProfile.objects.get(user_id = user.id)
        userprofile.department = department
        userprofile.phone = phone
        userprofile.realname = realname
        userprofile.leader_username = leader_username
        userprofile.leader_realname = leader_realname
        userprofile.leader_email = leader_email
        userprofile.leader_phone = leader_phone
        userprofile.save()
        
        #重置角色信息
        auth_user = User.objects.get(id=int(user_id))
        auth_user.role_set.clear()
        for item in roles:
            auth_user.role_set.add(int(item))
        
        # 日志
        Log(username=request.user.username,log_type=1,relate_id=user_id,content="execute edit user " + user.username + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/account/index", "message":u'编辑成功'}), mimetype='application/json')  
    return render_to_response('account/edit.html', {'user': user,'role_list':role_list},context_instance=RequestContext(request))

