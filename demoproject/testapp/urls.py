from django.urls import path

from .views import TaskCBV

urlpatterns =[
    path('', TaskCBV.as_view(), name='taskapi'),
]