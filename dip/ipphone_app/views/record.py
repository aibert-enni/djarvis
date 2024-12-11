import copy

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from ipphone_app.models import Record
from ipphone_app.forms import AddRecordForm
from utils import LogManager


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(
            request, "record/record.html", {"customer_record": customer_record}
        )
    else:
        messages.error(
            request, "Вы должны войти в систему, чтобы просмотреть эту страницу."
        )
        return redirect("home")


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Сотрудник успешно добавлен.")
        return redirect("home")
    else:
        messages.error(
            request, "Вы должны войти в систему, чтобы выполнить это действие."
        )
        return redirect("home")


class RecordAddView(LoginRequiredMixin, CreateView):
    model = Record
    form_class = AddRecordForm
    template_name = "record/add_record.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        record = form.save()
        LogManager.make_log(
            request=self.request,
            slug="create",
            by_user_id=self.request.user.id,
            next_values=record,
            model="Record",
        )
        messages.success(self.request, "Сотрудник успешно добавлен.")
        return redirect("home")


class RecordUpdateView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        current_record = Record.objects.get(id=kwargs.get("pk"))
        form = AddRecordForm(
            request.POST or None, request.FILES or None, instance=current_record
        )
        prev_record = copy.deepcopy(current_record)
        if form.is_valid():
            record = form.save()
            LogManager.make_log(
                request=self.request,
                slug="update",
                by_user_id=self.request.user.id,
                prev_values=prev_record,
                next_values=record,
                model="Record",
            )
            messages.success(request, "Сотрудник успешно обновлен!")
            return JsonResponse({"success": True})
        return JsonResponse(
            {
                "form_html": render_to_string(
                    "record/edit_record_form.html",
                    {"form": form, "current_record": current_record},
                    request=request,
                )
            }
        )


class RecordDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        record = get_object_or_404(Record, id=pk)
        record.delete()
        LogManager.make_log(
            request=self.request,
            slug="delete",
            by_user_id=self.request.user.id,
            next_values=record,
            model="Record",
        )
        messages.success(request, "Сотрудник успешно удален.")
        return JsonResponse({"success": True})


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(
            request.POST or None, request.FILES or None, instance=current_record
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Сотрудник успешно обновлен!")
            return JsonResponse({"success": True})
        return JsonResponse(
            {
                "form_html": render_to_string(
                    "record/edit_record_form.html",
                    {"form": form, "current_record": current_record},
                    request=request,
                )
            }
        )
    else:
        messages.success(request, "Вы должны войти в систему.")
        return redirect("home")

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


# def add_record(request):
#     form = AddRecordForm(request.POST or None, request.FILES or None)
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             if form.is_valid():
#                 add_record = form.save()
#                 messages.success(request, "Сотрудник успешно добавлен.")
#                 return redirect('home')
#         return render(request, 'add_record.html', {'form': form})
#     else:
#         messages.error(request, "Вы должны войти в систему.")
#         return redirect('home')

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
