# -*- coding:utf-8 -*-

from authority.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from log.models import Log, log2Extend
from utils.constants import log_level_dict


# our own code

@permission_required('system_manage')
def index(request):
    '''
    logs = Log.objects.order_by("-id")
    paginator = Paginator(logs, 10)
    currentPage = request.POST.get('pageNum', 1)
    
    try:
        pager = paginator.page(currentPage)
    except InvalidPage:
        pager = paginator.page(1)
        
    pager.object_list = log2Extend(pager.object_list)
    return render_to_response("log/index.html",{"log_list":pager}, context_instance=RequestContext(request))
    '''
    return render_to_response("log/index.html",{}, context_instance=RequestContext(request))


@permission_required('system_manage')
def search(request):
    retdir = {}
    if request.POST:
        logs = Log.objects.order_by('-create_time')
        if 'query' in request.POST and request.POST['query']:
            query = request.POST['query'].strip()
            retdir['query'] = query
            logs = logs.filter(username__icontains = query)
        
        paginator = Paginator(logs, 10)
        currentPage = request.POST.get('pageNum', 1)
        try:
            pager = paginator.page(currentPage)
        except InvalidPage:
            pager = paginator.page(1)
        
        pager.object_list = log2Extend(pager.object_list)
        
        return render_to_response('log/search.html', {'log_list':pager,'auth_set':request.session["authority_set"]})
    else:
        return  HttpResponseBadRequest("错误请求")

    
    