from decouple import config

env = config("DJANGO_ENV", default="dev").lower()

if env == 'dev':
    from .dev import *
elif env == 'prod':
    from .prod import *
else:
    from .dev import *