from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from brew_shareapi.views import register_user, login_user
from brew_shareapi.views import EntryView, BrewMethodView, CoffeeView, BrewerView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'entries', EntryView, 'entry')
router.register(r'methods', BrewMethodView, 'method')
router.register(r'coffees', CoffeeView, 'coffee')
router.register(r'brewers', BrewerView, 'brewer')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-ath', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
