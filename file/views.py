import json
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse
import os
from file.models import FileInfo, FolderInfo, Project
from file.untils import judge_filepath, format_size
from django.utils.http import urlquote
from django.contrib.auth.models import User
import shutil
from ErrorProcess import errorMessage as eM
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    pid = 3
    try:
        pro = Project.objects.get(project_id=pid)
    except:
        return JsonResponse(eM.errorCode404('没有数据'), safe=False)
    project_id = pro.project_id
    file_obj = FileInfo.objects.filter(project_id=project_id, belong_folder='')
    folder_obj = FolderInfo.objects.filter(project_id=project_id, belong_folder='')
    index_list = []
    for file in file_obj:
        file.is_file = True
        index_list.append(file)
    for folder in folder_obj:
        folder.is_file = False
        index_list.append(folder)
    breadcrumb_list = [{'tag': '全部文件', 'uri': ''}]
    return render(request, 'index.html',
                  {'index_list': index_list,  'breadcrumb_list': breadcrumb_list})


# @login_required
def folder(request):
    # user = str(request.user)
    # id = User.objects.get(username=user).id
    pid = 3
    pro = Project.objects.get(project_id=pid)
    project_id = pro.project_id

    pdir = request.GET.get('pdir')
    if pdir:
        if pdir[-1:] == '/':
            belong_folder = pdir
        else:
            belong_folder = pdir + '/'
    else:
        belong_folder = ''
    # file_obj = models.FileInfo.objects.filter(user_id=user_id, belong_folder=belong_folder)
    # folder_obj = models.FolderInfo.objects.filter(user_id=user_id, belong_folder=belong_folder)
    file_obj = FileInfo.objects.filter(project_id=project_id, belong_folder=belong_folder)
    folder_obj = FolderInfo.objects.filter(project_id=project_id, belong_folder=belong_folder)
    index_list = []
    for file in file_obj:
        file.is_file = True
        index_list.append(file)
    for folder in folder_obj:
        folder.is_file = False
        index_list.append(folder)
    breadcrumb_list = [{'tag': '全部文件', 'uri': ''}]
    uri = ''
    for value in pdir.split('/'):
        if value:
            uri = uri + value + '/'
            breadcrumb_list.append({'tag': value, 'uri': uri})
    return render(request, 'index.html',
                  {'index_list': index_list,  'breadcrumb_list': breadcrumb_list})

# 已改 就差增加项目进去
# @login_required
def delete_file(request):
    # user = str(request.user)
    # id = User.objects.get(username=user).id
    pid = 3
    pro = Project.objects.get(project_id=pid)
    project_id = pro.project_id
    file_path = request.GET.get('file_path')
    pwd = request.GET.get('pwd')
    f = FileInfo.objects.filter(file_path=file_path, project_id=project_id)
    if f:
        f.delete()
        try:
            os.remove(BASE_DIR + '/static/' + file_path)
        except Exception as e:
            print(e)
    return redirect('/folder/?pdir=' + pwd)

# 已改 就差增加项目进去
# @login_required
def rename_file(request):
    # user = str(request.user)
    # user_id = User.objects.get(username=user).id
    pid = 3
    pro = Project.objects.get(project_id=pid)
    project_id = pro.project_id
    old_file_name = request.GET.get('old_file_name')
    file_type = old_file_name.split('.')[-1]
    new_file_name = request.GET.get('new_file_name')+'.'+file_type
    pwd = request.GET.get('pwd')
    file_obj = FileInfo.objects.get(belong_folder=pwd, file_name=old_file_name, project_id=project_id)
    old_path = file_obj.file_path
    new_path = old_path.replace(old_file_name, new_file_name)
    file_obj.file_path = new_path
    old_full_path = BASE_DIR + '/static/' + old_path
    new_full_path = BASE_DIR + '/static/' + new_path
    os.rename(old_full_path, new_full_path)
    file_obj.file_name = new_file_name
    file_obj.save()
    return redirect('/folder/?pdir=' + pwd)
    # models.FileInfo.objects.get(file_path=file_path, user_id=user_id).delete()

