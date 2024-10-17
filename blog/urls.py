from django.urls import path
from .views import *

urlpatterns = [
    path('', BlogListView.as_view(), name='home_page'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_details'),
    #! the pk : primary key WE ONLY USE THE PRIMARY KEY
]
