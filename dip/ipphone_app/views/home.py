import json

from django.templatetags.static import static
from django.views.generic import ListView

from ipphone_app.models import Department, Record


class HomeView(ListView):
    model = Department  # Set the model for the ListView
    ordering = ["position"]
    template_name = "home/home.html"
    context_object_name = "departments"  # The context variable that holds departments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the departments and records
        departments = self.get_queryset()
        records = Record.objects.all().order_by("department__position", "position_id")

        # Add department records grouped by department
        department_records = {}
        for department in departments:
            department_records[department.id] = records.filter(
                department=department, is_active=True
            )

        # Convert records and departments to JSON
        records_json = list(
            records.values(
                "id",
                "is_active",
                "phone",
                "image",
                "full_name",
                "department__name",
                "department__position",
                "position",
                "position_id",
                "room",
                "email",
            )
        )
        # Set the image url to js could handle it
        for record in records_json:
            if record["image"]:
                record["image"] = "media/" + record["image"]

        records_json = json.dumps(records_json)

        departments_json = json.dumps(
            list(departments.values("id", "name", "position"))
        )

        # Add to context
        context["records"] = records
        context["all_employers_json"] = records_json
        context["departments_json"] = departments_json
        context["department_records"] = department_records

        return context
