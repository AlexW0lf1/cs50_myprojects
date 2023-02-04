from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("<int:lot_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("<str:category>", views.category_view, name="category"),
]
