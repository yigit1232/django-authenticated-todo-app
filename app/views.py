from django.shortcuts import render,redirect
from .forms import TodoForm,RegisterForm,LoginForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from .models import Todo

def index(request):
    form = TodoForm(request.POST or None)
    data = Todo.objects.all().order_by('-created_date')
    q = request.GET.get('q')
    if q:
        data = Todo.objects.filter(todo__icontains=q)
        count = data.count()
        return render(request, 'index.html', {'data': data, 'form': form, 'count': count,'q':q})
    if form.is_valid():
        if not request.user.is_authenticated:
            form = LoginForm()
            error = 'Please log in'
            return render(request,'login.html',{'form':form,'error':error})
        todo = form.cleaned_data.get('todo')
        if todo == '':
            error = 'Please enter a task'
            return render(request,'index.html',{'data':data,'form':form,'error':error})
        todo_obj = Todo(todo=todo)
        todo_obj.author = request.user
        todo_obj.save()
        return redirect('index')
    return render(request, 'index.html',{'form':form,'data':data})

def register_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        repassword = form.cleaned_data.get('repassword')
        if username == '' and password =='':
            error = 'All fields are required'
            return render(request, 'register.html',{'form':form,'error':error})
        if User.objects.filter(username=username).exists():
            error = 'Username already exists'
            return render(request, 'register.html', {'form': form, 'error': error})
        if password != repassword:
            error = 'Password does not match'
            return render(request, 'register.html', {'form': form, 'error': error})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request, 'register.html',{'form':form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = 'Invalid username or password'
            return render(request, 'login.html', {'form': form, 'error': error})
    return render(request, 'login.html',{'form':form})

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        return redirect('index')

def delete_todo(request,id):
    if not request.user.is_authenticated:
        return redirect('index')

    try:
        todo = Todo.objects.get(id=id,author=request.user)
        todo.delete()
        return redirect('index')
    except Todo.DoesNotExist:
        error = 'Todo does not exist'
        return redirect('index')

def update_todo(request,id):
    if not request.user.is_authenticated:
        return redirect('index')
    try:
        data = Todo.objects.get(id=id,author=request.user)
    except Todo.DoesNotExist:
        return redirect('index')
    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo =  form.cleaned_data.get('todo')
        if todo == '':
            error = 'Please enter a task'
            return render(request,'update.html',{'data':data,'form':form,'error':error})
        data.todo = todo
        data.save()
        return redirect('index')
    return render(request,'update.html',{'data':data,'form':form})

def my_todos(request):
    if not request.user.is_authenticated:
        return redirect('index')
    data = Todo.objects.filter(author=request.user).order_by('-created_date')
    return render(request,'my_todos.html',{'data':data})