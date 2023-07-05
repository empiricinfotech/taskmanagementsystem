from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username','email', 'first_name', 'last_name', 'is_staff','otp')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk','task_title','created_By','assign_To','startDate','endDate','status','progress','description','priority')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display=('id','title','pushed_by','read','createdDate','updatedDate','task_name')

@admin.register(TaskImages)
class TaskImagesAdmin(admin.ModelAdmin):
    list_display=('id','task','taskimage')