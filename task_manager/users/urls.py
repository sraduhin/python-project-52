from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.UsersListView.as_view(), name='users_index'),
    path('create/', views.UsersSignUpView.as_view(), name='users_create'),
    path('<int:pk>/update/', views.UsersUpdateView.as_view(),
         name='users_update'),
    path('<int:pk>/delete/', views.UsersDeleteView.as_view(),
         name='users_delete'),
]
