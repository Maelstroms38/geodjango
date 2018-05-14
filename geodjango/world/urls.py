from django.conf.urls import url
from .views import LookupView
urlpatterns = [
    # Lookup
    url(r'', LookupView.as_view(), name='lookup'),
]
