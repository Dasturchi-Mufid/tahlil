from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('types/',views.type,name='types'),
]