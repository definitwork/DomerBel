from users.forms import LoginForm, RegisterForm, EmailResetForm, RegisterFormEntity


def get_context_data(request):
    context = {
        'login_form': LoginForm(),
        'register_form': RegisterForm(),
        'register_form_entity': RegisterFormEntity(),
        'email_reset_form': EmailResetForm(),
    }
    return context
