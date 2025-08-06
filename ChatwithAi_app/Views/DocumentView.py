from rest_framework import viewsets
from DataBase_MPMS.models import Document
from rest_framework import permissions
from ..Serializer.DocumentSerializer import DocumentFilterSet, DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = DocumentFilterSet