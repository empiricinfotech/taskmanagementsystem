from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
import random
import datetime
from datetime import date
from django.db.models import Q
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Case, When,Value
from django.core.paginator import Paginator
import re
from django.http import JsonResponse


User = get_user_model()

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()
    get_object_or_404(Task, task_title=notification.task_name)
    return redirect('notificationView')

def notificationView(request):
    priority_order = {
        'Highest': 0,
        'High': 1,
        'Medium': 2,
        'Low': 3,
    }
    assignTask = Task.objects.filter(assign_To=request.user)
    get_tasks = Notification.objects.all()
    notifications= []
    p = Paginator(assignTask, 5) 
    page_number = request.GET.get('page')
    try:
        data = p.get_page(page_number)
    except :
        data = p.page(1)
    for i in data:
        task= i
        for j in get_tasks:
            taskname = (j.task_name)
            if taskname == task:
                notifications.append({   
                    "id":j.id,
                    "task_id":task.id,
                    "title":j.title,
                    "read":j.read,
                })
    return render(request,'notification.html',{'notifications':notifications,'data': data})

def homeview(request):
    form = createTaskForm()
    if request.method == 'POST':
        form = createTaskForm(request.POST)
        return JsonResponse({'form': form})
    else:
        form = createTaskForm(initial={'status': 'Open'})
        pending_form = createTaskForm(initial={'status': 'Pending'})
        context = {'form': form,'pending_form':pending_form}
        return render(request,'home.html',context) 

def pendingTaskView(request):
    form = createTaskForm()
    if request.method == 'POST':
        form = createTaskForm(request.POST)
        return JsonResponse({'form': form})
    else:
        form = createTaskForm(initial={'status': 'Pending'})
        context = {'form': form}
        return render(request,'home.html',context) 
    
@login_required
def create_task(request):
    form = createTaskForm()
    if request.method == 'POST':
        form = createTaskForm(request.POST)
        if form.is_valid():
            current_date = datetime.datetime.now().date()
            notification_msg = str(str(request.user) +' created ' + form.cleaned_data['task_title'])
            if form.cleaned_data['endDate'] is not None:
                if form.cleaned_data['startDate'] and form.cleaned_data['endDate'] >= current_date:
                    save_form = form.save()
                    save_form.created_By = request.user
                    save_form.save()
                    Notification.objects.create(title=notification_msg,pushed_by=request.user,task_name=save_form,createdDate=current_date)
                    return redirect('taskList')
                else:
                    return redirect('createtask')
            else:
                return redirect('createtask')
    return render(request,"task.html",{"form":form,'room_name':request.user})

