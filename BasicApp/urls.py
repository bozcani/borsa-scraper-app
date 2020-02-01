from django.urls import path
from django.contrib import admin

from . import views


app_name = 'BasicApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
]
