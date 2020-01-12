from urllib.parse import urlparse

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    See https://pydantic-docs.helpmanual.io/#settings for details on using and overriding this
    """
    name = 'frontender'
    auth_key = '23Q5XoB4lJVn9DZnuzEbK6u_yLibnf1Q3CpisVEKCUA='
    cookie_name = 'frontender'

    # Service Config
    email_service_port = "8081"
    music_service_port = "8082"

