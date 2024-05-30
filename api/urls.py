from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    Home,
    WatchListView,
    WatchDetail,
    StreamingChannels,
    ReviewList,
    ReviewDetail,
    WatchReviewList, CreateReview,
)

router = DefaultRouter()
router.register('streamer', StreamingChannels, basename='streaming_channels')

urlpatterns = [
    path("", Home.as_view(), name="home"),  #ROOT URL
    path("api/watch/all/", WatchListView.as_view(), name="watch_list"),
    path("api/watch/<slug:slug>/", WatchDetail.as_view(), name="watch_detail"),
    path("api/", include(router.urls)),
    # muted to use both as router. refractored  in StreamingChannels
    # path("api/stream/", StreamWatchList.as_view(), name="stream_list"),
    # path("api/stream/<str:str>/", StreamDetail.as_view(), name="stream_detail"),
    path("api/reviews/", ReviewList.as_view(), name="reviews_list"),
    path("api/reviews/<int:pk>/", ReviewDetail.as_view(), name="reviews_detail"),
    path("api/wath/<slug:slug>/reviews/", WatchReviewList.as_view(), name="wath_reviews_list"),
    path("api/watch/<slug:slug>/reviews/create/", CreateReview.as_view(), name="create_review"),

]
