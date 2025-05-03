from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from datablast.apps.podcast.models import (
    AntilibraryBook,
    AntilibraryBookCategoryMap,
    AntilibraryCategory,
    Podcast,
    Quote,
    QuotePerson,
    Video,
)


def index(request):
    """
    Fat Tony's home view.
    """

    podcast = Podcast.objects.latest("date_created")
    podcasts = Podcast.objects.filter(featured=True).order_by("-date_created")
    books = AntilibraryBook.objects.filter(featured=True).order_by("-date_created")[:6]
    videos = Video.objects.filter(featured=True).order_by("-date_created")[:6]

    return render(
        request,
        "podcast/index.html",
        {
            "podcast": podcast,
            "podcasts": podcasts,
            "transcript": True,
            "homepage": True,
            "books": books,
            "videos": videos,
        },
    )


def podcasts(request):
    """
    Podcast Episodes.
    """

    podcast = Podcast.objects.latest("date_created")
    podcasts = Podcast.objects.order_by("-date_created")[1:]

    return render(
        request,
        "podcast/podcasts.html",
        {
            "podcasts": podcasts,
            "podcast": podcast,
            "transcript": True,
            "active_link": "podcast-link",
        },
    )


def podcast(request, slug=None):
    """
    Podcast Episode.
    """

    podcast = get_object_or_404(Podcast, slug=slug.lower())
    podcasts = Podcast.objects.exclude(slug=slug.lower()).order_by("-eipsode_number")[
        :3
    ]
    return render(
        request,
        "podcast/podcast.html",
        {"podcast": podcast, "podcasts": podcasts},
    )


def antilibrary(request, slug=None):
    """
    Books.
    """

    filter = "All"
    page = request.GET.get("page", 1)
    categories = AntilibraryCategory.objects.order_by("name")
    books = AntilibraryBookCategoryMap.objects.order_by("-book__date_created").distinct()

    if slug:
        category = get_object_or_404(AntilibraryCategory, slug=slug.lower())
        books = AntilibraryBookCategoryMap.objects.filter(category=category).order_by(
            "-book__date_created"
        ).distinct()
        filter = category.name

    paginator = Paginator(books, 24)

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    if request.htmx:
        template_name = "podcast/snippet_antilibrary.html"
    else:
        template_name = "podcast/antilibrary.html"

    return render(
        request,
        template_name,
        {
            "categories": categories,
            "books": books,
            "filter": filter,
            "active_link": "antilibrary-link",
        },
    )


def videos(request):
    """
    Videos.
    """

    videos = Video.objects.order_by("-date_created")

    return render(
        request,
        "podcast/videos.html",
        {
            "videos": videos,
            "active_link": "videos-link",
        },
    )


def quotes(request, slug=None):
    """
    quotes.
    """

    filter = "All"
    page = request.GET.get("page", 1)
    people = QuotePerson.objects.order_by("name")
    quotes = Quote.objects.order_by("-date_created")

    if slug:
        person = get_object_or_404(QuotePerson, slug=slug.lower())
        quotes = quotes.filter(person=person)
        filter = person.name

    paginator = Paginator(quotes, 21)
    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        quotes = paginator.page(1)
    except EmptyPage:
        quotes = paginator.page(paginator.num_pages)

    if request.htmx:
        template_name = "podcast/snippet_quotes.html"
    else:
        template_name = "podcast/quotes.html"

    return render(
        request,
        template_name,
        {
            "people": people,
            "quotes": quotes,
            "filter": filter,
            "active_link": "quotes-link",
        },
    )


def about(request):
    """
    About.
    """

    return render(
        request,
        "podcast/about.html",
        {
            "active_link": "about-link",
        },
    )


def contact(request):
    """
    Contact.
    """

    return render(
        request,
        "podcast/contact.html",
        {
            "active_link": "contact-link",
        },
    )


def error_400(request, *args, **argv):
    return render(request, "podcast/400.html", status=400)


def error_403(request, *args, **argv):
    return render(request, "podcast/403.html", status=403)


def error_404(request, *args, **argv):
    return render(request, "podcast/404.html", status=404)


def error_500(request, *args, **argv):
    return render(request, "podcast/500.html", status=500)
