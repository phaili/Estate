from django.contrib import admin
from django.urls import path,re_path
from . import views
urlpatterns = [
    path('add_client', views.add_client),
    path('modify_client/<int:client_id>', views.modify_client),
    path('delete_client/<int:client_id>', views.delete_client),
    # path('query_client', views.query_client),  # #  ?userid=xx&name=xx
    path('find_all', views.find_all),  # #  ?userid=xx&name=xx
    # path('find_all_client', views.find_all_client),
    path('client_report_form', views.client_report_form),  # #  ?userid=xx&name=xx

]