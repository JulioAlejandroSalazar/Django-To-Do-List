from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *



@login_required
def home(request):
    user = request.user
    tasks = Task.objects.filter(user=user).order_by('-created').order_by('is_completed')
    context = {
        'user' : user,
        'tasks' : tasks,
    }
    return render(request, 'list/home.html', context)



@login_required
def create(request):
    if request.method == 'POST':
        user = request.user
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            messages.success(request, 'Task created successfully')
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong')
            return redirect('create')

    else:
        context = {
            'form' : TaskForm()
        }
        return render(request, 'list/create.html', context)



@login_required
def view(request, id):
    task = Task.objects.get(id=id)
    context = {
        'task' : task
    }
    return render(request, 'list/view.html', context)



@login_required
def search(request):
    user = request.user
    if request.method == 'GET':
        search_item = request.GET.get('search-area') or ''
        tasks = Task.objects.filter(title__icontains=search_item).filter(user=user)
        context = {
            'user' : user,
            'tasks' : tasks,
            'search_input' : search_item,
        }
        return render(request, 'list/home.html', context)
    else:
        messages.error(request, 'Something went wrong')
        return redirect('home')



@login_required
def complete(request, id):
    task = Task.objects.get(id=id)
    if task.is_completed == False:
        task.is_completed = True
        task.save()
        return redirect('home')
    else:
        task.is_completed = False
        task.save()
        return redirect('home')



@login_required
def edit(request, id):
    user = request.user
    task = Task.objects.get(id=id)
    if request.method == 'POST':
        new_task = TaskForm(request.POST, instance=task)
        if new_task.is_valid():
            instance = new_task.save(commit=False)
            instance.user = user
            instance.save()
            messages.success(request, 'Task edited successfully')
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong')
            return redirect('edit')

    else:
        context = {
            'form' : TaskForm(instance=task),
            'task' : task,
        }
        return render(request, 'list/edit.html', context)



@login_required
def delete(request, id):
    task = Task.objects.get(id=id)
    if request.method == 'POST':        
        task.delete()
        messages.success(request, 'Task deleted successfully')
        return redirect('home')

    else:
        context = {
            'task' : task
        }
        return render(request, 'list/delete.html', context)