@login_required
def taskList(request):
    priority_order = {
        'Highest': 0,
        'High': 1,
        'Medium': 2,
        'Low': 3,
    }
    priority_ordering_case = Case(*[When(priority=p, then=Value(priority_order[p])) for p in priority_order])
    createdTask = Task.objects.filter(Q(created_By=request.user)|Q(assign_To=request.user)).order_by(priority_ordering_case)
    if request.method == 'GET':
        createdTask = Task.objects.filter(Q(created_By=request.user)|Q(assign_To=request.user)).order_by(priority_ordering_case)
        users = User.objects.all()
        task = Task.objects.all()
        p = Paginator(createdTask, 10) 
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except :
            page_obj = p.page(1)
        context = {
            "current_user":request.user,
            "users" : users,
            "priorities":Task.PRIORITIES,
            "status_choice":Task.STATUS_CHOICES,
            "progress_choice":Task.PROGRESS_CHOICE,
            "tasks":task,
            'page_obj': page_obj,
            'flag':createdTask,
            'FlagDemo':"createdTask"
        }
        return render(request,'task_list.html',context=context)
    
    if request.method == 'POST':    
        searchIn = request.POST.get('searchIn',None)
        if (searchIn is not None) and (searchIn != ''):
            keyword = request.POST['searchIn']
            users = User.objects.all()
            task = Task.objects.filter(created_By = request.user)
            tasks = task.filter(Q(task_title__icontains=keyword)|Q(priority__icontains=keyword))
            p = Paginator(tasks,5) 
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)
            except :
                page_obj = p.page(1)
            return render(request,'task_list.html',{"createdTask":tasks,'page_obj': page_obj,"users" : users,})
        else:
            try:
                priorities = request.POST.get('priority',None)
                tasK = Task.objects.get(id=request.POST['id'])
                if tasK:
                    if request.POST['assign'] != 'None':
                        if request.FILES.getlist('upload'):
                            assignee = User.objects.get(email = request.POST['assign'])
                            tasK.task_title = request.POST['task_title']
                            tasK.status = request.POST['status_choice']
                            tasK.priority = request.POST['priorities']
                            tasK.description = request.POST['Desc']
                            tasK.assign_To = assignee
                            tasK.startDate = request.POST['startdate']
                            tasK.endDate = request.POST['duedate']
                            tasK.save()
                            taskImg = request.FILES.getlist('upload')
                            dependencies = request.POST.get('dependencies',None)
                            for image in taskImg:
                                TaskImages.objects.create(task=tasK,taskimage=image)
                            if (dependencies is not None) and (dependencies != ''):
                                depen = request.POST.getlist('dependencies')
                                for i in depen:
                                    dependency = Task.objects.get(id=i)
                                    tasK.dependency.add(dependency)
                            msg = str(str(request.user) +" assigned " + tasK.task_title + "Task To " + request.POST['assign'])
                            notification = Notification.objects.get(task_name=tasK)
                            notification.title = msg
                            notification.pushed_by = request.user
                            notification.read =False
                            notification.save()
                            url = f"http://127.0.0.1:8000/task/{tasK.id}"
                            send_notification_email(request.user,msg,url)
                            return render(request,'task_list.html')
                        elif (priorities is not None) and (priorities != ''):
                            assignee = User.objects.get(email = request.POST['assign'])
                            tasK.assign_To = assignee
                            tasK.priority = request.POST['priority']
                            tasK.status = request.POST['status']
                            tasK.progress = request.POST['progress']
                            tasK.save()
                            msg = str(str(request.user) +" assigned " + tasK.task_title + "Task To " + request.POST['assign'])
                            notification = Notification.objects.get(task_name=tasK)
                            notification.title = msg
                            notification.pushed_by = request.user
                            notification.read =False
                            notification.save()
                            url = f"http://127.0.0.1:8000/task/{tasK.id}"
                            send_notification_email(request.user,msg,url)
                            return render(request,'task_list.html')
                        else:
                            assignee = User.objects.get(email = request.POST['assign'])
                            tasK.task_title = request.POST['task_title']
                            tasK.status = request.POST['status_choice']
                            tasK.priority = request.POST['priorities']
                            tasK.description = request.POST['Desc']
                            tasK.assign_To = assignee
                            tasK.startDate = request.POST['startdate']
                            tasK.endDate = request.POST['duedate']
                            tasK.save()
                            dependencies = request.POST.get('dependencies',None)
                            if (dependencies is not None) and (dependencies != ''):
                                depen = request.POST.getlist('dependencies')
                                for i in depen: 
                                    dependency = Task.objects.get(id=i)
                                    tasK.dependency.add(dependency)
                            msg = str(str(request.user) +" assigned " + tasK.task_title + "Task To " + request.POST['assign'])
                            notification = Notification.objects.get(task_name=tasK)
                            notification.title = msg
                            notification.pushed_by = request.user
                            notification.read =False
                            notification.save()
                            url = f"http://127.0.0.1:8000/task/{tasK.id}"
                            send_notification_email(request.user,msg,url)
                            return render(request,'task_list.html')
                    else:
                        tasK.priority = request.POST['priority']
                        tasK.status = request.POST['status']
                        tasK.progress = request.POST['progress']
                        tasK.save()
                        return render(request,'task_list.html')
            except:
                current_date = date.today()
                if request.POST['startdate'] and request.POST['enddate'] is not None:
                    if  datetime.datetime.strptime(request.POST['startdate'], '%Y-%m-%d').date() and  datetime.datetime.strptime(request.POST['enddate'], '%Y-%m-%d').date() >= current_date:
                        title = request.POST['task_title']
                        assign_To = request.POST['assign_To']
                        startdate = request.POST['startdate']
                        enddate = request.POST['enddate']
                        status_choice = request.POST['status_choice']
                        progress_choice = request.POST['progress_choice']
                        priorities = request.POST['priorities'] 
                        Descrp = request.POST['Desc'] 
                        taskImg = request.FILES.getlist('upload')
                        depen = request.POST.getlist('tasksdepn')
                        if assign_To != "None":
                            assignn = User.objects.get(email = assign_To)
                            createTask = Task.objects.create(task_title=title,assign_To=assignn,created_By=request.user,startDate=startdate,endDate=enddate,status=status_choice,progress=progress_choice,priority=priorities,description=Descrp)
                            createTask.created_By = request.user
                            createTask.save()
                            for image in taskImg:
                                TaskImages.objects.create(task=createTask,taskimage=image)
                            for i in depen:
                                dependency = Task.objects.get(id=i)
                                createTask.dependency.add(dependency)  
                            notification_msg = str(str(request.user) +" assigned " + title + "Task To " + assign_To)
                            notification = Notification.objects.create(title=notification_msg,pushed_by=request.user,task_name=createTask,createdDate=current_date)
                            url = f"http://127.0.0.1:8000/task/{createTask.id}"
                            send_notification_email(assign_To,notification_msg,url)
                            return redirect('taskList')
                        else:
                            createTask = Task.objects.create(task_title=title,created_By=request.user,assign_To=None,startDate=startdate,endDate=enddate,status=status_choice,progress=progress_choice,priority=priorities,description=Descrp)
                            image_paths = []
                            for image in taskImg:
                                TaskImages.objects.create(task=createTask,taskimage=image)
                            for i in depen:
                                dependency = Task.objects.get(id=i)
                                createTask.dependency.add(dependency)  
                            createTask.save()
                            notification_msg = str(str(request.user) +" assigned " + title + "Task To " + assign_To)
                            notification = Notification.objects.create(title=notification_msg,pushed_by=request.user,task_name=createTask,createdDate=current_date)
                            return redirect('taskList')
                    else:
                        return redirect('taskList')
                else:
                    return redirect('taskList')    
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if (request.user == task.created_By):
        task.delete()
        return redirect('taskList')
    
