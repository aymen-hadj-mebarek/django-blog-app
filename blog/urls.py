from django.urls import path
from .views import *

urlpatterns = [
    path('', BlogListView.as_view(), name='home_page'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_details'),
    #! the pk : primary key WE ONLY USE THE PRIMARY KEY
    
    path('new/', NewBlogView.as_view(),name='blog_new'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]
