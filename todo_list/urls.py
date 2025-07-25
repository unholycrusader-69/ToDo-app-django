
from django.urls import path, include
from . import views

urlpatterns = [
  path("", views.nav, name = 'nav'),
  path('', views.todo_list_view, name='todo_list'),
  path('todo_list/', views.todo_list_view, name='todo_list'),
  path('toggle/<int:pk>/', views.toggle_finished, name='toggle_finished'),
  path('delete/<int:pk>/', views.delete_task, name = 'delete_task'),
  path('signup/', views.signup_view, name = 'signup'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('edit/<int:pk>/', views.edit_task, name='edit_task'),
  path('calendar/', views.weekly_calendar, name='calendar_view'),
  path('review/', views.review_page, name='review_page'),
  path('admin-review/', views.review_dashboard, name='review_dashboard'),
  
]