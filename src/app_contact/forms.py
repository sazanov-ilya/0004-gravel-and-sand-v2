from django import forms
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    """ Класс формы обратной связи """
    name = forms.CharField(label='Имя', max_length=255, required=True)
    # email = forms.EmailField(label='Email')
    from_email = forms.EmailField(label='Email', required=True)
    subject = forms.CharField(label='Тема', required=True)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), required=True)
    captcha = CaptchaField()
