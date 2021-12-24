import csv
import json
import os.path

import pandas as pd
from django.db.models import ProtectedError, manager
from django.utils import timezone

from Estate1.settings import BASE_DIR
from client.models import Client
from django.http import HttpResponse, JsonResponse

from ErrorProcess import errorMessage as eM

from project.models import Project

# http://127.0.0.1:8000/project/add_project
from task.models import TaskDistribution
from user.models import Manager


def add_project(request):
    if request.method == 'POST':
        if request.body:
            req = json.loads(request.body)
            project_name = req.get('project_name', '')
            project_schedule = req.get('project_schedule', '')
            project_price = req.get('project_price', '')
            project_beg_time = req.get('project_beg_time', '') #  timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            project_person_in_charge = req.get('project_person_in_charge', '')
            project_state = req.get('project_state', '未开始')
            # manager_id = req.get('manager_id')
            try:
                ci = req.get('client_id')
                if ci == '':
                    return JsonResponse(eM.errorCode400('客户id不正确'), safe=False)
            except Exception as e:
                print(e)
                return JsonResponse(eM.errorCode400('客户id不正确'), safe=False)
            pro = Project.objects.create(client_id=ci, project_name=project_name, project_price=project_price,
                                         project_beg_time=project_beg_time,
                                         project_person_in_charge=project_person_in_charge, project_state=project_state,
                                         project_schedule=project_schedule)
            # manager = Manager.objects.get(manager_id=manager_id)
            # if manager:
            #     pro.manager_set.add(manager)
            # else:
            #     return JsonResponse(eM.errorCode404('主管不存在'), safe=False)
            if pro:
                info = eM.successCode('录入成功')
                info['data'] = {
                    'project_id': pro.project_id,
                    'project_name': pro.project_name,
                    'project_price': pro.project_price,
                    'project_beg_time': pro.project_beg_time,
                    'project_person_in_charge': pro.project_person_in_charge,
                    'project_state': pro.project_state,
                    'project_schedule': pro.project_schedule,
                    'client_name': Client.objects.get(client_id=ci).client_name
                }
                return JsonResponse(info, safe=False)
            else:
                return JsonResponse(eM.errorCode404('录入失败'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)


# http://127.0.0.1:5000/project/find_all
# 拿主管id
def find_all(req):
    if req.method == 'GET':
        cs = Project.objects.all()
        cs_new = []
        for c in list(cs.values()):
            try:
                c['client_name'] = Client.objects.get(client_id=c['client_id']).client_name
            except Exception as e:
                print(e)
                return JsonResponse(eM.errorCode400('客户不存在'), safe=False)
            cs_new.append(c)
        info = eM.successCode('查询成功')
        info['data'] = cs_new
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 根据主管id找到它的项目
# http://127.0.0.1:5000/project/find_project_of_manager/4
def find_project_of_manager(request,  manager_id):
    if request.method == 'GET':
        manager = Manager.objects.get(manager_id=manager_id)
        projects = manager.project_manager.all().values()
        p = []
        for project in projects:
            p.append(list(Project.objects.filter(project_id=project.project_id)))
        info = eM.successCode('查询成功')
        info['data'] = p
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 根据项目id找到它的项目
# http://127.0.0.1:5000/project/find_project/4
def find_project(request,  project_id):
    if request.method == 'GET':
        try:
            pro = Project.objects.get(project_id=project_id)
            info = eM.successCode('查询成功')
            info['data'] = {
                'project_id': pro.project_id,
                'project_name': pro.project_name,
                'project_price': pro.project_price,
                'project_beg_time': pro.project_beg_time,
                'project_person_in_charge': pro.project_person_in_charge,
                'project_state': pro.project_state,
                'project_schedule': pro.project_schedule,
                'client_name': Client.objects.get(client_id=pro.client.client_id).client_name
            }
        except Exception as e:
            print(e)
            return JsonResponse('项目查找失败', safe=False)
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 根据员工id找到它的项目
# http://127.0.0.1:5000/project/find_project_of_staff/4
def find_project_of_staff(request, staff_id):
    if request.method == 'GET':
        tds = TaskDistribution.objects.filter(staff_id=staff_id).values()
        pids = set()
        for t in tds:
            pids.add(t['project_id'])
        ps = []
        for pid in pids:
            p = list(Project.objects.filter(project_id=pid).values())
            p[0]['client_name'] = Client.objects.get(client_id=p[0]['client_id']).client_name
            ps.append(p)
        info = eM.successCode('查询成功')
        info['data'] = ps
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# http://127.0.0.1:5000/project/modify_project/project_id
def modify_project(request, project_id):
    if request.method == 'POST':
        if request.body:
            req = json.loads(request.body)
            pro = Project.objects.get(project_id=project_id)
            pro.project_name = req.get('project_name', '空')
            pro.project_schedule = req.get('project_schedule', '0')
            pro.project_price = req.get('project_price', '0')
            pro.project_person_in_charge = req.get('project_person_in_charge', '*')
            pro.save()
            if pro:
                return JsonResponse(eM.successCode('录入成功'), safe=False)
            else:
                return JsonResponse(eM.errorCode404('录入失败'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# http://127.0.0.1:5000/project/modify_project_schedule
def modify_project_schedule(request):
    if request.method == 'POST':
        project_id = request.GET.get('project_id')
        project_state = request.GET.get('project_state')
        pro = Project.objects.get(project_id=project_id)
        if '后期'in project_state:
            pro.project_schedule = 66
        elif '渲染' in project_state:
            pro.project_schedule = 33
        else:
            pro.project_schedule = 0
        pro.save()
        return JsonResponse(eM.successCode('回滚成功'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)


def project_report_form(req):
    if req.method == 'GET':
        # 找到所有的客户信息。
        ps = Project.objects.all().values()
        # 客户信息添加到info中，info是一个字典
        df = pd.DataFrame(ps)
        df.to_csv(os.path.join(BASE_DIR, "static", "report_form/project_info.csv"), index=0)
        response = HttpResponse(content_type='text/csv')
        # 添加返回头说明如何处理这个返回对象，并指明文件名。attachment：作为附件的形式进行下载
        response['Content-Disposition'] = "attachment;filename=project_info.csv"
        # 创建写的对象
        writer = csv.writer(response)
        # 写入一行数据
        writer.writerow(df.columns)
        # 写入下一行数据
        for d in df.values:
            writer.writerow(d)
        return response
    else:
        return JsonResponse(eM.errorCode400('错误请求'), safe=False)

def delete_project(request, project_id):
    if request.method == 'DELETE':
        try:
            pro = Project.objects.get(project_id=project_id)
            pro.delete()
            return JsonResponse(eM.successCode('删除成功'), safe=False)
        except Client.DoesNotExist:
            return JsonResponse(eM.errorCode404('删除失败'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

