import csv
import json
import os
import re
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from ErrorProcess import errorMessage as eM
from Estate1.settings import BASE_DIR
from .models import Staff, Manager


# 统一初始密码为身份证后6位
#  http://127.0.0.1:5000/user/register
def register_view(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        account = req.get('account', '')
        pw = req.get('password', '')
        name = req.get('name', '')
        job = req.get('job', '')  # 职务
        phone = req.get('phone', '')
        department = req.get('department', '')
        if User.objects.filter(username=account):
            return JsonResponse(eM.errorCode400('您输入的账号重复，请重新输入'), safe=False, status=400)
        else:
            #插入账号
            user = User.objects.create_user(username=account, password=pw)
            # 建立员工账号
            staff = Staff.objects.create(account=user, name=name, job=job, phone=phone, department=department)
            if '员工' not in job:
                Manager.objects.create(manager_id=staff.staff_id, account=user, manager_name=name, manager_job=job,
                                       manager_phone=phone, manager_department=department)
            # login(request, user)  # 注册后免登录
            info = eM.successCode('注册成功')
            info['staffId'] = staff.staff_id
            # safe: 默认只支持返回字典类型数据，设置为false可以返回其他类型数据
            # json_dumps_params：设置是否转换成ASCII编码，不转则为中文，默认为true  json_dumps_params={"ensure_ascii": False}
            return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

#  http://127.0.0.1:8000/user/login
def login_view(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode())
        name = data.get('account', '')
        pw = data.get('password', '')
        remembered = data.get('remembered', '')
        # 校验参数
        if not all([name, pw]):
            return JsonResponse(eM.errorCode400('参数缺失！'))

        # if not re.match(r'^\w{5,20}$', name):  # 名字在5-20位之间
        #     return JsonResponse({eM.errorCode400("用户名格式有误")}, status=400)
        #
        # if not re.match(r'^\w{8,20}$', pw):    # 密码在8-20位之间
        #     return JsonResponse(eM.errorCode400("密码格式有误"), status=400)
        # if not User.objects.filter(username=name):
        #     return JsonResponse(eM.errorCode404("账号错误!"))
        user = authenticate(username=name, password=pw)
        if not user:
            return JsonResponse(eM.errorCode404("密码错误!"))
        if not user.is_active:
            return JsonResponse(eM.errorCode404('账号已被删除'))
        #保持登录状态
        login(request, user)

        if remembered:
            # 设置session有效期默认2周
            request.session.set_expiry(None)
        else:
            # 设置session有效期为0表示关闭浏览器页面则失效
            request.session.set_expiry(0)
        # 4、构建响应
        info = eM.successCode('ok')
        # if user.staff:
        info['data'] = {
            'staff_id': user.staff.staff_id,
            'account': name,
            'name': user.staff.name,
            'department': user.staff.department,
            'job': user.staff.job,
            'phone': user.staff.phone,
        }
        response = JsonResponse(info)
        # response.set_cookie(key='username', value=name, max_age=3600 * 24 * 14)
        return response
        # else:
        #     return JsonResponse(eM.errorCode400('没有关联的员工信息'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

def update_staff_info(request, staff_id):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            # 根据id查询一个客户对象
            staff = Staff.objects.get(staff_id=staff_id)
            staff.name = req.get('name', '')
            staff.phone = req.get('phone', '')
            staff.department = req.get('department', '')
            staff.job = req.get('job', '')
            manage = Manager.objects.get(manager_id=staff_id)
            manage.manager_name = req.get('name', '')
            manage.manager_phone = req.get('phone', '')
            manage.manager_department = req.get('department', '')
            manage.manager_job = req.get('job', '')
            staff.save()
            manage.save()
            return JsonResponse(eM.successCode('修改成功'), safe=False)
        except Staff.DoesNotExist:
            return JsonResponse(eM.errorCode404('不存在对应的客户'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 首页，必须登录才能访问。要是没登录会跳转到settings配置项中的。
#  http://127.0.0.1:8000/user/index
@login_required
def index_view(request):
    login_user = request.user
    response = JsonResponse(eM.successCode('ok'))
    return response

# 退出登录
#  http://127.0.0.1:8000/user/logout
def logout_view(req):
    logout(req)
    response = JsonResponse(eM.successCode('退出登录成功'))
    response.delete_cookie('username')
    return response




#  http://127.0.0.1:8000/user/find_all_staff
def find_all_staff(req):
    if req.method == 'GET':
        cs = Staff.objects.filter(job__contains='员工')

        info = eM.successCode('查询成功')
        info['data'] = list(cs)
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)


def find_depart_staff(request, depart):
    if request.method == 'GET':
        if '老板' in depart:
            cs = Staff.objects.all().values()
        elif '模型' in depart:
            cs = Staff.objects.filter(department__contains='模型').values()
        elif '渲染' in depart:
            cs = Staff.objects.filter(department__contains='渲染').values()
        elif '后期' in depart:
            cs = Staff.objects.filter(department__contains='后期').values()
        else:
            return JsonResponse(eM.errorCode400('参数错误'), safe=False)
        info = eM.successCode('查询成功')
        info['data'] = list(cs)
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

#  http://127.0.0.1:8000/user/find_all_manager
def find_all_manager(req):
    if req.method == 'GET':
        cs = Staff.objects.filter(job__contains='主管')
        info = eM.successCode('查询成功')
        info['data'] = list(cs)
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

def user_report_form(req):
    if req.method == 'GET':
        us = Staff.objects.all().values()
        df = pd.DataFrame(us)
        df.to_csv(os.path.join(BASE_DIR, "static", "report_form/client_info.csv"), index=0)
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


