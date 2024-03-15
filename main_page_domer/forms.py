from django import forms
from django.forms import ClearableFileInput
from mptt.forms import TreeNodeChoiceField

from advertisement.models import Region, Category
from main_page_domer.models import Store
from users.models import User
from users.validators import validate_email, validate_phone

class StoreForm(forms.ModelForm):
    region = forms.ModelChoiceField(queryset=Region.objects.filter(type="Город"), label="Регион, город, область",
                                    widget=forms.Select(attrs={'class': 'input_field'}))
    address = forms.CharField(max_length=255, required=False, label="Адрес",
                              widget=forms.TextInput(attrs={'class': 'input_field'}))
    category = TreeNodeChoiceField(queryset=Category.objects.all(), label="Раздел")
    title = forms.CharField(max_length=255, required=True, label="Название магазина",
                            widget=forms.TextInput(attrs={'class': 'input_field'}))
    slug = forms.SlugField(min_length=4, max_length=20, required=True,
                           label="Имя магазина, которое будет отображаться в URL-e страницы Вашего магазина "
                                 "(только латинские буквы и тире, должно начинаться с буквы и содержать от 4 до 20 символов",
                           widget=forms.TextInput(attrs={'class': 'input_field'}))
    description = forms.CharField(required=True, label="Описание", widget=forms.Textarea(attrs={'class': 'input_field'}))
    url = forms.URLField(required=False, label="Сайт магазина", widget=forms.URLInput(
        attrs={'class': 'input_field', 'placeholder': 'Должен начитаться с http:// или https://',
               'size': 40}))
    contact_name = forms.CharField(required=True, max_length=255, label="Контактное лицо",
                                   widget=forms.TextInput(attrs={'class': 'input_field'}))
    email = forms.EmailField(required=True, label="E-mail",
                             widget=forms.TextInput(attrs={'class': 'input_field', 'id': 'store_email'}))
    phone_num = forms.CharField(max_length=255, required=False, label="Телефон",
                                widget=forms.TextInput(attrs={'class': 'input_field'}),
                                validators=[validate_phone])
    video_link = forms.URLField(required=False, label="Ссылка на видеоролик YouTube", widget=forms.URLInput(
        attrs={'class': 'input_field', 'placeholder': 'Должен начитаться с http:// или https://', 'size': 40}))
    logo_image = forms.ImageField(required=False, label="Логотип",
                                  widget=ClearableFileInput(attrs={'class': 'input_field'}))
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Store
        fields = ['region', 'address', 'category', 'title', 'slug', 'description', 'url', 'contact_name', 'email',
                  'phone_num', 'video_link', 'logo_image', 'user']
