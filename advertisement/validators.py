from django.forms import forms


def validate_words(text):
    from .models import BadWords
    bw = BadWords.objects.all()
    for i in bw:
        if i.word in text:
            raise forms.ValidationError(f'Найдено запрещенное слово')
