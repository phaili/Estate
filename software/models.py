from django.db import models

from user.models import Staff
# Create your models here.
# # 软件
class Software(models.Model):
    software_id = models.AutoField('软甲id', primary_key=True)
    software_name = models.CharField('软件名字', max_length=20, default='')
    software_property = models.CharField('软件性质', max_length=20, default='')

    class Meta:
        db_table = '软件'

# 员工使用软件记录
class StaffUsingSoftwareRecord(models.Model):
    use_software_id = models.AutoField('软件使用记录id', primary_key=True)
    # software_name = models.CharField('软件名字', max_length=20, default='')
    # software_property = models.CharField('软件性质', max_length=20, default='')
    use_software_begin_time = models.CharField('软件使用开始时间', max_length=20, default='')
    use_software_end_time = models.CharField('软件使用结束时间', max_length=20, default='')

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    software_id = models.ForeignKey('Software', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = '员工使用软件记录'

    def sn(self):
        return self.staff.name
