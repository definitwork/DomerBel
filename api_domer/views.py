from uuid import uuid4

from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from transliterate import slugify
from rest_framework import status, serializers

from advertisement.models import Region, Category, Field, ElementTwo, PhotoAdvertisement, Advertisement, Store
from api_domer.serializers import GetListOfCitiesSerializer, GetListOfCategoriesSerializer, FieldSerialier, \
    ElementTwoSerializer, PhotoAdvertisementSerializer, AdvertisementSerializer, StoreSerializer, \
    AdditionalInformationSerializer, UserRegisterSerializer, UserLoginSerializer
from rest_framework.response import Response

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


@api_view(["POST"])
def registration_user(request):
    registration_serializer = UserRegisterSerializer(data=request.data, context={"request": request})
    if registration_serializer.is_valid():
        registration_serializer.save()
        return Response({'success': 'Вы успешно зарегистрированы'}, status=status.HTTP_201_CREATED)
    else:
        raise serializers.ValidationError(
            {"errors": registration_serializer.errors})


@api_view(["POST"])
def login_user(request):
    login_serializer = UserLoginSerializer(data=request.data, context={"request": request})
    if login_serializer.is_valid():
        user = authenticate(**login_serializer.validated_data)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            raise serializers.ValidationError({"user_undefined": "Пользователь не найден"})
    else:
        raise serializers.ValidationError(
            {"errors": login_serializer.errors})


@api_view(["GET"])
def logout_user(request):
    try:
        logout(request)
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)

