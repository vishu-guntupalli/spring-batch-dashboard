from __future__ import unicode_literals

from django.db import models

class BatchJobExecution(models.Model):
    job_execution_id = models.BigIntegerField(primary_key=True)
    version = models.BigIntegerField(blank=True, null=True)
    job_instance = models.ForeignKey('BatchJobInstance', models.DO_NOTHING)
    create_time = models.DateTimeField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    exit_code = models.CharField(max_length=2500, blank=True, null=True)
    exit_message = models.CharField(max_length=2500, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    job_configuration_location = models.CharField(max_length=2500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'batch_job_execution'


class BatchJobExecutionContext(models.Model):
    job_execution = models.ForeignKey(BatchJobExecution, models.DO_NOTHING, primary_key=True)
    short_context = models.CharField(max_length=2500)
    serialized_context = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'batch_job_execution_context'


class BatchJobExecutionParams(models.Model):
    job_execution = models.ForeignKey(BatchJobExecution, models.DO_NOTHING)
    type_cd = models.CharField(max_length=6)
    key_name = models.CharField(max_length=100)
    string_val = models.CharField(max_length=250, blank=True, null=True)
    date_val = models.DateTimeField(blank=True, null=True)
    long_val = models.BigIntegerField(blank=True, null=True)
    double_val = models.FloatField(blank=True, null=True)
    identifying = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'batch_job_execution_params'


class BatchJobInstance(models.Model):
    job_instance_id = models.BigIntegerField(primary_key=True)
    version = models.BigIntegerField(blank=True, null=True)
    job_name = models.CharField(max_length=100)
    job_key = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'batch_job_instance'
        unique_together = (('job_name', 'job_key'),)


class BatchStepExecution(models.Model):
    step_execution_id = models.BigIntegerField(primary_key=True)
    version = models.BigIntegerField()
    step_name = models.CharField(max_length=100)
    job_execution = models.ForeignKey(BatchJobExecution, models.DO_NOTHING)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    commit_count = models.BigIntegerField(blank=True, null=True)
    read_count = models.BigIntegerField(blank=True, null=True)
    filter_count = models.BigIntegerField(blank=True, null=True)
    write_count = models.BigIntegerField(blank=True, null=True)
    read_skip_count = models.BigIntegerField(blank=True, null=True)
    write_skip_count = models.BigIntegerField(blank=True, null=True)
    process_skip_count = models.BigIntegerField(blank=True, null=True)
    rollback_count = models.BigIntegerField(blank=True, null=True)
    exit_code = models.CharField(max_length=2500, blank=True, null=True)
    exit_message = models.CharField(max_length=2500, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'batch_step_execution'


class BatchStepExecutionContext(models.Model):
    step_execution = models.ForeignKey(BatchStepExecution, models.DO_NOTHING, primary_key=True)
    short_context = models.CharField(max_length=2500)
    serialized_context = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'batch_step_execution_context'

