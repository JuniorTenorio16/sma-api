from django.urls import re_path
from sma import views

urlpatterns=[
    re_path(r'sma$', views.smaApi)
]
