from django.contrib import admin
from .models import Client
# Register your models here.
class ClientManager(admin.ModelAdmin):
    list_display = ["client_id", "client_name", "client_phone", "client_qq", "client_email"]
    # 可通过点击name查看详细信息。
    list_display_links = ["client_id"]
    # 可更改
    list_editable = ['client_name', 'client_phone', "client_qq", "client_email"]
    # 添加搜索框，模糊搜索
    search_fields = ['client_name']


admin.site.register(Client, ClientManager)