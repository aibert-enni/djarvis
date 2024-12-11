from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from ipphone_app.models import Department
from ipphone_app.forms import AddDepartmentForm
from utils import LogManager


class AddDepartmentView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = AddDepartmentForm
    template_name = "department/add_department.html"

    def form_valid(self, form):
        department = form.save()
        LogManager.make_log(
            request=self.request,
            slug="create",
            by_user_id=self.request.user.id,
            next_values=department,
            model="Department",
        )
        messages.success(self.request, "Департамент успешно добавлен.")
        return redirect("home")


# def add_department(request):
#     form = AddDepartmentForm(request.POST or None)
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Департамент успешно добавлен.")
#                 return redirect('home')
#         return render(request, 'add_department.html', {'form': form})
#     else:
#         messages.error(request, "Вы должны войти в систему.")
#         return redirect('home')


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    fields = ["name", "position"]

    def form_valid(self, form):
        prev_department = self.get_object()
        department = form.save()
        LogManager.make_log(
            request=self.request,
            slug="update",
            by_user_id=self.request.user.id,
            prev_values=prev_department,
            next_values=department,
            model="Department",
        )
        messages.success(self.request, "Департамент успешно обновлен.")
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при обновлении департамента.")
        return JsonResponse({"success": False})


class DepartmentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        department = get_object_or_404(Department, id=pk)
        department.delete()
        LogManager.make_log(
            request=self.request,
            slug="delete",
            by_user_id=self.request.user.id,
            next_values=department,
            model="Department",
        )
        messages.success(request, "Департамент успешно удален.")
        return JsonResponse({"success": True})
