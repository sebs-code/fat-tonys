import asyncio
import aiohttp
import json

from django.conf import settings


async def list_guild_events():
    """
    Returns a list of upcoming events for the supplied guild ID
    Format of return is a list of one dictionary per event containing
    information.
    """

    discord_token = settings.DISCORD_TOKEN
    guild_id = settings.GUILD_ID
    base_api_url = 'https://discord.com/api/v8'
    auth_headers = {
        'Authorization': f'Bot {discord_token}',
        'User-Agent': 'DiscordBot (https://fattonys.net) Python/3.9 aiohttp/3.8.1',
        'Content-Type': 'application/json'
    }

    event_retrieve_url = f'{base_api_url}/guilds/{guild_id}/scheduled-events'
    async with aiohttp.ClientSession(headers=auth_headers) as session:
        try:
            async with session.get(event_retrieve_url) as response:
                response.raise_for_status()
                assert response.status == 200
                response_list = json.loads(await response.read())
        except Exception as e:
            print(f'EXCEPTION: {e}')
        finally:
            await session.close()
    return response_list


def suffix(day):
    """
    Get's the correct suffix for the day of the month
    """

    day = int(day)
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = f'{day}th'
    else:
        suffix = [f'{day}st', f'{day}nd', f'{day}rd'][day % 10 - 1]

    return suffix
