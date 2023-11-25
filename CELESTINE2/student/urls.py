"""
URL configuration for student project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',authenticate_view,name='authenticate-view'),
    path('register/',register_view,name="register-view"),
    path('verify/',verify_view,name="verify-view"),
    path('home/', home_view,name="home-view"),
    path('allstudents/',allstudents_view,name="allstudents-view"),
    path('deletestudent/',deletestudent,name='deletstudent-view'),
    # path('attendance/',attendance_view,name='attendance-view'),
    path('adminpage/',admin_view,name="admin-view"),
    path('grades/',grades_view,name='grades-view'),
    path('model/',model_view,name='model-view'),
    path('update/<str:pk>/',update_view,name='update-view'),
    path('adminpage/<str:username>/',admin_view,name='admin-view'),
    path('pdf_view/',ViewPDF,name='pdf_view'),
    path('pdf_download/',downloadPDF,name='pdf_download'),
    path('staff/',staff,name='staff-view'),
    path('deletestaff/<str:pk>/',deleteStaff,name='deletestaff-view'),
    path('deletestudent/<str:pk>/',deleteStudent,name='deletestudent-view'),
    path('fail/<str:pk>/',failView,name='fail-view'),
    path('logout/',logout_view,name='logout-view'),
    path('notifications/',notifications_view,name='notification-view'),
    path('reset_password/', 
    auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
    name='reset_password'),

    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name="password_sent.html"),
    name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name="password_complete.html"),
    name='password_reset_confirm'),

    path('reset_password_complete', 
    auth_views.PasswordResetCompleteView.as_view(template_name="reset_done.html"), 
    name='password_reset_complete'),
    path('updateattendance/',uploadAttendance_view,name='updateAttendance-view'),
    path('csv/',attendance_csv,name="attendance-csv"),
    path('attendancecsv/',download_attendance,name='download-attendance'),
    path('pyatt/',pyatt_view,name='pyatt-view'),
    path('jsatt/',jsatt_view,name='jsatt-view'),
    path('phpatt/',phpatt_view,name='phpatt-view'),
    path('sqlatt/',sqlatt_view,name='sqlatt-view'),
    path('downloadfail/',downloadfail_view,name='download-fail'),
    path('staffpage/',staffpage_view,name="staff-page")
    
    
]
