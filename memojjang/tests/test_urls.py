from django.test import TestCase
from django.urls import reverse, resolve
from memojjang.apps.memos.views import (
    home, memo_list, memo_create, memo_detail, memo_edit, memo_delete,
    login_view, logout_view, register
)


class TestUrls(TestCase):
    """URL 패턴 테스트"""

    def test_home_url_resolves(self):
        """홈 URL 테스트"""
        url = reverse("home")
        self.assertEqual(resolve(url).func, home)

    def test_memo_list_url_resolves(self):
        """메모 목록 URL 테스트"""
        url = reverse("memo_list")
        self.assertEqual(resolve(url).func, memo_list)

    def test_memo_create_url_resolves(self):
        """메모 생성 URL 테스트"""
        url = reverse("memo_create")
        self.assertEqual(resolve(url).func, memo_create)

    def test_memo_detail_url_resolves(self):
        """메모 상세 URL 테스트"""
        url = reverse("memo_detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, memo_detail)

    def test_memo_edit_url_resolves(self):
        """메모 수정 URL 테스트"""
        url = reverse("memo_edit", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, memo_edit)

    def test_memo_delete_url_resolves(self):
        """메모 삭제 URL 테스트"""
        url = reverse("memo_delete", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, memo_delete)

    def test_login_url_resolves(self):
        """로그인 URL 테스트"""
        url = reverse("login")
        self.assertEqual(resolve(url).func, login_view)

    def test_logout_url_resolves(self):
        """로그아웃 URL 테스트"""
        url = reverse("logout")
        self.assertEqual(resolve(url).func, logout_view)

    def test_register_url_resolves(self):
        """회원가입 URL 테스트"""
        url = reverse("register")
        self.assertEqual(resolve(url).func, register)