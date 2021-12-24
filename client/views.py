import codecs
import csv
import json
import os

from django.db.models import ProtectedError
from django.http import JsonResponse, HttpResponse

from Estate1 import settings
from Estate1.settings import BASE_DIR
from .models import Client
from ErrorProcess import errorMessage as eM
import pandas as pd
# Create your views here.


# 添加客户数据
# http://127.0.0.1:8000/client/add_client
# request必须为第一个参数
def add_client(request):
    # POST方法发数据， GET方法请求网页
    if request.method == 'POST':
        # client_name client_phone client_qq client_email
        dj = json.loads(request.body.decode())  # 获取前端传入的json数据。
        name = dj.get('client_name', '')  # client_name：json数据中的变量名，都参考模型中的字段设定； 没获取到就为''
        phone = dj.get('client_phone', '')
        qq = dj.get('client_qq', '')
        email = dj.get('client_email', '')
        # 数据库插入语句，插入不成功返回None       这些字段看Client模型类，id自动生成
        cu = Client.objects.create(client_name=name, client_phone=phone, client_qq=qq, client_email=email)
        if cu:
            # eM.successCode 是我自己编写的消息类。 safe=False：表示除了返回json外还可以返回其它类型
            return JsonResponse(eM.successCode('录入成功'), safe=False)
        else:
            return JsonResponse(eM.errorCode400('录入失败'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 修改客户 根据id
#  http://127.0.0.1:8000/client/modify_client/1
def modify_client(request, client_id):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            # 根据id查询一个客户对象
            client = Client.objects.get(client_id=client_id)
            client.client_name = req.get('client_name', '')
            client.client_phone = req.get('client_phone', '')
            client.client_email = req.get('client_email', '')
            client.client_qq = req.get('client_qq', '')
            # save方法保存修改的字段
            client.save()
            return JsonResponse(eM.successCode('修改成功'), safe=False)
        except Client.DoesNotExist:
            return JsonResponse(eM.errorCode404('不存在对应的客户'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

#  http://127.0.0.1:8000/client/query_client?phone=xx&name=xx
# def query_client(request):
#     name = request.GET.get('name', '')
#     phone = request.GET.get('phone', '')
#     client = Client.objects.filter(client_name=name, client_phone=phone)
#     if client:
#         info = eM.successCode('查询成功')
#         info['data'] = {
#             "client_id": client.client_id,
#             "client_name": name,
#             "client_phone": phone,
#             "client_email": client.client_email,
#             "client_qq": client.client_qq
#         }
#         return JsonResponse(info, safe=False)
#     else:
#         return JsonResponse(eM.errorCode404('查询失败，不存在对应的客户'), safe=False)

#  http://127.0.0.1:8000/client/delete_client/1
def delete_client(request, client_id):
    if request.method == 'DELETE':
        try:
            cli = Client.objects.get(id=client_id)
            cli.delete()
            return JsonResponse(eM.successCode('删除成功'), safe=False)
        except Client.DoesNotExist:
            return JsonResponse(eM.errorCode404('删除失败'), safe=False)
        except ProtectedError:
            return JsonResponse(eM.errorCode403('存在外键约束'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

#  http://127.0.0.1:5000/client/find_all
def find_all(request):
    if request.method == 'GET':
        # 找到所有的客户信息。
        cs = Client.objects.all().values()
        info = eM.successCode('查询成功')
        # 客户信息添加到info中，info是一个字典
        info['data'] = list(cs)
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

def client_report_form(req):
    if req.method == 'GET':
        # 找到所有的客户信息。
        cs = Client.objects.all().values()
        # 客户信息添加到info中，info是一个字典
        df = pd.DataFrame(cs)
        df.to_csv(os.path.join(BASE_DIR, "static", "report_form/client_info.csv"), index=0)
        response = HttpResponse(content_type='text/csv')
        # 添加返回头说明如何处理这个返回对象，并指明文件名。attachment：作为附件的形式进行下载
        response['Content-Disposition'] = "attachment;filename=client_info.csv"
        # 创建写的对象
        writer = csv.writer(response)
        writer.writerow(df.columns)
        # 写入下一行数据
        for d in df.values:
            writer.writerow(d)
        return response
    else:
        return JsonResponse(eM.errorCode400('错误请求'), safe=False)