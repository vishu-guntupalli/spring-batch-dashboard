from django.shortcuts import render
from .models import *
from django.db import connection


__batch_exec_sql__ = 'select bi.job_name,bi.job_instance_id,be.start_time,be.end_time,be.status,bp.key_name,bp.date_val, se.step_name,se.start_time,' \
                   'se.end_time,se.status,se.read_count,se.write_count,se.filter_count,se.commit_count ' \
                   'from batch_job_instance bi ' \
                   'inner join batch_job_execution be on (bi.job_instance_id = be.job_instance_id) ' \
                   'inner join batch_job_execution_params bp on (be.job_execution_id=bp.job_execution_id) ' \
                   'inner join batch_step_execution se on (be.job_execution_id=se.job_execution_id)  ' \
                   'order by bi.job_name, bi.job_instance_id'

__batch_exec_result_set__ = ('jobName', 'jobInstanceId', 'jobStartTime', 'jobEndTime', 'jobStatus', 'keyName', 'keyDateValue', 'stepName',
                             'stepStartTime','stepEndTime','stepStatus','stepReadCount','stepWriteCount','stepFilterCount',
                             'stepCommitCount')

__most_run_job_sql__ = 'select job_name from batch_job_instance ' \
                       'group by job_name having count(job_name) = (select max(count(job_name)) ' \
                       'from batch_job_instance group by job_name)'

__most_run_job_result_set__ = ('jobName')

def most_run_job(request):
    most_run_job_results = []
    most_run_job_rows = __run_query__(__most_run_job_sql__)

    for most_run_job_result in most_run_job_rows:
        most_run_job_dict = dict(zip(__most_run_job_result_set__,most_run_job_result))
        most_run_job_results.append(most_run_job_dict)

    return most_run_job_results


def dashboard(request):
    results = []
    formatted_results = []
    rows = __run_query__(__batch_exec_sql__)

    for result_2 in rows:
        rowsDict = dict(zip(__batch_exec_result_set__, result_2))
        results.append(rowsDict)

    for result_1 in results:
        job_already_present = False
        for formatted_result_1 in formatted_results:
            if formatted_result_1['jobName'] == result_1['jobName']:
                job_already_present = True

        if not job_already_present:
            job_object = {}
            job_object['jobName'] = result_1['jobName']
            job_object['jobInstances'] = []
            for result_2 in results:
                job_instance = {}
                job_instance_present = False
                if result_1['jobName'] == result_2['jobName']:
                    for formatted_result_2 in formatted_results:
                        for jobInstanceRow in formatted_result_2['jobInstances']:
                            if jobInstanceRow['jobInstanceId'] == result_2['jobInstanceId']:
                                job_instance_present = True
                    if not job_instance_present:
                        __build_job_instance__(job_instance, result_2)
                        for result_3 in results:
                            if (result_3['jobName'] == result_2['jobName']) and (
                                        result_2['jobInstanceId'] == result_3['jobInstanceId']):
                                job_step = __build_job_step__(result_3)
                                job_instance['jobSteps'].append(job_step)
                        job_object['jobInstances'].append(job_instance)
            formatted_results.append(job_object)
    return render(request, 'templates/dashboard.html', {'all_jobs': formatted_results})


def __build_job_step__(result_3):
    job_step = {}
    job_step['stepName'] = result_3['stepName']
    job_step['stepStartTime'] = result_3['stepStartTime']
    job_step['stepEndTime'] = result_3['stepEndTime']
    job_step['stepStatus'] = result_3['stepStatus']
    job_step['stepReadCount'] = result_3['stepReadCount']
    job_step['stepWriteCount'] = result_3['stepWriteCount']
    job_step['stepFilterCount'] = result_3['stepFilterCount']
    job_step['stepCommitCount'] = result_3['stepCommitCount']
    return job_step


def __build_job_instance__(job_instance, result_2):
    job_instance['jobInstanceId'] = result_2['jobInstanceId']
    job_instance['jobStartTime'] = result_2['jobStartTime']
    job_instance['jobEndTime'] = result_2['jobEndTime']
    job_instance['jobStatus'] = result_2['jobStatus']
    job_instance['keyName'] = result_2['keyName']
    job_instance['keyDateValue'] = result_2['keyDateValue']
    job_instance['jobSteps'] = []

def __run_query__(sql_query):
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
    return rows