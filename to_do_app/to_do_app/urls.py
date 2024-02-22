"""
URL configuration for to_do_app project.

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
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from django.urls import path
from django.contrib.auth import views as auth_views
from to_do import views
from to_do.views import HomePage_view, register_view, login_view, tasks_view, add_task_view, delete_task_view
from to_do.views import CustomPasswordResetView
from to_do.views import logout_view


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', HomePage_view, name="home"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('tasks/', tasks_view, name='tasks'),
    path('addtask/', add_task_view, name='addtask'),
    path('update_task_status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    # for ticking the box when task done
    path('delete_task/<int:task_id>/', delete_task_view, name='delete_task'),
    path('logout/', logout_view, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),

    # incercare
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
