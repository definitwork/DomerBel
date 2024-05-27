from rest_framework import serializers
from transliterate import slugify
from django.utils import formats

from advertisement.models import Region, Category, Field, Spisok, ElementTwo, Element, Advertisement, Store
from main_page_domer.models import Publication


class GetListOfCitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class GetListOfCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ElementTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementTwo
        fields = 'title',


class ElementSerializer(serializers.ModelSerializer):
    elementtwo_set = ElementTwoSerializer(many=True, read_only=True)

    class Meta:
        model = Element
        fields = 'id', 'title', 'elementtwo_set'


class SpisokSerializer(serializers.ModelSerializer):
    element_set = ElementSerializer(many=True, read_only=True)

    class Meta:
        model = Spisok
        fields = 'title', 'element_set'


class FieldSerialier(serializers.ModelSerializer):
    spisok = SpisokSerializer(read_only=True)

    class Meta:
        model = Field
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'title']


class PhotoAdvertisementSerializer(serializers.Serializer):
    InMemoryUploadedFile = serializers.ImageField()


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['article', 'title', "price",
                  'category', 'bearer', 'region',
                  'preview_image', 'contact_name',
                  'email', 'phone_num', 'description',
                  'video_link', 'store']


class AdditionalInformationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    error = serializers.CharField()


class PublicationSearchSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """ Переопределяем вывод даты в формате 'd-m-Y H:i' """
        representation = super().to_representation(instance)
        representation['date_of_create'] = formats.date_format(instance.date_of_create, "d-m-Y H:i")
        return representation

    class Meta:
        model = Publication
        fields = '__all__'


class PublicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publication
        fields = ['user', 'title', 'announcement', 'description', 'preview_image', 'video_link',]
        # fields = "__all__"
