import json
from django.db.models import ProtectedError
from django.http import JsonResponse
from .models import StaffUsingSoftwareRecord
from ErrorProcess import errorMessage as eM
from django.utils import timezone
# Create your views here.


# 添加客户数据
# http://127.0.0.1:8000/software/add_software_record
# request必须为第一个参数
def add_software_record(request):
    if request.method == 'POST':
        dj = json.loads(request.body.decode())
        name = dj.get('software_name', '')
        software_property = dj.get('software_property', '')
        use_software_begin_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        use_software_end_time = request.get('use_software_end_time', '')
        staff_id = request.get('staff_id', '')
        sus = StaffUsingSoftwareRecord.objects.create(staff_id=staff_id, software_name=name, use_software_begin_time=use_software_begin_time,
                                                     use_software_end_time=use_software_end_time, software_property=software_property)
        if sus:
            return JsonResponse(eM.successCode('录入成功'), safe=False)
        else:
            return JsonResponse(eM.errorCode400('录入失败'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

# 修改客户 根据id
#  http://127.0.0.1:8000/software/modify_software_record/1
def modify_software_record(request, software_record_id):
    # if request.method == 'POST':
    #     req = json.loads(request.body)
    #     try:
    #         # 根据id查询一个客户对象
    #         software_record = StaffUsingSoftwareRecord.objects.get(id=software_record_id)
    #         software_record.software_name = req.get('software_name', '')
    #         software_record.software_property = req.get('software_property', '')
    #         software_record.use_software_begin_time = req.get('use_software_begin_time', '')
    #         software_record.use_software_end_time = req.get('use_software_end_time', '')
    #         # save方法保存修改的字段
    #         software_record.save()
    #         return JsonResponse(eM.successCode('修改成功'), safe=False)
    #     except StaffUsingSoftwareRecord.DoesNotExist:
    #         return JsonResponse(eM.errorCode404('不存在对应的客户'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

#  http://127.0.0.1:8000/software/query_client?staff=xx
 # 通过员工id查找软件使用记录
def query_software_record(request):
    if request.method == 'GET':
        staff_id = request.GET.get('staff_id', '')
        software_record = StaffUsingSoftwareRecord.objects.filter(staff_id=staff_id)
        if software_record:
            info = eM.successCode('查询成功')
            info['data'] = list(software_record)
            return JsonResponse(info, safe=False)
        else:
            return JsonResponse(eM.errorCode404('查询失败，不存在对应的客户'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

#  http://127.0.0.1:8000/software/delete_software_record/1
def delete_software_record(request, software_record_id):
    if request.method == 'DELETE':
        try:
            sof = StaffUsingSoftwareRecord.objects.get(id=software_record_id)
            sof.delete()
            return JsonResponse(eM.successCode('删除成功'), safe=False)
        except StaffUsingSoftwareRecord.DoesNotExist:
            return JsonResponse(eM.errorCode404('删除失败'), safe=False)
        except ProtectedError:
            return JsonResponse(eM.errorCode403('存在外键约束'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

#  http://127.0.0.1:8000/software/find_all
def find_all(request):
    if request.method == 'GET':
        cs = StaffUsingSoftwareRecord.objects.all().values()
        info = eM.successCode('查询成功')
        info['data'] = list(cs)
        return JsonResponse(info, safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)

def add_software(request):
    if request.method == 'POST':
        dj = json.loads(request.body.decode())
        name = dj.get('software_name', '')
        software_property = dj.get('software_property', '')
        sus = StaffUsingSoftwareRecord.objects.create(software_name=name,  software_property=software_property)
        if sus:
            return JsonResponse(eM.successCode('录入成功'), safe=False)
        else:
            return JsonResponse(eM.errorCode400('录入失败'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)