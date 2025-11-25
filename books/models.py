from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=150, verbose_name='Book Title')
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name='URL Slug')
    author = models.CharField(max_length=100, verbose_name='Author')
    publication_year = models.PositiveIntegerField(verbose_name='Publication Year')
    cover_image = models.ImageField(upload_to='cover/', blank=True, null=True, verbose_name='Cover Image')
    summary = models.TextField(blank=True, verbose_name='Summary')
    full_text = models.TextField(blank=True, verbose_name='Full Book Test')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f'{self.title} by {self.author}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'slug':self.slug})


class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')