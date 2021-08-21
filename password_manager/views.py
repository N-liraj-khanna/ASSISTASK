from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Location
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.hashers import check_password
from .encryption import *

# Create your views here.
@login_required
def home(request):
    user = request.user
    location = Location.objects.filter(author = user)
    context = {
        'location': location
    }
    return render(request, "main/home.html", context)

class LocationCreateView(CreateView):
    template_name = 'main/location_form.html'
    model = Location
    fields = [
        'website_name',
        'website_link',
        'website_username',
        'website_password',
        'website_notes',
        'master_password',
    ]

    def form_valid(self, form):
        if form.is_valid():
            user = self.request.user
            form.instance.author = user

            form_master_password = form.instance.master_password
            # the field titled "master_password" in Location model 

            user_password = self.request.user.password
            # hashed master password in database 

            if not check_password(form_master_password, user_password):
                messages.add_message(self.request, messages.ERROR, 'Wrong Master Password')
                return redirect("create-pass")
            else: 
                website_password = form.instance.website_password

                form.instance.website_password = encrypt(form_master_password.encode(), website_password.encode())

                form.instance.website_password = encrypt(form_master_password.encode(), form.instance.website_password.encode())
                # to encrypt twice

                form.instance.master_password = ''
                # Clears out "master_password" of Location so that it isn't stored database 
                # If not, it will be stored as plain text
                # Storing plain text passwords has to be avoided at all costs
                
                return super().form_valid(form)
        else:
            messages.error(self.request, "Error")
            messages.add_message(self.request, messages.ERROR, 'Error')


@login_required
def view(request, pk):
    user = request.user
    location = Location.objects.get(id=pk, author=user)
    message = ''
    if request.method =="POST":
        user_password = location.website_password
        password = request.POST.get("password_field")
        if decrypted := decrypt(password.encode(), user_password):
            decrypted = decrypt(password.encode(), decrypted)
            context = {
                'location': location,
                'decrypted': decrypted,
                'confirmed': True, # user provided the right password
            }
            return render(request, "main/detail_view.html", context)
        else:
            message = 'try again'
    
    context = {
        'location': location,
        'message': message,
    }

    return render(request, "main/detail_view.html", context)
