from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    otp =models.PositiveIntegerField(blank=True,null=True)
    email = models.EmailField(('email address'), unique=True)
    profile_img = models.ImageField(upload_to="profileImages",null=True,blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class Task(models.Model):
    PRIORITIES = (
        ("Highest","Highest"),
        ("High","High"),
        ("Medium","Medium"),
        ("Low","Low")
    )
    STATUS_CHOICES = (
    ("Done","Done"),
    ("Pending","Pending"),
    ("InProgress", "InProgress"),
    ("Open", "Open"),
    )
    PROGRESS_CHOICE = (
        ("0%","0%"),
        ("10%","10%"),
        ("20%","20%"),
        ("30%","30%"),
        ("40%","40%"),
        ("50%","50%"),
        ("60%","60%"),
        ("70%","70%"),
        ("80%","80%"),
        ("90%","90%")
    )
    task_title = models.CharField(max_length=400, verbose_name='task_title',blank=True,null=True)
    created_By = models.ForeignKey(User,related_name="createduser", on_delete=models.SET_NULL, blank=True, null=True)
    assign_To = models.ForeignKey(User,related_name="assigneduser" ,on_delete=models.SET_NULL, blank=True, null=True ,default="None")
    startDate = models.DateField(default=timezone.now, blank=True)  
    endDate = models.DateField(blank=True)
    status = models.CharField(max_length = 20,choices = STATUS_CHOICES,default = 'Open')
    progress = models.CharField(max_length=20, choices = PROGRESS_CHOICE,default = '0%' ,blank=True, null=True)
    description = models.CharField(max_length=255, blank=False, null = False)
    priority = models.CharField(max_length = 20,choices = PRIORITIES,default = 'Low')
    dependency = models.ManyToManyField("Task",related_name="dependencies",blank=True)
    
    def __str__(self):  
        return self.task_title

class Notification(models.Model):
    title = models.CharField(max_length=255)
    pushed_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=False)
    read = models.BooleanField(default=False, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True,)
    updatedDate = models.DateTimeField(auto_now=True)
    task_name = models.ForeignKey(Task,on_delete=models.CASCADE, blank=True, null=False)
    
    class Meta:
        ordering = ['-createdDate']
        
class TaskImages(models.Model):
    task = models.ForeignKey(Task,on_delete=models.SET_NULL,blank=True,null=True)
    taskimage = models.ImageField(upload_to='taskImage', null=True, blank=True)