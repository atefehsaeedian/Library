from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from model_bakery import baker
from books.models import Book, FavoriteBook

class BookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = baker.make(User)
        self.book = baker.make(
            Book,
            title="Test Book",
            slug="test-book",
            full_text="Secret content",
            summary="Public summary"
        )

    def test_book_list_view_status_and_template(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_anonymous_hide_full_text(self):
        response = self.client.get(reverse('books:book_detail', kwargs={'slug':'test-book'}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.book.full_text)

    def test_book_detail_authenticated_shows_full_text(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('books:book_detail', kwargs={'slug':'test-book'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.full_text)

    def test_add_to_favorite_creates_favorite_and_redirects(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('books:favorite', kwargs={'slug':'test-book'}))
        self.assertEqual(response.status_code, 302)
        # Adding to favorites button
        self.assertTrue(FavoriteBook.objects.filter(user=self.user, book=self.book).exists())

    def test_remove_from_favorite_deletes_and_redirects(self):
        self.client.force_login(self.user)
        # Adding
        FavoriteBook.objects.create(user=self.user, book=self.book)
        # Removing
        response = self.client.post(reverse('books:favorite', kwargs={'slug': 'test-book'}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FavoriteBook.objects.filter(user=self.user, book=self.book).exists())

    def test_my_books_view_only_show_user_favorites(self):
        other_user = baker.make(User)
        other_book = baker.make(Book, slug='other-book')

        baker.make(FavoriteBook, user=other_user, book=self.book)
        baker.make(FavoriteBook, user=other_user, book=other_book)

        my_favorite_book = baker.make(Book, slug='my-book')
        baker.make(FavoriteBook, user=self.user, book=my_favorite_book)

        self.client.force_login(self.user)
        response = self.client.get(reverse('books:my_books'))
        self.assertEqual(response.status_code, 200)
        favorites = response.context['favorites']
        self.assertEqual(favorites.count(), 1)
        self.assertEqual(favorites.first().book.slug, 'my-book')