@login_required
def display_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    depen = task.dependency.all() 
    depen_titles = depen.values_list('id', flat=True)
    images = TaskImages.objects.filter(task=task)
    assignTo = User.objects.all()
    tasks = Task.objects.all()
    return render(request, 'task_display.html',{"task":task,"user":request.user,"depen_titles":depen_titles,"depen":depen,"images":images,"assignTo":assignTo,"tasks":tasks} )

def deleteTaskIamge(request, pk):
    task = get_object_or_404(TaskImages, pk=pk)
    task.delete()
    return JsonResponse({'success': True})
    
@login_required
def edit_task(request, pk):
    if request.method == 'GET':
        return render(request, 'task_list.html')
    if request.method == 'POST':
        p = request.POST['id']
        return render(request, 'task_list.html')

def generateOTP():
    return random.randrange(1000 , 9999)

def send_otp_email(email):
    otp = generateOTP()
    print('OTP-------------email------------------ ',otp)

    message = Mail(
        from_email='nk.empiric@gmail.com',
        to_emails=f'{email}',
        subject='Sending with Twilio SendGrid is Fun',
        html_content=f'<strong>Your verification code is: {otp}</strong>'
        )
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    user = User.objects.get(email=email)
    user.otp = otp
    user.save()
    return email

def send_notification_email(email,msg,url):
    message = Mail(
        from_email='nk.empiric@gmail.com',
        to_emails=f'{email}',
        subject='Task details',
        html_content=(f"{msg}<strong>Task Details URL :</strong> {url}")
        )
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    return email

def filter_tasks(request):
    keyword = request.POST.get('searchIn')
    tasks = Task.objects.filter(task_title__icontains=keyword) if keyword else Task.objects.all()
    return render(request, 'task_list.html', {'createdTask': tasks})

def forgotpasswordview(request):
    if request.method == 'POST':
        email = request.POST['email'] 
        if not User.objects.filter(email=email).first():
            return redirect('forgotpassword')
        else:
            user_obj = User.objects.get(email=request.POST['email'] ) 
            request.session['email'] = request.POST['email']
            send_otp_email(user_obj)
            return redirect('verifyotp')  
    return render(request,'forgotpassword.html')

def verifyotpview(request):
    if request.session.has_key('email'):
        email = request.session['email']
        user_otp = User.objects.get(email=email)
        my_otp = str(user_otp.otp)
        if request.method == 'POST':
            otp = str(request.POST.get('otp'))
            if otp == my_otp:
                return redirect('resetpassword')
            else:
                return render(request,'verifyotp.html',{"Invalid":"Invalid"})
    return render(request,'verifyotp.html')

