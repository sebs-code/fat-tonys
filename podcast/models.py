from ckeditor.fields import RichTextField
from django.db import models


class AntilibraryBook(models.Model):
    """
    Represents an Antilibrary Book.
    """

    name = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    cover_image = models.CharField(max_length=1000)
    date_created = models.DateField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return "{0} - {1} - Featured: {2}".format(
            self.name,
            self.author,
            self.featured,
        )


class AntilibraryCategory(models.Model):
    """
    Represents an Antilibrary Category.
    """

    name = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000)
    order = models.IntegerField(default=1)

    def __str__(self):
        return "{0}".format(
            self.name,
        )

    def get_absolute_url(self):
        return f"/antilibrary/{self.slug}/" 


class AntilibraryBookCategoryMap(models.Model):
    """
    Represents an Antilibrary Book:Category mapping.
    """

    book = models.ForeignKey(AntilibraryBook, on_delete=models.CASCADE)
    category = models.ForeignKey(AntilibraryCategory, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(
            self.book.name,
            self.category.name,
        )


class QuotePerson(models.Model):
    """
    Represents a person who said a quote.
    """

    name = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000)

    def __str__(self):
        return "{0}".format(self.name)
    
    def get_absolute_url(self):
        return f"/quotes/{self.slug}/" 


class Quote(models.Model):
    """
    Represents a quote.
    """

    quote = models.TextField()
    person = models.ForeignKey(QuotePerson, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{0} - {1}".format(self.person.name, self.quote)


class Video(models.Model):
    """
    Represents a Fat Tony's Video.
    """

    title = models.CharField(max_length=1000)
    thumbnail = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    featured = models.BooleanField(default=False)
    date_created = models.DateField()

    def __str__(self):
        return "{0}".format(
            self.title,
        )


class Insight(models.Model):
    """
    Represents a Fat Tony's Insight.
    """

    title = models.CharField(max_length=1000)
    body = models.CharField(max_length=2000)

    def __str__(self):
        return "{0}".format(
            self.title,
        )


class Podcast(models.Model):
    """
    Represents a podcast.
    """

    title = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000)
    description = models.CharField(max_length=2000)
    headshot = models.CharField(max_length=1000)
    bkg_colour = models.CharField(max_length=10)
    audio_url = models.CharField(max_length=10000)
    date_created = models.DateField()
    eipsode_number = models.IntegerField(default=1)
    season_number = models.IntegerField(default=1)
    summary = RichTextField(default="No Summary Available")
    transcript = RichTextField(default="No Transcript Available")
    resources = RichTextField(default="No Summary Available")
    featured = models.BooleanField(default=False)

    def __str__(self):
        return "{0} - {1}".format(
            self.eipsode_number,
            self.title,
        )

    def get_absolute_url(self):
        return f"/episode/{self.slug}/" 