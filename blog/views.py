from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import BlogModel

class BlogListView(ListView):
    model = BlogModel
    template_name = "home.html"
    context_object_name = "blogsList"
    
class BlogDetailView(DetailView):
    model = BlogModel
    template_name = "blog_detail.html"
    context_object_name = "blog"
    
class NewBlogView(CreateView):
    model = BlogModel
    template_name = "new_blog.html"
    fields = ['title', 'body', 'author']    # this will specify the fields that will be included in the form
    
class BlogUpdateView(UpdateView):
    model = BlogModel
    template_name = "update_blog.html"
    fields = ['title', 'body']
    
class BlogDeleteView(DeleteView):
    model = BlogModel
    template_name = "delete_blog.html"
    context_object_name = "blog"
    success_url = reverse_lazy('home_page')