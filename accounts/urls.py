from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUPView.as_view(), name='sign_up'),
]
