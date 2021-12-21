import os

ENVIRONMENT = os.environ.get('ENVIRONMENT', '')

if ENVIRONMENT:
    print("Loading {} Settings".format(ENVIRONMENT.upper()))

else:
    print("Unknown ENV Loading DEVELOPMENT Settings")

if ENVIRONMENT == 'production':
    from shelix.settings.production import *

elif ENVIRONMENT == 'testing':
    from shelix.settings.testing import *

else:
    from shelix.settings.development import *
