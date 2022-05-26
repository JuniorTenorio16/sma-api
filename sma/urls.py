from django.urls import re_path
from sma import views

urlpatterns=[
    re_path(r'(?P<pair>\D+)/mms', views.smaApi),
    re_path(r'^missing/', views.recordingMissing, name='list-missing')
]
