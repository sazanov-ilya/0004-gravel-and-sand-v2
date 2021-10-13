"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app_order.views import home, page_not_found
from project_core import settings

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    # url('', include('social_django.urls', namespace='social')),
    path('orders/', include('app_order.urls')),  # http://127.0.0.1:8000/orders/
    path('users/', include('app_users.urls')),  # http://127.0.0.1:8000/users/
    path('contact/', include('app_contact.urls')),  # http://127.0.0.1:8000/contact/
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # В режиме отладки подгружаем медиафайлы
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found  # старница не найдена
# handler500 = page_not_found  # ошибка сервера
# handler403 = page_not_found  # доступ запрещен
# handler400 = page_not_found  # невозможно обработать запрос


