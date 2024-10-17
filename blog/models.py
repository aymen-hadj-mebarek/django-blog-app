from django.db import models

# Create your models here.


class BlogModel(models.Model):
    title = models.CharField(max_length=20)
    body = models.TextField()
    author = models.ForeignKey(
        'auth.User',                #! this is the foreing class that is associated to the foreign key
        on_delete=models.CASCADE    #! this will specify that when the user is deleted the blog will be deleted too 
    )
    
    def __str__(self):
        return self.title
    
    