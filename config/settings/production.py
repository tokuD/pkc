import environ

from .base import *

env = environ.Env()
env.read_env(str(BASE_DIR.joinpath('.env')))

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')