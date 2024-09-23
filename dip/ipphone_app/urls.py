from django.urls import path
from . import views
from django.contrib import admin
from .views import DepartmentUpdateView, RecordUpdateView, DepartmentDeleteView, RecordDeleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('add_department/', views.add_department, name='add_department'),
    # path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('edit-department/<int:pk>/', DepartmentUpdateView.as_view(), name='edit_department'),
    # path('edit-record/<int:pk>/', RecordUpdateView.as_view(), name='edit_record'),
    path('edit-record/<int:pk>/', views.update_record, name='edit_record'),
    path('delete-department/<int:pk>/', DepartmentDeleteView.as_view(), name='delete_department'),
    path('delete-record/<int:pk>/', RecordDeleteView.as_view(), name='delete_record'),

    # кастомные доп ссылки
    path('admin/', views.login_user, name='login'),
    path('dj-admin/', admin.site.urls),
    
]
