from rest_framework.decorators import api_view
from transliterate import slugify

from advertisement.models import Region, Category, Field, ElementTwo, PhotoAdvertisement, Advertisement
from api_domer.serializers import GetListOfCitiesSerializer, GetListOfCategoriesSerializer, FieldSerialier, \
    ElementTwoSerializer, PhotoAdvertisementSerializer, AdvertisementSerializer
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
def get_category_list(request):
    categories = Category.objects.filter(parent_id=request.query_params.get('id'))
    serializer = GetListOfCategoriesSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_field_list(request):
    fieldlist = Field.objects.filter(category_id=request.query_params.get('id')).select_related('spisok').prefetch_related('spisok__element_set__elementtwo_set').order_by('id')
    serializer = FieldSerialier(fieldlist, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_elementtwo_list(request):
    if request.query_params.get('slug') == 'undefined':
        return Response()
    else:
        elementstwo = ElementTwo.objects.filter(element_id=request.query_params.get('slug'))
        serializer = ElementTwoSerializer(elementstwo, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def save_advertisement(request):
    additional_information = dict(request.data.copy())
    serializer = AdvertisementSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        keys_to_delete = ['csrfmiddlewaretoken', 'preview_img', 'photo_files']
        keys_to_delete.extend(serializer.data.keys())
        for key in keys_to_delete:
            if key in additional_information:
                additional_information.pop(key)
        for i in additional_information:
            additional_information[i] = additional_information.get(i)[0]
        new_advertisement = Advertisement(author=request.user, article=serializer.validated_data.get('article'),
                                          title=serializer.validated_data.get('title'), price=serializer.validated_data.get('price'),
                                          category=serializer.validated_data.get('category'), bearer=serializer.validated_data.get('bearer'),
                                          region=serializer.validated_data.get('region'), contact_name=serializer.validated_data.get('contact_name'),
                                          email=serializer.validated_data.get('email'), phone_num=serializer.validated_data.get('phone_num'),
                                          description=serializer.validated_data.get('description'), video_link=serializer.validated_data.get('video_link'),
                                          additional_information=additional_information, slug=slugify(serializer.validated_data.get('title')),
                                          store=serializer.validated_data.get('store'))
        new_advertisement.save()
        if request.data.getlist('photo_files') != ['']:
            for photo in request.data.getlist('photo_files'):
                if photo.name == request.data.get("preview_img"):
                    new_advertisement.preview_image = photo
                    new_advertisement.save()
                else:
                    additional_photo = PhotoAdvertisement(photo=photo, advertisement=new_advertisement)
                    additional_photo.save()
    return Response()
