from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from api.throttling import ReviewCreateThrottle, ReviewListThrottle
from .models import WatchList, StreamingPlatform, Review
from .serializers import WatchSerializer, StreamingPlatformSerializer, ReviewSerializer
from api.custom_permission import AdminOrReadOnly, ReviewUserOrReadOnly


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        reviewer = self.request.query_params.get('reviewer', None)
        return Review.objects.filter(reviewer__username=reviewer)


class Home(APIView):
    def get(self, request):
        return JsonResponse({"message": "this is a test api using django"})


# shorter version of ReviewList and ReviewDetail
class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

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
    throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reviewer__username', 'active']


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


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


class StreamingPlatformCreateView(generics.ListCreateAPIView):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer
    permission_classes = [AdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class StreamingPlatformDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer
    permission_classes = [AdminOrReadOnly]


class WatchListView(APIView):

    def get(self, request):
        content = WatchList.objects.all()
        serializer = WatchSerializer(content, many=True, context={"request": request})
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
        content = WatchDetail.get_object(slug)
        if content is None:
            return JsonResponse({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchSerializer(content, context={'request': request})
        return JsonResponse(serializer.data)

    def put(self, request, slug):
        content = WatchDetail.get_object(slug)
        if content is None:
            return JsonResponse({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchSerializer(content, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            original_data = WatchSerializer(content).data
            serializer.save()
            updated_data = serializer.data
            changes = {field: updated_data[field] for field in updated_data if
                       updated_data[field] != original_data[field]}
            if len(changes) > 0:
                return JsonResponse({"result": f"changes on {changes}"}, status=status.HTTP_200_OK)
            return JsonResponse({"result": "not modified"}, status=status.HTTP_304_NOT_MODIFIED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
