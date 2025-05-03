import csv

import boto3
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from podcast.models import (
    AntilibraryBook,
    AntilibraryBookCategoryMap,
    AntilibraryCategory,
)


class Command(BaseCommand):
    help = "Uploads books from the books .csv file to the antilibrary database."

    def handle(self, *args, **options):
        # Read the books .csv file
        import os

        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)
        reader = csv.reader(open("/app/podcast/management/commands/books.csv", "r"))
        next(reader)  # Skip the header row
        print("Starting to upload books...")

        for row in reader:
            # Get values from the row
            title = row[0]
            author = row[1]
            category_name = row[2]
            url = row[3]
            book_image_url = row[4]

            # Get the book image file extension
            book_image_file_extension = book_image_url.split(".")[-1]

            # Construct the cloudfront cover image url
            cover_image = (
                "https://d2m0g093fmwt3a.cloudfront.net/books/"
                + slugify(title)
                + "."
                + book_image_file_extension
            )

            with transaction.atomic():
                # Create the book object
                book, created = AntilibraryBook.objects.get_or_create(
                    name=title,
                    slug=slugify(title),
                    author=author,
                    url=url,
                    cover_image=cover_image,
                )
                print("Created book: {0}".format(book))

                # Get or create the category object
                print("Searching for category: {0}".format(category_name))
                category = AntilibraryCategory.objects.filter(
                    name=category_name
                ).first()
                if not category:
                    category = AntilibraryCategory.objects.create(
                        name=category_name,
                        slug=slugify(category_name),
                    )
                    category.save()
                    print("Created category: {0}".format(category))
                else:
                    print("Found category: {0}".format(category))

                # Create the book-category mapping
                (
                    book_category_map,
                    created,
                ) = AntilibraryBookCategoryMap.objects.get_or_create(
                    book=book,
                    category=category,
                )
                print("Created book-category mapping: {0}".format(book_category_map))

                # Upload the cover image to S3
                s3 = boto3.client(
                    "s3",
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                )
                key_name = "books/" + slugify(title) + "." + book_image_file_extension
                image = requests.get(book_image_url, stream=True).raw
                s3.upload_fileobj(
                    image, "fattonys.net", key_name, ExtraArgs={"ACL": "public-read"}
                )

            print("Completed uploading books.")
