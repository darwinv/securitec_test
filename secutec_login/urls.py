from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.SignInView.as_view(), name='login')
]
