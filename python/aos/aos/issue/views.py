from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.contrib.auth.models import User
from issue.models import rt
import simplejson
from role.models import Role

def index(request):
    return render_to_response('issue/index.html',{})

def search(request):
    #retdir = {}
    if request.POST:
        rt_list = rt.objects.order_by('-rt_id')

        if 'query' in request.POST and request.POST['query']:
            query = request.POST['query'].strip()
            #print query,rt_list
            rt_list = rt.objects.filter(rt_id=query)

        paginator = Paginator(rt_list, 10)
        currentPage = request.POST.get('pageNum', 1)
        try:
            pager = paginator.page(currentPage)
        except InvalidPage:
            pager = paginator.page(1)
        
        return render_to_response('issue/search.html', {'rt_list':pager})
    else:
        return  HttpResponseBadRequest("Bad Request!")

def add(request):
    role_list = Role.objects.all()
    if request.POST:
        username = request.POST.get("username")
        realname = request.POST.get("realname")
        email = request.POST.get("email")
        roles = request.POST.getlist("role")
        department = request.POST.get("department")
        phone = request.POST.get("phone")

        leader_username = request.POST.get("leader_username")
        leader_realname = request.POST.get("leader_realname")
        leader_email = request.POST.get("leader_email")
        leader_phone = request.POST.get("leader_phone")
        leader_roles = request.POST.getlist("leader_role")

        usernames = User.objects.filter(username__iexact=username)
        emails = User.objects.filter(email__iexact=email)

        if usernames:
            return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'username is existing'}), mimetype='application/json')
        if emails:
            return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'E-mail is existing'}), mimetype='application/json')

        if leader_username != None and leader_username != '':
            if leader_realname == None or leader_realname == '' or leader_email == None or leader_email == '' or leader_phone == None or leader_phone == '':
                return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'not null'}), mimetype='application/json')
            leader_users = User.objects.filter(username__iexact=leader_username)
            if leader_users:
                leader_user = leader_users[0]
                leader_emails = User.objects.filter(email__iexact=leader_email).exclude(id=int(leader_user.id))
                if leader_emails:
                    return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u' existing'}), mimetype='application/json')
                leader_user.email = leader_email
                leader_user.save()
                userprofile = UserProfile.objects.get(user_id = leader_user.id)
                userprofile.realname = leader_realname
                userprofile.phone = leader_phone
                userprofile.save()
            else:
                leader_emails = User.objects.filter(email__iexact=leader_email)
                if leader_emails:
                    return HttpResponse(simplejson.dumps({"statusCode":403,  "message":u'is existing'}), mimetype='application/json')
                leader_password = make_password(leader_username, salt=None, hasher='default')
                leader_user = User(username=leader_username, email=leader_email, password=leader_password)
                leader_user.save()
                leader_userprofile = UserProfile(user=leader_user, realname=leader_realname, phone=leader_phone)
                leader_userprofile.save()

            for leader_item in leader_roles:
                leader_user.role_set.add(int(leader_item))

            Log(username=request.user.username,log_type=1,relate_id=leader_user.id,content="execute add leader_user " + leader_user.username + " success!", level=1).save()

        password = make_password(username, salt=None, hasher='default')

        user = User(username=username, email=email, password=password)
        user.save()
        userprofile = UserProfile(user=user, department=department, phone=phone, realname=realname,
                                  leader_username=leader_username,
                                  leader_realname=leader_realname,
                                  leader_email=leader_email,
                                  leader_phone=leader_phone)
        userprofile.save()

        for item in roles:
            user.role_set.add(int(item))

        Log(username=request.user.username,log_type=1,relate_id=user.id,content="execute add user " + user.username + " success!", level=1).save()

        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/account/index", "message":u'success'}), mimetype='application/json')

    return render_to_response('account/add.html',{'role_list':role_list},context_instance=RequestContext(request))
