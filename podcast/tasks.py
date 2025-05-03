# tasks.py
import aiohttp
import asyncio
import json
import pytz
from urllib import request

from celery import shared_task
from django.conf import settings
import sentry_sdk
import tweepy

from datetime import datetime, timedelta
from dateutil.parser import parse
from django.utils import timezone

from datablast.apps.podcast.models import Quote, Insight, AntilibraryBook, Podcast
from datablast.apps.podcast.utils import list_guild_events, suffix



@shared_task
def x_post_fat_tony_quote():
    """
    Post a random quote from the Fat Tony's quote collection to Twitter(X).
    """

    # Get a random quote
    quote = Quote.objects.order_by('?').first()

    # Format it
    post = f'{quote.quote}\n\n- {quote.person.name}'

    # (X)Tweet it out
    client = tweepy.Client(
        consumer_key=settings.X_PODCAST_CONSUMER_KEY,
        consumer_secret=settings.X_PODCAST_CONSUMER_SECRET,
        access_token=settings.X_PODCAST_ACCESS_TOKEN,
        access_token_secret=settings.X_PODCAST_ACCESS_TOKEN_SECRET,
    )

    # Post tweet
    try:
        client.create_tweet(text=post)
        sentry_sdk.capture_message(f"Tweet successfully posted: {post}", "info")
    except Exception as e:
        print("Error sending tweet:", e)
        sentry_sdk.capture_exception(e)


@shared_task
def x_post_fat_tony_insight():
    """
    Post a random insight from the Fat Tony's insight collection to Twitter(X).
    """

    # Get a random insight
    insight = Insight.objects.order_by('?').first()

    # Format it
    post = f'{insight.title}\n\n {insight.body}'

    # (X)Tweet it out
    client = tweepy.Client(
        consumer_key=settings.X_PODCAST_CONSUMER_KEY,
        consumer_secret=settings.X_PODCAST_CONSUMER_SECRET,
        access_token=settings.X_PODCAST_ACCESS_TOKEN,
        access_token_secret=settings.X_PODCAST_ACCESS_TOKEN_SECRET,
    )

    # Post tweet
    try:
        client.create_tweet(text=post)
        sentry_sdk.capture_message(f"Tweet successfully posted: {post}", "info")
    except Exception as e:
        print("Error sending tweet:", e)
        sentry_sdk.capture_exception(e)


@shared_task
def x_post_fat_tony_book():
    """
    Post a random book from the Fat Tony's antilibrary to Twitter(X).
    """

    # Get a random tweet
    book = AntilibraryBook.objects.order_by('?').first()

    # Format it
    post = f'📚 Antilibrary Book of the Week\n\n {book.name} by {book.author}'

    # (X)Tweet it out
    client = tweepy.Client(
        consumer_key=settings.X_PODCAST_CONSUMER_KEY,
        consumer_secret=settings.X_PODCAST_CONSUMER_SECRET,
        access_token=settings.X_PODCAST_ACCESS_TOKEN,
        access_token_secret=settings.X_PODCAST_ACCESS_TOKEN_SECRET,
    )

    auth = tweepy.OAuth1UserHandler(
        settings.X_PODCAST_CONSUMER_KEY,
        settings.X_PODCAST_CONSUMER_SECRET,
        settings.X_PODCAST_ACCESS_TOKEN,
        settings.X_PODCAST_ACCESS_TOKEN_SECRET,
    )

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Upload image
    request.urlretrieve(book.cover_image, 'image.png')

    media = api.media_upload('image.png')

    # Post tweet with image
    try:
        client.create_tweet(text=post, media_ids=[media.media_id])
        sentry_sdk.capture_message(f"Tweet successfully posted: {post}",
                                   "info")
        print("Tweet successfully posted:", post)
    except Exception as e:
        print("Error sending tweet:", e)
        sentry_sdk.capture_exception(e)


