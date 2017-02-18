from django.shortcuts import render
from .models import *
from django.db import connection


__batch_exec_sql__ = 'select bi.job_name,be.start_time,be.end_time,be.status,bp.key_name,bp.date_val, se.step_name,se.start_time,' \
                   'se.end_time,se.status,se.read_count,se.write_count,se.filter_count,se.commit_count from batch_job_instance bi ' \
                   'inner join batch_job_execution be on (bi.job_instance_id = be.job_instance_id) ' \
                   'inner join batch_job_execution_params bp on (be.job_execution_id=bp.job_execution_id) ' \
                   'inner join batch_step_execution se on (be.job_execution_id=se.job_execution_id)  ' \
                   'order by bi.job_name, be.start_time'

__batch_resultset__ = ('jobName', 'jobStartTime', 'jobEndTime', 'jobStatus', 'keyName', 'keyDateValue', 'stepName',
                       'stepStartTime','stepEndTime','stepStatus','stepReadCount','stepWriteCount','stepFilterCount',
                       'stepCommitCount')

def dashboard(request):
    results = []
    with connection.cursor() as cursor:
        cursor.execute(__batch_exec_sql__)
        rows = cursor.fetchall()
    for row in rows:
        rowsDict = dict(zip(__batch_resultset__,row))
        results.append(rowsDict)

    return render(request, 'templates/index.html', {'all_jobs': results})
