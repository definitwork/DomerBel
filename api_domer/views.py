from uuid import uuid4

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework import status, serializers, generics, filters
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from advertisement.models import Region, Category, Field, ElementTwo, PhotoAdvertisement, Advertisement, Store, Element, \
    ErrorFile
from api_domer.serializers import GetListOfCitiesSerializer, GetListOfCategoriesSerializer, FieldSerialier, \
    ElementTwoSerializer, AdvertisementSerializer, StoreSerializer, \
    UserRegisterSerializer, UserLoginSerializer, PasswordResetSerializer, \
    SavePhotoPublicationSerializer, SavePublicationSerializer, EditPublicationSerializer, PublicationSearchSerializer, \
    ElementSerializer, GetListOfCategoriesFieldsSerializer

from api_domer.filters import PublicationsFilter

from main_page_domer.models import PhotoPublication, Publication

from rest_framework.response import Response

from api_domer.utils import validate_additional_information
from config.settings import env_keys
from users.models import User


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
            raise serializers.ValidationError({"errors": {"email": "Пользователь не найден. Проверьте правильность введенных данных.", "password": ''}})
    else:
        raise serializers.ValidationError({"errors": login_serializer.errors})


@api_view(["POST"])
def logout_user(request):
    try:
        logout(request)
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def password_reset(request):
    password_reset_serializer = PasswordResetSerializer(data=request.data, context={"request": request})
    if password_reset_serializer.is_valid():
        email = password_reset_serializer.validated_data.get('email')
        url = env_keys.get("URL")
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_url = reverse_lazy('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        send_mail(
            subject='Восстановление пароля',
            message=f'''
            Вы получили это письмо, потому что Вы (или кто-то другой) запросили восстановление пароля от учётной записи 
            на сайте {url}, которая связана с этим адресом электронной почты.
            
            Для восстановления пароля перейдите по данной ссылке: 
            
            {url}{activation_url}
            
            Спасибо, что используете наш сайт!
            
            Команда сайта {url}
            
            
            Если вы не запрашивали восстановление пароля, то проигнорируйте это сообщение''',
            from_email=None,
            recipient_list=[email],
            fail_silently=False)
        return Response({'success': 'На ваш адрес электронной почты было отправлено письмо для восстановления '
                                    'пароля. Если письмо не пришло, проверьте папку спам.'},
                        status=status.HTTP_200_OK)
    else:
        raise serializers.ValidationError(
            {"errors": password_reset_serializer.errors})


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
    """ Сохранение новой публикации """
    error_serializer = {'errors': []}
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
            serializer = SavePublicationSerializer(data=query_dict)
            if serializer.is_valid():
                serializer.save()
                if preview_image_list != []:
                    for preview_image in preview_image_list:
                        serializer_for_photo_publication = SavePhotoPublicationSerializer(
                            data={"publications": serializer.instance.id, "photo": preview_image})
                        if serializer_for_photo_publication.is_valid():
                            serializer_for_photo_publication.save()
                        else:
                            for field, errors in serializer_for_photo_publication.errors.items():
                                error_serializer['errors'].append(
                                    f"Поле '{field}' не прошло валидацию. Ошибки: {errors}")
                            return Response({"error": "Ошибка валидации данных ", "detail": error_serializer},
                                            status=status.HTTP_400_BAD_REQUEST)
            else:
                for field, errors in serializer.errors.items():
                    error_serializer['errors'].append(f"Поле '{field}' не прошло валидацию. Ошибки: {errors}")
                return Response({"error": "Ошибка валидации данных", "detail": error_serializer},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({"error": "Ошибка при сохранении публикации",
                             "detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"created": "Публикация успешно сохранена"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def edit_publication(request):
    """ Сохранение публикации после редактирования """
    error_serializer = {'errors': []}
    if request.method == "POST":
        try:
            query_dict = request.data.dict()
            flag_edited_publication = False
            main_img_name = request.data.get('main_img')
            edited_publication = Publication.objects.get(slug=query_dict.get("dataSlag"))
            serializer_edit_publication = EditPublicationSerializer(data=query_dict)

            if not request.FILES.get('preview_image'):
                del query_dict['preview_image']
                preview_image_list = []
            else:
                preview_image_list = request.FILES.getlist('preview_image')

            if serializer_edit_publication.is_valid() and main_img_name != 'undefined':
                validated_data = serializer_edit_publication.validated_data

                if query_dict.get("title") != edited_publication.title:  # Проверяем изменился ли заголовок
                    edited_publication.title = validated_data.get("title")
                    flag_edited_publication = True

                if query_dict.get("announcement") != edited_publication.announcement:  # Проверяем изменилась ли аннотация
                    edited_publication.announcement = validated_data.get("announcement")
                    flag_edited_publication = True

                if query_dict.get("description") != edited_publication.description:  # Проверяем изменился ли текст статьи
                    edited_publication.description = validated_data.get("description")
                    flag_edited_publication = True

                if query_dict.get("video_link") != edited_publication.video_link:  # Проверяем изменился ли ссылка на видео
                    edited_publication.video_link = validated_data.get("video_link")
                    flag_edited_publication = True

                if not preview_image_list:  # Проверяем есть ли новые загруженные картинки
                    if main_img_name != edited_publication.preview_image:
                        PhotoPublication.objects.filter(photo=main_img_name).update(
                            photo=edited_publication.preview_image)
                        edited_publication.preview_image = main_img_name
                        flag_edited_publication = True
                else:
                    new_main_img_file = False
                    for preview_img in preview_image_list:
                        if preview_img.name == main_img_name:
                            main_img_name = preview_img
                            preview_image_list.remove(preview_img)
                            new_main_img_file = True

                    if main_img_name != edited_publication.preview_image and not new_main_img_file:  # Главная картинка изменилась и ее нет в новых файлах
                        PhotoPublication.objects.filter(photo=main_img_name).update(
                            photo=edited_publication.preview_image)
                        edited_publication.preview_image = main_img_name
                        flag_edited_publication = True
                    elif main_img_name != edited_publication.preview_image and new_main_img_file:  # Главная картинка изменилась и она в новых файлах
                        p = PhotoPublication(photo=edited_publication.preview_image, publications=edited_publication)
                        p.save()
                        edited_publication.preview_image = main_img_name
                        flag_edited_publication = True

                    if preview_image_list:  # Если есть новые файлы сохраняем их
                        flag_edited_publication = True
                        for preview_image in preview_image_list:
                            serializer_for_photo_publication = SavePhotoPublicationSerializer(
                                data={"publications": edited_publication.id, "photo": preview_image})
                            if serializer_for_photo_publication.is_valid():
                                serializer_for_photo_publication.save()
                            else:
                                for field, errors in serializer_for_photo_publication.errors.items():
                                    error_serializer['errors'].append(
                                        f"Поле '{field}' не прошло валидацию. Ошибки: {errors}")
                                return Response({"error": "Ошибка валидации данных ", "detail": error_serializer},
                                                status=status.HTTP_400_BAD_REQUEST)

                if query_dict.get('deletedImages'):  # Если есть файлы на удаление удаляем их
                    deleted_images = query_dict.get('deletedImages').split(',')
                    PhotoPublication.objects.filter(photo__in=deleted_images).delete()
                    flag_edited_publication = True

                if flag_edited_publication:  # Если были изменения в публикации то сохраняем их
                    edited_publication.moderated = False
                    edited_publication.save()

            else:
                for field, errors in serializer_edit_publication.errors.items():
                    error_serializer['errors'].append(f"Поле '{field}' не прошло валидацию. Ошибки: {errors}")
                return Response({"error": "Ошибка валидации данных ", "detail": error_serializer},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({"error": "Ошибка при изменении публикации",
                             "detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"update": "Публикация успешно изменена"}, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_element_list(request):
    '''Отадет элементы связанные с полем по id'''
    elements = Element.objects.filter(spisok_id__field=request.query_params.get('id'))
    serializer = ElementSerializer(elements, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_subcategory_list(request):
    '''Отдает подкатегориии и их поля по id категории'''
    categories = Category.objects.filter(parent_id=request.query_params.get('id')).prefetch_related('field_set__spisok__element_set__elementtwo_set')
    serializer = GetListOfCategoriesFieldsSerializer(categories, many=True)
    return Response(serializer.data)


