from django import forms
<<<<<<< HEAD

from main_page_domer.models import Publication


class PublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = '__all__'
        
=======
from django_recaptcha.fields import ReCaptchaField

from users.validators import validate_email


class FeedbackForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'required': 'Не указан email'}, label='Ваш e-mail:',
                             validators=[validate_email], widget=forms.EmailInput(attrs={'class': 'input_field'}))
    subject = forms.CharField(required=True, max_length=255, error_messages={'required': 'Не указана тема письма'},
                            label="Тема письма:", widget=forms.TextInput(attrs={'class': 'input_field'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'input_field'}), required=True,
                              error_messages={'required': 'Отсутствует текст письма'}, label='Текст письма:')
    captcha = ReCaptchaField(label='')
>>>>>>> pre-dev
