from django import forms
from ipphone_app.models import Department, Record

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
        widget=forms.NumberInput(attrs={"placeholder": "Позиция", "class": "form-control"}),
        label="Позиция сотрудника в департаменте (Для сортировки)"
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
    image = forms.ImageField(
        required=False, # Сделаем необязательным, как указано в модели
        widget=forms.ClearableFileInput(attrs={"placeholder": "Фото","class": "form-control"}),
        label="Фото"
    )

    class Meta:
        model = Record
        exclude = ("created_at",)  # Исключим автоматические и технические поля

class UpdateRecordForm(forms.ModelForm):
    phone = forms.CharField(
        required=False,  # Сделаем поле необязательным, как указано в модели
        widget=forms.TextInput(attrs={"placeholder": "Внутренний номер", "class": "form-control"}),
        label="Внутренний номер"
    )
    full_name = forms.CharField(
        required=False,  # Это поле обязательно
        widget=forms.TextInput(attrs={"placeholder": "Ф.И.О.", "class": "form-control"}),
        label="Ф.И.О."
    )
    room = forms.CharField(
        required=False,  # Сделаем необязательным, как указано в модели
        widget=forms.TextInput(attrs={"placeholder": "Кабинет", "class": "form-control"}),
        label="Кабинет"
    )
    department = forms.ModelChoiceField(
        required=False,
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={"placeholder": "Департамент","class": "form-control"}),
        label="Департамент"
    )
    email = forms.CharField(
        required=False,  # Сделаем необязательным, как указано в модели
        widget=forms.TextInput(attrs={"placeholder": "Почта", "class": "form-control"}),
        label="Почта"
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={"placeholder": "Ваше фото", "class": "form-control"}
        ),
        label="Фото"
    )
    position = forms.CharField()

    class Meta:
        model = Record
        exclude = ('created_at', 'position_id', 'position', 'is_active')