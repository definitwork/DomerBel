from rest_framework.decorators import api_view
from advertisement.models import Region, Category
from api_domer.serializers import GetListOfCitiesSerializer, GetListOfCategoriesSerializer
from rest_framework.response import Response


# Отдаёт список городов type='Город' по id выбранной области type='Область' из модели Region
@api_view(["GET", "POST"])
def get_list_of_cities(request, id):
    cities = Region.objects.filter(parent_id=id)
    serializer = GetListOfCitiesSerializer(cities, many=True)
    return Response(serializer.data)

# Отдаёт список всех категорий из модели Category
@api_view(["GET", "POST"])
def get_list_of_categories(request):
    categories = Category.objects.all()
    serializer = GetListOfCategoriesSerializer(categories, many=True)
    return Response(serializer.data)