from rest_framework import serializers

from core.models import Album


class AlbumSerializer(serializers.ModelSerializer):
    """Serializer for creating album"""

    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ('id',)


class AlbumCoverSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to albums"""

    class Meta:
        model = Album
        fields = ('id', 'album_cover',)
        read_only_fields = ('id',)
