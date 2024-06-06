import factory
from factory.django import DjangoModelFactory
from api.models import WatchList, StreamingPlatform


class StreamingPlatformFactory(DjangoModelFactory):
    class Meta:
        model = StreamingPlatform

    streamer = factory.Faker('company')
    about = factory.Faker('catch_phrase')
    url = factory.Faker('url')


class WatchListFactory(DjangoModelFactory):
    class Meta:
        model = WatchList

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')
    platform = factory.SubFactory(StreamingPlatformFactory)
    active = True
    average_rating = factory.Faker('pyfloat', positive=True, min_value=1, max_value=5)
    number_rating = factory.Faker('pyint', min_value=1, max_value=1000)
