from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns=[
  path('', login_required(views.Index.as_view()), name="index"),
  path('delete/<int:pk>/', login_required(views.Delete.as_view()), name="delete"),
  path('update/<int:pk>/', login_required(views.Update.as_view()), name="update"),
  path('complete/<int:pk>/', login_required(views.complete), name="complete"),
]