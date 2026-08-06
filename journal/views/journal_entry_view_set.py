from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers

from base.views.company_base_view_set import CompanyBaseViewSet
from journal.constants import JournalStatus
from journal.models.journal_entry import JournalEntry
from journal.serializers.journal_entry_serializer import (
    JournalEntryDetailSerializer,
    JournalEntryListSerializer,
    JournalEntrySerializer,
)
from journal.serializers.post_journal_serializer import PostJournalSerializer


# Create your views here.
class JournalEntryViewSet(CompanyBaseViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related("lines")

    def get_serializer_class(self):
        if self.action == "list":
            return JournalEntryListSerializer

        if self.action == "retrieve":
            return JournalEntryDetailSerializer

        if self.action == "post":
            return PostJournalSerializer

        return JournalEntrySerializer

    def perform_destroy(self, instance):
        if instance.status == JournalStatus.POSTED:
            raise serializers.ValidationError(
                {"details": ["Posted journals cannot be deleted."]}
            )

        super().perform_destroy(instance)

    @action(detail=True, methods=["post"])
    def post(self, request, *args, **kwargs):
        journal = self.get_object()
        serializer = self.get_serializer(
            data=request.data, context={"journal": journal, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        journal = serializer.save()

        return Response(JournalEntryDetailSerializer(journal).data)
