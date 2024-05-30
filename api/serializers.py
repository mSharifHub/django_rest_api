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

    def create(self, validated_data):
        watchlist = self.context['watchlist']
        reviewer = self.context['reviewer']
        return Review.objects.create(reviewer=reviewer, watchlist=watchlist, **validated_data)


class StreamingPlatformSerializer(serializers.HyperlinkedModelSerializer):  # users url instead of id
    watchlist = WatchSerializer(many=True, read_only=True)

    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     view_name='watch_detail',
    #     lookup_field='slug',
    #     read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"

# def title_len(value):
#     if len(value) > 10:
#         raise serializers.ValidationError("Title must be less than 10 characters")
#
#
# def description_len(value):
#     if len(value) < 20:
#         raise serializers.ValidationError("Description must be at least 20 characters")
#
#
# class MovieSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(validators=[title_len])  # field validator
#     description = serializers.CharField(validators=[description_len])  # field validator
#     activate = serializers.BooleanField()
#
#     class Meta:
#         model = Movie
#         fields = ['id', 'title', 'description', 'activate']
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get("description", instance.description)
#         instance.activate = validated_data.get('activate', instance.activate)
#         instance.save()
#         return instance

# Object level validate
# def validate(self, data):
#     if data["title"] == data["description"]:
#         raise serializers.ValidationError("Title and Description cannot be the same.")
#     else:
#         return data

# Field level validator as validate_<fieldName>(self,value): ......
# def validate_description(self, value):
#     if len(value) < 50:
#         raise serializers.ValidationError("Description must be at least 50 characters")
