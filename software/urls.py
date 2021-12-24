from django.urls import path
from . import views

urlpatterns = [
    path('add_software_record', views.add_software_record),
    path('modify_software_record/<int:software_record_id>', views.modify_software_record),
    path('query_software_record/<int:staff>', views.query_software_record),
    path('delete_software_record/<int:software_record_id>', views.delete_software_record),
    path('find_all', views.find_all),
    path('add_software', views.add_software),
]