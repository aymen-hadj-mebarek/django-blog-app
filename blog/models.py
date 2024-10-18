from django.db import models
from django.urls import reverse

# Create your models here.


class BlogModel(models.Model):
    title = models.CharField(max_length=20)
    body = models.TextField()
    author = models.ForeignKey(
        'auth.User',                #! this is the foreing class that is associated to the foreign key
        on_delete=models.CASCADE    #! this will specify that when the user is deleted the blog will be deleted too 
    )
    
    #? this will be sent automatically after creating a new blog
    #? this is a used method that saves a lot of work where it specifies where to send, and what to send
    def get_absolute_url(self):
        return reverse("blog_details", args=[self.id])
        #! django recommend using self.id rather than self.pk
    
    
    def __str__(self):
        return self.title
    
    