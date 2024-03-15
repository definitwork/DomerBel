from django import forms
from django.forms import ClearableFileInput
from mptt.forms import TreeNodeChoiceField

from advertisement.models import Store, Region, Category
from users.models import User
from users.validators import validate_email, validate_phone


