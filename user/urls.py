from . import views
from django.urls import path
urlpatterns = [
    path('login', views.login_view),
    path('register', views.register_view),
    path('logout', views.logout_view),
    path('index', views.index_view),
    path('update_staff_info/<int:staff_id>', views.update_staff_info),
    path('find_all_staff', views.find_all_staff),
    path('find_all_manager', views.find_all_manager),
    path('find_depart_staff/<str:depart>', views.find_depart_staff),
    path('user_report_form', views.user_report_form),


]