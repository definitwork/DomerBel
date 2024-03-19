from rest_framework import serializers

from advertisement.models import Region, Category, Field, Spisok, ElementTwo, Element


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
        fields = 'title', 'elementtwo_set'


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
