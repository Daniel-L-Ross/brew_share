"""brew_share URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from brew_shareapi.views import EntryView, BrewMethodView, CoffeeView, BrewerView
# from brew_shareapi.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'entries', EntryView, 'entry')
router.register(r'methods', BrewMethodView, 'method')
router.register(r'coffees', CoffeeView, 'coffee')
router.register(r'brewers', BrewerView, 'brewer')

urlpatterns = [
    # path('register', register_user),
    # path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-ath', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
