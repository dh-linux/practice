#!coding:utf-8
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from django.shortcuts import redirect, render, render_to_response
from django.core.paginator import Paginator
from django.conf import settings
from resource.models import Domain
from plan.models import Vip, PlanHistory
from ssp.utils import tools
import datetime, types
from django.utils import simplejson
from django.core.paginator import Paginator
from django.db.models.query_utils import Q

def get_domain():
   dname_list = []
   dname_dict = Domain.objects.values("dname").distinct()
   for dname in dname_dict:
       dname_list.append(dname.get("dname"))
   return dname_list

def get_data(dname):
    data = []
    url = "http://rdop.matrix.sina.com.cn/dns/index.php/Interface/domain?dname=%s" % dname
    for i in simplejson.loads(tools.opreq(url)):
        if i.get("type") == "A"  and i.get("data") not in data:
            data.append(i.get("data"))
    return data 

def get_vip_jifang(vip):
    v = Vip.objects.filter(vip=vip).values()
    if v:
        jf = v[0]['m_room']
    else:
        url = "http://duomo.intra.sina.com.cn/?r=duomoRest/api"
        vpp = vip + ":80"
        post_dic = '{"action":"getByVip","vip":"%s"}' % vpp
        rs = simplejson.loads(tools.opreq_post(url, post_dic))
        weight = len(rs['datas'][0].get('poolmember'))*10
        jf = rs['datas'][0]['group'].split('.')[-1]
        Vip.objects.create(vip=vip, m_room=jf, vweight=weight)
    return jf.lower()

def index(request):
    return render(request, 'plan/index.html')

def route(request):
    if request.method == "POST":
        yuan_type=request.POST.get("yuan_type")
        if yuan_type == "jf_plan":
            return redirect("/plan/list/jifang/")
        elif yuan_type == "domain_plan":
            return redirect("/plan/list/domain/")
    else:
        return render(request, "error.html")

#域名数据处理
def list(request, style):
    if style == "jifang":
        if request.method == "POST":       
            jifang = request.POST.get('jifang')
            domain_vj = []
            dname_list = get_domain()
            for dname in dname_list:
                vip_jf_dict = {}
                vj = []
                vips = get_data(dname)
                for vip in vips:
                    vip_jf = get_vip_jifang(vip)
                    vj.append({'vip':vip,'jf':vip_jf})
                if jifang in [i['jf'] for i in vj]:
                    domain_vj.append({'dname':dname,'vj':vj,'jf':jifang})
            return HttpResponse(simplejson.dumps(domain_vj, ensure_ascii=False))
        else:
            return render(request, "plan/jifang_plan.html")
    elif style == "domain":
        pass
    else:
        pass

def processing_data(a,b):
    a_bili = {}
    b_bili = {}
    for i in a:
        a_bili[i] = a[i]*sum(b.values())/sum(a.values())
    
    for i in b:
        b_bili[i] = b[i]
    
    a_bili_list = sorted(a_bili.iteritems(), key=lambda d:d[1])
    b_bili_list = sorted(b_bili.iteritems(), key=lambda d:d[1])
    
    ba_dict = {}
    
    x=0
    for b_item in b_bili_list:
        ba_dict[b_item[0]] = []
        a = 0
        i = 0
        for a_item in a_bili_list:
            if x < (len(b_bili_list) - 1):
                a += a_item[1]
                if len(ba_dict[b_item[0]]) > 1 and a > b_item[1]:
                    break
                ba_dict[b_item[0]].append(a_item[0])
                del a_bili_list[i]
                i+=1
            else:
                ba_dict[b_item[0]].append(a_item[0])
        x+=1

    c = {}

    for k in ba_dict:
        for v in ba_dict[k]:
            c[v] = k
    return c
     

def result(request, rsst):
    if rsst == "jifang":
        dname_sd = []
        change = []
        dname = request.POST
        for dname in request.POST.getlist('dname'):
            dname_sd.append({'dname':dname, 'dname_svip':request.POST.getlist('svip_'+dname), 'dname_dvip':request.POST.getlist('dvip_'+dname)})  
        for item in dname_sd:
            dname = item['dname']
            for svip in item['dname_svip']:
                view_list = view_list = Domain.objects.filter(dname=dname, data=svip).values_list('view', flat=True)
                view_dict = {}
                for i in view_list:
                    view_dict[i] = Domain.objects.get(view=i).dweight

                dvip_dict={}
                for j in item['dname_dvip']:
                    dvip_dict[j]=Vip.objects.get(vip=j).vweight

                view_vip_dict = processing_data(view_dict, dvip_dict)
                for view, dvip in view_vip_dict.iteritems():
                    change.append({'domain':dname, 'from':svip, 'group':view, 'to':dvip, 'ttl':60})

        post_dic = {"key":"e161db4e35aa3017a4c49ecb", "change":change}
        url = 'http://10.212.0.62:8080/api'
        print post_dic
        rs = simplejson.loads(tools.opreq_post(url, simplejson.dumps(post_dic)))
        print rs
        if int(rs['code']) == 0:
            status = 'y'
#            for item in change:
#                s_obj = Domain.objects.get(dname=item['domain'], view=item['group'])
#                s_obj.data = item['to']
#                s_obj.save()
        else:
            status = 'n'
        Hdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        PlanHistory.objects.create(PID=rs['taskId'], user='yadong3', status=status, date=Hdate)

        return HttpResponse(simplejson.dumps(rs))
    elif rsst == "domain":
        pass
    else:
        pass

def taskapi(request):
    post_data = request.POST.get('search_data')
    if post_data:
        try:
            search_data = int(post_data)
        except:
            search_data = post_data
        if type(search_data) is types.IntType:
            tasks = PlanHistory.objects.filter(PID=search_data)
        else:
            tasks = PlanHistory.objects.filter((Q(user=search_data)|Q(date=search_data)))
    else:
        tasks = PlanHistory.objects.all()
    page_tasks = Paginator(tasks, 10)
    page = request.POST.get('page')
    page_task = page_tasks.page(page)
    task_list = [{'PID':task_obj.PID, 'user':task_obj.user, 'date':task_obj.date, 'status':task_obj.get_status_display()} for task_obj in page_task]
    return HttpResponse(simplejson.dumps(task_list))

def  task(request):
    if request.method == "POST":
        post_data = request.POST.get('search')
        try:
            search_data = int(post_data)
        except:
            search_data = post_data

        if type(search_data) is types.IntType:
            tasks = PlanHistory.objects.filter(PID=search_data)
        else:
            tasks = PlanHistory.objects.filter((Q(user=search_data)|Q(date=search_data)))
    else:
        search_data = ""
        tasks = PlanHistory.objects.all()
    print search_data
    page_tasks = Paginator(tasks, 10)
    page_task = page_tasks.page(1)
    task_count = page_tasks.count
    page_list = range(1, page_tasks.num_pages+1)
    return render(request, "plan/history.html", {'tasks':tasks, 'page_list':page_list, 'task_count':task_count, 'page_task':page_task, 'search_data':search_data})