"""cinema_app URL Configuration

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
    2. Add a URL to urlpatterns:  path('cinema/', include('cinema.urls'))
"""
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import CreateView

from cinema.forms import UserForm
from django.contrib.auth import views as auth_views

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_failure'

urlpatterns = [
    path('', include('cinema.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserForm,
            success_url=reverse_lazy('cinema:session_list')
        ),
        name='registration'
    ),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('pages/', include('pages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
        )

