from rest_framework import serializers
from .models import Book, FavoriteBook
from comments.serializers import CommentSerializer


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'author', 'summary', 'publication_year', 'cover_image']


class BookDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'author', 'publication_year',
                  'cover_image', 'summary', 'comments', 'is_favorite']

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and getattr(request.user, 'is_authenticated', False):
            return FavoriteBook.objects.filter(user=request.user, book=obj).exists()
        return False