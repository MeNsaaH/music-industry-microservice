import sys
import grpc
import logging
from aiohttp import web
from aiohttp.hdrs import METH_POST
from aiohttp.web_exceptions import HTTPFound
from aiohttp.web_response import Response
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from pydantic import BaseModel, ValidationError, constr

from . import app_pb2, app_pb2_grpc


@template('index.jinja')
async def index(request):
    """
    This is the view handler for the "/" url.

    :param request: the request object see http://aiohttp.readthedocs.io/en/stable/web_reference.html#request
    :return: context for the template.
    """
    # Note: we return a dict not a response because of the @template decorator
    return {
        'title': request.app['settings'].name,
        'intro': "Success! you've setup a basic aiohttp app.",
    }


async def process_add_songs_form(request):
    data = dict(await request.post())
    data["track_number"] = int(data["track_number"])
    try:
        m = app_pb2.AddSongRequest(**data)
    except ValidationError as exc:
        return exc.errors()

#     # simple demonstration of sessions by saving the username and pre-populating it in the form next time
#     session = await get_session(request)
#     session['username'] = m.username
    request.app["music_stub"].AddSong(m)
    raise HTTPFound(request.app.router['music'].url_for())


@template('songs.jinja')
async def music(request):
    songs = request.app['music_stub'].GetSongs(app_pb2.Empty())
    return {'songs': songs }


@template('add_songs.jinja')
async def add_music(request):
    artists = request.app['music_stub'].GetArtists(app_pb2.Empty())
    albums = request.app['music_stub'].GetAlbums(app_pb2.Empty())
    if request.method == METH_POST:
        # the 302 redirect is processed as an exception, so if this coroutine returns there's a form error
        form_errors = await process_add_songs_form(request)
    else:
        form_errors = None

    # simple demonstration of sessions by pre-populating username if it's already been set
    session = await get_session(request)
    username = session.get('username', '')

    return {'form_errors': form_errors, 'username': username, "artists": artists, "albums": albums}
