from django.contrib.sitemaps import GenericSitemap
from django.contrib import sitemaps
from django.urls import reverse
from django.contrib.sites.models import Site

from .models import Podcast, AntilibraryCategory, QuotePerson


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.6

    def items(self):
        return ["podcast:index", "podcast:about", "podcast:contact", "podcast:episodes", "podcast:videos", "podcast:antilibrary", "podcast:quotes"]

    def location(self, item):
        return reverse(item)

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='fattonys.net', name='fattonys.net')
        return super().get_urls(site=site, **kwargs)


class CustomGenericSitemap(GenericSitemap):
    def get_urls(self, site=None, **kwargs):
        site = Site(domain='fattonys.net', name='fattonys.net')
        return super().get_urls(site=site, **kwargs)


sitemaps = {
    "static": StaticViewSitemap,
    "episodes": CustomGenericSitemap({"queryset": Podcast.objects.all(), "date_field": "date_created"}, priority=1.0),
    "antilibrary-categories": CustomGenericSitemap({"queryset": AntilibraryCategory.objects.all()}, priority=1.0),
    "quote-people": CustomGenericSitemap({"queryset": QuotePerson.objects.all()}, priority=1.0)
}
