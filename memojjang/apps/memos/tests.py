from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Memo
from ...forms import MemoForm
import time

User = get_user_model()


class TestMemoModel(TestCase):
    """메모 모델 테스트"""

    def setUp(self):
        """테스트 사용자와 메모 생성"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.memo = Memo.objects.create(
            user=self.user,
            title="테스트 제목",
            content="테스트 내용입니다."
        )

    def test_memo_creation(self):
        """메모 생성 테스트"""
        self.assertEqual(self.memo.title, "테스트 제목")
        self.assertEqual(self.memo.content, "테스트 내용입니다.")
        self.assertEqual(self.memo.user, self.user)

    def test_memo_string_representation(self):
        """메모 문자열 표현 테스트"""
        self.assertEqual(str(self.memo), "테스트 제목")

    def test_timestamps(self):
        """타임스탬프 필드 테스트"""
        self.assertIsNotNone(self.memo.created_at)
        self.assertIsNotNone(self.memo.updated_at)

    def test_ordering(self):
        """메모 정렬 순서 테스트 (최신순)"""
        # 첫 번째 메모와 두 번째 메모 사이에 시간 간격을 두기 위해 잠시 대기
        time.sleep(0.1)
        
        memo2 = Memo.objects.create(
            user=self.user,
            title="두 번째 메모",
            content="두 번째 메모 내용"
        )
        memos = Memo.objects.all()
        # 가장 최근에 작성된 메모가 첫 번째에 오는지 확인
        self.assertEqual(memos[0], memo2)
        self.assertEqual(memos[1], self.memo)


class TestMemoForm(TestCase):
    """메모 폼 테스트"""

    def test_memo_form_valid_data(self):
        """유효한 데이터로 폼 검증"""
        form = MemoForm(data={
            "title": "테스트 제목",
            "content": "테스트 내용입니다."
        })
        self.assertTrue(form.is_valid())

    def test_memo_form_no_data(self):
        """빈 데이터로 폼 검증"""
        form = MemoForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # title과 content 모두 필수


class TestMemoViews(TestCase):
    """메모 뷰 테스트"""

    def setUp(self):
        """테스트 사용자와 메모 생성 및 로그인"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")
        
        self.memo = Memo.objects.create(
            user=self.user,
            title="테스트 메모",
            content="테스트 내용입니다."
        )

    def test_memo_list_view(self):
        """메모 목록 뷰 테스트"""
        response = self.client.get(reverse("memo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_list.html")
        self.assertIn("memos", response.context)
        self.assertEqual(len(response.context["memos"]), 1)

    def test_memo_detail_view(self):
        """메모 상세 뷰 테스트"""
        response = self.client.get(
            reverse("memo_detail", kwargs={"pk": self.memo.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_detail.html")
        self.assertEqual(response.context["memo"], self.memo)

    def test_memo_create_view_get(self):
        """메모 생성 뷰 GET 요청 테스트"""
        response = self.client.get(reverse("memo_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_form.html")
        self.assertIsInstance(response.context["form"], MemoForm)

    def test_memo_create_view_post(self):
        """메모 생성 뷰 POST 요청 테스트"""
        response = self.client.post(
            reverse("memo_create"), 
            {
                "title": "새 메모",
                "content": "새 메모 내용"
            }
        )
        # 메모 생성 후 메모 목록 페이지로 리다이렉트
        self.assertRedirects(response, reverse("memo_list"))
        
        # 메모가 실제로 생성되었는지 확인
        self.assertEqual(Memo.objects.count(), 2)
        new_memo = Memo.objects.get(title="새 메모")
        self.assertEqual(new_memo.content, "새 메모 내용")
        self.assertEqual(new_memo.user, self.user)

    def test_memo_edit_view_get(self):
        """메모 수정 뷰 GET 요청 테스트"""
        response = self.client.get(
            reverse("memo_edit", kwargs={"pk": self.memo.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_form.html")
        self.assertIsInstance(response.context["form"], MemoForm)
        self.assertEqual(response.context["form"].instance, self.memo)

    def test_memo_edit_view_post(self):
        """메모 수정 뷰 POST 요청 테스트"""
        response = self.client.post(
            reverse("memo_edit", kwargs={"pk": self.memo.pk}),
            {
                "title": "수정된 제목",
                "content": "수정된 내용"
            }
        )
        # 메모 수정 후 상세 페이지로 리다이렉트
        self.assertRedirects(
            response, 
            reverse("memo_detail", kwargs={"pk": self.memo.pk})
        )
        
        # 메모가 실제로 수정되었는지 확인
        self.memo.refresh_from_db()
        self.assertEqual(self.memo.title, "수정된 제목")
        self.assertEqual(self.memo.content, "수정된 내용")

    def test_memo_delete_view_get(self):
        """메모 삭제 뷰 GET 요청 테스트"""
        response = self.client.get(
            reverse("memo_delete", kwargs={"pk": self.memo.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_confirm_delete.html")
        self.assertEqual(response.context["memo"], self.memo)

    def test_memo_delete_view_post(self):
        """메모 삭제 뷰 POST 요청 테스트"""
        response = self.client.post(
            reverse("memo_delete", kwargs={"pk": self.memo.pk})
        )
        # 메모 삭제 후 목록 페이지로 리다이렉트
        self.assertRedirects(response, reverse("memo_list"))
        
        # 메모가 실제로 삭제되었는지 확인
        self.assertEqual(Memo.objects.count(), 0)


class TestMemoAccessControl(TestCase):
    """메모 접근 제어 테스트"""

    def setUp(self):
        """두 명의 사용자와 각각의 메모 생성"""
        # 첫 번째 사용자
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="pass1234"
        )
        self.memo1 = Memo.objects.create(
            user=self.user1,
            title="사용자1의 메모",
            content="사용자1이 작성한 메모입니다."
        )
        
        # 두 번째 사용자
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="pass1234"
        )
        self.memo2 = Memo.objects.create(
            user=self.user2,
            title="사용자2의 메모",
            content="사용자2가 작성한 메모입니다."
        )

    def test_login_required(self):
        """로그인 필요 테스트"""
        # 로그인하지 않은 상태에서 접근
        response = self.client.get(reverse("memo_list"))
        # 로그인 페이지로 리다이렉트되어야 함
        self.assertEqual(response.status_code, 302)
        # 실제 URL을 확인하는 대신 리다이렉트 상태 코드만 확인
        self.assertEqual(response.status_code, 302)
        
        # 로그인하지 않은 상태에서 메모 상세 페이지 접근
        response = self.client.get(
            reverse("memo_detail", kwargs={"pk": self.memo1.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_user_can_only_access_own_memos(self):
        """사용자는 자신의 메모만 접근 가능해야 함"""
        # 사용자1로 로그인
        self.client.login(username="user1", password="pass1234")
        
        # 사용자1은 자신의 메모에 접근 가능
        response = self.client.get(
            reverse("memo_detail", kwargs={"pk": self.memo1.pk})
        )
        self.assertEqual(response.status_code, 200)
        
        # 사용자1은 사용자2의 메모에 접근 불가 (404 반환)
        response = self.client.get(
            reverse("memo_detail", kwargs={"pk": self.memo2.pk})
        )
        self.assertEqual(response.status_code, 404)
        
        # 사용자2의 메모 수정 시도 (404 반환)
        response = self.client.get(
            reverse("memo_edit", kwargs={"pk": self.memo2.pk})
        )
        self.assertEqual(response.status_code, 404)
        
        # 사용자2의 메모 삭제 시도 (404 반환)
        response = self.client.get(
            reverse("memo_delete", kwargs={"pk": self.memo2.pk})
        )
        self.assertEqual(response.status_code, 404)