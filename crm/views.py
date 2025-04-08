from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm, CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


def homepage(request):

    context = {'first_name': 'John Doe'}

    return render(request, 'crm/index.html', context)


def create_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view-tasks')
    
    context = {'TaskForm' : form}
    
    return render(request, 'crm/create-task.html', context)


def tasks(request):
    
    queryDataAll = Task.objects.all()
    context = {'allTasks' : queryDataAll}
    
    return render(request, 'crm/view-task.html', context)
    

def task1(request):
    
    queryDataSingle = Task.objects.get(id=3)
    context = {'singleTask' : queryDataSingle}
    
    return render(request, 'crm/task1.html', context)


def register(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('my-login')
        
    context = {'RegistrationForm': form}
              
    return render(request, 'crm/register.html', context)


def my_login(request):
    
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            
    context = {'LoginForm' : form}
    return render(request, 'crm/my-login.html', context)


@login_required(login_url='my-login')
def dashboard(request):
                
    return render(request, 'crm/dashboard.html')


def update_task(request, pk):
    task = Task.objects.get(id=pk)
    
    form = TaskForm(instance=task)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        
        if form.is_valid():
            form.save()
            return redirect('view-tasks')
    
    context = {'UpdateTask' : form}
    
    return render(request, 'crm/update-task.html', context)


def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    
    form = TaskForm(instance=task)
    
    if request.method == 'POST':
        
        task.delete()
        
        return redirect('view-tasks')
    
    return render(request, 'crm/delete-task.html')

    
def contact(request):

    clientlist = [

        {
            'id': '1',
            'name': 'John Doe',
            'occupation': 'Electrical Engineer'
        },

        {
            'id': '2',
            'name': 'Raj Jayaraj',
            'occupation': 'Aerospae Engineer'
        }
    ]

    context = {'mainclientlist': clientlist}

    return render(request, 'crm/contact.html', context)



def user_logout(request):
    auth.logout(request)
    
    return redirect("")