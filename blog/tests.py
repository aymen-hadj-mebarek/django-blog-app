from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import BlogModel

# Create your tests here.
class BlogTests(TestCase):
    def setUp(self):
        #! for creating a fake user 
        self.user = get_user_model().objects.create_user(
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
    def test_blog_list_view_logged_in(self):
        #! Log in the user first
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home_page'))
        # response = self.client.get('/blog/') 
        
        #? we start by comparing the status code : 200 means the page exists
        self.assertEqual(response.status_code, 200)
        #? then we check the template used in this page
        self.assertTemplateUsed(response, "home.html")
        #? finally we check if a title of the blog is in the page
        self.assertContains(response, self.blog)
        
    def test_blog_list_view_logged_out(self):
        response = self.client.get(reverse('home_page'))
        
        #? we start by comparing the status code : 200 means the page exists
        self.assertEqual(response.status_code, 200)
        #? then we check the template used in this page
        self.assertTemplateUsed(response, "home.html")
        #? finally we check if a title of the blog is in the page
        self.assertNotContains(response, self.blog)
        self.assertContains(response, "You need to log in from")
        
    
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
        
    def test_get_absolute_url(self):
        self.assertEqual(self.blog.get_absolute_url(), '/blog/1/') 
        
    def test_blog_create_view(self):
        #! when testing a post form we use post with the infos we are going to post in the form
        response = self.client.post(reverse('blog_new'), {
            'title': 'new blog',
            'body': 'this is the body of test blog',
            'author': self.user
        })
        self.assertEqual(response.status_code, 200)
        # testing that the url exists
        # testing that the right things are placed : 
        self.assertContains(response, 'new blog')
        self.assertContains(response, 'this is the body of test blog')
        
    def test_blog_update_view(self):
        response = self.client.post(reverse('blog_update', args='1'), {
            'title': 'updated blog',
            'body': 'this is the updated body of test blog',
        })
        self.assertEqual(response.status_code, 302)   # 302 means redirected to a new page
        self.assertEqual(BlogModel.objects.get(pk=1).title, 'updated blog')
        
    def test_blog_delete_view(self):
        response = self.client.post(reverse('blog_delete', args='1'))
        self.assertEqual(response.status_code, 302)   # 302 means redirected to a new page
        self.assertFalse(BlogModel.objects.filter(pk=self.blog.id).exists()) # this should check that the database is empty now
        
    def test_logging_in(self):
        response = self.client.post(reverse('login'),{'username':"testuser", 'password':"testpassword"})
        self.assertEqual(response.status_code, 302) 
        self.assertTemplateUsed("login.html")
        self.assertTemplateUsed("home.html")
        
    def test_signin_up(self):
        response = self.client.post(reverse('sign_up'),{'username':"test2user", 'password':"test2password", 'password2':"test2password"})
        
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed("signup.html")
        self.assertTemplateUsed("home.html")
        