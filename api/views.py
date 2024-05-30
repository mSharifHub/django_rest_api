from django.db.migrations import serializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, mixins, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from .models import WatchList, StreamingPlatform, Review
from .serializers import WatchSerializer, StreamingPlatformSerializer, ReviewSerializer


class Home(APIView):
    def get(self, request):
        return JsonResponse({"message": "this is a test api using django"})


# shorter version of ReviewList and ReviewDetail
class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        slug = self.kwargs['slug']

        try:
            watch = WatchList.objects.get(slug=slug)
        except WatchList.DoesNotExist:
            raise NotFound({"error": "Watch list does not exist"}, status.HTTP_404_NOT_FOUND)
        serializer.save(watchlist=watch)


class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class WatchReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            watch = WatchList.objects.get(slug=slug)
        except WatchList.DoesNotExist:
            return Review.objects.none()
        return Review.objects.filter(watch=watch)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"error": "Content not found or no reviews available"},
                                status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


# class WatchReviewList(mixins.ListModelMixin, generics.GenericAPIView):
#     serializer_class = ReviewSerializer
#
#     def get_queryset(self):
#         slug = self.kwargs['slug']
#         try:
#             watch = WatchList.objects.get(slug=slug)
#         except WatchList.DoesNotExist:
#             return Review.objects.none()
#         return Review.objects.filter(watch=watch)
#
#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         if not queryset.exists():
#             return JsonResponse({"error": "Content not found or no reviews available"},
#                                 status=status.HTTP_404_NOT_FOUND)
#         return self.list(request, *args, **kwargs)
#
#
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()  # Ensure queryset is correctly defined
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamingChannels(viewsets.ModelViewSet):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer


# class StreamingChannels(viewsets.ViewSet):
#
#     def list(self, request):
#         platform = StreamingPlatform.objects.all()
#         serializer = StreamingPlatformSerializer(platform, many=True, context={"request": request})
#         return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
#
#     def retrieve(self, request, slug=None):
#         queryset = StreamingPlatform.objects.all()
#         content = get_object_or_404(queryset, slug=slug)
#         serializer = StreamingPlatformSerializer(content, context={"request": request})
#         return JsonResponse(serializer.data, status=status.HTTP_200_OK)
#
#     def create(self, request):
#         serializer = StreamingPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# class StreamingChannelsList(APIView):
#     def get(self, request):
#         platforms = StreamingPlatform.objects.all()
#         serializer = StreamingPlatformSerializer(platforms, many=True, context={"request": request})
#         if platforms.exists():
#             return JsonResponse({'platforms': serializer.data}, safe=False, status=status.HTTP_200_OK)
#         return JsonResponse({"error_message": "could not get platforms"}, status=status.HTTP_400_BAD_REQUEST)
#
#     def post(self, request):
#         serializer = StreamingPlatformSerializer(data=request.data, context={"request": request})
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class StreamingChannelsDetail(APIView):
#     @staticmethod
#     def get_object(url):
#         try:
#             return StreamingPlatform.objects.get(url=url)
#         except StreamingPlatform.DoesNotExist:
#             return None
#
#     def get(self, request, url):
#         stream = StreamingChannelsDetail.get_object(url)
#         if stream is None:
#             return JsonResponse({"error": "Stream not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StreamingPlatformSerializer(stream, context={"request": request})
#         return JsonResponse(serializer.data)
#
#     def put(self, request, url):
#         stream = StreamingChannelsDetail.get_object(url)
#         if stream is None:
#             return JsonResponse({"error": "Stream not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StreamingPlatformSerializer(stream, data=request.data, context={"request": request})
#         if serializer.is_valid():
#             original_data = StreamingPlatformSerializer(stream).data
#             serializer.save()
#             updated_data = serializer.data
#             changes = {field: updated_data[field] for field in updated_data if
#                        updated_data[field] != original_data[field]}
#             if len(changes) > 0:
#                 return JsonResponse({"result": f"changes on {changes}"}, status=status.HTTP_200_OK)
#             return JsonResponse({"result": "not modified"}, status=status.HTTP_304_NOT_MODIFIED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListView(APIView):
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchSerializer(movies, many=True, context={"request": request})
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        if not request.data:
            return JsonResponse({'error': 'No data'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WatchSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetail(APIView):
    @staticmethod
    def get_object(slug):
        try:
            return WatchList.objects.get(slug=slug)
        except WatchList.DoesNotExist:
            return None

    def get(self, request, slug):
        movie = WatchDetail.get_object(slug)
        if movie is None:
            return JsonResponse({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchSerializer(movie, context={'request': request})
        return JsonResponse(serializer.data)

    def put(self, request, slug):
        movie = WatchDetail.get_object(slug)
        if movie is None:
            return JsonResponse({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchSerializer(movie, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            original_data = WatchSerializer(movie).data
            serializer.save()
            updated_data = serializer.data
            changes = {field: updated_data[field] for field in updated_data if
                       updated_data[field] != original_data[field]}
            if len(changes) > 0:
                return JsonResponse({"result": f"changes on {changes}"}, status=status.HTTP_200_OK)
            return JsonResponse({"result": "not modified"}, status=status.HTTP_304_NOT_MODIFIED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET", "POST"])
# def movies_list_api(request):
#     if request.method == "GET":
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["GET", "PUT", "DELETE"])
# def movie_detail_api(request, slug):
#     movie = Movie.objects.get(slug=slug)
#
#     if request.method == "GET":
#         try:
#             serializer = MovieSerializer(movie)
#             return Response(serializer.data)
#         except Movie.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     elif request.method == "PUT":
#         original_data = MovieSerializer(movie).data
#         serializer = MovieSerializer(movie, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             updated_data = serializer.data
#             changes = {
#                 field: updated_data[field] for field in updated_data if
#                 updated_data[field] != original_data[field]
#             }
#             return JsonResponse(changes)
#         return JsonResponse(
#             data={
#                 "message": "Movie may have been deleted",
#                 "error": serializer.errors
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     elif request.method == "DELETE":
#         movie.delete()
#         return JsonResponse({"message": "movie deleted"}, status=status.HTTP_204_NO_CONTENT)
