from accounts.decorators import admin_only, allowed_user, unauthenticated_user
from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse
from django.contrib.auth.models import User, Group

from .form import *
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
# @allowed_user(allowed_roles=['admin'])
@admin_only
def home(request):
    return render(request,'home.html')


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='user')
            user.groups.add(group)
            return redirect('login')
    context ={'form':form}
    return render(request, 'register.html',context)

@unauthenticated_user
def loginPage(request):   

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    context ={}
    return render(request,'login.html')


def teacher(request):
    data = User.objects.get(id=request.user.id)
    context={'data':data}
    return render(request, 'teacher.html',context) 

def student(request):
    return render(request,'student.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')