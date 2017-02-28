class BatchSql:

    batch_exec_result_set = ('jobName', 'jobInstanceId', 'jobStartTime', 'jobEndTime', 'jobStatus', 'keyName', 'keyDateValue', 'stepName',
                            'stepStartTime', 'stepEndTime', 'stepStatus', 'stepReadCount', 'stepWriteCount', 'stepFilterCount',
                            'stepCommitCount')

    batch_exec_sql =     'select bi.job_name,bi.job_instance_id,be.start_time,be.end_time,be.status,bp.key_name,bp.date_val, se.step_name,se.start_time,' \
                         'se.end_time,se.status,se.read_count,se.write_count,se.filter_count,se.commit_count ' \
                         'from batch_job_instance bi ' \
                         'inner join batch_job_execution be on (bi.job_instance_id = be.job_instance_id) ' \
                         'inner join batch_job_execution_params bp on (be.job_execution_id=bp.job_execution_id) ' \
                         'inner join batch_step_execution se on (be.job_execution_id=se.job_execution_id)  ' \
                         'order by bi.job_name, bi.job_instance_id'

    job_run_result_set = ('jobName', '')

    most_run_job_sql = 'select job_name from batch_job_instance ' \
                       'group by job_name having count(job_name) = (select max(count(job_name)) ' \
                       'from batch_job_instance group by job_name)'

    least_run_job_sql = 'select job_name from batch_job_instance ' \
                        'group by job_name having count(job_name) = (select min(count(job_name)) ' \
                        'from batch_job_instance group by job_name)'

    job_success_failure_result_set = ('jobName', 'totalCount', 'failedCount', 'succeededCount')

    job_success_failure_sql =     'with total_times as ' \
                                  '( ' \
                                  'select i1.job_name as job_name, count(i1.job_name) as job_count ' \
                                  'from batch_job_instance i1 ' \
                                  'inner join batch_job_execution e1 on (i1.job_instance_id=e1.job_instance_id) ' \
                                  'group by i1.job_name ), ' \
                                  'times_failed as ' \
                                  '( ' \
                                  'select i1.job_name as job_name, count(i1.job_name) as job_count ' \
                                  'from batch_job_instance i1 ' \
                                  'inner join batch_job_execution e1 on (i1.job_instance_id=e1.job_instance_id) ' \
                                  "where e1.status='FAILED' group by i1.job_name " \
                                  '), ' \
                                  'times_succeeded as ' \
                                  '( ' \
                                  'select i1.job_name as job_name, count(i1.job_name) as job_count ' \
                                  'from batch_job_instance i1 ' \
                                  'inner join batch_job_execution e1 on (i1.job_instance_id=e1.job_instance_id) ' \
                                  "where e1.status='COMPLETED' " \
                                  'group by i1.job_name ' \
                                  ') ' \
                                  'select total.job_name, total.job_count as total_times, failed.job_count as failed, succeeded.job_count as succeeded ' \
                                  'from total_times total ' \
                                  'left outer join times_failed failed on (total.job_name=failed.job_name) ' \
                                  'left outer join times_succeeded succeeded on (total.job_name=succeeded.job_name)'

    total_time_ran_result_set = ('days', 'hours', 'minutes', 'seconds')

    total_time_ran_sql =     'with total_time_ran as ' \
                             '( ' \
                             'select numtodsinterval( ' \
                             'sum( extract(day from (end_time-start_time)) * 86400 + ' \
                             'extract(hour from (end_time-start_time)) * 3600 + ' \
                             'extract(minute from (end_time-start_time)) * 60 + ' \
                             "extract(second from (end_time-start_time)) ), 'SECOND') as total_time " \
                             'from batch_job_execution ' \
                             ') ' \
                             'select extract(day from total_time) as days, ' \
                             'extract(hour from total_time) as hours, ' \
                             'extract(minute from total_time) as minutes, ' \
                             'extract(second from total_time) as seconds from total_time_ran'
