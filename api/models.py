from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


class StreamingPlatform(models.Model):
    streamer = models.CharField(max_length=50)
    about = models.TextField(max_length=150)
    url = models.URLField(unique=True, blank=True)

    def __str__(self):
        return self.streamer

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = f"https://www.{self.streamer}.com"
        super().save(*args, **kwargs)


class WatchList(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    platform = models.ForeignKey(StreamingPlatform, on_delete=models.CASCADE, related_name="watchlist", default=1)
    active = models.BooleanField(default=True)
    average_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or slugify(self.title) != self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Review(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False,
                                         blank=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.watchlist.title} - {self.rating}"
