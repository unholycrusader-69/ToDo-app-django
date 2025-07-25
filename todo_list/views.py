from django.shortcuts import render,redirect , get_object_or_404
from .models import ToDo,Review,UserNote
from .forms import ToDoForm,CustomLoginForm,CustomSignupForm,ReviewForm,UserNoteForm
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from datetime import time,date,datetime,timedelta
from django.utils import timezone
import random

@login_required
def nav(request):
    today = date.today()
    week_dates = [today + timedelta(days=i) for i in range(7)]
    todos = ToDo.objects.filter(deadline__in=week_dates).order_by('deadline')

    calendar_data = {}
    for day in week_dates:
        calendar_data[day] = todos.filter(deadline=day)

    
    note, _ = UserNote.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('nav') 
    else:
        form = UserNoteForm(instance=note)

    return render(request, 'registration/navbar.html', {
        'calendar_data': calendar_data,
        'week_dates': week_dates,
        'form': form,
    })

@login_required
def todo_list_view(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)

            hour = int(request.POST.get('deadline_hour'))
            minute = int(request.POST.get('deadline_minute'))
            ampm = request.POST.get('deadline_ampm')

            if ampm == 'PM' and hour != 12:
                hour += 12
            elif ampm == 'AM' and hour == 12:
                hour = 0

            todo.deadline_time = time(hour, minute)

            todo.save()
            return redirect('todo_list')
    else:
        form = ToDoForm()

    todos = ToDo.objects.all()
    return render(request, 'registration/todo_list.html', {'form': form,'todos': todos})

@require_POST
def toggle_finished(request, pk):
    todo = get_object_or_404(ToDo , pk = pk)
    print("Before:", todo.finished)
    todo.finished = not todo.finished
    todo.save()
    print("After:", todo.finished)
    return redirect('todo_list')


def delete_task(request,pk):
    todo = get_object_or_404(ToDo, pk = pk)
    todo.delete()
    return redirect('todo_list')

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please log in.")
            return redirect('login')
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('nav')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_task(request,pk):
    todo = get_object_or_404(ToDo, pk=pk)

    if request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)

        if form.is_valid():
           
            updated_todo = form.save(commit=False)

           
            hour = request.POST.get('deadline_hour')
            minute = request.POST.get('deadline_minute')
            ampm = request.POST.get('deadline_ampm')

            if hour and minute and ampm:
                hour = int(hour)
                minute = int(minute)

                if ampm == 'PM' and hour != 12:
                    hour += 12
                elif ampm == 'AM' and hour == 12:
                    hour = 0

                updated_todo.deadline_time = time(hour, minute)

            updated_todo.save()
            return redirect('todo_list')
    else:
       
        initial = {
            'deadline_hour': todo.deadline_time.strftime('%I') if todo.deadline_time else '',
            'deadline_minute': todo.deadline_time.strftime('%M') if todo.deadline_time else '',
            'deadline_ampm': todo.deadline_time.strftime('%p') if todo.deadline_time else '',
        }
        form = ToDoForm(instance=todo, initial=initial)

    return render(request, 'edit_task.html', {'form': form, 'todo': todo})

def weekly_calendar(request):
    today = date.today()
    week = [today + timedelta(days=i) for i in range(7)]

    todos_by_day = {}
    for day in week:
        todos_by_day[day] = ToDo.objects.filter(deadline=day, user=request.user)

    return render(request, 'calendar_view.html', {
        'week': week,
        'todos_by_day': todos_by_day
    })

@login_required
def review_page(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            print("FORM IS VALID — saving review...")  # Debug line
            Review.objects.create(
                user=request.user,
                message=form.cleaned_data['message']
            )
            return redirect('nav')
        else:
            print("FORM IS INVALID:", form.errors)
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'form': form})

def is_superuser(user):
    return user.is_superuser  

@user_passes_test(is_superuser)
def review_dashboard(request):
    reviews = Review.objects.order_by('-submitted_at')
    return render(request, 'review_dashboard.html', {'reviews': reviews})