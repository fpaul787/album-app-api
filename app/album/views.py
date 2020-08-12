from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


from core.models import Album

from album import serializers


class AlbumViewSet(viewsets.ModelViewSet):
    """Manage albums in the database"""
    serializer_class = serializers.AlbumSerializer
    queryset = Album.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'artist']

    def get_queryset(self):
        """Retrieve the albums"""

        if 'search' in self.request.GET:
            query = self.request.query_params.get('search')
            # print(query)
            

            # weigh search by artist first and album name second
            # search_vector = SearchVector('name', weight='B') + \
            #                 SearchVector('artist', weight='A')
            # search_query = SearchQuery(query)

            # results = Album.objects.annotate(
            #     rank=SearchRank(search_vector, search_query)
            # ).filter(rank__gte=0.3).order_by('-rank')
            # self.queryset = Album.objects.all()
            results = Album.objects.annotate(
                search=SearchVector('name', 'artist'),
            ).filter(search=query)
            self.queryset = results
        else:
            results = Album.objects.all()
            self.queryset = results
            
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

class AlbumYearFilter(ListAPIView):
    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        """Retrieve the albums"""
        # print(self.kwargs['year'])
        year = self.kwargs['year']
        self.queryset = Album.objects.filter(release_date__year=year)
        return self.queryset
