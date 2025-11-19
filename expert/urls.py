from . import views
from django.urls import path

urlpatterns = [
    path('', views.diagnose_view, name='diagnose')
]
