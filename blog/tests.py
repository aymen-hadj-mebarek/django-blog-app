from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import BlogModel

# Create your tests here.
class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username= 'testuser',
            email= 'testuser@example.com',
            password= 'testpassword'
        )        
        self.blog = BlogModel.objects.create(
            title='the test blog',
            body='the blog of today is about a little thing',
            author=self.user
        )        
        
    #* we start by testing the representation of the blog
    def test_string_representation(self):
        represntation = BlogModel(pk=1)
        self.assertEqual(str(represntation), represntation.title)
        
    #* we test the content of the blog
    def test_blog_content(self):
        self.assertEqual(self.blog.title, "the test blog")
        self.assertEqual(self.blog.body, "the blog of today is about a little thing")
        self.assertEqual(self.blog.author, self.user)
        
    #* now we test the post list view
    #? in this we are going to test the view, that it exists and has the correct data, and the correct template
    def test_blog_list_view(self):
        response = self.client.get(reverse('home_page'))
        # response = self.client.get('/blog/') 
        
        #? we start by comparing the status code : 200 means the page exists
        self.assertEqual(response.status_code, 200)
        #? then we check the template used in this page
        self.assertTemplateUsed(response, "home.html")
        #? finally we check if a title of the blog is in the page
        self.assertContains(response, self.blog)
        
    
    #* now we test the post detail view (i will tempte to do this myself)
    def test_blog_detail_view(self):
        response = self.client.get('/blog/1/')
        # we start by the response status code
        self.assertEqual(response.status_code, 200)
        # the we make sure the right template is used 
        self.assertTemplateUsed(response, "blog_detail.html")
        self.assertTemplateUsed(response, "base.html")      #! this will check if the base template is used 
        self.assertTemplateNotUsed(response, "home.html")   #! this will detect if we used a non necessary template
        # now we check the content of the page
        self.assertContains(response, self.blog)
        
        #! in the tutorial, it did somethin interesting 
        no_response = self.client.get('/blog/10000/')    # he created a blog that doesnt exist to check its status code
        self.assertEqual(no_response.status_code, 404)
        