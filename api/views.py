from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status, generics, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import WatchList, StreamingPlatform, Review
from .serializers import WatchSerializer, StreamingPlatformSerializer, ReviewSerializer
from api.custom_permission import AdminOrReadOnly, ReviewUserOrReadOnly


class Home(APIView):
    def get(self, request):
        return JsonResponse({"message": "this is a test api using django"})


# shorter version of ReviewList and ReviewDetail
class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        try:
            watchlist_ = WatchList.objects.get(slug=slug)
        except WatchList.DoesNotExist:
            raise NotFound({"error": "Watch list does not exist"}, status.HTTP_404_NOT_FOUND)

        reviewer_ = self.request.user

        if not reviewer_.is_authenticated:
            raise ValidationError({"error": "Authentication required"}, status.HTTP_401_UNAUTHORIZED)

        review_query = Review.objects.filter(reviewer=reviewer_, watchlist=watchlist_)

        if review_query.exists():
            raise NotFound(f"{reviewer_}  already posted a review", status.HTTP_400_BAD_REQUEST)
        if watchlist_.number_rating == 0:
            watchlist_.average_rating = serializer.validated_data['rating']
        else:
            watchlist_.average_rating = (watchlist_.average_rating + serializer.validated_data['rating']) / 2
        watchlist_.number_rating += 1
        serializer.save(watchlist=watchlist_, reviewer=reviewer_)


class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AdminOrReadOnly]


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]


class WatchReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            watchlist_ = WatchList.objects.get(slug=slug)
        except WatchList.DoesNotExist:
            return Review.objects.none()
        return Review.objects.filter(watchlist=watchlist_)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"error": "Content not found or no reviews available"},
                                status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class StreamingChannels(viewsets.ModelViewSet):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer


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
