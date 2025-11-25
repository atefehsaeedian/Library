from django.contrib import admin
from .models import Book, FavoriteBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year']
    prepopulated_fields = {'slug':('title', )}
    search_fields = ['title', 'author']
    fields = ['title', 'slug', 'author', 'publication_year', 'cover_image', 'summary', 'full_text']


admin.site.register(FavoriteBook)