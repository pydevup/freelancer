from django.urls import path
from . import views

app_name = 'taskmanager'

urlpatterns = [
    #path('homepage/', views.HomepageView.as_view(), name='homepage'),
    path('', views.index, name='index'),
    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.home, name='home'),
    path('profile/<username>', views.user_profile, name='profile'),
    path('post_project/', views.post_project, name='post_project'),
    path('myprojects/', views.myprojects, name='myprojects'),
	path('project_description/<int:project_id>/', views.project_description, name='project_description'),
    path('browse_jobs/', views.browse_jobs, name='browse_jobs'),
    path('<int:user_id>/jobForm/', views.jobForm, name='jobForm'),
    path('list/', views.list, name='list'),
    path('<int:user_id>/requestForm/', views.requestForm, name='requestForm'),
]
