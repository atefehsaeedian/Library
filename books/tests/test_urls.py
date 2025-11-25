from django.test import TestCase
from django.urls import reverse, resolve
from books import views

class BooksURLsTest(TestCase):

    def test_book_list_url_resolves(self):
        url = reverse('books:book_list')
        self.assertEqual(resolve(url).func.view_class, views.BookListView)

    def test_book_detail_url_resolves(self):
        url = reverse('books:book_detail', kwargs={'slug':'test-book'})
        self.assertEqual(resolve(url).func.view_class, views.BookDetailView)

    def test_favorite_url_resolves(self):
        url = reverse('books:favorite', kwargs={'slug':'test-book'})
        self.assertEqual(resolve(url).func.view_class, views.FavoriteView)

    def test_my_books_url_resolves(self):
        url = reverse('books:my_books')
        self.assertEqual(resolve(url).func.view_class, views.MyBooksView)

