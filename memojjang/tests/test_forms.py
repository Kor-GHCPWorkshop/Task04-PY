from django.test import TestCase
from memojjang.forms import MemoForm, UserRegistrationForm
from memojjang.apps.users.models import User


class TestMemoForm(TestCase):
    """메모 폼 테스트"""

    def test_memo_form_valid_data(self):
        """유효한 데이터로 폼 검증"""
        form = MemoForm(data={
            "title": "테스트 제목",
            "content": "테스트 내용"
        })
        self.assertTrue(form.is_valid())

    def test_memo_form_empty_title(self):
        """제목이 없는 경우 폼 검증"""
        form = MemoForm(data={
            "content": "테스트 내용"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_memo_form_empty_content(self):
        """내용이 없는 경우 폼 검증"""
        form = MemoForm(data={
            "title": "테스트 제목"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_memo_form_widgets(self):
        """폼의 위젯 속성 테스트"""
        form = MemoForm()
        self.assertEqual(form.fields["title"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["content"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["content"].widget.attrs["rows"], 5)


class TestUserRegistrationForm(TestCase):
    """사용자 등록 폼 테스트"""

    def setUp(self):
        """기존 사용자 생성"""
        self.existing_user = User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="password123"
        )

    def test_form_valid_data(self):
        """유효한 데이터로 폼 검증"""
        form = UserRegistrationForm(data={
            "username": "newuser",
            "email": "new@example.com",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123"
        })
        self.assertTrue(form.is_valid())

    def test_form_password_mismatch(self):
        """비밀번호 불일치 검증"""
        form = UserRegistrationForm(data={
            "username": "newuser",
            "email": "new@example.com",
            "password1": "ComplexPass123",
            "password2": "DifferentPass123"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_username_exists(self):
        """이미 존재하는 사용자명 검증"""
        form = UserRegistrationForm(data={
            "username": "existinguser", # 이미 존재하는 사용자명
            "email": "new@example.com",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_css_classes(self):
        """폼 필드의 CSS 클래스 테스트"""
        form = UserRegistrationForm()
        for field_name in ["username", "email", "password1", "password2"]:
            self.assertEqual(form.fields[field_name].widget.attrs["class"], "form-control")