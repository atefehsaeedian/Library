from django.test import TestCase
from model_bakery import baker
from django.contrib.auth.models import User
from books.models import Book
from comments.models import Comment


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = baker.make(User, username="testuser")
        self.book = baker.make(Book, title="Test Book", slug="test-book")

    def test_comment_creation(self):
        comment = Comment.objects.create(
            book=self.book,
            user=self.user,
            text="This is a great book!"
        )
        self.assertEqual(comment.text, "This is a great book!")
        self.assertEqual(comment.user.username, "testuser")
        self.assertEqual(comment.book.title, "Test Book")
        self.assertTrue(comment.created)

    def test_comment_str_representation(self):
        comment = baker.make(
            Comment,
            user=self.user,
            book=self.book,
            text="Amazing read!"
        )
        expected = f"{self.user} on {self.book}"
        self.assertEqual(str(comment), expected)

    def test_comment_ordering_by_created_descending(self):
        baker.make(Comment, book=self.book, user=self.user, _quantity=3)
        comments = Comment.objects.all()
        self.assertGreater(comments[0].created, comments[1].created)
        self.assertGreater(comments[1].created, comments[2].created)

    def test_related_name_comments_on_book(self):
        baker.make(Comment, book=self.book, user=self.user, _quantity=5)
        self.assertEqual(self.book.comments.count(), 5)