@shared_task
def x_post_fat_tony_podcast_rewind():
    """
    Post a random previous podcast to Twitter for listeners to re-listen to.
    """

    # Get a random podcast
    podcast = Podcast.objects.order_by('?').first()

    # Format it
    post = f'⏪ Podcast Rewind - Listen Again \n\n {podcast.title} \n\n https://fattonys.net/episode/{podcast.slug}'

    # (X)Tweet it out
    client = tweepy.Client(
        consumer_key=settings.X_PODCAST_CONSUMER_KEY,
        consumer_secret=settings.X_PODCAST_CONSUMER_SECRET,
        access_token=settings.X_PODCAST_ACCESS_TOKEN,
        access_token_secret=settings.X_PODCAST_ACCESS_TOKEN_SECRET,
    )

    # Post tweet
    try:
        client.create_tweet(text=post)
        sentry_sdk.capture_message(f"Tweet successfully posted: {post}", "info")
    except Exception as e:
        print("Error sending tweet:", e)
        sentry_sdk.capture_exception(e)

@shared_task
def x_post_fat_tony_event_reminder():
    """
    Post reminders for Fat Tony's events
    """

    # Get existing events
    events = asyncio.run(list_guild_events())

    # Get UTC date times for upcoming events
    now = timezone.now()
    thirty_minutes_from_now = now + timedelta(minutes=30)
    one_day_from_now = now + timedelta(days=1)
    one_week_from_now = now + timedelta(weeks=1)
    one_month_from_now = now + timedelta(weeks=4)

    for event in events:
        # Get event name
        event_name = event['name']
        # Get event join date
        pretty_join = f'👇 Click Below to Join\n\n  {settings.DISCORD_INVITE_LINK}'
        # Get start datetime object
        scheduled_start_time_utc = parse(event['scheduled_start_time']).astimezone(timezone.utc)
        # Get start times
        london_start_time = datetime.strftime(timezone.localtime(scheduled_start_time_utc, pytz.timezone('Europe/London')),
                                              '%I:%M %p')
        rome_start_time = datetime.strftime(timezone.localtime(scheduled_start_time_utc, pytz.timezone('Europe/Rome')),
                                            '%I:%M %p')
        los_angeles_start_time = datetime.strftime(
            timezone.localtime(scheduled_start_time_utc, pytz.timezone('America/Los_Angeles')), '%I:%M %p')
        new_york_start_time = datetime.strftime(
            timezone.localtime(scheduled_start_time_utc, pytz.timezone('America/New_York')), '%I:%M %p')
        pretty_start_time = f'⏰ LA {los_angeles_start_time} // NYC {new_york_start_time} // UK {london_start_time} // EUR {rome_start_time}'
        # Get date
        pretty_date_weekday = datetime.strftime(scheduled_start_time_utc, "%A")
        pretty_date_day = suffix(datetime.strftime(scheduled_start_time_utc, "%-d"))
        pretty_date_month = datetime.strftime(scheduled_start_time_utc, "%B")
        pretty_date = f'📅 {pretty_date_weekday} {pretty_date_day} {pretty_date_month}'

        # Does event start within the next 30 mins?
        if now < scheduled_start_time_utc < thirty_minutes_from_now:
            title = "🚨 Event Reminder | Starting in the next 30 minutes"

        # Does event start within the next day + 30 mins?
        elif one_day_from_now < scheduled_start_time_utc < (one_day_from_now + timedelta(minutes=30)):
            title = "🚨 Event Reminder | Tomorrow"

        # Does event start within the next week +  30 mins?
        elif one_week_from_now < scheduled_start_time_utc < (one_week_from_now + timedelta(minutes=30)):
            title = "🚨 Event Reminder | One Week Today"

        # Does event start within the next month + 30 mins?
        elif one_month_from_now < scheduled_start_time_utc < (one_month_from_now + timedelta(minutes=30)):
            title = "🚨 Event"

        # Event doesn't match any of those criteria
        else:
            title = None

        # Only Tweet if we have a title
        if title:
            # Format tweet
            post = f'{title}\n\n {event_name} \n\n {pretty_date} \n\n {pretty_start_time} \n\n {pretty_join}'

            # (X)Tweet it out
            client = tweepy.Client(
                consumer_key=settings.X_PODCAST_CONSUMER_KEY,
                consumer_secret=settings.X_PODCAST_CONSUMER_SECRET,
                access_token=settings.X_PODCAST_ACCESS_TOKEN,
                access_token_secret=settings.X_PODCAST_ACCESS_TOKEN_SECRET,
            )

            # Post tweet
            try:
                client.create_tweet(text=post)
                print("Tweet successfully posted:", post)
            except Exception as e:
                print("Error sending tweet:", e)
