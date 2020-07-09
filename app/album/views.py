from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import Album

from album import serializers


class AlbumViewSet(viewsets.ModelViewSet):
    """Manage albums in the database"""
    serializer_class = serializers.AlbumSerializer
    queryset = Album.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Retrieve the albums"""
        self.queryset = Album.objects.all()
        return self.queryset

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.AlbumSerializer
        elif self.action == 'upload_image':
            return serializers.AlbumCoverSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new album"""
        serializer.save()

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to an album"""
        album = self.get_object()
        serializer = self.get_serializer(
            album,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
