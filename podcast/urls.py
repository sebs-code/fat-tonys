from django.contrib.sitemaps.views import sitemap
from django.urls import path

from datablast.apps.podcast.views import about, antilibrary, contact, index, podcast, podcasts, quotes, videos
from datablast.apps.podcast.models import Podcast
from datablast.apps.podcast.sitemaps import sitemaps

app_name = "podcast"
urlpatterns = [
    path("", index, name="index"),
    path("episodes/", podcasts, name="episodes"),
    path("episode/<slug:slug>/", podcast, name="episode"),
    path("antilibrary/", antilibrary, name="antilibrary"),
    path("antilibrary/<slug:slug>/", antilibrary, name="antilibrary-category"),
    path("videos/", videos, name="videos"),
    path("quotes/", quotes, name="quotes"),
    path("quotes/<slug:slug>/", quotes, name="quotes-person"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap")
]