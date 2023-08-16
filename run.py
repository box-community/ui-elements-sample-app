# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import sys
from flask_migrate import Migrate
from flask_minify import Minify

from apps.config import config_dict
from apps import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

# The configuration
CONFIG_MODE = "Debug" if DEBUG else "Production"

try:

    # Load the configuration using the default values
    app_config = config_dict[CONFIG_MODE.capitalize()]

except KeyError:
    sys.exit("Error: Invalid <config_mode>. Expected values [Debug, Production] ")

app = create_app(app_config)

Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

if DEBUG:
    app.logger.info("DEBUG            = " + str(DEBUG))
    app.logger.info("FLASK_ENV        = " + os.getenv("FLASK_ENV"))
    app.logger.info("Page Compression = " + "FALSE" if DEBUG else "TRUE")
    app.logger.info("DBMS             = " + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info("ASSETS_ROOT      = " + app_config.ASSETS_ROOT)
    app.logger.info("JWT_CLIENT_ID    = " + app_config.JWT_CLIENT_ID)
    app.logger.info("CACHE_DIR        = " + app_config.CACHE_DIR)
    app.logger.info("CACHE_TYPE       = " + app_config.CACHE_TYPE)
    app.logger.info("CACHE_DEFAULT_TIMEOUT = " + str(app_config.CACHE_DEFAULT_TIMEOUT))

if __name__ == "__main__":
    app.run()
