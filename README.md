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
