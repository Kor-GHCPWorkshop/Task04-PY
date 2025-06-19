from django.db import models
from django.conf import settings


class Memo(models.Model):
    """메모 모델
    
    사용자가 작성한 메모를 저장하는 모델입니다.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memos"
    )
    title = models.TextField(
        verbose_name="제목"
    )
    content = models.TextField(
        verbose_name="내용"
    )
    created_at = models.DateTimeField(
        verbose_name="작성일시",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="수정일시",
        auto_now=True
    )
    reminder_date = models.DateTimeField(
        verbose_name="리마인드 일시",
        null=True,
        blank=True,
        help_text="메모를 리마인드 받을 날짜와 시간"
    )
    is_reminded = models.BooleanField(
        verbose_name="리마인드 완료",
        default=False,
        help_text="리마인드가 완료되었는지 여부"
    )

    class Meta:
        """메모 모델 메타 클래스"""
        db_table = "memos"
        ordering = ["-created_at"]
        verbose_name = "메모"
        verbose_name_plural = "메모들"

    def __str__(self):
        """메모 제목을 문자열로 반환"""
        return self.title
