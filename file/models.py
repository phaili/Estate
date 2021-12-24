from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from project.models import Project


class FileInfo(models.Model):
    id = models.AutoField('文件id', primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=128, verbose_name='存储路径')
    file_name = models.CharField(max_length=128, verbose_name='文件名')
    update_time = models.CharField(max_length=30, verbose_name='上传时间')
    file_type = models.CharField(max_length=32, verbose_name='文件类型')
    file_size = models.CharField(max_length=16, verbose_name='文件大小')
    belong_folder = models.CharField(max_length=64, verbose_name='所属文件夹')

    class Meta:
        db_table = '文件'


class FolderInfo(models.Model):
    id = models.AutoField('文件夹id', primary_key=True)
    update_time = models.CharField(max_length=30, verbose_name='上传时间')
    belong_folder = models.CharField(max_length=64, verbose_name='所属文件夹')
    folder_name = models.CharField(max_length=64, verbose_name='文件夹名')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = '文件夹'
