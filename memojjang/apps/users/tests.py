from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import User


class TestUserModel(TestCase):
    """사용자 모델 테스트"""

    def setUp(self):
        """테스트에 필요한 사용자 생성"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

    def test_user_creation(self):
        """사용자 생성이 올바르게 이루어지는지 테스트"""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_user_string_representation(self):
        """사용자 문자열 표현 테스트"""
        self.assertEqual(str(self.user), "testuser")

    def test_timestamps(self):
        """타임스탬프 필드 테스트"""
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)


class TestUserAuthentication(TestCase):
    """사용자 인증 기능 테스트"""

    def setUp(self):
        """테스트 사용자 생성"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.login_url = reverse("login")
        self.register_url = reverse("register")
        self.logout_url = reverse("logout")

    def test_register_page_loads(self):
        """회원가입 페이지가 로드되는지 테스트"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_user_registration(self):
        """회원가입 기능이 올바르게 작동하는지 테스트"""
        user_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "securepass123",
            "password2": "securepass123"
        }
        response = self.client.post(self.register_url, user_data)
        
        # 회원가입 후 메모 목록 페이지로 리다이렉트 되어야 함
        self.assertRedirects(response, reverse("memo_list"))
        
        # 사용자가 실제로 생성되었는지 확인
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_page_loads(self):
        """로그인 페이지가 로드되는지 테스트"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_success(self):
        """로그인 성공 테스트"""
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertRedirects(response, reverse("memo_list"))
        
        # 로그인 상태 확인
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_failure(self):
        """로그인 실패 테스트"""
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 200)  # 다시 로그인 페이지로
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        """로그아웃 기능 테스트"""
        # 먼저 로그인
        self.client.login(username="testuser", password="testpass123")
        
        # 로그아웃
        response = self.client.get(self.logout_url)
        
        # 로그아웃 후 홈페이지로 리다이렉트
        self.assertRedirects(response, reverse("home"))
        
        # 로그아웃 상태 확인
        self.assertFalse(response.wsgi_request.user.is_authenticated)