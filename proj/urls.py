from django.urls import path

from app.views import index_view, check_view, result_view
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static


favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
style_view = RedirectView.as_view(url='/static/app/style.css', permanent=True)

urlpatterns = [
    path('', index_view, name='index'),
    path('check/', check_view, name='check'),
    path('favicon.ico', favicon_view, name='favicon'),
    path('static/style.css', favicon_view, name='favicon'),
    path('<url_str>', result_view, name='result'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
