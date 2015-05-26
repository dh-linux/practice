#!coding:utf-8

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.template import loader
from django.utils import simplejson
from ssp.utils import tools
from resource.models import Domain,VieWeight
from resource.service import weight


VIP_API= 'http://rdop.matrix.sina.com.cn/loadbalance/index.php/Interface/vip?vip='
DOMAIN_API = 'http://rdop.matrix.sina.com.cn/dns/index.php/Interface/domain?dname='

def index(request):
    t = loader.get_template('resource/domain/addnew.html')
    # c = RequestContext(request, {'SIDEBAR': settings.SIDEBAR})
    c = RequestContext(request)
    return HttpResponse(t.render(c))

def addNew2DB(request,insert_ids):
    insert_list = []
    for insert_id in insert_ids:
        view = request.POST.get('attach_' + insert_id, '')
        dweight = weight.get_weight(view)
        insert_info = Domain(
            dname        =request.POST.get('dname_' + insert_id, ''),
            is_dynamic   =request.POST.get('dynamic_' + insert_id, ''),
            view         =view,
            type         =request.POST.get('type_' + insert_id, ''),
            data         =request.POST.get('data_' + insert_id, ''),
            app          =request.POST.get('gname_' + insert_id, ''),
            status       =request.POST.get('enabled_' + insert_id, ''),
            dweight      =dweight
            )
        insert_list.append(insert_info)
    return Domain.objects.bulk_create(insert_list)

def addNew(request):
    insert_ids = request.POST.getlist('dinfo')
    rs={}
    #print 'dname_' + insert_ids[0],request.POST.get('dname_' + insert_ids[0])
    if insert_ids:
        if Domain.objects.filter(dname=request.POST.get('dname_' + insert_ids[0])).count() > 0:
            if simplejson.loads(request.POST.get('force_add')) == 1:
                Domain.objects.filter(dname=request.POST.get('dname_' + insert_ids[0])).delete()
                rs['code'] = addNew2DB(request, insert_ids) and True or False
            else:
                rs['code'] = True
                rs['msg'] = '域名相关数据已经存在，如需更新请点击强制录入'
        else:
            rs['code'] = addNew2DB(request, insert_ids) and True or False
    else:
        rs['code'] = False
    return HttpResponse(simplejson.dumps(rs, ensure_ascii=False))

def ajGetInfo(request):
    rs={}
    data = []
    dsrc = request.POST.get('dsrc', '')
    typ = request.POST.get('type', '')
    if typ == 'domain':
        url = DOMAIN_API + dsrc
    elif typ == 'vip':
        url = VIP_API + dsrc
    data_all = simplejson.loads(tools.opreq(url))
    for item in data_all:
        if item.get("enabled") == "true":
            data.append(item)
    rs['type']=typ
    rs['data']=data
    return HttpResponse(simplejson.dumps(rs, ensure_ascii=False))

def viewInfo(request):
    t = loader.get_template('resource/domain/viewinfo.html')
    # c = RequestContext(request, {'SIDEBAR': settings.SIDEBAR})
    c = RequestContext(request)
    return HttpResponse(t.render(c))

def ajGetDomainInfoFromDB(request):
    domain_info_tmp, rs, data_tmp = {}, {}, []
    get_domain_infos = Domain.objects.filter(dname=request.POST.get('dname')).all()
    for domain_info in get_domain_infos:
        domain_info_tmp['dname'] = domain_info.dname
        domain_info_tmp['is_dynamic'] = domain_info.is_dynamic
        domain_info_tmp['view'] = domain_info.view
        domain_info_tmp['type'] = domain_info.type
        domain_info_tmp['data'] = domain_info.data
        domain_info_tmp['app'] = domain_info.app
        domain_info_tmp['status'] = domain_info.status
        print domain_info_tmp
        data_tmp.append(domain_info_tmp)
    print data_tmp
    if data_tmp:
        rs['data']=data_tmp
        rs['code']=True
    else:
        rs['code']=False
    return HttpResponse(simplejson.dumps(rs, ensure_ascii=False))

def handles(request, act):
    if act=='index':
        return index(request)
    elif act=='add':
        return addNew(request)
    elif act=='getinfo':
        return ajGetInfo(request)
    elif act=='view':
        return viewInfo(request)
    elif act=='queryinfo':
        return ajGetDomainInfoFromDB(request)

def addweight(request):
    view = request.GET['view']
    weight = request.GET['weight']
    typ    = request.GET.get('type')
    force  = request.GET.get('force')

    if VieWeight.objects.filter(view=view).count() > 0:
        if force != "1":
            return HttpResponse("相关VIEW存在，如需变更请加参数force=1")
        else:
            VieWeight.objects.save(view=view, weight=weight, typ=typ, force_update=True)
            return HttpResponse("ok")
    else:
        VieWeight.objects.create(view=view, weight=weight, typ=typ)
        return HttpResponse("ok")