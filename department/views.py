# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Department, Consumer
from .serializers import CategorySerializer


class DepartmentView(APIView):
    """

    :param request:
    :return:
    """
    #
    def get(self, request):
        if self.request.method == 'GET':
            departments = Department.objects.all().prefetch_related('entries')
            root_id = self.request.GET.get('root-id', None)
            departments = departments.get(id=root_id).get_descendants(include_self=True)
            departments_consumers = {y.id: y.entries.all()
                                     for y in departments}  # type: dict
            departments_consumers = {k: v.values('id', 'first_name', 'last_name')
                                     for k, v in departments_consumers.items() if v.exists()}
            # пробрасываем искомое значение
            departments_serializer = CategorySerializer(departments, many=True,
                                                        context={'id': root_id, 'consumers': departments_consumers})
            serialized_data = departments_serializer.data[:]
            # убираем пустые элементы
            filtered_serialized_data = [y for y in serialized_data if y is not None]
            return Response(filtered_serialized_data)
