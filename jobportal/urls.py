"""jobportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from job.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf.urls import url
urlpatterns = [
    url(r'^media/(?P<path>.*)$',serve,{'document_root':  settings.MEDIA_ROOT}),
    url(r'static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),
    path('forget_password/',forget_password, name='forget_password'),
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('admin_login',admin_login,name="admin_login"),
    path('admin_home',admin_home,name="admin_home"),
    path('Logout',Logout,name="Logout"),
    path('contact',contact,name="contact"),
    path('user_signup',user_signup,name="user_signup"),
    path('recruiter_signup',recruiter_signup,name="recruiter_signup"),
    path('user_login',user_login,name="user_login"),
    path('recruiter_login',recruiter_login,name="recruiter_login"),
    path('user_home',user_home,name="user_home"),
    path('about',about,name="about"),
    path('change_passwordadmin',change_passwordadmin,name="change_passwordadmin"),
    path('change_passworduser',change_passworduser,name="change_passworduser"),
    path('change_passwordrecruiter',change_passwordrecruiter,name="change_passwordrecruiter"),
    path('recruiter_home',recruiter_home,name="recruiter_home"),
    path('job_list',job_list,name="job_list"),
    path('add_job',add_job,name="add_job"),
    path('user_latestjobs',user_latestjobs,name="user_latestjobs"),
    path('job_detail/<int:pid>',job_detail,name="job_detail"),
    path('application_success/<int:pid>',application_success,name="application_success"),
    path('marketing',marketing,name="marketing"),
    path('Customer_Service',Customer_Service,name="Customer_Service"),
    path('Project_Management',Project_Management,name="Project_Management"),
    path('Human_Resource',Human_Resource,name="Human_Resource"),
    path('Bussiness_Development',Bussiness_Development,name="Bussiness_Development"),
    path('Sales_and_Communication',Sales_and_Communication,name="Sales_and_Communication"),
    path('Teaching_and_Education',Teaching_and_Education,name="Teaching_and_Education"),
    path('Design_and_Creative',Design_and_Creative,name="Design_and_Creative"),
    path('recruiter_all',recruiter_all,name="recruiter_all"),
    path('delete_recruiter/<int:pid>',delete_recruiter,name="delete_recruiter"),
    path('joblist_companies/<int:pid>',joblist_companies,name="joblist_companies"),
    path('search-blogs',BlogSearchView.as_view(),name="search_blogs"),
    path('delete_job/<int:pid>',delete_job,name="delete_job"),
    path('view_users',view_users,name="view_users"),
    path('delete_user/<int:pid>',delete_user,name="delete_user"),
    path('latest_jobs',latest_jobs,name="latest_jobs"),
    path('services',services,name="services"),
    path('change_status/<int:pid>',change_status,name="change_status"),
    path('applied_candidatelist',applied_candidatelist,name="applied_candidatelist"),
    path('build_cv',build_cv,name="build_cv"),
    path('resume/<int:pid>',resume,name="resume"),
    path('privacy_policy',privacy_policy,name="privacy_policy"),
    path('edit_jobdetail/<int:pid>',edit_jobdetail,name="edit_jobdetail"),
    path('upcoming_jobs',upcoming_jobs,name="upcoming_jobs"),
    path('password_reset_done',password_reset_done,name="password_reset_done"),
    path('edit_profile',edit_profile,name="edit_profile"),
    path('edit_profilerecruiter',edit_profilerecruiter,name="edit_profilerecruiter"),
    path('email_setting',email_setting,name="email_setting")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# handler404='job.views.error_404_view'