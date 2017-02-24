__batch_exec_sql__ = 'select bi.job_name,bi.job_instance_id,be.start_time,be.end_time,be.status,bp.key_name,bp.date_val, se.step_name,se.start_time,' \
                     'se.end_time,se.status,se.read_count,se.write_count,se.filter_count,se.commit_count ' \
                     'from batch_job_instance bi ' \
                     'inner join batch_job_execution be on (bi.job_instance_id = be.job_instance_id) ' \
                     'inner join batch_job_execution_params bp on (be.job_execution_id=bp.job_execution_id) ' \
                     'inner join batch_step_execution se on (be.job_execution_id=se.job_execution_id)  ' \
                     'order by bi.job_name, bi.job_instance_id'

__most_run_job_sql__ = 'select job_name from batch_job_instance ' \
                       'group by job_name having count(job_name) = (select max(count(job_name)) ' \
                       'from batch_job_instance group by job_name)'

__least_run_job_sql__ = 'select job_name from batch_job_instance ' \
                        'group by job_name having count(job_name) = (select min(count(job_name)) ' \
                        'from batch_job_instance group by job_name)'

__job_success_failure_sql__ = 'with total_times as ' \
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
                                'where e1.status=''FAILED'' group by i1.job_name ' \
                                '), ' \
                                'times_succeeded as ' \
                                '( ' \
                                'select i1.job_name as job_name, count(i1.job_name) as job_count ' \
                                'from batch_job_instance i1 ' \
                                'inner join batch_job_execution e1 on (i1.job_instance_id=e1.job_instance_id) ' \
                                'where e1.status=''COMPLETED'' ' \
                                'group by i1.job_name ' \
                                ') ' \
                                'select total.job_name, total.job_count as total_times, failed.job_count as failed, succeeded.job_count as succeeded ' \
                                'from total_times total ' \
                                'inner join times_failed failed on (total.job_name=failed.job_name) ' \
                                'inner join times_succeeded succeeded on (total.job_name=succeeded.job_name)'