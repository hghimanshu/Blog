from django.shortcuts import render
from .models import CustomUser
from django.http import HttpResponse
from .forms import registerUser

from .models import CustomUser


def createUser(request):
    template_name = "users/register.html"
    form = registerUser(request.POST or None)
    context = {
        'form': form
    }

    if form.is_valid():

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        name = form.cleaned_data.get('fullname')

        info = {'email': email, 'password': password, 'fullname': name}

        CustomUser.objects.create_user(**info)
        context['form'] = registerUser()

    return render(request, template_name, context)