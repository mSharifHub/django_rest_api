from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    Home,
    WatchListView,
    WatchDetail,
    StreamingChannels,
    ReviewList,
    ReviewDetail,
    WatchReviewList, CreateReview, UserReview,
)

router = DefaultRouter()
router.register('streamer', StreamingChannels, basename='streaming_channels')

urlpatterns = [
    path("", Home.as_view(), name="home"),  # ROOT URL
    path("api/watch/all/", WatchListView.as_view(), name="watch_list"),
    path("api/watch/<slug:slug>/", WatchDetail.as_view(), name="watch_detail"),
    path("api/", include(router.urls)),
    path("api/reviews/", ReviewList.as_view(), name="reviews_list"),
    path("api/reviews/<int:pk>/", ReviewDetail.as_view(), name="reviews_detail"),
    path("api/watch/<slug:slug>/reviews/", WatchReviewList.as_view(), name="wath_reviews_list"),
    path("api/watch/<slug:slug>/reviews/create/", CreateReview.as_view(), name="create_review"),
    # path("api-auth/", include('rest_framework.urls')),
    path("api/reviews/<str:username>/", UserReview.as_view(), name="user_reviews_detail"),

]