# 已改 就差增加项目进去
# @login_required
def rename_folder(request):
    # user = str(request.user)
    # user_id = User.objects.get(username=user).id
    pid = 3
    pro = Project.objects.get(project_id=pid)
    project_id = pro.project_id
    old_folder_name = request.GET.get('old_folder_name')
    new_folder_name = request.GET.get('new_folder_name')
    pwd = request.GET.get('pwd')
    folder_obj = FolderInfo.objects.get(belong_folder=pwd, folder_name=old_folder_name, project_id=project_id)
    folder_obj.folder_name = new_folder_name
    old_belong_folder = folder_obj.belong_folder + old_folder_name + '/'
    new_belong_folder = folder_obj.belong_folder + new_folder_name + '/'
    old_full_path = BASE_DIR + '/static/'  + '/' + old_belong_folder
    new_full_path = BASE_DIR + '/static/' + '/' + new_belong_folder
    os.rename(old_full_path, new_full_path)
    folder_belong_folder_objs = FolderInfo.objects.filter(belong_folder__startswith=old_belong_folder,
                                                                 project_id=project_id)
    for folder_belong_folder_obj in folder_belong_folder_objs:
        tmp_belong_folder = folder_belong_folder_obj.belong_folder.replace(old_belong_folder, new_belong_folder)
        folder_belong_folder_obj.belong_folder = tmp_belong_folder
        folder_belong_folder_obj.save()
    file_belong_folder_objs = FileInfo.objects.filter(belong_folder__startswith=old_belong_folder,
                                                             project_id=project_id)
    for file_belong_folder_obj in file_belong_folder_objs:
        tmp_belong_folder = file_belong_folder_obj.belong_folder.replace(old_belong_folder, new_belong_folder)
        file_belong_folder_obj.belong_folder = tmp_belong_folder
        file_belong_folder_obj.save()
    folder_obj.save()
    return redirect('/folder/?pdir=' + pwd)

# 已改 就差增加项目进去
# @login_required
def delete_folder(request):
    pwd = request.GET.get('pwd')
    folder_name = request.GET.get('folder_name')
    try:
        FolderInfo.objects.filter(belong_folder__contains=folder_name).delete()
        FolderInfo.objects.filter(folder_name=folder_name).delete()
        FileInfo.objects.filter(belong_folder__contains=folder_name).delete()
        rm_dir = BASE_DIR + '/static/' + pwd + folder_name
        shutil.rmtree(rm_dir)
    except Exception as e:
        print(e)
    return redirect('/folder/?pdir=' + pwd)

# 已改 就差增加项目进去
# @login_required
def mkdir(request):
    # user = request.user
    # user_id = User.objects.get(username=user).id
    pid = 3
    pro = Project.objects.get(project_id=pid)
    project_id = pro.project_id
    pwd = request.GET.get('pwd')
    folder_name = request.GET.get('folder_name')
    update_time = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        FolderInfo.objects.create(project_id=project_id, folder_name=folder_name, belong_folder=pwd,
                                         update_time=update_time)
        user_path = os.path.join(BASE_DIR, 'static')
        os.mkdir(user_path + '/' + pwd + folder_name)
    except Exception as e:
        print(e)
    return redirect('/folder/?pdir=' + pwd)

