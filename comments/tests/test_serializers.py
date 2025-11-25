from django.test import TestCase, RequestFactory
from model_bakery import baker
from comments.serializers import CommentSerializer
from django.contrib.auth.models import User


class CommentSerializerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = baker.make(User, username="ali123")
        self.book = baker.make('books.Book', title="Python Book")
        self.comment = baker.make(
            'comments.Comment',
            user=self.user,
            book=self.book,
            text="Very helpful book!"
        )

    def test_comment_serializer_contains_expected_fields(self):
        serializer = CommentSerializer(self.comment)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'id', 'user', 'text', 'created'})

    def test_comment_serializer_user_field_is_username(self):
        serializer = CommentSerializer(self.comment)
        self.assertEqual(serializer.data['user'], "ali123")

    def test_comment_serializer_text_field(self):
        serializer = CommentSerializer(self.comment)
        self.assertEqual(serializer.data['text'], "Very helpful book!")

    def test_comment_serializer_read_only_user_field(self):

        data = {
            'text': 'New comment',
            'user': 'someone_else'
        }
        serializer = CommentSerializer(self.comment, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.user.username, "ali123")