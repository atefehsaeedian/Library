from django.urls import path
from . import views



app_name = 'books'
urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<slug:slug>/favorite/', views.FavoriteView.as_view(), name='favorite'),
    path('book/<slug:slug>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('my-books/', views.MyBooksView.as_view(), name='my_books'),

]