from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^job-meta/',views.job_meta, name='job_meta'),
    url(r'^$',views.dashboard, name='dashboard')
]