#!/usr/bin/env python
import random
import argparse

"""
Generates a site configuration file with some randomized passwords for Django settings and
development default values for some site-specific settings. Do not save generated file to version control.
When deploying to server replace development settings with actual settings on the server.
"""


def generate_site_config(site_config_file_path):
    with open(site_config_file_path, "w", encoding="utf-8") as site_config_file:
        site_config_file.write("ALLOWED_HOSTS = ['127.0.0.1']\n")
        site_config_file.write(
            "CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']\n"
        )
        site_config_file.write(
            "CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']\n"
        )
        site_config_file.write(
            "DEBUG = True  # Can be True on development server but must be False when deploying\n"
        )
        site_config_file.write("SECURE_SSL_REDIRECT = False\n")
        site_config_file.write("CSRF_COOKIE_SECURE = False\n")
        site_config_file.write("SESSION_COOKIE_SECURE = False\n")
        chars = "abcdefghijklmnopqrstuvxyz01234567890_-!*"
        secret_key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        site_config_file.write("SECRET_KEY = '%s'\n" % secret_key)
        site_config_file.write("OPENAI_API_KEY = 'your_openai_api_key'\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "site_config_file_path", help="Where site_config file will be placed"
    )
    args = parser.parse_args()
    generate_site_config(args.site_config_file_path)
