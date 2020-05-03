from django.urls import path
from .views import DepartmentView
app_name = "departments"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('department-tree/', DepartmentView.as_view()),
]