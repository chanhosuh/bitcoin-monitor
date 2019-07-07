"""bitcoin_monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from bitcoin_monitor import settings
from bitcoin_monitor.views import FrontendAppView
from blocks import views


# from django.views.generic.base import RedirectView


router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()
router.register(r'blocks', views.BlockViewSet)

urlpatterns = [
    # path('', RedirectView.as_view(url='tickers/')),
    path('admin/', admin.site.urls),
    # websocket price feeds
    path('tickers/', include('prices.urls')),
    # Django REST Framework
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', FrontendAppView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
