from django.urls import path, include

from polls.views import aggregate_poll_count, PollList

urlpatterns = [
    path('', PollList.as_view()),
    path('count', aggregate_poll_count),
]
