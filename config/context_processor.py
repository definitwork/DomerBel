from users.forms import LoginForm, RegisterForm, EmailResetForm, RegisterFormEntity
from config.settings import env_keys


def get_context_data(request):
    context = {
        'login_form': LoginForm(),
        'register_form': RegisterForm(),
        'register_form_entity': RegisterFormEntity(),
        'email_reset_form': EmailResetForm(),
        "public_key" : env_keys.get('RECAPTCHA_PUBLIC_KEY'),
    }
    return context
