from rest_framework.decorators import api_view
from advertisement.models import Region, Category, Field, ElementTwo, PhotoAdvertisement
from api_domer.serializers import GetListOfCitiesSerializer, GetListOfCategoriesSerializer, FieldSerialier, \
    ElementTwoSerializer, PhotoAdvertisementSerializer
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


@api_view(['GET'])
def get_region_list(request):
    regions = Region.objects.all()
    serializer = GetListOfCitiesSerializer(regions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_category_list(request, id):
    categories = Category.objects.filter(parent_id=id)
    serializer = GetListOfCategoriesSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_field_list(request, id):
    fieldlist = Field.objects.filter(category_id=id).select_related('spisok').prefetch_related('spisok__element_set__elementtwo_set').order_by('id')
    serializer = FieldSerialier(fieldlist, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_elementtwo_list(request, slug):
    if slug == 'undefined':
        return Response()
    else:
        elementstwo = ElementTwo.objects.filter(element_id=slug)
        serializer = ElementTwoSerializer(elementstwo, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def save_advertisement(request):
    # for i in request.data.getlist('photo_files'):
    #     if i.name != request.data.get("preview_img"):
    #         print(i, "доп фото")
    #     else:
    #         print(i, "главная картинка")
        # photo = PhotoAdvertisement(photo=i, advertisement_id=1)
        # photo.save()
    # serializer = PhotoAdvertisementSerializer(request.data.get('photo_files'), many=True)
    print(request.data)
    return Response()
