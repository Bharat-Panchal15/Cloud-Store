import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

@pytest.mark.django_db
class TestLoginView:
    def setup_method(self):
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.password = "testpassword123"
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password=self.password)

    def test_login_view_get(self, client):
        response = client.get(self.login_url)
        
        assert response.status_code == 200
    
    def test_successful_login(self, client):
        response = client.post(self.login_url, { "email": self.user.email, "password": self.password })

        assert response.status_code == 302
        assert response.url == self.home_url

    def test_login_invalid_credentials(self, client):
        response = client.post(self.login_url, { "email": self.user.email, "password": "wrongpassword" }, follow=True)

        assert response.status_code == 200
        assert "Invalid email or password." in response.content.decode()
    
    def test_authenticated_user_redirect(self, client):
        client.login(username=self.user.username, password=self.password)

        response = client.get(self.login_url)

        assert response.status_code == 302
        assert response.url == self.home_url