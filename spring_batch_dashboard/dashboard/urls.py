from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^job-meta/',views.job_meta, name='job_meta'),
    url(r'^job-success-failure',views.job_success_failure_ratio, name='job_success_failure_ratio'),
    url(r'^$',views.dashboard, name='dashboard')
]