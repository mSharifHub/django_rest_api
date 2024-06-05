from .models import WatchList, StreamingPlatform, Review
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['reviewer', "watchlist"]


class WatchSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"

    # def create(self, validated_data):
    #     watchlist = self.context['watchlist']
    #     reviewer = self.context['reviewer']
    #     return Review.objects.create(reviewer=reviewer, watchlist=watchlist, **validated_data)


class StreamingPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"
