from django import forms
from .models import Record, Department

class AddRecordForm(forms.ModelForm):
    is_active = forms.BooleanField(
        required=False,  # Булевые поля обычно необязательные
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),  # Виджет для чекбокса
        label="Активен"
    )
    phone = forms.CharField(
        required=False,  # Сделаем поле необязательным, как указано в модели
        widget=forms.TextInput(attrs={"placeholder": "Внутренний номер", "class": "form-control"}),
        label=""
    )
    full_name = forms.CharField(
        required=True,  # Это поле обязательно
        widget=forms.TextInput(attrs={"placeholder": "Ф.И.О. сотрудника", "class": "form-control"}),
        label=""
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,  # В модели установлено null=True и blank=True
        widget=forms.Select(attrs={"class": "form-control"}),
        label=""
    )
    position = forms.CharField(
        required=False,  # Сделаем необязательным, как в модели
        widget=forms.TextInput(attrs={"placeholder": "Должность", "class": "form-control"}),
        label=""
    )
    position_id = forms.IntegerField(
        required=False,  # Поле необязательно по модели
        widget=forms.NumberInput(attrs={"placeholder": "Позиция", "class": "form-control"})
    )
    room = forms.CharField(
        required=False,  # Сделаем необязательным, как указано в модели
        widget=forms.TextInput(attrs={"placeholder": "Кабинет", "class": "form-control"}),
        label=""
    )
    email = forms.CharField(
        required=False,  # Сделаем необязательным, как указано в модели
        widget=forms.TextInput(attrs={"placeholder": "Почта", "class": "form-control"}),
        label=""
    )

    class Meta:
        model = Record
        exclude = ("created_at",)  # Исключим автоматические и технические поля

class AddDepartmentForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Название департамента", "class": "form-control"}),
        label=""
    )
    position = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "Позиция", "class": "form-control"}),
        label=""
    )

    class Meta:
        model = Department
        fields = ['name', 'position']  # Определим только нужные поля