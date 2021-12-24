from django.contrib import admin
from .models import StaffUsingSoftwareRecord, Software


# Register your models here.
class StaffUsingSoftwareRecordManager(admin.ModelAdmin):
    list_display = ["use_software_id",  "use_software_begin_time", "use_software_end_time", "sn"]
    # 可通过点击name查看详细信息。
    list_display_links = ["use_software_id"]

    # 添加搜索框，模糊搜索
    search_fields = ['sn']
    list_per_page = 20


class SoftwareManager(admin.ModelAdmin):
    list_display = ["software_id", "software_name", "software_property"]
    list_display_links = ["software_id"]
    search_fields = ['software_name']
    list_per_page = 20


admin.site.register(Software, SoftwareManager)
admin.site.register(StaffUsingSoftwareRecord, StaffUsingSoftwareRecordManager)