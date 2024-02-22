from django.contrib.auth.decorators import login_required  # cand stergi contu tre sa fi logat in a tau
from django.contrib.auth.views import PasswordResetView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages  # pt mesajul de deleted successfully
from .forms import RegisterForm, AddTaskForm, CustomPasswordResetForm
from .forms import LoginForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout  # pt delogare user
from .models import TodoItem


def HomePage_view(request):
    return render(request, 'HomePage.html')


def register_view(request):
    if request.method == "GET":  # pt ca e get tre sa il importam din hr.forms
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect(reverse("home"))

    return render(request, "register.html", {
        'form': form  # trimiti formu form
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("tasks"))  # Redirect to your home page for now
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def tasks_view(request):
    if request.user.is_authenticated:
        tasks = TodoItem.objects.filter(user=request.user)  # Fetch tasks for the logged-in user
        context = {
            'tasks': tasks
        }
        return render(request, 'tasks.html', context)
    else:
        # Redirect to the login page or handle the case where the user is not logged in
        pass


from django.http import JsonResponse


def add_task_view(request):
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the logged-in user to the task
            # Set due date and priority from the form
            task.due_date = form.cleaned_data['due_date']
            task.priority = form.cleaned_data['priority']
            task.save()

            # Construct the task data to be sent back in the JSON response
            task_data = {
                'id': task.id,
                'task': task.task,
                'description': task.description,
                'status': task.status,
                'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format the datetime if needed
                'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,  # Format due date if set
                'priority': task.priority,
            }

            return JsonResponse({'success': True, 'task': task_data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = AddTaskForm()

    return render(request, 'add_task.html', {'form': form})


@csrf_exempt  # Use this decorator for the process of ticking the box when the task is done
def update_task_status(request, task_id):
    if request.method == 'POST':
        try:
            task = TodoItem.objects.get(pk=task_id)
            is_checked = request.POST.get('is_checked') == 'true'
            task.status = is_checked
            task.save()
            return JsonResponse({'success': True})
        except TodoItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task does not exist'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def delete_task_view(request, task_id):
    try:
        task = TodoItem.objects.get(pk=task_id)
        task.delete()
        return JsonResponse({'success': True})
    except TodoItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task does not exist'})


def logout_view(request):
    logout(request)
    return redirect(reverse("home"))


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')  # Redirect to home after account deletion
    else:
        return redirect('home')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = '/password_reset/done/'


# incercare
