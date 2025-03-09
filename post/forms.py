from django import forms
from .models import Post, Comment
from captcha.fields import ReCaptchaField


class PostForm(forms.ModelForm):
    recaptcha = ReCaptchaField()

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'image',
        ]
class CommentForm(forms.ModelForm):
    recaptcha = ReCaptchaField()

    class Meta:
            model = Comment
            fields = [
                'name',
                'content',
            ]