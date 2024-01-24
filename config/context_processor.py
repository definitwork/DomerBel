from users.forms import LoginForm, RegisterForm, EmailResetForm


def get_context_data(request):
    context = {
        'login_form': LoginForm(),
        'register_form': RegisterForm(),
        'email_reset_form': EmailResetForm()
    }
    return context
