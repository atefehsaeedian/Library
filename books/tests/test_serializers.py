from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from model_bakery import baker
from books.serializers import BookListSerializer, BookDetailSerializer
from books.models import Book, FavoriteBook

class BookSerializersTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = baker.make(User)
        self.book = baker.make(
            Book,
            title="Secret Book",
            full_text="This is very secret content",
            summary="Public summary"
        )

    def test_list_serializer_does_not_include_full_text(self):
        serializer = BookListSerializer(self.book)
        self.assertNotIn('full_text', serializer.data)
        self.assertIn('summary', serializer.data)

    # def test_detail_serializer_hides_full_text_for_anonymous(self):
    #     request = self.factory.get('/')
    #     request.user = type('AnonymousUser', (), {'is_authenticated': False})()
    #     serializer = BookDetailSerializer(self.book, context={'request': request})
    #     self.assertEqual(serializer.data['full_text'], '')
    #
    # def test_detail_serializer_shows_full_text_for_authenticated(self):
    #     request = self.factory.get('/')
    #     request.user = self.user
    #     serializer = BookDetailSerializer(self.book, context={'request': request})
    #     self.assertIn("very secret content", serializer.data['full-text'])

    def test_is_favorite_field(self):
        request = self.factory.get('/')
        request.user = self.user
        baker.make(FavoriteBook, user=self.user, book=self.book)
        serializer = BookDetailSerializer(self.book, context={'request': request})
        self.assertTrue(serializer.data['is_favorite'])