from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
# Create your views here.

class SignUPView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home_page')
    template_name ='registration/signup.html'
