import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

@pytest.mark.django_db
class TestLogoutView:
    def setup_method(self):
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.login_url = reverse('login')
    
    def test_logout_clears_session_and_redirects(self, client):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword123")

        client.force_login(user)

        response = client.get(self.logout_url)

        assert response.status_code == 302
        assert response.url == self.home_url
        assert "_auth_user_id" not in client.session
    
    def test_logout_requires_authentication(self, client):
        response = client.get(self.logout_url)

        assert response.status_code == 302
        assert response.url.startswith(self.login_url)