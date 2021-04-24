from django.test import TestCase
from django.contrib.auth.models import User
import time
from .models import *

# django_code_coverage = '23.5% coverage'

# Create your tests here.
class UserTestCase(TestCase):
    def test_simple(self):
        self.assertEqual(1 + 1, 2)
    
    def test_unknown_url(self):
        response = self.client.get('/incorrect')
        self.assertEqual(response.status_code, 404)

    def test_without_users(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        })

    def test_list_users_with_users_usernames(self):
        User.objects.create(username='Kelly')
        User.objects.create(username='John')
        response = self.client.get('/v1/users/')  
        self.assertEqual(response.status_code, 200)
        usernames = {row['username'] for row in response.json()['results']} # Куча
        self.assertEqual(usernames, {'John', 'Kelly'})
        #self.assertEqual(usernames, {'Kelly', 'Kelly'})


    def test_list_users_with_users(self):
        User.objects.create(username='Kelly')
        time.sleep(0.01)
        User.objects.create(username='John')
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        'email': '',
                        'first_name': '',
                        'last_name': '',
                        'url': 'http://testserver/v1/users/John/',
                        'username': 'John'
                    },
                    {
                        'email': '',
                        'first_name': '',
                        'last_name': '',
                        'url': 'http://testserver/v1/users/Kelly/',
                        'username': 'Kelly'
                    }
                ]
            }
        )


class FollowTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='Kevin')
        self.user2 = User.objects.create(username='Tom')
        self.user3 = User.objects.create(username='Mo')
        Follow.objects.create(follower=self.user1, follows=self.user2)
    
    def test_data_exist(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Follow.objects.count(), 1)

    def test_new_follow_correct(self):
        self.client.force_login(self.user1)
        responce = self.client.post(f'/v1/follow/{self.user3.username}/')
        self.assertEqual(responce.status_code, 201)
        self.assertEqual(Follow.objects.count(), 2)
        
        self.assertIsNotNone(Follow.objects.get(
            follower=self.user1,
            follows=self.user3,
         ))
    
    def test_unfollow_correct(self):
        self.client.force_login(self.user1)
        responce = self.client.delete(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(responce.status_code, 204)
        self.assertEqual(Follow.objects.count(), 0)

    def test_follow_dublicated_failed(self):
        self.client.force_login(self.user1)
        self.assertEqual(Follow.objects.count(), 1)
        responce = self.client.post(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(responce.status_code, 201)
        self.assertEqual(Follow.objects.count(), 1)

    def test_follow_yourself_failed(self):
        self.client.force_login(self.user1)
        responce = self.client.post(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(responce.status_code, 400)

    def test_unfollow_not_exist_return_fail(self):
        self.client.force_login(self.user1)
        responce = self.client.delete(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(responce.status_code, 400)