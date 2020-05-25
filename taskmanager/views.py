from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from .models import Project, CustomUser
from datetime import datetime

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'homepage.html')
    else:
        return HttpResponseRedirect(reverse('taskmanager:home'))

def jobForm(request,user_id):
    return HttpResponse("You're looking at job form.")

def list(request):
    return HttpResponse("You're looking at list.")

def requestForm(request,user_id):
    return HttpResponse("You're looking at request form.")

def signup_user(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        phone_number = request.POST['phno']
        bio = request.POST['bio']
        gender = request.POST['gender']
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email,)
        cuser = CustomUser(user=user, phone_number=phone_number, bio=bio, gender=gender)
        login(request, user)
        user.save()
        cuser.save()
        return HttpResponseRedirect(reverse("taskmanager:home"))
    return render(request, 'signup.html', context)

def login_user(request):
    if request.method == 'POST':
        context = dict()
        username = request.POST['name']
        password = request.POST['passwd']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.COOKIES.get('post_project'):
                return form_state(request, id=2)
            else:
                return HttpResponseRedirect(reverse('taskmanager:home'))
        else:
            if request.COOKIES.get('post_project'):
                context['post_project'] = 'post_project'
            context['error_message'] = 'Username or password is incorrect'
            return render(request, 'login.html', context)
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('taskmanager:index'))

def form_state(request, id=1):
    context = dict()
    if id == 1:
        project_name = request.POST['name']
        description = request.POST['desc']
        deadline = request.POST['deadline']
        context['post_project'] = 'post_project'
        response = render(request, 'login.html', context)
        response.set_cookie('post_project', 'post_project')
        response.set_cookie('name', str(project_name))
        response.set_cookie('desc', str(description))
        response.set_cookie('deadline', str(deadline))
        return response
    else:
        context['name'] = request.COOKIES.get('name')
        context['desc'] = request.COOKIES.get('desc')
        context['deadline'] = request.COOKIES.get('deadline')
        context['post_project'] = 'post_project'
        response = render(request, 'postproject.html', context)
        response.delete_cookie('post_project')
        response.delete_cookie('name')
        response.delete_cookie('desc')
        response.delete_cookie('deadline')
        return response

def post_project(request):
    if request.method == 'POST':
        project_name = request.POST['name']
        description = request.POST['desc']
        deadline = request.POST['deadline']
        if request.user.is_authenticated:
            project = Project()
            project.project_name = project_name
            project.description = description
            project.leader = CustomUser.objects.get(user=request.user.id)
            project.deadline = deadline
            project.postedOn=datetime.now()
            project.save()
            return redirect('taskmanager:project_description',project.id)
        else:
            return form_state(request)
    return render(request, "postproject.html")

def applicable_jobs(cuser):
    if not cuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.exclude(leader=cuser)

    jobs = set()
    if projects:
        for project in projects:
            if not project.isCompleted:
                jobs.add(project)
    if jobs:
        print(jobs)
        sorted(jobs, key=lambda x: x.postedOn, reverse=True)
    return jobs

def browse_jobs(request):
    context = dict()
    cuser = None
    if request.user.is_authenticated:
        cuser = CustomUser.objects.get(user=request.user)
    context['jobs'] = applicable_jobs(cuser)
    return render(request, 'browsejobs.html', context)


def home(request):
    if not request.user.is_superuser and request.user.is_authenticated:
        context = dict()
        cuser = CustomUser.objects.get(user=request.user)
        jobs_recommended = applicable_jobs(cuser)
        posted_projects = Project.objects.filter(
            leader=cuser).order_by('-postedOn')
        if len(posted_projects) == 0:
            context['posted_projects'] = None
        else:
            context['posted_projects'] = posted_projects
        context['jobs_recommended'] = jobs_recommended
        return render(request, 'dashboard.html', context)
    elif request.user.is_superuser:
        return redirect('/admin/')
    else:
        return HttpResponseRedirect(reverse('taskmanager:index'))


def project_description(request, project_id):
    project = Project.objects.get(id=project_id)
    if not project.isCompleted:
        if project.deadline < datetime.now().date():
            project.isCompleted = True
            project.save()
    context = dict()
    context['project'] = project
    context['project_id'] = project_id
    year = project.deadline.strftime("%Y")
    month = project.deadline.strftime("%m")
    date = project.deadline.strftime("%d")
    context['year'] = year
    context['month'] = month
    context['date'] = date
    if request.user.is_authenticated:
        context['is_leader'] = (project.leader.user == request.user)
    return render(request, 'projectdescription.html', context)

def user_profile(request, username):
    
    context = dict()
    user = User.objects.get(username=username)
    cuser = CustomUser.objects.get(user=user)
    context['cuser'] = cuser
    return render(request, 'profile.html', context)

def myprojects(request):
    if request.user.is_authenticated:
        context={}
        cuser=CustomUser.objects.get(user=request.user)
        posted_projects = Project.objects.filter(
            leader=cuser).order_by('-postedOn')
        context['posted_projects'] = posted_projects
        return render(request, 'myprojects.html',context)
    return render(request, 'login.html')
