#project app url
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('register',views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('index', views.index, name="index"),
    path('add', views.addTodo, name='add'),
    path('complete/<todo_id>', views.completeTodo, name='complete'),
    path('showComplete', views.showComplete, name='showComplete'),
    path('clearAll', views.clearAll, name='clearAll'),
    path('showActive', views.showActive, name='showActive'),
    path('showAll', views.showAll, name='showAll'),
    path('deleteTag/<todo_id>', views.deleteTag, name='deleteTag'),
    path('generic/pools/',views.UserList.as_view()),
    path('generic/pools/<int:id>',views.UserList.as_view())


]
