from django import forms

from ipphone_app.models import RecordFormConfiguration


class RecordFormConfigurationForm(forms.ModelForm):

    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Сделать формы активными?",
    )

    # permissions for record update
    phone = forms.BooleanField(
        required=False,  # Это поле обязательно
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Позволить изменить - внутренний номер",
    )
    full_name = forms.BooleanField(
        required=False,  # Это поле обязательно
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Позволить изменить - Ф.И.О",
    )
    room = forms.BooleanField(
        required=False,  # Это поле обязательно
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Позволить изменить - номер кабинета",
    )
    department = forms.BooleanField(
        required=False,  # Это поле обязательно
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Позволить изменить - департамент",
    )
    email = forms.BooleanField(
        required=False,  # Это поле обязательно
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Позволить изменить - почту",
    )
    image = forms.BooleanField(
        required=False,  # Это поле обязательно
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Позволить изменить - фото",
    )
    position = forms.BooleanField(
        required=False,  # Это поле обязательно
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Позволить изменить - должность",
    )

    expire_time_duration = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )
    attempts_number = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Количество попыток для открытия ссылки",
    )

    class Meta:
        model = RecordFormConfiguration
        exclude = ("name",)
