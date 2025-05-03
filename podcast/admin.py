from django.contrib import admin

from datablast.apps.podcast.models import (
    AntilibraryBook,
    AntilibraryBookCategoryMap,
    AntilibraryCategory,
    Podcast,
    Quote,
    QuotePerson,
    Video,
    Insight,
)

admin.site.register(AntilibraryBook)
admin.site.register(AntilibraryCategory)
admin.site.register(AntilibraryBookCategoryMap)
admin.site.register(Video)
admin.site.register(Insight)
admin.site.register(Quote)
admin.site.register(QuotePerson)
admin.site.register(Podcast)
