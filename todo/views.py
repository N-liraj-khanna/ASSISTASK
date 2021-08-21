from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, FormView
from django.views.generic.edit import DeleteView, UpdateView
from .models import ToDo
from .forms import CreateForm


class Index(ListView, FormView):
  model = ToDo
  template_name = 'todo/index.html'
  context_object_name="tasks"
  fields = ['task', 'completed',]
  form_class = CreateForm
  success_url = '/'

  def get_queryset(self):
    # return super().get_queryset()
    return super().get_queryset().filter(user=self.request.user)
  
  def post(self, request):
    form = CreateForm(request.POST)
    if form.is_valid():
      event=form.save(commit=False)
      event.user=request.user
      event.save()
      return redirect('index')
    
    return render(request, 'todo/index.html', context={"error": True, "tasks": ToDo.objects.all(), "form": self.form_class})
  
class Delete(DeleteView):
  template_name='todo/delete.html'
  model=ToDo

  def get_success_url(self):
      return reverse("index")
    
    
class Update(UpdateView):
  template_name='todo/update.html'
  fields = ['task', 'completed',]
  model=ToDo

  def get_success_url(self):
      return reverse("index")

def complete(request, pk):
  obj=ToDo.objects.get(id=pk)
  obj.completed=not obj.completed
  obj.save()
  return redirect('index')