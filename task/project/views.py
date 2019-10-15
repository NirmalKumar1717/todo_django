from django.shortcuts import render, redirect
from django.contrib.auth.models import  auth ,User
from django.contrib import messages
from .models import Login, Todo
from .forms import TodoForm
from django.views.decorators.http import require_POST
from rest_framework import generics
from rest_framework import mixins
from . serializers import UserSerializer     #API
from django.shortcuts import get_object_or_404 #API
from rest_framework.views import APIView       #API
from rest_framework.response import Response   #API
from rest_framework import status              #API

# Create your views here.
def home(request):
    return render(request, 'page.html')


def register(request):
    if request.method == 'POST':
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      username = request.POST['username']
      password1 = request.POST['password1']
      password2 = request.POST['password2']
      email = request.POST['email']
      
      
      
      if password1 == password2: 
         if User.objects.filter(username=username).exists():
             messages.info(request, 'username  taken')
             return redirect('register')
         
         elif User.objects.filter(email=email).exists():
             messages.info(request, 'email  taken')

             return redirect('register')  
         else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password1, email=email)
            user.save();
            print('user created')
            return redirect('login')
      else:
        messages.info(request, 'password not match')
        return redirect('register')    
      
     

    else:
     return render(request, 'register.html')
     
     
def login(request):
   if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
           
      user = auth.authenticate(username=username,password=password)
           
      if user is not None:
          auth.login(request, user)
          return redirect('index')
      else:
          messages.info(request, 'Invalid username or password')
          return redirect('login')
         
           
   else:
      return render(request, 'login.html')
 

def logout(request):
    auth.logout(request)
    return redirect('/')



## Todo Coding.....

def index(request):
    task = Todo.objects.order_by('id') #Todo is the model Name.
    ''' we create some objects in django admin,we have 
    taken the all of the object in order by id and store it in one variable '''

    form = TodoForm() #TodoForm is the form name

    context = {'task': task, 'form': form} #djinja format.

    return render(request, 'index.html', context)
@require_POST
def addTodo(request):
    form = TodoForm(request.POST)

    if form.is_valid():
        new = Todo(text=request.POST['text'])
        new.save()
    return redirect ('index')

def completeTodo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    if todo.complete == True:
        todo.complete = False
        todo.save()
        return redirect('index')
    elif todo.complete == False:
        todo.complete = True
        todo.save()
        return redirect('index')
    else:
        return redirect('index')



def showComplete(request):
    task = Todo.objects.filter(complete__exact=True)
    form = TodoForm() #TodoForm is the form name

    context = {'task': task, 'form': form} #djinja format.

    return render(request, 'index.html', context)

def showActive(request):
    task = Todo.objects.filter(complete__exact=False)
    form = TodoForm() #TodoForm is the form name

    context = {'task': task, 'form': form} #djinja format.

    return render(request, 'index.html', context)


def clearAll(request):
    Todo.objects.all().delete()

    return redirect('index')

def showAll(request):
     Todo.objects.all()

     return redirect('index')


def deleteTag(request, todo_id):
    a = Todo.objects.get(pk=todo_id)
    a.delete()
    return redirect('index')



#Generic API Coding.....

class UserList(generics.GenericAPIView,
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self,request):
        return self.create(request)
    
    '''def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)'''

    def put(self,request, id=None):
        return self.update(request, id)
        
    '''def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)'''

    def delete(self,request, id=None):
        return self.destroy(request, id)


