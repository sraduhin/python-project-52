from django.urls import path
from task_manager.labels import views

urlpatterns = [
    path('', views.LabelsListView.as_view(), name='labels_index'),
    path('create/', views.LabelsCreateView.as_view(), name='labels_create'),
    path('<int:pk>/update/', views.LabelsUpdateView.as_view(), name='labels_update'),
    path('<int:pk>/delete/', views.LabelsDeleteView.as_view(), name='labels_delete'),
]
