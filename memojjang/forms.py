from django import forms
from django.contrib.auth.forms import UserCreationForm
from .apps.users.models import User
from .apps.memos.models import Memo


class MemoForm(forms.ModelForm):
    """메모 작성 및 수정을 위한 폼"""
    
    class Meta:
        model = Memo
        fields = ["title", "content", "reminder_date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "reminder_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local"
                }
            ),
        }


class UserRegistrationForm(UserCreationForm):
    """사용자 회원가입을 위한 폼"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"