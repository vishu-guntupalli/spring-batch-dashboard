from django.shortcuts import render
from django.db import connection
from .batch_sql import BatchSql
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required()
def total_time_ran(request):
    total_time_ran_result = __run_query__(BatchSql.total_time_ran_sql)
    return dict(zip(BatchSql.total_time_ran_result_set, total_time_ran_result[0]))

@login_required()
def job_success_failure_ratio(request):
    job_success_failure_results = []
    job_success_failure_rows = __run_query__(BatchSql.job_success_failure_sql)

    for job_success_failure_row in job_success_failure_rows:
        job_success_failure_dict = dict(zip(BatchSql.job_success_failure_result_set, job_success_failure_row))
        job_success_failure_results.append(job_success_failure_dict)

    return JsonResponse(job_success_failure_results, safe=False)

@login_required()
def most_run_job(request):
    most_run_job_results = []
    most_run_job_rows = __run_query__(BatchSql.most_run_job_sql)

    for most_run_job_result in most_run_job_rows:
        most_run_job_dict = dict(zip(BatchSql.job_run_result_set, most_run_job_result))
        most_run_job_results.append(most_run_job_dict)

    return most_run_job_results

@login_required()
def least_run_job(request):
    least_run_job_results = []
    least_run_job_rows = __run_query__(BatchSql.least_run_job_sql)

    for least_run_job_result in least_run_job_rows:
        least_run_job_dict = dict(zip(BatchSql.job_run_result_set, least_run_job_result))
        least_run_job_results.append(least_run_job_dict)

    return least_run_job_results

@login_required()
def dashboard(request):
    totalTimeRan = total_time_ran(request)
    mostRunJob = most_run_job(request)
    leastRunJob = least_run_job(request)

    dashboard = {}
    dashboard['totalTimeRan'] = totalTimeRan
    dashboard['mostRunJob'] = mostRunJob[0]
    dashboard['leastRunJob'] = leastRunJob[0]

    return render(request, 'templates/dashboard.html', {'dashboard' : dashboard})

@login_required()
def job_meta(request):
    results = []
    formatted_results = []
    rows = __run_query__(BatchSql.batch_exec_sql)

    for result_2 in rows:
        rowsDict = dict(zip(BatchSql.batch_exec_result_set, result_2))
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
    return render(request, 'templates/job-meta.html', {'all_jobs': formatted_results})


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