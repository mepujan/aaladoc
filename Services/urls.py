from django.urls import path

from .views import ServicePage, SingleServicePage, AboutUsView

app_name = 'Services'
urlpatterns = [
    path('', ServicePage.as_view(), name='services'),
    path('service/<id>', SingleServicePage.as_view(), name='singleService'),
    path('about/', AboutUsView.as_view(), name='about')
]
