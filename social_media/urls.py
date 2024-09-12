from django.urls import path

from social_media.views import sign_up, log_in, search_users, send_request, accept_request, reject_request, \
    list_friends, list_pending_requests

urlpatterns = [
    path('sign-up/', sign_up),
    path('log-in/', log_in),
    path('search/', search_users),
    path('request/accept/<int:pk>', accept_request),
    path('request/reject/<int:pk>', reject_request),
    path('request/send/<int:pk>', send_request),
    path('friends/list/', list_friends),
    path('requests/pending/', list_pending_requests)
]