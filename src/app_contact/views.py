from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError

from app_contact.forms import ContactForm

# для клчей почты
from project_core import settings


class ContactFormView(FormView):
    """ Класс формы обратной связи """
    # FormView - базовый класс для форм не связанных с моделями
    form_class = ContactForm
    template_name = 'contact/contact/contact.html'
    success_url = reverse_lazy('home')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #    """ Добавляем мексины """
    #    context = super().get_context_data(**kwargs)  # получаем текущий контент
    #    c_def = self.get_user_context(title='Регистрация')
    #    return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        """ Отправка корректной формы """
        # print(form.cleaned_data)
        return redirect('home')


def contact_form_view(request):
    # если метод GET, вернем форму
    if request.method == 'GET':
        form = ContactForm()  # формируем пустую форму
    elif request.method == 'POST':
        # если метод POST, проверим форму и отправим письмо
        form = ContactForm(request.POST)  # формируем форму с заполненными данными
        if form.is_valid():
            # name = form.cleaned_data['name']
            # from_email = form.cleaned_data['from_email']
            # subject = form.cleaned_data['subject']
            # message = form.cleaned_data['message']

            subject = form.cleaned_data['subject']
            body = {
                'name': form.cleaned_data['name'],
                'from_email': form.cleaned_data['from_email'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                # send_mail(f'{subject} от {from_email}', message,
                #          settings.DEFAULT_FROM_EMAIL, settings.RECIPIENTS_EMAIL)
                send_mail(subject, message,
                          settings.DEFAULT_FROM_EMAIL,
                          settings.RECIPIENTS_EMAIL
                          )
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect('contact_form_sent')  # форма успешной отправки
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, "contact/contact/contact.html", {'form': form})


def contact_form_sent(request):
    return HttpResponse('Отправлено! Спасибо за вашу заявку.')

