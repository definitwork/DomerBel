from django import forms

from main_page_domer.models import Publication


class PublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = '__all__'
        