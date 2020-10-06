"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from Register import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/',include('Register.urls')),
    path('',views.PostList.as_view(),name='home'),
    path('admin/', admin.site.urls,name='admin'),
    path('logout/',views.user_logout,name='logout'),
    path('post/<slug:slug>/',views.PostDetail.as_view(), name='details'),
    path('create/',views.createPost, name='create'),
    path('update/<slug:slug>/',views.UpdatePost.as_view(),name='update'),
    path('delete/<slug:slug>/',views.DeletePost.as_view(),name='delete'),
    path('<int:pk>/',views.UserPost.as_view(),name='myPost')
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)
