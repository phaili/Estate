from django.contrib import admin
from .models import Staff, Manager, StaffTurnover, StaffEvaluation

class StaffManager(admin.ModelAdmin):
    admin.site.site_header = '信息后台管理'
    admin.site.site_title = '信息管理'
    list_display = ["staff_id", "account", "name", "phone", "department", "job"]
    # 可通过点击name查看详细信息。
    list_display_links = ["name"]

    # 可更改
    list_editable = ['job', 'department']

    # 过滤器
    list_filter = ['department']

    # 添加搜索框，模糊搜索
    search_fields = ['name']


class ManageManager(admin.ModelAdmin):
    list_display = ["manager_id", "account", "manager_name", "manager_phone", "manager_department", "manager_job"]
    # 可通过点击name查看详细信息。
    list_display_links = ["manager_name"]
    # 可更改
    list_editable = ['manager_job', 'manager_department']
    # 过滤器
    list_filter = ['manager_department']

    # 添加搜索框，模糊搜索
    search_fields = ['manager_name']

class StaffEvaluationManager(admin.ModelAdmin):
    list_display = ["staff_evaluation_id", "staff_evaluation_info", "staff_evaluation_time", "cn"]
    # 可通过点击name查看详细信息。
    list_display_links = ["staff_evaluation_id"]
    # 可更改
    list_editable = ['staff_evaluation_info']

    # 添加搜索框，模糊搜索
    search_fields = ['cn']


class StaffTurnoverManager(admin.ModelAdmin):
    list_display = ["staff_turnover_id", "staff_turnover_basic_salary", "staff_turnover_deduction","staff_turnover_total", "cn"]
    # 可通过点击name查看详细信息。
    list_display_links = ["staff_turnover_id"]
    # 可更改
    list_editable = ["staff_turnover_basic_salary", "staff_turnover_deduction", "staff_turnover_total"]

    # 添加搜索框，模糊搜索
    search_fields = ['cn']


admin.site.register(Staff, StaffManager)
admin.site.register(Manager, ManageManager)
admin.site.register(StaffEvaluation, StaffEvaluationManager)
admin.site.register(StaffTurnover, StaffTurnoverManager)