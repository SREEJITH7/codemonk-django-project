from django.urls import path
from .views import RegisterView, LoginView, RefreshView, ParagraphIngestView, SearchView

urlpatterns = [
    path("auth/register", RegisterView.as_view(), name="register"),
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/refresh", RefreshView.as_view(), name="token_refresh"),
    path("paragraphs", ParagraphIngestView.as_view(), name="paragraphs"),
    path("search", SearchView.as_view(), name="search"),
]
