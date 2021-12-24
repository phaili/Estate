from django.db import models

# Create your models here.
# 客户负责人
class Client(models.Model):
    client_id = models.AutoField('客户id', primary_key=True)
    client_name = models.CharField("客户姓名", max_length=20, default='')
    client_phone = models.CharField('客户电话', max_length=20, default='')
    client_qq = models.CharField('客户qq', max_length=14, default='')
    # 改
    client_email = models.EmailField('客户邮箱')

    class Meta:
        db_table = '客户'

