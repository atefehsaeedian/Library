from django.test import TestCase
from model_bakery import baker
from django.contrib.auth.models import User
from books.models import Book, FavoriteBook


class BookModelTest(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.book = baker.make(
            Book,
            title='Test Book',
            slug='test-book',
            author='Test Author',
            publication_year='2025',
            summary='Short summary',
            full_text='This is full text'
        )

    def test_book_str(self):
        self.assertEqual(str(self.book), 'Test Book by Test Author')

    def test_slug_auto_generation(self):
        self.assertTrue(self.book.slug)
        self.assertIn('test-book', self.book.slug.lower())

    def test_favorite_book_creation(self):
        FavoriteBook.objects.create(user=self.user, book=self.book)
        self.assertEqual(FavoriteBook.objects.count(), 1)
