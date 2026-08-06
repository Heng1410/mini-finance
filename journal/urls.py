from django.urls import include, path
from rest_framework import routers

from journal.views.journal_entry_view_set import JournalEntryViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"journals", JournalEntryViewSet)

urlpatterns = [path("", include(router.urls))]
