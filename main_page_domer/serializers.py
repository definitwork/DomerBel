from rest_framework import serializers

from advertisement.models import Region, Category


class GetListOfCitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class GetListOfCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'