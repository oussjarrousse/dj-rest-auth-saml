import os

SECRET_KEY = "fake-key-for-testing"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    # TODO: Add these to documentation
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",  # this is django-allauth
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.saml",  # saml support from django-allauth
    "dj_rest_auth",  # this is dj-rest-auth
    "dj_rest_auth_saml",  # this package
]

# https://docs.djangoproject.com/en/4.2/ref/contrib/sites/
SITE_ID = 1

ROOT_URLCONF = "dj_rest_auth_saml.urls"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # TODO: Add these to documentation
    "allauth.account.middleware.AccountMiddleware",
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

SOCIAL_LOGIN_SAML_ENABLED = True
SOCIALACCOUNT_PROVIDERS = {"saml": {"Apps": []}}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

APP_HOST = "testserver"
APP_NAME = "example"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SOCIAL_LOGIN_SAML_IDP_PROVIDER_ID = "IDP_PROVIDER_ID"
SOCIAL_LOGIN_SAML_SP_ID = "example"
SOCIAL_LOGIN_SAML_IDP_SSO_URL = "https://idp.com/sso/example"
SOCIAL_LOGIN_SAML_ATTRIBUTE_MAPPING = {
    "uid": "uid",
    "email": "email",
    "email_verified": "email_verified",
    "first_name": "first_name",
    "last_name": "last_name",
}
# DUMMY CERTICICATE
SOCIAL_LOGIN_SAML_IDP_X509CERT = "-----BEGIN CERTIFICATE-----MIIDgzCCAmugAwIBAgIgbfzemuHXtDqHhLUilGPrfZTSC13MBVEiLsRQkV3RVtIwDQYJKoZIhvcNAQEFBQAwVjEJMAcGA1UEBhMAMQkwBwYDVQQKDAAxCTAHBgNVBAsMADEQMA4GA1UEAwwHaWRwLmNvbTEPMA0GCSqGSIb3DQEJARYAMRAwDgYDVQQDDAdpZHAuY29tMB4XDTI0MDEwOTEzMTgxNloXDTM0MDEwOTEzMTgxNlowRDEJMAcGA1UEBhMAMQkwBwYDVQQKDAAxCTAHBgNVBAsMADEQMA4GA1UEAwwHaWRwLmNvbTEPMA0GCSqGSIb3DQEJARYAMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr58t8F82CWKw6CUaj/Sr6+XvB93fAmNsThN3SwMZuclXpkqrHpvuklTeQQ486EtZOM0FqtX8J/2jJiX3vChblZj3emg5dZJFq+8KntQQi9eqU5h2qtusoxAGRfXOhY7uWZu9uGb0oo5qy5lMYVRHpsPQwmsCLyK+t0woexUUWEO28l5QCYMwKa9E4MfyqsGxt9JT2c+aAmHjzKVDobQLF9YK3QW1V0w9qaGR1ooDOYbFFI7DjQysxLkFOfbb8QPf7KxC6XA96CKcY//whF6jCq0JjLHLHK3TdWdjBU1m6vqQFAIBpZyF2OaCPQtGEAYLQ0hV8PPzcD81ZWnobqW+EQIDAQABo08wTTAdBgNVHQ4EFgQUmXLYfBoLue3qFaoyqIOhXb4mDpkwHwYDVR0jBBgwFoAUmXLYfBoLue3qFaoyqIOhXb4mDpkwCwYDVR0RBAQwAoIAMA0GCSqGSIb3DQEBBQUAA4IBAQBlWoYxEWQREZDfDxE8lqDFinTi7Nq6+z4ETtcrktCmxHMcB6DHWULEoGFRAo+8+yOOanzUBhXZT0CUND8x9QiofeT8JKjr4Id9p8SFR6c4rcuXFl9+P3GZlxkOBiP/KIufaGInnTSNH0xfN9Tp/bzESLZArplbYptsj7L8XogQ1KMma4ixXu+2FGDEKiZjjwnT9SdKdEQypwAoINNcma/DupEpyy+X359RkCUZSQsvDlcgqWEVxBWzCU+kIrj+MpjNzGUlxgSMN32mQ/htyJw//+ymmJcCrijYTa+b8N55vpFxuVRezq0rGqqJxMHiD1ju9sCMrywrzfKdgqbg73IE-----END CERTIFICATE-----"
