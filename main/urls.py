from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('types/',views.typee,name='types'),
    path('type-detail/<int:id>/',views.type_detail,name='type_detail'),
]