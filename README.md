# Django Blog App : 
this web app is for learning purposes where we can divide the whole process into 11 chapters that will  be updated when i finish each one of them.

**this project was made by following the book `Django for Beginners` by `WILLIAM S. VINCENT`**
where you can but his book from [this link](https://djangoforbeginners.com/).

# 1. CHAPTER 1 : `GETTING STARTED`
in this chapter we just created our own app, where we used bunch of commands that are installed with django, but let's start this from the beginning :
## 1. installing django : 

for installing django we could simply use the following command : 
```python
pip install django
```
## 2. Initializing the project :

once django is installed, we can start the project by the commands : 
```python
django-admin startproject blog_app # this will initialize the project
python manage.py startapp blog # this  will create the mini-app in the django project `blog`
```
This will create our project and the app in it.
Once we did this, we need to update the settings file in the project directory : 
`./blog_app/settings.py`
where we update the apps included in the project to include the app we just created : 
```python
INSTALLED_APPS = [
    ...., # old apps
    'blog.apps.BlogConfig', # new app
]
```
Next in our app application is to run the migrations and make them happen for that we execute : 
```powershell
python manage.py runmigrations # this will run the migrations to update all the necessary database file
python manage.py migrate # and finally migrate all the migrations and do the update
```
now we can start creating the app.

## 3. Creating the templates : 
For inserting the templates we need to create a template folder in the project, for that we use : 
```powershell
mkdir templates
touch home.html
touch base.html
```

and then we need just to include the template folder in the project setting : 
```python
# in the : ./blog_app/settings.py file
TEMPLATES = [
    {
        ...,
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # this is the important line in here
        ....,
    },
]
```

now we create our templates that are `home.html` for the menu of the blogs, and `blog_detail.html` for the details of one selected blog.

*the `base.html` is a just for extending the files and templates from it so i can keep the same format*

We can see the architecture of our project like this : 
```powershell
.
├── blog
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── blog_app
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
├── README.md
└── templates
    ├── base.html
    ├── blog_detail.html
    └── home.html

```

and then we need to update our `urls.py` and `views.py` files in the blog app folder.
```python
# in the : ./blog/views.py file
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import BlogModel

class BlogListView(ListView):
    model = BlogModel
    template_name = "home.html"
    context_object_name = "blogsList"
    
class BlogDetailView(DetailView):
    model = BlogModel
    template_name = "blog_detail.html"
    context_object_name = "blog"
```

```python
# in the : ./blog/urls.py file
from django.urls import path
from .views import *

urlpatterns = [
    path('', BlogListView.as_view(), name='home_page'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_details'),
]
#------------------------------------------------------------------------
# in the : ./blog_app/urls.py file
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls'))
]
```

**But what is this model thing ?**
lets answer this question in the next step : 
## 4. Models : 
the models are the way django understands the database with, as it uses `ORM (object-relational-mapping)`. 

It makes it easy to manipulate and use the database.
we simply define the models we are going to use in the apps, and they will be included automatically in the project as the app is included in the `settings.py` file.

in our project we need 2 models : 
- Model for Blogs
- Model for Users

that are both included in the `models.py` file
```python
from django.db import models

# Create your models here.


class BlogModel(models.Model):
    title = models.CharField(max_length=20)
    body = models.TextField()
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.title
```
as for the users they are included by default in django (you need to love django for this).

and this will give us access to all the models **we import** from the admin menu in the web app :
```python
from django.contrib import admin

from .models import BlogModel
admin.site.register(BlogModel)
```

## 5. Everything Working together :
Now we need to only fill our html files, and see the magic happens : 
for this i used **Class View Templates** to create my views, as you can see [above](#3-creating-the-templates-)

we only need to show include the views in the html files : for this you can check and copy the code of the folder `templates` in my repository.

# CHAPTER 2 : `FORMS`
in this chapter we will integrate forms in our application, this will give the possibility to **create**, **update** and **delete** blogs from ou app.

## 1. Updating the URLS :
for this we will create a url for each operation that we will perform, resulting in a code like this :
```python
# in the file : ./blog/urls.py

urlpatterns = [
    ...    
    path('new/', NewBlogView.as_view(),name='blog_new'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]
```

this code will not work until we create the views that are for each url

## 2. Updating the views : 
With django updating the views is really easy, as it gives us the possibility to implement already built-in views for the purposes of updating, creating and deleting posts (blogs).
```python
# in the file : ./blog/views.py

from django.views.generic import DeleteView, CreateView, UpdateView
```

then we implement the views each with its class inherited from the views imported : 
```python
class NewBlogView(CreateView):
    model = BlogModel
    template_name = "new_blog.html"
    fields = ['title', 'body', 'author']
    
class BlogUpdateView(UpdateView):
    model = BlogModel
    template_name = "update_blog.html"
    fields = ['title', 'body']
    
class BlogDeleteView(DeleteView):
    model = BlogModel
    template_name = "delete_blog.html"
    context_object_name = "blog"
    success_url = reverse_lazy('home_page')
```

let's explain each of the classes : 
- **NewBlogView :** is for creating a new blog, where the fields that will be in the form are `['title', 'body', 'author']` and will automatically be added to the `BlogModel` 

- **BlogUpdateView :** is for updating a blog, where the fields that will *can* be updated are `['title', 'body']` and will automatically be added to the `BlogModel` with the **id** that is selected in the url
`update/*<int:pk>*/`

- **BlogDeleteView :** is for deleting a blog, where we can see it doesn't require any field, but a **success_url** where it will redirect the user after the successful delete of a blog with the **id** that is selected in the url : `delete/*<int:pk>*/`

## 3. Adding the templates : 
After adding the templates for each view, we will end up with these files in the templates directory :
```powershell
templates/
├── base.html
├── blog_detail.html
├── delete_blog.html
├── home.html
├── new_blog.html
└── update_blog.html
```
for the templates the good part is that we can add directly the forms generated by **django** by using just a small piece of code : 
```html
<form action="" method="POST">
    {% csrf_token %} 
    {{ form.as_p }}
    <!-- this will import the form parameters and fields -->
    <input type="submit" value="Add Blog">
</form>
```
this same code will be used for adding a new blog and update an existing blog *(there will be some diferences in the submit context only)*

As for the delete template, we only need a form of **confirmation** of the delete, in this case we only need a simple form : 
```html
<form action="" method="POST">
    {% csrf_token %}
        <p>Are you sure you want to delete the post {{blog.title}}</p>
        <input type="submit" value="Confirm">
</form>
```

to resume how the forms work we can just say :
- **Creating new blog :** go to URL of adding ➔ filling the form ➔ automatically adding the blog
- **updating the blog :** selecting the blog to update ➔ updating the fields desired ➔ automatic update by **Django**
- **Deleting a blog :** select the blog to delete ➔ confirmation of delete ➔ redirecting to home page