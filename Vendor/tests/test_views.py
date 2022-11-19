from django.test import TestCase
from django.urls import reverse 

class TestView(TestCase):

    def test_show_reg_page(self):
        response=self.client.get(reverse('register'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"accounts/register.html")

    def test_show_index_page(self):
        response=self.client.get(reverse('index'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"restaurant/index.html")

    def test_show_login_page(self):
        response=self.client.get(reverse('login'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"accounts/login.html")

    def test_should_register_user(self):
        self.user = {
            "email":"testcase1@gmail.com",
            "firstname":"test1case",
            "lastname":"case",
            "password":"password",
            "confirmpass":"password",
            "address":"addres89 jjjs",
            "contact":"99989987890"
        }

        response = self.client.post(reverse("register"),self.user)
        self.assertEquals(response.status_code,302)
        
    def test_should_login_user(self):
        self.user = {
            "username":"test1",
            "password":"test1"  
        }
        response = self.client.post(reverse("login"),self.user)
        self.assertEquals(response.status_code,302)

        
    '''def test_should_not_register(self):
        self.user = {
            "email":"testcase1@gmail.com",
            "firstname":"test1case",
            "lastname":"case",
            "password":"password",
            "confirmpass":"password",
            "address":"addres89 jjjs",
            "contact":"99989987890"
        }
        self.user2 = {
            "email":"testcase1@gmail.com",
            "firstname":"test1case",
            "lastname":"case",
            "password":"password",
            "confirmpass":"password",
            "address":"addres89 jjjs",
            "contact":"99989987890"
        }
       
        self.client.post(reverse("register"),self.user)
        response = self.client.post(reverse("register"),self.user2)
        self.assertEquals(response.status_code,409)
'''
