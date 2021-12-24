from django.urls import path
from . import views

urlpatterns = [
    path('add_project', views.add_project),
    path('find_all', views.find_all),
    path('modify_project/<int:project_id>', views.modify_project),
    path('modify_project_schedule', views.modify_project_schedule),
    path('delete_project/<int:project_id>', views.delete_project),
    path('project_report_form', views.project_report_form),
    path('find_project_of_staff/<int:staff_id>', views.find_project_of_staff),
    path('find_project_of_manager/<int:manager_id>', views.find_project_of_manager),
    path('find_project/<int:project_id>', views.find_project),
]