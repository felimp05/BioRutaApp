from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

@login_required
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form': UserCreationForm
        })
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                print(".")
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html',{
                'form': UserCreationForm,
                'error': "usuaio ya existe"
                })             
        return render(request, 'signup.html',{
                'form': UserCreationForm,
                'error': "contraseña no coincide"
                })
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=True)

    return render(request, 'tasks.html',{
        'tasks': tasks
    })

@login_required
def tasks_complete(request):
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')

    return render(request, 'tasks.html',{
        'tasks': tasks
    })

@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
        'form': TaskForm
        })
    else:
        
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': "Por favor validar los datos"
            })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
            task = get_object_or_404(Task,id=task_id, user=request.user)
            form = TaskForm(instance=task)
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form
            })
    else:
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            form=TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error': "Por favor validar los datos"
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.dateCompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('home')

def iniSesion(request):
        if request.method == 'GET':
            return render(request, 'iniSesion.html',{
            'form': AuthenticationForm
            })
        else:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

            if user is None:
                return render(request, 'iniSesion.html',{
            'form': AuthenticationForm,
            'error': "El usuario no se encontro"
            })
            else:
                login(request,user)
                if user.username == "VIVIANA":
                    return redirect('home')
                else:
                    return redirect('tasks')