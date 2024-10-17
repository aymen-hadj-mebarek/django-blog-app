from django.shortcuts import render
from django.views.generic import ListView, DetailView
# Create your views here.

from .models import BlogModel

class BlogListView(ListView):
    model = BlogModel
    template_name = "home.html"
    context_object_name = "blogsList"
    
class BlogDetailView(DetailView):
    model = BlogModel
    template_name = "blog_detail.html"
    context_object_name = "blog"