from django.db import models

# # 任务
from project.models import Project
from user.models import Staff, Manager


class Task(models.Model):
    task_id = models.AutoField('任务id', primary_key=True)
    task_info = models.CharField('任务描述', max_length=80, default='')
    task_property = models.CharField('任务性质', max_length=20, default='')

    class Meta:
        db_table = '任务'


# # 任务分配
class TaskDistribution(models.Model):
    task_distribution_id = models.AutoField('分配任务id', primary_key=True)

    # task_distribution_schedule = models.CharField('分配任务进度', max_length=20, default='')
    task_distribution_state = models.CharField('分配任务状态', max_length=20, default='')
    task_distribution_is_accepted = models.CharField('分配任务是否被接收', max_length=6, default='')
    task_distribution_begin_time = models.CharField('分配任务开始时间', max_length=20, default='')
    task_distribution_end_time = models.CharField('分配任务结束时间', max_length=20, default='')

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = '任务分配'

# # 任务审核
class TaskAdvise(models.Model):
    task_advise_id = models.AutoField('任务审核id', primary_key=True)
    # 同意，不同意并写出意见。
    task_advise_content = models.CharField('任务审核建议', max_length=100, default='')
    # task_access = models.CharField('任务审核是否通过', max_length=6, default='')
    task_reviewer = models.CharField('任务审核人', max_length=20, default='')

    task_distribution = models.ForeignKey('TaskDistribution', on_delete=models.CASCADE)

    class Meta:
        db_table = '任务审核'