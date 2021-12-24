from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
# F对象 Q对象
# class MyUser(AbstractUser):
#     staff_id_fk = models.OneToOneField()


# F对象 Q对象
from project.models import Project


class Staff(models.Model):
    # 工号、姓名、部门、职务、联系方式。员工可能出现离职、部门调动、升职、降级等情况
    staff_id = models.AutoField('工号', primary_key=True)
    #  账号
    account = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    name = models.CharField('员工名字', max_length=20, default='')
    phone = models.CharField('联系方式', max_length=15, default='')
    department = models.CharField('部门', max_length=30, default='')
    job = models.CharField('职务', max_length=30, default='模型员工')

    class Meta:
        db_table = '员工'
        # verbose_name = 'staff'
        # verbose_name_plural = verbose_name

class Manager(models.Model):
    # 工号、姓名、部门、职务、联系方式。员工可能出现离职、部门调动、升职、降级等情况
    manager_id = models.IntegerField('主管工号', primary_key=True)
    account = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    manager_name = models.CharField('主管姓名', max_length=20, default='')
    manager_phone = models.CharField('主管电话', max_length=20, default='')
    manager_department = models.CharField('主管所属部门', max_length=20, default='')
    manager_job = models.CharField('主管职务', max_length=20, default='模型主管')
    # 建立多对多联系
    project_manager = models.ManyToManyField(Project)

    class Meta:
        db_table = '主管'

# 员工评估
class StaffEvaluation(models.Model):
    staff_evaluation_id = models.AutoField('员工评估id', primary_key=True)
    staff_evaluation_info = models.CharField('员工评估内容', max_length=20, default='')
    staff_evaluation_time = models.CharField('员工评估记录时间', max_length=20, default='')

    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)

    class Meta:
        db_table = '员工评价'

    def cn(self):
        return self.staff.name

# 员工流水
class StaffTurnover(models.Model):
    staff_turnover_id = models.AutoField('员工流水id', primary_key=True)
    staff_turnover_basic_salary = models.CharField('员工基础工资', max_length=20, default='')
    staff_turnover_deduction = models.CharField('扣款', max_length=20, default='')
    staff_turnover_total = models.CharField('总工资', max_length=20, default='')

    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)

    class Meta:
        db_table = '员工流水'

    def cn(self):
        return self.staff.name