from django.shortcuts import render,redirect,get_object_or_404
from .models import ToDO
# Create your views here.

def todo_list(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            ToDO.objects.create(
                title=title,
                description=description,
            )
        return redirect('todo_list')

    status = request.GET.get('status','all')
    todos = ToDO.objects.all()

    if status == 'pending':
        todos = todos.filter(completed=False)
    elif status == 'completed':
        todos = todos.filter(completed=True)

    return render(request,'todos/todo_list.html',{'todos':todos,'status':status})



def delete_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(ToDO, pk=pk)
        todo.delete()
    return redirect('todo_list')


def toggle_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(ToDO, pk=pk)
        todo.completed = not todo.completed
        todo.save(update_fields=['completed'])

    return redirect('todo_list')
    


