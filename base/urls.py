from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import TaskList, CustomLoginView, TaskCreate, TaskDelete, TaskUpdate, registerView


urlpatterns = [
    path('', TaskList.as_view(), name="tasks"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name="logout"),

    path('create/', TaskCreate.as_view(), name="create"),
    path('delete/<int:pk>', TaskDelete.as_view(), name='delete'),
    path('edit/<int:pk>', TaskUpdate.as_view(), name="edit"),
    path('register/', registerView, name="register"),
]
