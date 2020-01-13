import sys
import os
from pathlib import Path
import aiohttp_jinja2
import aiohttp_session
import grpc
import jinja2
from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage


from .settings import Settings
from . import views
from . import app_pb2, app_pb2_grpc

THIS_DIR = Path(__file__).parent
STATIC_DIR = os.path.join(THIS_DIR, 'static')


def get_grpc_stub(stub, port):
    channel = grpc.insecure_channel(f"localhost:{port}")
    return stub(channel)

async def startup(app: web.Application):
    settings: Settings = app["settings"]
    app["email_stub"] = get_grpc_stub(app_pb2_grpc.EmailServiceStub, settings.email_service_port)
    app["music_stub"] = get_grpc_stub(app_pb2_grpc.SongServiceStub, settings.music_service_port)


async def cleanup(app: web.Application):
    # Some grpc clean up tasks
    pass


async def create_app():
    app = web.Application()
    settings = Settings()
    app.update(
        settings=settings,
        static_root_url="/static/",
    )

    jinja2_loader = jinja2.FileSystemLoader(str(THIS_DIR / "templates"))
    aiohttp_jinja2.setup(app, loader=jinja2_loader)

    app.on_startup.append(startup)
    app.on_cleanup.append(cleanup)

    aiohttp_session.setup(app, EncryptedCookieStorage(settings.auth_key, cookie_name=settings.cookie_name))

    app.router.add_get("/", views.index, name="index")
    app.router.add_get("/music", views.music, name="music")
    app.router.add_route("*", "/music/add", views.add_music, name="add-music"),
    app.add_routes([web.static('/static', STATIC_DIR)])

    return app
