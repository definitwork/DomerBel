from uuid import uuid4

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


@api_view(['GET', 'POST', 'PATCH'])
def save_advertisement(request):
    additional_information = dict(request.data.copy())
    print(additional_information)
    serializer = AdvertisementSerializer(data=request.data)
    serializer.is_valid()
    keys_to_delete = ['csrfmiddlewaretoken', 'preview_img', 'photo_files', 'deleted_images', 'advertisement']
    keys_to_delete.extend(serializer.data.keys())
    for key in keys_to_delete:
        if key in additional_information:
            del additional_information[key]
    key_error = []
    for i in additional_information:
        if '' in additional_information.get(i):
            key_error.append(i)
    additional_information_filter = Field.objects.filter(id__in=key_error).exclude(error='')
    serializer_additional_error = AdditionalInformationSerializer(data=additional_information_filter, many=True)
    serializer_additional_error.is_valid()
    if request.method == "POST":
        if serializer.is_valid() and not serializer_additional_error.data:
            additional_information_save = Field.objects.filter(id__in=additional_information).order_by('id')
            for i in additional_information_save:
                additional_information[i.title] = ', '.join(additional_information.pop(f'{i.id}'))
            new_advertisement = Advertisement(author=None if request.user.is_anonymous else request.user,
                                              additional_information=additional_information,
                                              **serializer.validated_data)
                                              # article=serializer.validated_data.get('article'),
                                              # title=serializer.validated_data.get('title'), price=serializer.validated_data.get('price'),
                                              # category=serializer.validated_data.get('category'), bearer=serializer.validated_data.get('bearer'),
                                              # region=serializer.validated_data.get('region'), contact_name=serializer.validated_data.get('contact_name'),
                                              # email=serializer.validated_data.get('email'), phone_num=serializer.validated_data.get('phone_num'),
                                              # description=serializer.validated_data.get('description'), video_link=serializer.validated_data.get('video_link'),
                                              #  store=serializer.validated_data.get('store'))
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
    if request.method == 'PATCH':
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
                        if not advertisement.preview_image in deleted_images:
                            PhotoAdvertisement.objects.create(photo=advertisement.preview_image,
                                                              advertisement=advertisement)
                        advertisement.preview_image = photo
                        advertisement.save()
                        preview_img = advertisement.preview_image
                        print("save in files")
                    else:
                        additional_photo = PhotoAdvertisement(photo=photo, advertisement=advertisement)
                        additional_photo.save()
                        print('save additional')

            print(advertisement.preview_image)
            print(preview_img)
            if advertisement.preview_image != preview_img:
                if not advertisement.preview_image in deleted_images:
                    PhotoAdvertisement.objects.create(photo=advertisement.preview_image,
                                                      advertisement=advertisement)
                    print("change preview")
                if preview_img:
                    advertisement.preview_image = preview_img
                    advertisement.save()
                    PhotoAdvertisement.objects.filter(photo=preview_img).delete()
                print('save in perview')

            if request.data.getlist('deleted_images'):
                PhotoAdvertisement.objects.filter(photo__in=deleted_images).delete()
                # advertisement.author = None if request.user.is_anonymous else request.user
                # advertisement.additional_information = additional_information
                # advertisement.article = serializer.validated_data.get('article')
                # advertisement.title = serializer.validated_data.get('title')
                # advertisement.price = serializer.validated_data.get('price')
                # advertisement.category = serializer.validated_data.get('category')
                # advertisement.bearer = serializer.validated_data.get('bearer'),
                # advertisement.region = serializer.validated_data.get('region')
                # advertisement.contact_name = serializer.validated_data.get('contact_name')
                # advertisement.email = serializer.validated_data.get('email')
                # advertisement.phone_num = serializer.validated_data.get('phone_num')
                # advertisement.description = serializer.validated_data.get('description')
                # advertisement.video_link = serializer.validated_data.get('video_link')
                # advertisement.store = serializer.validated_data.get('store')




                    # print(request.data.get('deleted_images').split(','))
                    # for i in images:
                    #     if i.photo in request.data.get('deleted_images').split(','):
                    #         print(i)
                    # for image in request.data.getlist('deleted_images'):

                # if request.data.getlist('photo_files') != ['']:
                #     for photo in request.data.getlist('photo_files'):
                #         if photo.name == request.data.get("preview_img"):
                #             advertisement.preview_image = photo
                #             advertisement.save()
                #         else:
                #             additional_photo = PhotoAdvertisement(photo=photo, advertisement=advertisement)
                #             additional_photo.save()
                print(johannnn)
                return Response({"update": "объявление успешно изменено"}, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
                raise serializers.ValidationError(
                    {"error_additional": serializer_additional_error.data, "error": serializer.errors})
    return Response()

@api_view(['PUT'])
def update_advertisement(request):
    pass
