from django.db import models

# Create your models here.

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Department(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children_departments', db_index=True,
                            on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['id']

    def __str__(self):
        return self.name


class Consumer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='entries')

    def __str__(self):
        return self.first_name + ',' + self.last_name
