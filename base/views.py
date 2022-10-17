from dataclasses import fields
from typing import Optional
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from django.contrib import messages

# Create your views here.


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/tasks.html'
    context_object_name = 'tasks'
    fields = "__all__"
    ordering = ['completed']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user)
        context['tasks'] = context['tasks'].filter(
            user=self.request.user)

        search_input = self.request.GET.get('search') or ''

        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input
        return context


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class TaskCreate(CreateView):
    model = Task
    fields = ["title", "completed"]
    template_name: str = "base/create.html"
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name: str = 'task'
    success_url: Optional[str] = reverse_lazy('tasks')
    template_name: str = 'base/delete.html'

    # def get_queryset(self):
    #     user = self.request.user
    #     return self.model.objects.filter(user=user)


class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'completed']
    template_name: str = 'base/edit.html'
    success_url = reverse_lazy('tasks')


def registerView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect('tasks')
        else:
            messages.info(request, 'invalid registration details')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'base/register.html', context)
