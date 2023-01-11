from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path('', views.TasksListView.as_view(), name='tasks_index'),
    path('create/', views.TasksCreateView.as_view(), name='tasks_create'),
    path('<int:pk>', views.TasksDetailView.as_view(), name='tasks_show'),
    path('<int:pk>/update/', views.TasksUpdateView.as_view(), name='tasks_update'),
    path('<int:pk>/delete/', views.TasksDeleteView.as_view(), name='tasks_delete'),
]
