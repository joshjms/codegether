from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Project, UserProfile
from datetime import datetime, date

import re
import markdown

from markdown.extensions.codehilite import CodeHiliteExtension

# Create your views here.

def index(request):
    recent_projects = Project.objects.all().order_by('-id')[:5]
    return render(request, 'codegether/index.html', {
        'recent_projects': recent_projects,
    })

def login_user(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        
        return render(request, 'codegether/login.html', {'form_state': request.POST, 'error': 'Invalid credentials'})

    return render(request, 'codegether/login.html')

def register_user(request):
    if request.method == 'POST':
        email=request.POST['email']

        username=request.POST['username']
        password=request.POST['password']
        confirm_password=request.POST['confirm-password']

        if password != confirm_password:
            return render(request, 'codegether/register.html', {'form_state': request.POST, 'error': 'Your password did not match.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'codegether/register.html', {'form_state': request.POST, 'error': 'Email has been registered. Try logging in instead.'})
        
        if bool(re.findall(r"\s",username)):
            return render(request, 'codegether/register.html', {'form_state': request.POST, 'error': 'Invalid characters for username. Check for whitespaces or illegal characters.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'codegether/register.html', {'form_state': request.POST, 'error': 'Username has been taken. Choose a new username.'})

        newUser = User.objects.create_user(username, email, password)
        newUser.save()

        login(request, newUser)
        
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'codegether/register.html')

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def view_project(request, slug):
    project=get_object_or_404(Project, slug=slug)
    hilite = CodeHiliteExtension(guess_lang=False)
    content=markdown.markdown(project.desc, extensions=['fenced_code', 'md_in_html', hilite])
    skills=project.requirements.split(', ')
    creator=project.creator
    creator_profile=UserProfile.objects.get(user=creator)
    return render(request, 'codegether/view_project.html', {
        'project': project,
        'creator': creator,
        'creator_profile': creator_profile,
        'content': content,
        'skills': skills,
    })

@login_required
def post_project(request):
    if request.method == 'POST':
        form_data=request.POST
        project=Project(name=form_data['title'], desc=form_data['content'], requirements=form_data['skills'], github_url=form_data['github_url'], creator=request.user)
        project.save()
        return HttpResponseRedirect(reverse('list'))
    return render(request, 'codegether/post_project.html')

@login_required
def project_list(request):
    projects=Project.objects.all().order_by('-id')
    user_profile=get_object_or_404(UserProfile,user=request.user)
    page=1
    if request.method=='GET':
        try:
            projects=projects.filter(name__icontains=request.GET['search']) | projects.filter(requirements__icontains=request.GET['search']) | projects.filter(creator__username=request.GET['search'])
        except:
            pass
        try:
            page=request.GET['page']
        except:
            pass
        try:
            if request.GET['sort'] == 'latest':
                projects=projects.order_by('-id')
            if request.GET['sort'] == 'popular':
                projects=projects.annotate(Upvotes=Count('upvotes')).order_by('-Upvotes')
                print(projects.all())
        except:
            pass
    paginator=Paginator(projects,5)
    projects_in_page=paginator.get_page(page)
    return render(request, 'codegether/project_list.html', {
        'projects': projects_in_page,
        'form_state': request.GET,
        'cur_page': page,
    })

@login_required
def upvote(request, pid):
    project=get_object_or_404(Project,id=pid)
    user_profile=get_object_or_404(UserProfile, user=request.user)
    if user_profile not in project.upvotes.all():
        project.upvotes.add(user_profile)
    else:
        project.upvotes.remove(user_profile)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def profile(request, username):
    if User.objects.filter(username=username).exists() == False:
        return HttpResponseRedirect(reverse('index'))
    
    user=get_object_or_404(User,username=username)
    return render(request, 'codegether/user.html', {
        'profile': user,
    })

@login_required
def profile_edit(request, username):
    user=get_object_or_404(User,username=username)

    if request.user.username != username:
        return HttpResponseRedirect(reverse('profile', args=[str(user.username)]))
        

    if request.method == 'POST':
        new_bio = request.POST['bio']

        if 'pfp' in request.FILES:
            new_pfp = request.FILES['pfp']

        user.userprofile.bio = new_bio

        if 'pfp' in request.FILES:
            user.userprofile.pfp = new_pfp

        user.save()
        return HttpResponseRedirect(reverse('profile', args=[str(user.username)]))

    return render(request, 'codegether/edit_user.html', {
        'profile': user,
    })