class ResetPasswordView(View):
    def get(self, request):
        return render(request,'resetpassword.html')
    def post(self, request):
        if request.session.has_key('email'):
            user = request.session['email']
            user = User.objects.get(email=request.session['email'])
            password_pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
            if user:
                newpassword = request.POST['newpassword']
                if newpassword != '':
                    if re.fullmatch(password_pattern, newpassword):
                        user.set_password(newpassword)
                        user.save()
                        return redirect('profile')
                    else:
                        return render(request,'resetpassword.html',{"PasswordWrong":"Invalid Password"})
                else:
                    return render(request,'resetpassword.html')
        else:
            user = User.objects.get(email=request.user)
            if user:
                newpassword = request.POST['newpassword']
                if newpassword != '':
                    if re.fullmatch(password_pattern, newpassword):
                        user.set_password(newpassword)
                        user.save()
                        return redirect('profile')
                    else: 
                        return render(request,'resetpassword.html',{"PasswordWrong":"Invalid Password"})
                else:
                    return render(request,'resetpassword.html')
        return render(request,'resetpassword.html')
    
class ResetPwdView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'resetpwd.html')
    def post(self, request, *args, **kwargs):
        if request.session.has_key('email'):
            user = request.session['email']
            password_pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
            try:
                user = User.objects.get(username=request.session['email'])
                if user:
                    newpassword = request.POST['newpassword']
                    if newpassword != '':
                        if re.fullmatch(password_pattern, newpassword):
                            user.set_password(newpassword)
                            user.save()
                            return redirect('profile')
                        else:
                            return render(request,'resetpwd.html',{"PasswordWrong":"Invalid Password"})
                    else:
                        return render(request,'resetpwd.html')
            except:
                user = User.objects.get(email=request.session['email'])
                if user:
                    newpassword = request.POST['newpassword']
                    if newpassword != '':
                        if re.fullmatch(password_pattern, newpassword):
                            user.set_password(newpassword)
                            user.save()
                            return redirect('profile')
                        else: 
                            return render(request,'resetpwd.html',{"PasswordWrong":"Invalid Password"})
                    else:
                        return render(request,'resetpwd.html')
        else:
            user = User.objects.get(username=request.user)
            if user:
                newpassword = request.POST['newpassword']
                if newpassword != '':
                    if re.fullmatch(password_pattern, newpassword):
                        user.set_password(newpassword)
                        user.save()
                        return redirect('profile')
                    else:
                        return render(request,'resetpwd.html',{"PasswordWrong":"Invalid Password"})
                else:
                    return render(request,'resetpwd.html')
        return render(request,'resetpwd.html')

def loginview(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            login(request, user)
            request.session['email'] = request.POST['username']
            return redirect("profile")
        else:
            try:
                user = User.objects.get(email=request.POST['username'])
                user = authenticate(username=user.username, password=request.POST['password'])
                
                if user is not None:
                    login(request, user)
                    request.session['email'] = request.POST['username']
                    return render(request, "profile.html", context={'user': user})
            except User.DoesNotExist:
                pass
            return render(request,'login.html',{"not_found":"User Not Found"})
    return render(request,'login.html') 

def signupview(request):    
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    password_pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if username != '':
            if email != '':
                if re.fullmatch(regex, email):
                    if password != '':
                        if re.fullmatch(password_pattern, password):
                            if not User.objects.filter(username=username).exists():
                                if not User.objects.filter(email=email).exists():
                                    user = User.objects.create(username=username,email=email,password=password)
                                    user.set_password(password)
                                    user.is_staff = True
                                    user.is_admin = True
                                    user.is_superuser = True
                                    user.save()
                                    return redirect("login")
                                else:
                                    return redirect("signup")
                            return redirect("signup")
                        else:
                            return render(request,"signup.html",{"passwordError":"Invalid Password"})
                    else:
                        return redirect("signup")   
                else:
                    return render(request,"signup.html",{"invalid":"Enter Valid Email Address"})
            else:
                return redirect("signup")
        else:
            return redirect("signup")  
    return render(request,"signup.html")

class ProfileView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user = request.user
        form = editProfileForm(instance=user)
        return render(request, 'profile.html', {'form': form})

    def patch(self, request, *args, **kwargs):
        form = editProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, 'profile.html', {'form': form})
    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            if request.FILES['uploaded_file']:
                user.profile_img = request.FILES['uploaded_file']
                user.save() 
                pro_img= user.profile_img
                context = {
                "cover_pic":pro_img.url
                }
                return render(request, 'profile.html',  context=context)
        except:
            form = editProfileForm(request.POST,instance=request.user)
            if form.is_valid():
                form.save()
                return render(request, 'profile.html', {'form': form,"Success":"Updated"})
            else:
                return render(request, 'profile.html', {'form': form,"error":"Error"})
def logoutview(request):
    logout(request)
    return redirect("login")


   