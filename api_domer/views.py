from uuid import uuid4

from cgi import print_environ_usage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status, serializers, generics, filters
from slugify import slugify


from advertisement.models import Region, Category, Field, ElementTwo, PhotoAdvertisement, Advertisement, Store
from api_domer.filters import PublicationsFilter
from api_domer.serializers import (GetListOfCitiesSerializer, GetListOfCategoriesSerializer, FieldSerialier,
                                   ElementTwoSerializer, AdvertisementSerializer, PublicationSearchSerializer,
                                   PublicationSerializer, StoreSerializer, AdditionalInformationSerializer)
from main_page_domer.models import PhotoPublication, Publication

from api_domer.utils import validate_additional_information


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
    fieldlist = Field.objects.filter(category_id=request.query_params.get('id')).select_related(

        'spisok').prefetch_related('spisok__element_set__elementtwo_set').order_by('id')
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


@api_view(['POST'])
def save_advertisement(request):
    additional_information = dict(request.data.copy())
    serializer = AdvertisementSerializer(data=request.data)
    serializer.is_valid()
    keys_to_delete = ['csrfmiddlewaretoken', 'preview_img', 'photo_files']
    keys_to_delete.extend(serializer.data.keys())
    serializer_additional_error, additional_information = validate_additional_information(keys_to_delete,
                                                                                          additional_information)
    if serializer.is_valid() and not serializer_additional_error.data:
        additional_information_save = Field.objects.filter(id__in=additional_information).order_by('id')
        for i in additional_information_save:
            additional_information[i.title] = ', '.join(additional_information.pop(f'{i.id}'))
        new_advertisement = Advertisement(author=None if request.user.is_anonymous else request.user,
                                          additional_information=additional_information,
                                          **serializer.validated_data)
        new_advertisement.save()
        if request.data.getlist('photo_files') != ['']:
            for photo in request.data.getlist('photo_files'):
                if photo.name == request.data.get("preview_img"):
                    new_advertisement.preview_image = photo
                    new_advertisement.save()
                else:
                    additional_photo = PhotoAdvertisement(photo=photo, advertisement=new_advertisement)
                    additional_photo.save()
        return Response({"created": "объявление успешно создано"}, status=status.HTTP_201_CREATED)
    else:
        raise serializers.ValidationError(
            {"error_additional": serializer_additional_error.data, "error": serializer.errors})



@api_view(['PATCH'])
def update_advertisement(request):
    additional_information = dict(request.data.copy())
    serializer = AdvertisementSerializer(data=request.data)
    serializer.is_valid()
    keys_to_delete = ['csrfmiddlewaretoken', 'preview_img', 'photo_files', 'deleted_images', 'advertisement']
    keys_to_delete.extend(serializer.data.keys())
    serializer_additional_error, additional_information = validate_additional_information(keys_to_delete,
                                                                                          additional_information)
    if serializer.is_valid() and not serializer_additional_error.data:
        additional_information_save = Field.objects.filter(id__in=additional_information).order_by('id')
        for i in additional_information_save:
            additional_information[i.title] = ', '.join(additional_information.pop(f'{i.id}'))
        deleted_images = request.data.get('deleted_images').split(',')
        preview_img = request.data.get("preview_img")
        Advertisement.objects.filter(id=request.data.get('advertisement')
                                     ).update(author=None if request.user.is_anonymous else request.user,
                                              additional_information=additional_information,
                                              **serializer.validated_data)
        advertisement = Advertisement.objects.get(id=request.data.get('advertisement'))

        if request.data.getlist('photo_files') != ['']:
            for photo in request.data.getlist('photo_files'):
                if photo.name == preview_img:
                    if advertisement.preview_image not in deleted_images:
                        PhotoAdvertisement.objects.create(photo=advertisement.preview_image,
                                                          advertisement=advertisement)
                    advertisement.preview_image = photo
                    advertisement.save()
                    preview_img = advertisement.preview_image
                else:
                    additional_photo = PhotoAdvertisement(photo=photo, advertisement=advertisement)
                    additional_photo.save()

        if advertisement.preview_image != preview_img:
            if advertisement.preview_image not in deleted_images:
                PhotoAdvertisement.objects.create(photo=advertisement.preview_image,
                                                  advertisement=advertisement)
            if preview_img:
                advertisement.preview_image = preview_img
                PhotoAdvertisement.objects.filter(photo=preview_img).delete()
            else:
                advertisement.preview_image = None
            advertisement.save()

        if request.data.getlist('deleted_images'):
            PhotoAdvertisement.objects.filter(photo__in=deleted_images).delete()

        return Response({"update": "объявление успешно изменено"}, status=status.HTTP_200_OK)
    else:
        raise serializers.ValidationError(
            {"error_additional": serializer_additional_error.data, "error": serializer.errors})


class ThisPublicationSearchListAPIView(generics.ListAPIView):
    """ Выводим все новости секции """
    queryset = Publication.objects.all()
    serializer_class = PublicationSearchSerializer
    pagination_class = LimitOffsetPagination  # Пагинация
    # Поиск по заголовку, содержанию и дате
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'announcement', 'description']  # Поля, по которым будет выполняться поиск
    filterset_class = PublicationsFilter


@api_view(['POST'])
def save_publication(request):
    if request.method == "POST":
        try:
            query_dict = request.data.dict()
            main_img_name = request.data.get('main_img')
            preview_image_list = request.FILES.getlist('preview_image')
            if len(preview_image_list) > 1:
                for preview_img in preview_image_list:
                    if preview_img.name == main_img_name:
                        query_dict['preview_image'] = preview_img
                        preview_image_list.remove(preview_img)
            else:
                preview_image_list = []
            query_dict['user'] = request.user.id
            query_dict['slug'] = slugify(str(query_dict['title']))
            serializer = PublicationSerializer(data=query_dict)
            if serializer.is_valid():
                serializer.save()
                if preview_image_list != []:
                    for preview_image in preview_image_list:
                        p = PhotoPublication(
                            publications = serializer.instance,
                            photo = preview_image
                        )
                        p.save()
            else:
                for field, errors in serializer.errors.items():
                    print(f"Поле '{field}' не прошло валидацию. Ошибки: {errors}")
        except Exception as error:
            print('error: ', error)
    return Response()


@api_view(['POST'])
def edit_publication(request):
    if request.method == "POST":
        try:
            query_dict = request.data.dict()
            print('=====================================================================')
            print('1', query_dict)
            print('=====================================================================')
        #     main_img_name = request.data.get('main_img')
        #     preview_image_list = request.FILES.getlist('preview_image')
        #     if len(preview_image_list) > 1:
        #         for preview_img in preview_image_list:
        #             if preview_img.name == main_img_name:
        #                 query_dict['preview_image'] = preview_img
        #                 preview_image_list.remove(preview_img)
        #     else:
        #         preview_image_list = []
        #     query_dict['user'] = request.user.id
        #     query_dict['slug'] = slugify(str(query_dict['title']))
        #     serializer = PublicationSerializer(data=query_dict)
        #     if serializer.is_valid():
        #         serializer.save()
        #         if preview_image_list != []:
        #             for preview_image in preview_image_list:
        #                 p = PhotoPublication(
        #                     publications = serializer.instance,
        #                     photo = preview_image
        #                 )
        #                 p.save()
        #     else:
        #         print("serializer don't ok")
        #         for field, errors in serializer.errors.items():
        #             print(f"Поле '{field}' не прошло валидацию. Ошибки: {errors}")
        except Exception as error:
            print('2 error: ', error)
    return Response()
