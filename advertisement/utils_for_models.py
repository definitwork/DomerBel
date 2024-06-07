import random
import os

from uuid import uuid4
from slugify import slugify
from PIL import Image, ImageDraw, ImageFont
from hashlib import md5


def upload_to(instance, filename):
    """Хэширование имени файла и распределение
       файлов по приложениям и далее в разные папки
       случайным образом"""
    folders = ('folder1', 'folder2', 'folder3')
    save_folder = random.choice(folders)
    ext = os.path.splitext(filename)[1]
    name = str(instance.pk or '') + filename
    filename = md5(name.encode('utf8')).hexdigest() + ext
    basedir = os.path.join(instance._meta.app_label)
    return os.path.join(basedir, save_folder, filename)


def add_watermark_to_photo(photo):
    """Добавление водяного знака на изображение"""
    photo = Image.open(photo)
    draw = ImageDraw.Draw(photo)
    width, height = photo.size
    font = ImageFont.truetype("arial_bolditalicmt.ttf", int(width / 100 * 6))
    watermark_word = "ДОМер.бел"
    x = width - 10
    y = height - 10
    watermark_text = Image.new("RGBA", photo.size, (255, 255, 255, 0))
    watermark = ImageDraw.Draw(watermark_text)
    watermark.text((x, y), watermark_word, (255, 255, 255, 80), font=font, anchor='rb')
    photo = photo.convert(mode="RGBA")
    photo = Image.alpha_composite(photo, watermark_text)
    return photo

def unique_slugify(slug):
    """ Генератор уникальных SLUG для
        моделей, в случае существования
        такого SLUG."""
    unique_slug = f'{uuid4()}-{slugify(slug)}'
    return unique_slug
