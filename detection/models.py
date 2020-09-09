from django.db import models

# Create your models here.
class Task(models.Model):
    task_name=models.CharField(max_length=200)
    video_num=models.IntegerField(default=0)
    task_status=models.CharField(max_length=200,default="")
    detection_item=models.CharField(max_length=200,default="")
    #detection_item=models.CharField(max_length=100)
    start_time=models.DateTimeField('date published')
    finish_time=models.DateTimeField('date published')

class Video(models.Model):
    task=models.ForeignKey(Task, on_delete=models.CASCADE)
    video_name=models.CharField(max_length=200)
    detection_status=models.FloatField(default=0.0)

class Error(models.Model):
    video=models.ForeignKey(Video, on_delete=models.CASCADE)
    error_time=models.CharField(max_length=200)
    error_kind=models.CharField(max_length=200)
    error_info=models.CharField(max_length=200)

class Log(models.Model):
    task=models.IntegerField(default=0)
    video=models.IntegerField(default=0)
    time=models.DateTimeField('date published')
    log_level=models.CharField(max_length=200)