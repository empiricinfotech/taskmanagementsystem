from django.urls import path
from TaskApp.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     path("",loginview,name="login"),
     path("signup/",signupview,name="signup"),
     path("filter_tasks/",filter_tasks,name="filter_tasks"),
     path("createtask/",create_task,name="createtask"),
     path("pendingTaskView/",pendingTaskView,name="pendingTaskView"),
     path("notificationView/",notificationView,name="notificationView"),
     path("home/",homeview,name="home"),
     path("tasklist/",taskList,name="taskList"),
     path("task/<int:pk>",display_task,name="display_task"),
     path("image/<int:pk>",deleteTaskIamge,name="deleteTaskIamge"),
     path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
     path('<int:notification_id>/markasread/', mark_notification_as_read, name='mark_notification_as_read'),
     path('edit/<int:pk>', edit_task, name='edit_task'),
     path("verifyotp/",verifyotpview,name="verifyotp"),
     path("forgotpassword/",forgotpasswordview,name="forgotpassword"),
     path("resetpassword/",ResetPasswordView.as_view(),name="resetpassword"),
     path("resetpasword/",ResetPwdView.as_view(),name="resetpasword"),
     path("logout/", logoutview, name="logout"),
     path('profile/', ProfileView.as_view(), name='profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
