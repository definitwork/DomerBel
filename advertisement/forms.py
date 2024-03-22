from django.forms import ClearableFileInput
from mptt.forms import TreeNodeChoiceField

from advertisement.models import Store, Region, Category
from django import forms

from users.models import User


class StoreForm(forms.ModelForm):
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(type="Город"),
        label="Регион, город, область",
        widget=forms.Select(attrs={"class": "input_field"}),
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        label="Адрес",
        widget=forms.TextInput(attrs={"class": "input_field"}),
    )
    category = TreeNodeChoiceField(queryset=Category.objects.all(), label="Раздел")
    title = forms.CharField(
        max_length=255,
        label="Название магазина",
        widget=forms.TextInput(attrs={"class": "input_field"}),
    )
    slug = forms.SlugField(
        min_length=4,
        max_length=20,
        label="Имя магазина, которое будет отображаться в URL-e страницы Вашего магазина "
        "(только латинские буквы и тире, должно начинаться с буквы и содержать от 4 до 20 символов",
        widget=forms.TextInput(attrs={"class": "input_field"}),
    )
    description = forms.CharField(
        label="Описание", widget=forms.Textarea(attrs={"class": "input_field"})
    )
    url = forms.URLField(
        required=False,
        label="Сайт магазина",
        widget=forms.URLInput(
            attrs={
                "class": "input_field",
                "placeholder": "Должен начитаться с http:// или https://",
                "size": 40,
            }
        ),
    )
    contact_name = forms.CharField(
        max_length=255,
        label="Контактное лицо",
        widget=forms.TextInput(attrs={"class": "input_field"}),
    )
    email = forms.EmailField(
        label="E-mail", widget=forms.TextInput(attrs={"class": "input_field"})
    )
    phone_num = forms.CharField(
        max_length=255,
        required=False,
        label="Телефон",
        widget=forms.TextInput(attrs={"class": "input_field"}),
    )
    video_link = forms.URLField(
        required=False,
        label="Ссылка на видеоролик YouTube",
        widget=forms.URLInput(
            attrs={
                "class": "input_field",
                "placeholder": "Должен начитаться с http:// или https://",
                "size": 40,
            }
        ),
    )
    logo_image = forms.ImageField(
        required=False,
        label="Логотип",
        widget=ClearableFileInput(attrs={"class": "input_field"}),
    )
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Store
        fields = [
            "region",
            "address",
            "category",
            "title",
            "slug",
            "description",
            "url",
            "contact_name",
            "email",
            "phone_num",
            "video_link",
            "logo_image",
            "user",
        ]
