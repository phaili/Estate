from django.contrib import admin
from .models import Project
# Register your models here.
class ProjectManager(admin.ModelAdmin):
    list_display = ["project_id", "project_name", "project_schedule", "project_price", "project_beg_time", "project_person_in_charge", "project_state", "cn"]
    # 可通过点击name查看详细信息。
    list_display_links = ["project_id"]
    # 可更改
    list_editable = ['project_name', 'project_price', "project_person_in_charge", "project_state"]
    # 添加搜索框，模糊搜索
    search_fields = ['project_name']
    list_per_page = 20
    ordering = ('-project_beg_time', )
    # fk_fields 设置显示外键字段
    # fk_fields = ['client']


admin.site.register(Project, ProjectManager)