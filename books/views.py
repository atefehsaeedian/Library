from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookListSerializer, BookDetailSerializer
from .models import Book, FavoriteBook
from comments.models import Comment
from django.views.generic import ListView,DetailView


# List all books
class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    ordering = ['-id']

# Book detail can be seen if user logged in
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object

        if self.request.user.is_authenticated:
            context['show_full_text'] = True
            context['is_favorite'] = FavoriteBook.objects.filter(
                user=self.request.user,
                book=book
            ).exists()
        else:
            context['show_full_text'] = False
            context['is_favorite'] = False
        return context

class BookListAPI(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer

class BookDetailAPI(APIView):
    def get(self, request, slug):
        book = get_object_or_404(Book, slug=slug)
        serializer = BookDetailSerializer(book, context={'request':request})
        data = serializer.data
        if not request.user.is_authenticated:
            data['full_text'] = ''
        return Response(data)

class FavoriteView(LoginRequiredMixin, APIView):
    def post(self, request, slug):
        book = get_object_or_404(Book, slug=slug)

        if FavoriteBook.objects.filter(user=request.user, book=book).exists():
            FavoriteBook.objects.filter(user=request.user, book=book).delete()
            messages.info(request, f'"{book.title}" removed from favorites.')
        else:
            FavoriteBook.objects.create(user=request.user, book=book)
            messages.success(request, f'"{book.title}" added to favorites!')

        return redirect(book.get_absolute_url())

class AddCommentView(LoginRequiredMixin, APIView):
    def post(self, request, slug):
        book = get_object_or_404(Book, slug=slug)
        text = request.POST.get('text', '').strip()
        if not text:
            messages.error(request, 'Comment can not be empty!', 'danger')
        else:
            Comment.objects.create(book=book, user=request.user, text=text)
            messages.success(request, 'Your comment has been successfully added.', 'success')
        return redirect(book.get_absolute_url())

class MyBooksView(LoginRequiredMixin, ListView):
    template_name = 'books/my_books.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return FavoriteBook.objects.filter(user=self.request.user).select_related('book')
