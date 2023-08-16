# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))
    jwt_path = os.path.normpath(os.path.join(basedir, os.pardir)) + "/.config.json"
    private_key_path = os.path.normpath(os.path.join(basedir, os.pardir)) + "/.private.key"

    # Set up the App SECRET_KEY
    # SECRET_KEY = config('SECRET_KEY'  , default='S#perS3crEt_007')
    SECRET_KEY = os.getenv("SECRET_KEY", "S#perS3crEt_007")
    FERNET_KEY = os.getenv("FERNET_KEY", "SFtrRFVSUgbyv6iSPgT4JWt9AfmNMKU8TtYcKxpSvI8=")

    # UI Elements Demo
    REDIRECT_URI = os.getenv("REDIRECT_URI", "")
    DEMO_FOLDER_NAME = os.getenv("DEMO_FOLDER_NAME", "Bookings")
    SIGN_TEMPLATE_ID = os.getenv("SIGN_TEMPLATE_ID", "1003591818911")

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Assets Management
    ASSETS_ROOT = os.getenv("ASSETS_ROOT", "/static/assets")

    # JWT Manual Configuration
    JWT_CLIENT_ID = os.getenv("JWT_CLIENT_ID", "")
    JWT_CLIENT_SECRET = os.getenv("JWT_CLIENT_SECRET", "")
    JWT_PUBLIC_KEY_ID = os.getenv("JWT_PUBLIC_KEY_ID", "")
    JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY", "")
    JWT_PASSPHRASE = os.getenv("JWT_PASSPHRASE", "")
    JWT_ENTERPRISE_ID = os.getenv("JWT_ENTERPRISE_ID", "")
    JWT_EXPIRATION_SECONDS = os.getenv("JWT_EXPIRATION_SECONDS", 3600)

    # Caching Configuration
    CACHE_DIR = os.path.join(basedir, "cache")
    CACHE_TYPE = "FileSystemCache"
    CACHE_DEFAULT_TIMEOUT = JWT_EXPIRATION_SECONDS

    # Webhook keys
    WH_KEY_A = os.getenv("WH_KEY_A", "your webhook primary key")
    WH_KEY_B = os.getenv("WH_KEY_B", "your webhook secondary key")

    # Sign Admin
    TASK_USER_ID = os.getenv("TASK_USER_ID")


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        os.getenv("DB_ENGINE", "mysql"),
        os.getenv("DB_USERNAME", "appseed_db_usr"),
        os.getenv("DB_PASS", "pass"),
        os.getenv("DB_HOST", "localhost"),
        os.getenv("DB_PORT", 3306),
        os.getenv("DB_NAME", "appseed_db"),
    )


class DebugConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "db.test.sqlite3")
    WTF_CSRF_ENABLED = False  # this will remove the csrf_token from the forms for testing purposes


# Load all possible configurations
config_dict = {"Production": ProductionConfig, "Debug": DebugConfig, "Testing": TestConfig}
