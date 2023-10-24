"""
URL configuration for happywedding project.

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
from weddingapp import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
     path('login/',views.login,name='login'),
    path('loginhome/',views.loginhome,name='loginhome'),
    path('logout/',views.handlelogout,name='handlelogout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('adminfirst/',views.adminfirst,name="adminfirst"),
    path('vendorhome/',views.vendorhome,name="vendorhome"),
    path("adminhome/",views.adminhome,name="adminhome"),
    path("create_user/",views.create_user,name="create_user"),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path("update_user/<int:user_id>/",views.update_user,name="update_user"),
    path('update_profile/',views.update_profile,name="update_profile"),
    path('change_password/', PasswordChangeView.as_view(success_url=reverse_lazy('login')), name='change_password'),
    path('change_password/done/', PasswordChangeDoneView.as_view(), name='change_password_done'),


]

