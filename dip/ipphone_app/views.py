from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record, Department
from .forms import AddRecordForm, AddDepartmentForm 
from django.views.generic import ListView
import json
from django.views.generic.edit import UpdateView
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

def home(request):
    departments = Department.objects.all().order_by('position')
    records = Record.objects.all().order_by('department__position', 'position_id')
    department_records = {}
    for department in departments:
        department_records[department.id] = records.filter(department=department, is_active=True)
    records_json = json.dumps(
        list(
            records.values(
                'id', 
                'is_active',
                'phone', 
                'full_name', 
                'department__name', 
                'department__position',
                'position', 
                'position_id',
                'room', 
                'email'
            )
        )
    )
    departments_json = json.dumps(list(departments.values('id', 'name', 'position')))

    return render(request, 'home.html', {'departments': departments, 'records': records, 'all_employers_json': records_json, 'departments_json': departments_json, 'department_records': department_records})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему!")
            return redirect('home')
        else:
            messages.error(request, "Ошибка входа. Попробуйте еще раз.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('home')

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "Вы должны войти в систему, чтобы просмотреть эту страницу.")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Сотрудник успешно добавлен.")
        return redirect('home')
    else:
        messages.error(request, "Вы должны войти в систему, чтобы выполнить это действие.")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Сотрудник успешно удален.")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "Вы должны войти в систему.")
        return redirect('home')

def add_department(request):
    form = AddDepartmentForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_department = form.save()
                messages.success(request, "Департамент успешно добавлен.")
                return redirect('home')
        return render(request, 'add_department.html', {'form': form})
    else:
        messages.error(request, "Вы должны войти в систему.")
        return redirect('home')

# def update_record(request, pk):
#     if request.user.is_authenticated:
#         current_record = Record.objects.get(id=pk)
#         form = AddRecordForm(request.POST or None, instance=current_record)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Record Has Been Updated!")
#             return redirect('home')
#         return render(request, 'update_record.html', {'form':form})
#     else:
#         messages.success(request, "You Must Be Logged In...")
#         return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            messages.success(request, "Сотрудник успешно обновлен!")
            return JsonResponse({'success': True})
        return JsonResponse({'form_html': render_to_string('edit_record_form.html', {'form': form, 'current_record': current_record}, request=request)})
    else:
        messages.success(request, "Вы должны войти в систему.")
        return redirect('home')

    # try:
    #     current_record = Record.objects.get(id=pk)

    #     if request.method == 'POST':  # Сначала проверяем, является ли запрос POST
    #         form = AddRecordForm(request.POST or None, instance=current_record)
    #         if form.is_valid():
    #             form.save()
    #             messages.success(request, "Record Has Been Updated!")
    #             return JsonResponse({'success': True})
    #         else:
    #             return JsonResponse({'success': False, 'form_html': render_to_string('edit_record_form.html', {'form': form}, request=request)})
        
    #     # GET-запрос: отображаем форму
    #     else:
    #         form = AddRecordForm(instance=current_record)
    #         return JsonResponse({'form_html': render_to_string('edit_record_form.html', {'form': form}, request=request)})

    # except Exception as e:
    #     print(f"Ошибка: {e}")  # Выводим ошибку в консоль
    #     return JsonResponse({'success': False, 'error': str(e)})

class DepartmentUpdateView(UpdateView):
    model = Department
    fields = ['name', 'position']

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Департамент успешно обновлен.")
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при обновлении департамента.")
        return JsonResponse({'success': False})

class DepartmentDeleteView(View):
    def post(self, request, pk):
        department = get_object_or_404(Department, id=pk)
        department.delete()
        messages.success(request, "Департамент успешно удален.")
        return JsonResponse({'success': True})

class RecordUpdateView(UpdateView):
    model = Record
    fields = ['is_active', 'full_name', 'position', 'position_id', 'phone', 'email', 'room']

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Сотрудник успешно обновлен.")
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при обновлении сотрудника.")
        return JsonResponse({'success': False})

class RecordDeleteView(View):
    def post(self, request, pk):
        record = get_object_or_404(Record, id=pk)
        record.delete()
        messages.success(request, "Сотрудник успешно удален.")
        return JsonResponse({'success': True})
