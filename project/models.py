from django.db import models
from client.models import Client

# 项目
class Project(models.Model):
    project_id = models.AutoField('项目id', primary_key=True)
    project_name = models.CharField('项目名字', max_length=30, default='')
    project_schedule = models.CharField('项目进度', max_length=10, default='')
    project_price = models.CharField('项目报价', max_length=10, default='')
    project_beg_time = models.CharField('项目开始时间', max_length=20, default='')
    project_person_in_charge = models.CharField('项目负责人', max_length=20, default='')
    project_state = models.CharField('项目状态', max_length=10, default='')
    # 删除客户时，会触发异常。
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = '项目'

    def cn(self):
        return self.client.client_name

    cn.short_description = '客户名称'







