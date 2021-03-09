from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("mylistings",views.mylistings, name="mylistings"),
    path("listings/<int:id>", views.listing, name="listing"),
    path("mybids", views.mybids, name="mybids"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:id>", views.category, name="category")
]
