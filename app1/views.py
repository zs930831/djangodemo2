# coding=utf-8
from django.shortcuts import render, HttpResponse, redirect
from app1 import models
import json

# Create your views here.
def busniess(request):
    # QuerySet
    # [obj1('id','caption','code'),obj1('id','caption','code').....]
    v1 = models.Business.objects.all()
    # QuerySet
    # dic [{'id':'1','caption':sa},{'id':'1','caption':sa}....]
    v2 = models.Business.objects.all().values("id", "caption")
    # QuerySet
    # tuple:[(1,sa),(2,sb)]
    v3 = models.Business.objects.all().values_list("id", "caption")
    return render(request, "business.html", {"v1": v1, "v2": v2, "v3": v3})

def host(request):
    if request.method == "GET":
        obj = models.Host.objects.filter(nid__gt=0)
        # 用双下划线去执行跨表取的操作
        obj1 = models.Host.objects.all().values("nid", "hostname", "b_id", "b__caption")
        #元组obj2
        obj2 = models.Host.objects.all().values_list("nid", "hostname", "b_id", "b__caption")
        b_list = models.Business.objects.all()
        return render(request, "host.html", {"obj": obj, 'obj1': obj1, 'obj2': obj2, 'b_list': b_list})
    elif request.method == "POST":
        h = request.POST.get("hostname")
        i = request.POST.get("ip")
        p = request.POST.get("port")
        b = request.POST.get("b_id")
        models.Host.objects.create(hostname=h,
                                   ip=i,
                                   port=p,
                                   b_id=b)
        return redirect("/host")


def test(request):
    ret={"status":200,"error":None,"data":None}
    try:
        h = request.POST.get("hostname")
        i = request.POST.get("ip")
        p = request.POST.get("port")
        b = request.POST.get("b_id")
        if h and len(h) > 5:
            models.Host.objects.create(hostname=h,
                                       ip=i,
                                       port=p,
                                       b_id=b)

        else:
            ret["status"]=500
            ret["error"]="太短了"
    except Exception as e:
        ret["status"] = 500
        ret["error"] = "出错了"
    return HttpResponse(json.dumps(ret))

def test1(request):
    ret={"status":200,"error":None,"data":None}
    try:
        n = request.POST.get("nid")
        h = request.POST.get("hostname")
        i = request.POST.get("ip")
        p = request.POST.get("port")
        b = request.POST.get("b_id")
        if h and len(h) > 5:
            models.Host.objects.filter(nid=n).update(hostname=h,
                                       ip=i,
                                       port=p,
                                       b_id=b)

        else:
            ret["status"]=500
            ret["error"]="更新出错"
    except Exception as e:
        ret["status"] = 500
        ret["error"] = "出错了"
    return HttpResponse(json.dumps(ret))

def app(request):
    if request.method=="GET":
        applist=models.Application.objects.all()
        # for app in applist:
        #     print(app.name,app.r.all())
        #     for a in app.r.all():
        #         print(a.hostname,a.ip)
        hostlist=models.Host.objects.all()
        return render(request,"app.html",{"applist":applist,"hostlist":hostlist})
    elif request.method=="POST":
        appname=request.POST.get("appname")
        hostlist=request.POST.getlist("hostlist")
        obj=models.Application.objects.create(name=appname)
        obj.r.add(*hostlist)
        return redirect("/app")

def ajax_app(request):
    ret={"status":200,"data":None,"error":None}
    try:
        appname = request.POST.get("appname")
        hostlist = request.POST.getlist("hostlist")
        if hostlist and appname:
            obj = models.Application.objects.create(name=appname)
            obj.r.add(*hostlist)
        else:
            ret["status"] = 500
            ret["error"]="appname或者hostlist为空"
    except Exception as e:
        ret["error"]="出错了"
        ret["status"]=500
    print (appname,ret)
    return HttpResponse(json.dumps(ret))