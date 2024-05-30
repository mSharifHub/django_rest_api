from django.contrib import admin
from .models import WatchList, StreamingPlatform, Review


@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fields = ['title', 'slug', 'description', 'platform','active']


@admin.register(StreamingPlatform)
class StreamingPlatformAdmin(admin.ModelAdmin):
    fields = ['streamer', 'url', 'about']
    readonly_fields = ['url']

    def save_model(self, request, obj, form, change):
        if not obj.url:
            obj.url = f"https://www.{obj.streamer}.com"
        super().save_model(request, obj, form, change)


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    pass


