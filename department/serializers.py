from collections import OrderedDict

from rest_framework import serializers

from .models import Department, Consumer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'parent']


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ['id', 'first_name', 'last_name', 'department']


class HierarchyDepartmentSerializer(serializers.ModelSerializer):
    counter = 0

    employees = serializers.SerializerMethodField(read_only=True)

    def get_employees(self, obj):
        consumers = self.context["consumers"]
        current_consumers = consumers.get(obj.id) if consumers is not None else None
        return current_consumers if current_consumers is not None else None

    class Meta:
        model = Department
        fields = ('id', 'name', 'parent', 'employees', 'children_departments')

    def get_fields(self):
        fields = super(HierarchyDepartmentSerializer, self).get_fields()
        fields['children_departments'] = HierarchyDepartmentSerializer(many=True)
        return fields

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        #убираем ненужные вызовы к бд, искомый элемент уже получен
        if self.counter == -1:
            return None

        fields = self._readable_fields
        for field in fields:
            attribute = field.get_attribute(instance)
            ret[field.field_name] = field.to_representation(attribute)

        if str(instance.id) == self.context["id"]:
            #помечаем, что искомый элемент уже получен
            self.counter = -1

        return ret
