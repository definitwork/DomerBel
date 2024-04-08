from rest_framework.decorators import api_view
from transliterate import slugify
from rest_framework import status, serializers

from advertisement.models import Region, Category, Field, ElementTwo, PhotoAdvertisement, Advertisement, Store
from api_domer.serializers import GetListOfCitiesSerializer, GetListOfCategoriesSerializer, FieldSerialier, \
    ElementTwoSerializer, PhotoAdvertisementSerializer, AdvertisementSerializer, StoreSerializer, \
    AdditionalInformationSerializer
from rest_framework.response import Response


# Отдаёт список городов type='Город' по id выбранной области type='Область' из модели Region
@api_view(["GET", "POST"])
def get_list_of_cities(request, id):
    cities = Region.objects.filter(parent_id=id)
    serializer = GetListOfCitiesSerializer(cities, many=True)
    return Response(serializer.data)


# Отдаёт список всех категорий из модели Category для добавления/редактирования магазина
@api_view(["GET", "POST"])
def get_list_of_categories(request):
    categories = Category.objects.filter(level__lte=1)
    serializer = GetListOfCategoriesSerializer(categories, many=True)
    return Response(serializer.data)


# Отдает список дочерних категорий по родительскому id (для поиска магазиноа и поиска в ЛК)
@api_view(["GET", "POST"])
def get_categories_for_search(request, id):
    categories = Category.objects.filter(parent_id=id)
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


@api_view(['GET'])
def get_store_for_advertisement(request):
    stores = Store.objects.filter(user=request.user.id)
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def save_advertisement(request):
    additional_information = dict(request.data.copy())
    if request.method == "POST":
        serializer = AdvertisementSerializer(data=request.data)
        serializer.is_valid()
        keys_to_delete = ['csrfmiddlewaretoken', 'preview_img', 'photo_files']
        keys_to_delete.extend(serializer.data.keys())
        for key in keys_to_delete:
            if key in additional_information:
                additional_information.pop(key)
        key_error = []
        for i in additional_information:
            if '' in additional_information.get(i):
                key_error.append(i)
        additional_information_filter = Field.objects.filter(id__in=key_error).exclude(error='')
        serializer_additional_error = AdditionalInformationSerializer(data=additional_information_filter, many=True)
        serializer_additional_error.is_valid()
        if serializer.is_valid() and not serializer_additional_error.data:
            additional_information_save = Field.objects.filter(id__in=additional_information).order_by('id')
            for i in additional_information_save:
                additional_information[i.title] = ' '.join(additional_information.pop(f'{i.id}'))
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
            return Response({"created": "объявление успешно создано"},status=status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError({"error_additional": serializer_additional_error.data, "error": serializer.errors})
    return Response()
