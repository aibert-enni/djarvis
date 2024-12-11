from django.urls import path
from ipphone_app import views
from django.contrib import admin
from ipphone_app.views import DepartmentUpdateView, HomeView, DepartmentDeleteView, RecordDeleteView, RecordAddView, \
    SendRecordsFormsView, RecordUpdateFormView, RecordUpdateView, AddDepartmentView, LogListView, LogDetailView, \
    RecordFormConfigurationView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # auth
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # record
    path('record/<int:pk>', views.customer_record, name='record'),
    # path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('delete-record/<int:pk>/', RecordDeleteView.as_view(), name='delete_record'),
    path('add_record/', RecordAddView.as_view(), name='add_record'),
    # path('edit-record/<int:pk>/', RecordUpdateView.as_view(), name='edit_record'),
    # path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('edit-record/<int:pk>/', RecordUpdateView.as_view(), name='edit_record'),
    # path('edit-record/<int:pk>/', views.update_record, name='edit_record'),

    # department
    path('add_department/', AddDepartmentView.as_view(), name='add_department'),
    path('edit-department/<int:pk>/', DepartmentUpdateView.as_view(), name='edit_department'),
    path('delete-department/<int:pk>/', DepartmentDeleteView.as_view(), name='delete_department'),

    # record forms
    path('record_update_form/<str:token>/', RecordUpdateFormView.as_view(), name='record_update_form'),
    path('send_forms/', SendRecordsFormsView.as_view(), name='send_forms'),
    path('record_form_configuration/<int:pk>', RecordFormConfigurationView.as_view(), name='record_form_configuration'),

    # logs
    path('logs/', LogListView.as_view(), name='logs'),
    path('log/<int:pk>/', LogDetailView.as_view(), name='log'),

    # кастомные доп ссылки
    path('admin/', views.login_user, name='login'),
    path('dj-admin/', admin.site.urls),
    
]
