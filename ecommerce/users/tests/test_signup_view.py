import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestSignupView:
    def setup_method(self):
        self.signup_url = reverse('signup')
        self.home_url = reverse('home')

    def test_signup_view_get(self, client):
        response = client.get(self.signup_url)

        assert response.status_code == 200

    def test_successful_signup(self, client):
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
        }

        response = client.post(self.signup_url, payload)

        assert response.status_code == 302
        assert response.url == self.home_url
        assert User.objects.filter(username="testuser").exists()
    
    def test_password_mismatch(self, client):
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "password_confirm": "differentpassword123",
        }

        response = client.post(self.signup_url, payload, follow=True)

        assert response.status_code == 200
        assert "Passwords do not match." in response.content.decode()
        assert not User.objects.filter(username="testuser").exists()
    
    def test_signup_existing_username(self, client):
        User.objects.create_user(username="testuser", email="test@example1.com", password="testpassword123")

        payload = {
            "username": "testuser",
            "email": "test@example2.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
        }

        response = client.post(self.signup_url, payload, follow=True)

        assert response.status_code == 200
        assert "Username already taken." in response.content.decode()
        assert User.objects.filter(username="testuser").count() == 1
    
    def test_signup_existing_email(self, client):
        User.objects.create_user(username="testuser1", email="test@example.com", password="testpassword123")

        payload = {
            "username": "testuser2",
            "email": "test@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
        }

        response = client.post(self.signup_url, payload, follow=True)

        assert response.status_code == 200
        assert "Email already registered." in response.content.decode()
        assert User.objects.filter(email="test@example.com").count() == 1
    
    def test_signup_view_redirect_if_authenticated(self, client):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword123")

        client.force_login(user)

        response = client.get(self.signup_url)

        assert response.status_code == 302
        assert response.url == self.home_url