# 已改
# @login_required
def download_file(request):

    file_path = request.GET.get('file_path')
    file_name = file_path.split('/')[-1]
    file_dir = BASE_DIR + '/static/' + file_path
    file = open(file_dir, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename={}'.format(urlquote(file_name))
    response['msg'] = '文件下载成功'
    return response

# 已改 就差增加项目进去
# @login_required
def upload_file(request):
    if request.method == "POST":
        # user_name = str(request.user)
        # user_obj = User.objects.get(username=user_name)
        pid = 3
        pro = Project.objects.get(project_id=pid)
        project_id = pro.project_id
        file_obj = request.FILES.get('file')
        file_type = judge_filepath(file_obj.name.split('.')[-1].lower())
        pwd = request.POST.get('file_path')

        update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(update_time)
        file_size = format_size(file_obj.size)
        file_name = file_obj.name
        # save_path = BASE_DIR + '/static/' + user_name + '/' + pwd
        save_path = BASE_DIR + '/static/' + pwd
        # file_path = user_name + '/' + pwd + file_name
        file_path = '/' + pwd + file_name
        # print(belong_folder, folder_name, save_path)
        FileInfo.objects.create(project_id=project_id, file_path=file_path,
                                       file_name=file_name, update_time=update_time, file_size=file_size,
                                       file_type=file_type, belong_folder=pwd)
        with open(save_path + file_name, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        return redirect('/')


# @login_required
def file_type(request):
    # user = request.user
    # user_id = User.objects.get(username=user).id
    file_type = request.GET.get('file_type')
    pid = 3
    pro = Project.objects.get(project_id=pid)
    project_id = pro.project_id
    file_list = []
    if file_type == 'all':
        file_obj = FileInfo.objects.filter(project_id=project_id)
    else:
        file_obj = FileInfo.objects.filter(file_type=file_type, project_id=project_id)
    for file in file_obj:
        file_list.append({'file_path': file.file_path, 'file_name': file.file_name,
                          'update_time': str(file.update_time), 'file_size': file.file_size,
                          'file_type': file.file_type})
    return JsonResponse(file_list, safe=False)


# @login_required
def search(request):
    file_type = request.GET.get('file_type')
    file_name = request.GET.get('file_name')
    user = request.user
    user_id = User.objects.get(username=user).id
    file_list = []
    if file_type == 'all':
        file_obj = FileInfo.objects.filter(file_name__icontains=file_name, user_id=user_id)
    else:
        file_obj = FileInfo.objects.filter(file_type=file_type, file_name__icontains=file_name, user_id=user_id)
    for file in file_obj:
        file_list.append({'file_path': file.file_path, 'file_name': file.file_name,
                          'update_time': str(file.update_time), 'file_size': file.file_size,
                          'file_type': file.file_type})
    return JsonResponse(file_list, safe=False)


def mkdir_pro_cli_time(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        project_id = 3
        # project_id = req.get('project_id', '3')
        project_name = req.get('project_name', '')
        client_name = req.get('client_name', '')
        project_beg_time = req.get('project_beg_time', '')
        date = project_beg_time.split(' ')[0]    # time.strftime('%Y-%m-%d')
        folder_name = project_name+"-"+client_name+"-"+date
        update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            FolderInfo.objects.create(folder_name=folder_name, belong_folder='', update_time=update_time, project_id=project_id)
            FolderInfo.objects.create(folder_name="jpg", belong_folder=folder_name+"/", update_time=update_time, project_id=project_id)
            FolderInfo.objects.create(folder_name="后期文件", belong_folder=folder_name+"/", update_time=update_time, project_id=project_id)
            FolderInfo.objects.create(folder_name="模型文件", belong_folder=folder_name+"/", update_time=update_time, project_id=project_id)
            FolderInfo.objects.create(folder_name="小样", belong_folder=folder_name+"/", update_time=update_time, project_id=project_id)
            FolderInfo.objects.create(folder_name="渲染文件", belong_folder=folder_name+"/", update_time=update_time, project_id=project_id)
            FolderInfo.objects.create(folder_name="资料", belong_folder=folder_name+"/", update_time=update_time, project_id=project_id)

            FolderInfo.objects.create(folder_name="原始文件", belong_folder=folder_name + "/后期文件/", update_time=update_time,
                                      project_id=project_id)
            FolderInfo.objects.create(folder_name="原始模型", belong_folder=folder_name + "/模型文件/", update_time=update_time,
                                      project_id=project_id)
            FolderInfo.objects.create(folder_name="最终模型", belong_folder=folder_name + "/模型文件/", update_time=update_time,
                                      project_id=project_id)
            FolderInfo.objects.create(folder_name="原始渲染", belong_folder=folder_name + "/渲染文件/", update_time=update_time,
                                      project_id=project_id)
            FolderInfo.objects.create(folder_name="最终渲染", belong_folder=folder_name + "/渲染文件/", update_time=update_time,
                                      project_id=project_id)

            path = BASE_DIR + '/static/'
            os.mkdir(path + folder_name)
            os.mkdir(path + folder_name+"/"+"jpg")
            os.mkdir(path + folder_name+"/"+"后期文件")
            os.mkdir(path + folder_name+"/"+"模型文件")
            os.mkdir(path + folder_name+"/"+"小样")
            os.mkdir(path + folder_name+"/"+"渲染文件")
            os.mkdir(path + folder_name+"/"+"资料")
            os.mkdir(path + folder_name + "/后期文件/"+"原始文件")
            os.mkdir(path + folder_name + "/模型文件/"+"原始模型")
            os.mkdir(path + folder_name + "/模型文件/"+"最终模型")
            os.mkdir(path + folder_name + "/渲染文件/"+"原始渲染")
            os.mkdir(path + folder_name + "/渲染文件/"+"最终渲染")

            return JsonResponse(eM.successCode('文件创建成功'), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(eM.errorCode404('文件创建失败'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)
#
#
#
#
# # 上传文件夹，但是里面的文件会统一在一个文件夹中
# # http://127.0.0.1:8000/file/upload_folder
# def upload_folder(req):
#     if req.method == 'POST':
#         files = req.FILES.getlist('folder')
#         for file in files:
#             # 获取文件名，文件对象的__str__属性返回的是文件名
#             file_name = str(file)
#             with open(os.path.join(settings.MEDIA_ROOT, file_name), 'wb') as f:
#                 # 分块写入，防止大文件卡死
#                 for chunk in file.chunks(chunk_size=2014):
#                     f.write(chunk)
#         return JsonResponse(eM.successCode('上传成功'), safe=False)
#
# # http://127.0.0.1:8000/file/upload_file
# def upload_file(request):
#     if request.method == 'GET':
#         return render(request, 'testUploadFile.html')
#     if request.method == 'POST':
#         file_obj = request.FILES.get('file', '')
#         try:
#             with open(os.path.join(settings.MEDIA_ROOT, file_obj.name), 'wb') as f:
#                 for chunk in file_obj.chunks():
#                     f.write(chunk)
#             return JsonResponse(eM.successCode('文件上传成功'), safe=False)
#         except Exception:
#             return JsonResponse(eM.errorCode404('文件上传失败'), safe=False)
#
# def readFile(filename,chunk_size=512):
#     with open(filename,'rb') as f:
#         while True:
#             c=f.read(chunk_size)
#             if c:
#                 yield c
#             else:
#                 break
#
# def download_file(request):
#     if request.method == 'POST':
#         req = json.loads(request.body)
#         file_path = req.get('file_path', '')
#         file_name = file_path.split('/')[-1]
#         file_dir = settings.MEDIA_ROOT + "\\" + file_path
#         if not os.path.isfile(file_dir):  # 判断下载文件是否存在
#             return JsonResponse(eM.errorCode404("文件不存在"))
#         with open(file_dir, 'rb') as f:
#
#             response = StreamingHttpResponse(readFile(file_dir))
#             info = eM.successCode('文件下载成功')
#             response['status'] = info['status']
#             response['msg'] = info['msg']
#             # response['Content-Type'] = 'application/octet-stream'
#             # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
#             response['Content-Type'] = 'application/octet-stream'
#             response['Content-Disposition'] = 'attachment;filename={}'.format(urlquote(file_name))
#             return response
#         return JsonResponse(eM.errorCode404('文件下载失败'), safe=False)
#     return JsonResponse(eM.errorCode404('文件下载失败1'), safe=False)



