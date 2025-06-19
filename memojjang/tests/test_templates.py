from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from memojjang.apps.memos.models import Memo

User = get_user_model()


class TestTemplates(TestCase):
    """템플릿 렌더링 테스트"""

    def setUp(self):
        """테스트 사용자와 메모 생성"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.memo = Memo.objects.create(
            user=self.user,
            title="테스트 메모",
            content="테스트 내용입니다."
        )

    def test_home_template(self):
        """홈 템플릿 테스트"""
        # 로그인하지 않은 상태
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "메모짱~!")
        self.assertContains(response, "로그인하기")
        self.assertContains(response, "회원가입")
        
        # 로그인한 상태
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "메모 작성하기")
        self.assertNotContains(response, "로그인하기")

    def test_memo_list_template(self):
        """메모 목록 템플릿 테스트"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("memo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_list.html")
        self.assertContains(response, "나의 메모 목록")
        self.assertContains(response, "테스트 메모")
        self.assertContains(response, "새 메모 작성")

    def test_memo_detail_template(self):
        """메모 상세 템플릿 테스트"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("memo_detail", kwargs={"pk": self.memo.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_detail.html")
        self.assertContains(response, "테스트 메모")
        self.assertContains(response, "테스트 내용입니다.")
        self.assertContains(response, "수정")
        self.assertContains(response, "삭제")

    def test_memo_form_template(self):
        """메모 폼 템플릿 테스트"""
        self.client.login(username="testuser", password="testpass123")
        
        # 메모 생성 폼
        response = self.client.get(reverse("memo_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_form.html")
        self.assertContains(response, "새 메모 작성")
        
        # 메모 수정 폼
        response = self.client.get(
            reverse("memo_edit", kwargs={"pk": self.memo.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_form.html")
        self.assertContains(response, "메모 수정")

    def test_memo_delete_template(self):
        """메모 삭제 확인 템플릿 테스트"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("memo_delete", kwargs={"pk": self.memo.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_confirm_delete.html")
        self.assertContains(response, "정말로 이 메모를 삭제하시겠습니까?")

    def test_login_template(self):
        """로그인 템플릿 테스트"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")
        self.assertContains(response, "로그인")
        self.assertContains(response, "사용자 이름")
        self.assertContains(response, "비밀번호")
        self.assertContains(response, "회원가입")

    def test_register_template(self):
        """회원가입 템플릿 테스트"""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertContains(response, "회원가입")
        self.assertContains(response, "이미 계정이 있으신가요?")