
from django.contrib import admin
from django.urls import path
from timetable import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('add-schedule/', views.add_schedule, name='add_schedule'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit_schedule/', views.edit_schedule, name='edit_schedule'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('workload_monitoring/', views.workload_monitoring, name='workload_monitoring'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
]
