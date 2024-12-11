from django import forms
from ipphone_app.models import Department

class AddDepartmentForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Название департамента", "class": "form-control"}),
        label=""
    )
    position = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "Позиция департамента (Для сортировки)", "class": "form-control"}),
        label=""
    )

    class Meta:
        model = Department
        fields = ['name', 'position']  # Определим только нужные поля