from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import ToDO


@login_required
def todo_list(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            ToDO.objects.create(
                user=request.user,
                title=title,
                description=description,
            )

        return redirect('todo_list')

    status = request.GET.get('status', 'all')

    # Users can see only their own tasks.
    todos = ToDO.objects.filter(user=request.user)

    if status == 'pending':
        todos = todos.filter(completed=False)
    elif status == 'completed':
        todos = todos.filter(completed=True)

    return render(
        request,
        'todos/todo_list.html',
        {'todos': todos, 'status': status},
    )


@login_required
def toggle_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(
            ToDO, pk=pk, user=request.user
        )
        todo.completed = not todo.completed
        todo.save(update_fields=['completed'])

    return redirect('todo_list')


@login_required
def delete_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(
            ToDO, pk=pk, user=request.user
        )
        todo.delete()

    return redirect('todo_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo_list')
    else:
        form = UserCreationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form},
    )