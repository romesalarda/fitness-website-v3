from django.urls import path
from .views import BlacklistTokenUpdateView, CustomUserCreate

urlpatterns = [
    path("user/create/", CustomUserCreate.as_view(), name="create_user"),
    path('user/logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]
