from django.urls import path, include
from . import views
app_name = 'register'

urlpatterns =[
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='user_login'),
    path('help/',views.user_login,name='help'),
]