from django.shortcuts import render
from .models import *
from django.db.models import F


def dashboard(request):
    all_jobs = BatchJobInstance.objects.select_related('batchjobexecution').all()
    return render(request, 'templates/index.html', {'all_jobs': all_jobs})

def get_complete_job_object(request):
    return None
