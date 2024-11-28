"""
URL configuration for meu_crud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from produtos import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.listar_produtos, name='listar_produtos'),  # Página de lista de produtos
    path('admin/', admin.site.urls),
    path('produtos/', include('produtos.urls')),  # Suas URLs do app produtos
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login padrão do Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),  # Página de cadastro
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'django.views.defaults.page_not_found'  # Manipulador padrão para 404
handler500 = 'django.views.defaults.server_error'    # Manipulador padrão para 500