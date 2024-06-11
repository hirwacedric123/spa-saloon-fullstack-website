from django.urls import path
from . import views
from .views import subscribe
urlpatterns = [   

    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('service/', views.service, name='service'),
    path('about/', views.about, name='about'),
    path('specialist/', views.specialist, name='specialist'),
    path('subscribe/', subscribe, name='subscribe'),
    path('contact_view/', views.contact_view, name='contact_view'),

]

