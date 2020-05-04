from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import DepartmentViewSet, HierarchyDepartmentView, ConsumerViewSet

app_name = "departments"

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'consumers', ConsumerViewSet)
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('department-tree/', HierarchyDepartmentView.as_view())
]
urlpatterns.extend(router.urls)
