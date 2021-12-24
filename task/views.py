import csv
import json
import os

import pandas as pd
from django.db.models import ProtectedError
from django.http import JsonResponse, HttpResponse

from Estate1.settings import BASE_DIR
from user.models import Staff, Manager
from .models import Task, TaskDistribution, TaskAdvise
from ErrorProcess import errorMessage as eM

############################################# task #################################################
# http://127.0.0.1:8000/task/add_task
def add_task(request):
    if request.method == 'POST':
        dj = json.loads(request.body.decode())
        task_info = dj.get('task_info', '')
        cu = Task.objects.create(task_info=task_info)
        if cu:
            return JsonResponse(eM.successCode('录入成功'), safe=False)
        else:
            return JsonResponse(eM.errorCode400('录入失败'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 修改任务 根据id
#  http://127.0.0.1:8000/task/modify_task/1
def modify_task(request, task_id):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            # 根据id查询一个客户对象
            task = Task.objects.get(id=task_id)
            task.task_info = req.get('task_info', '')
            # save方法保存修改的字段
            task.save()
            return JsonResponse(eM.successCode('修改成功'), safe=False)
        except Task.DoesNotExist:
            return JsonResponse(eM.errorCode404('不存在对应的任务'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

#  http://127.0.0.1:8000/task/query_task?task_id=1
def query_task(request):
    if request.method == 'GET':
        task_id = request.GET.get('task_id', '')
        task = Task.objects.filter(task_id=task_id)
        if task:
            info = eM.successCode('查询成功')
            info['data'] = {
                "task_id": task_id,
                "task_info": task.task_info
            }
            return JsonResponse(info, safe=False)
        else:
            return JsonResponse(eM.errorCode404('查询失败，不存在对应的任务'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

#  http://127.0.0.1:8000/task/delete_task/1
def delete_task(request, task_id):
    if request.method == 'DELETE':
        try:
            cli = Task.objects.get(id=task_id)
            cli.delete()
            return JsonResponse(eM.successCode('删除成功'), safe=False)
        except Task.DoesNotExist:
            return JsonResponse(eM.errorCode404('删除失败'), safe=False)
        except ProtectedError:
            return JsonResponse(eM.errorCode403('存在外键约束'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

#  http://127.0.0.1:8000/task/find_all_task
def find_all_task(request):
    if request.method == 'GET':
        cs = Task.objects.all().values()
        info = eM.successCode('查询成功')
        # 客户信息添加到info中，info是一个字典
        info['data'] = list(cs)
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

################################################################################################################
############################################# TaskDistribution #################################################
################################################################################################################

# 导入主管数据到主管表
def import_manager(request):
    managers = Staff.objects.exclude(job__contains='员工')
    ms = Manager.objects.all().values()
    manager_ids = []
    for mi in ms:
        manager_ids.append(mi['manager_id'])
    for manager in managers:
        if manager.staff_id not in manager_ids:
            Manager.objects.create(manager_id=manager.staff_id, manager_name=manager.name, manager_phone=manager.phone,
                                   manager_department=manager.department, manager_job=manager.job, account=manager.account)
    return JsonResponse(eM.successCode('录入成功'), safe=False)


# request必须为第一个参数
# http://127.0.0.1:5000/task/add_task_distribution
def add_task_distribution(request):
    # POST方法发数据， GET方法请求网页
    if request.method == 'POST':
        if request.body:
            dj = json.loads(request.body.decode())  # 获取前端传入的json数据。
            task_info = dj.get('task_info', '')
            task_property = dj.get('task_property', '')
            cu = Task.objects.create(task_info=task_info, task_property=task_property)
            if not cu:
                return JsonResponse(eM.successCode('任务录入失败'), safe=False)
            task_distribution_state = dj.get('task_distribution_state', '已分配')
            task_distribution_is_accepted = dj.get('task_distribution_is_accepted', '否')
            task_distribution_begin_time = dj.get('task_distribution_begin_time', '')
            task_distribution_end_time = dj.get('task_distribution_end_time', '')

            project = dj.get('project_id', '')
            staff = dj.get('staff_id', '')
            manager = int(dj.get('manager_id', ''))
            try:
                ctd = TaskDistribution.objects.create(task_distribution_state=task_distribution_state,
                                                      task_distribution_is_accepted=task_distribution_is_accepted,
                                                      task_distribution_begin_time=task_distribution_begin_time,
                                                      task_distribution_end_time=task_distribution_end_time,
                                                      project_id=project, staff_id=staff, manager_id=manager, task_id=cu.task_id)
            except Exception as e:
                print(e)
                return JsonResponse(eM.errorCode400('项目分配录入失败'), safe=False)
            if ctd:
                return JsonResponse(eM.successCode('录入成功'), safe=False)
            else:
                return JsonResponse(eM.errorCode400('项目分配录入失败'), safe=False)
        else:
            return JsonResponse(eM.errorCode404('body为空'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 通过项目id 和 主管id得到相应的任务信息
# http://127.0.0.1:5000/task/get_task?project_id=3&manager_id=5
def get_task(request):
    if request.method == 'GET':
        mi = request.GET.get('manager_id')
        pi = request.GET.get('project_id')
        td = TaskDistribution.objects.filter(manager_id=mi, project_id=pi).values()
        if td:
            all_task_info = list(td)
            all_task_info_new = []
            for task in all_task_info:
                task1 = Task.objects.get(task_id=task['task_id'])
                task['task_info'] = task1.task_info
                task['task_property'] = task1.task_property
                all_task_info_new.append(task)
            info = eM.successCode('查询成功')
            info['data'] = list(all_task_info_new)
            return JsonResponse(info, safe=False)
        return JsonResponse(eM.errorCode404('没有任务'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 根据员工id得到它的未接受任务。
# http://127.0.0.1:5000/task/get_staff_task/x
def get_staff_task(request, staff_id):
    if request.method == 'GET':
        t = TaskDistribution.objects.filter(staff_id=staff_id, task_distribution_is_accepted='否')
        if t:
            info = eM.successCode('ok')
            all_task_info = list(t.values())
            all_task_info_new = []
            for task in all_task_info:
                task1 = Task.objects.get(task_id=task['task_id'])
                task['task_info'] = task1.task_info
                task['task_property'] = task1.task_property
                all_task_info_new.append(task)
            info['data'] = all_task_info_new
            return JsonResponse(info, safe=False)
        else:
            return JsonResponse(eM.errorCode404('没有新任务'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 根据员工id得到它的已接受任务。
# http://127.0.0.1:5000/task/get_staff_task_accepted/x
def get_staff_task_accepted(request, staff_id):
    if request.method == 'GET':
        t = TaskDistribution.objects.filter(staff_id=staff_id)
        t = t.exclude(task_distribution_is_accepted='否')
        t = t.exclude(task_distribution_is_accepted='已拒绝')
        if t:
            info = eM.successCode('ok')
            all_task_info = list(t.values())
            all_task_info_new = []
            for task in all_task_info:
                task1 = Task.objects.get(task_id=task['task_id'])
                task['task_info'] = task1.task_info
                task['task_property'] = task1.task_property
                all_task_info_new.append(task)
            info['data'] = all_task_info_new
            return JsonResponse(info, safe=False)
        else:
            return JsonResponse(eM.errorCode404('没有任务'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)


# 修改任务已被接受 根据id
#  http://127.0.0.1:5000/task/modify_task_accepted/1
def modify_task_accepted(request, task_distribution_id):
    if request.method == 'POST':
        try:
            # 根据id查询一个客户对象
            task_distribution = TaskDistribution.objects.get(task_distribution_id=task_distribution_id)
            task_distribution.task_distribution_is_accepted = '是'
            # save方法保存修改的字段
            task_distribution.save()
            return JsonResponse(eM.successCode('修改成功'), safe=False)
        except Task.DoesNotExist:
            return JsonResponse(eM.errorCode404('不存在对应的任务'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 修改任务已被拒绝 根据id
# http://127.0.0.1:5000/task/modify_task_reject/1
def modify_task_reject(request, task_distribution_id):
    if request.method == 'POST':
        try:
            # 根据id查询一个客户对象
            print(task_distribution_id)
            task_distribution = TaskDistribution.objects.get(task_distribution_id=task_distribution_id)
            task_distribution.task_distribution_is_accepted = '已拒绝'
            # save方法保存修改的字段
            task_distribution.save()
            return JsonResponse(eM.successCode('修改成功'), safe=False)
        except Task.DoesNotExist:
            return JsonResponse(eM.errorCode404('不存在对应的任务'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)


# 修改任务已被接受 根据id
#  http://127.0.0.1:5000/task/modify_task_finished/1
def modify_task_finished(request, task_distribution_id):
    if request.method == 'POST':
        try:
            task_distribution = TaskDistribution.objects.get(task_distribution_id=task_distribution_id)
            task_distribution.task_distribution_is_accepted = '已完成'
            # save方法保存修改的字段
            task_distribution.save()
            return JsonResponse(eM.successCode('完成成功'), safe=False)
        except Task.DoesNotExist:
            return JsonResponse(eM.errorCode404('不存在对应的任务'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 员工已完成的任务量报表

def staff_task_report_form(req, staff_id):
    if req.method == 'GET':
        df = pd.DataFrame(TaskDistribution.objects.filter(staff_id=staff_id, task_distribution_is_accepted='已完成').values())
        df.to_csv(os.path.join(BASE_DIR, "static", "report_form/staff_task_info.csv"), index=0)
        response = HttpResponse(content_type="application/octet-stream")  # text/csv
        # 添加返回头说明如何处理这个返回对象，并指明文件名。attachment：作为附件的形式进行下载
        response['Content-Disposition'] = "attachment;filename=user_info.csv"
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

#  http://127.0.0.1:5000/task/query_task_distribution?task_distribution_id=1
def query_task_distribution(request):
    task_distribution_id = request.GET.get('task_distribution_id', '')
    task_distribution = TaskDistribution.objects.filter(task_distribution_id=task_distribution_id)
    if task_distribution:
        info = eM.successCode('查询成功')
        info['data'] = {
            "task_distribution_id": task_distribution_id,
            "task_distribution_state": task_distribution.task_distribution_state,
            "task_distribution_is_accepted": task_distribution.task_distribution_is_accepted,
            "task_distribution_begin_time": task_distribution.task_distribution_begin_time,
            "task_distribution_endline": task_distribution.task_distribution_endline,
            "project": task_distribution.project,
            "staff": task_distribution.staff,
            "manager": task_distribution.manager,
            "task": task_distribution.task,
        }
        return JsonResponse(info, safe=False)
    else:
        return JsonResponse(eM.errorCode404('查询失败，不存在对应的任务'), safe=False)

#  http://127.0.0.1:8000/task/task_distribution/delete_task_distribution/1
def delete_task_distribution(request, task_distribution_id):
    if request.method == 'DELETE':
        try:
            cli = TaskDistribution.objects.get(id=task_distribution_id)
            cli.delete()
            return JsonResponse(eM.successCode('删除成功'), safe=False)
        except TaskDistribution.DoesNotExist:
            return JsonResponse(eM.errorCode404('删除失败'), safe=False)
        except ProtectedError:
            return JsonResponse(eM.errorCode403('存在外键约束'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

#  http://127.0.0.1:8000/task/task_distribution/find_all_distribution
def find_all_distribution(request):
    if request.method == 'GET':
        # 找到所有的客户信息。
        cs = TaskDistribution.objects.all().values()
        info = eM.successCode('查询成功')
        # 客户信息添加到info中，info是一个字典
        info['data'] = list(cs)
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 统计员工工作量
def find_workload(request, staff_id):
    if request.method == 'GET':
        info = eM.successCode('查询成功')
        info['data'] = list(TaskDistribution.objects.filter(staff_id=staff_id).values())
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)


################################################################################################################
############################################# TaskAdvise #################################################
################################################################################################################

# 添加任务
# http://127.0.0.1:8000/task/task_advise/add_task_advise
# request必须为第一个参数
def add_task_advise(request):
    # POST方法发数据
    if request.method == 'POST':
        dj = json.loads(request.body.decode())  # 获取前端传入的json数据。
        task_advise_content = dj.get('task_advise_content', '')
        task_reviewer = dj.get('task_reviewer', '')
        task_distribution = dj.get('task_distribution', '')

        cu = Task.objects.create(task_advise_content=task_advise_content,
                                 task_reviewer=task_reviewer,
                                 task_distribution=task_distribution)
        if cu:
            # eM.successCode 是我自己编写的消息类。 safe=False：表示除了返回json外还可以返回其它类型
            return JsonResponse(eM.successCode('录入成功'), safe=False)
        else:
            return JsonResponse(eM.errorCode400('录入失败'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)


# 修改任务 根据id
#  http://127.0.0.1:8000/task/task_advise/modify_task_advise/1
def modify_task_advise(request, task_advise_id):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            # 根据id查询一个客户对象
            task_advise = TaskAdvise.objects.get(id=task_advise_id)
            task_advise.task_advise_content = req.get('task_advise_content', '')
            task_advise.task_reviewer = req.get('task_reviewer', '')
            task_advise.task_distribution = req.get('task_distribution', '')

            # save方法保存修改的字段
            task_advise.save()
            return JsonResponse(eM.successCode('修改成功'), safe=False)
        except Task.DoesNotExist:
            return JsonResponse(eM.errorCode404('不存在'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)


#  http://127.0.0.1:8000/task/task_advise/query_task_advise?task_advise_id=1
def query_task_advise(request):
    task_advise_id = request.GET.get('task_advise_id', '')
    task_advise = TaskAdvise.objects.filter(task_advise_id=task_advise_id)
    if task_advise:
        info = eM.successCode('查询成功')
        info['data'] = {
            "task_advise_id": task_advise_id,
            "task_advise_content": task_advise.task_advise_content,
            "task_reviewer": task_advise.task_reviewer,
            "task_distribution": task_advise.task_distribution
        }
        return JsonResponse(info, safe=False)
    else:
        return JsonResponse(eM.errorCode404('查询失败，不存在'), safe=False)


#  http://127.0.0.1:8000/task/task_advise/delete_task_advise/1
def delete_task_advise(request, task_advise_id):
    if request.method == 'DELETE':
        try:
            cli = TaskAdvise.objects.get(id=task_advise_id)
            cli.delete()
            return JsonResponse(eM.successCode('删除成功'), safe=False)
        except TaskAdvise.DoesNotExist:
            return JsonResponse(eM.errorCode404('删除失败'), safe=False)
        except ProtectedError:
            return JsonResponse(eM.errorCode403('存在外键约束'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)


#  http://127.0.0.1:8000/task/task_advise/find_all
def find_all_advise(request):
    if request.method == 'GET':
        # 找到所有的客户信息。
        cs = TaskAdvise.objects.all().values()
        info = eM.successCode('查询成功')
        # 客户信息添加到info中，info是一个字典
        info['data'] = list(cs)
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)