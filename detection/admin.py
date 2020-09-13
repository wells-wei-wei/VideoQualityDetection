from django.contrib import admin
from . import models

class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'video_num', 'task_status', 'detection_item', 'start_time', 'finish_time')
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=models.Task):
        return False

class VideoAdmin(admin.ModelAdmin):
    list_display = ('task', 'video_name', 'detection_status')
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=models.Video):
        return False

class ErrorAdmin(admin.ModelAdmin):
    list_display = ('video', 'error_time', 'error_kind', 'error_info')
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=models.Error):
        return False

class LogAdmin(admin.ModelAdmin):
    list_display = ('task', 'video', 'time', 'log_level')
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=models.Log):
        return False


admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.Error, ErrorAdmin)
admin.site.register(models.Log, LogAdmin)