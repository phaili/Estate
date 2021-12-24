from django.urls import path
from . import views

urlpatterns = [

    path('add_task', views.add_task),
    path('modify_task/<int:task_id>', views.modify_task),
    path('query_task/<int:task_id>', views.query_task),
    path('delete_task/<int:task_id>', views.delete_task),
    path('find_all_task', views.find_all_task),
    path('import_manager', views.import_manager),

    path('add_task_distribution', views.add_task_distribution),
    path('modify_task_accepted/<int:task_distribution_id>', views.modify_task_accepted),
    path('modify_task_reject/<int:task_distribution_id>', views.modify_task_reject),
    path('modify_task_finished/<int:task_distribution_id>', views.modify_task_finished),
    path('staff_task_report_form', views.staff_task_report_form),


    path('query_task_distribution/<int:task_distribution_id>', views.query_task_distribution),
    path('delete_task_distribution/<int:task_distribution_id>', views.delete_task_distribution),
    path('find_all_distribution', views.find_all_distribution),
    path('get_task', views.get_task),
    path('get_staff_task/<int:staff_id>', views.get_staff_task),
    path('get_staff_task_accepted/<int:staff_id>', views.get_staff_task_accepted),

    path('add_task_advise', views.add_task_advise),
    path('modify_task_advise/<int:task_advise_id>', views.modify_task_advise),
    path('query_task_advise/<int:task_advise_id>', views.query_task_advise),
    path('delete_task_advise/<int:task_advise_id>', views.delete_task_advise),
    path('find_all_advise', views.find_all_advise),
]