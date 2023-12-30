from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
#from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy # when form submitted successfuly it redirect to another page
from .models import Task

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin # any view will inherit that will work only when user authuntcated 
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth import login  # after register redierct to login page




class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields= '__all__'   # it takes a fields like create and update views
    redirect_authenticated_user = True #if user is authentcated he shouldn't use this page until he loged out
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    # now I should redirect user after registeration to his Lists view and login automaticly

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user) # if user is register successfuly login him automaticly
        return super(RegisterPage,self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')   # if user is login restrict him from go to login page (or its url) and redirect him to lists view
        return super(RegisterPage,self).get( *args, **kwargs)


# Create your views here.   # class based view --> list,detail,update,destroy
class TaskList(LoginRequiredMixin,ListView):  #in settings.py I will add login section to redirect user to login page if he not authentcated   #camel case # view all tasks
    model = Task
    #template_name = 'custom_task_list.html'  # You can specify a custom template name
    context_object_name = 'tasks' # customize the name of objects from object_list to tasks which used to loop in template
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: # it's a defined function return only the data wich is for specific user
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user) # to return only tasks of logeed user in the list
        context['count'] = context['tasks'].filter(complete = False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:    # search-area is the name of the input in html file
            context['tasks'] = context['tasks'].filter(
                title__icontains = search_input
                # title__icontains  serach for all chars, startwith seach for first chars
            )
        context['search_input'] = search_input  # to do not remove searched text after press search
        
        return context
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task    
    context_object_name = 'task'
    template_name = 'base/task.html' #write --> appname/filename.html
    # temp name by default should be modelname_anyname.html
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task  
    fields = ['title','description','complete'] #'__all__' fields in the model #this for modelform wich is part of createview   
    success_url = reverse_lazy('tasks') #tasks is the name of url of home page it in urls.py
    
    def form_valid(self, form):    # defined function to add added tasks to loggedin user only automaticly
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
    
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
    

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')