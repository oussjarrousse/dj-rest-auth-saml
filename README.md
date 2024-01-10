# dj-rest-auth-saml

## Overview

`dj-rest-auth-saml` is a Django App that is actually a plugin for the `dj-rest-auth` that gives it the possibility to interact with `django-allauth` with SAML 2.0 support.

## Requirements:

Make sure that `django-allauth` is installed with the SAML 2.0 extension:

```bash
pip install django-allauth[SAML]
```

## Installation

To install `dj-rest-auth-saml` run:

```bash
pip install dj-rest-auth-saml
```

In the settings.py you should have the following:

```python
INSTALLED_APPS = [
    # ...
    "django.contrib.sites",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",  # this is django-allauth
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.saml",  # saml support from django-allauth
    "dj_rest_auth", # this is dj-rest-auth
    "dj_rest_auth_saml"  # this package
]

SITE_ID = 1

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware", # this is important for allauth
]

SOCIAL_LOGIN_SAML_ENABLED = True

SOCIALACCOUNT_PROVIDERS = {
    "saml": {"Apps": [

    ]}
}
```

## Configurations:

follow the detailed in the following link to add your SAML provider(s) in the SOCIALACCOUNT_PROVIDERS["saml"]["Apps"] list:

https://docs.allauth.org/en/latest/socialaccount/providers/saml.html

alternatively you can add a migration that adds your SAML provider to the database using the utility function `dj_rest_auth_saml.utils.add_default_saml_application` that requires the following configurations to be set in the `settings.py` file:

```python
SOCIAL_LOGIN_SAML_IDP_PROVIDER_ID = "IDP_PROVIDER_ID"  # For Google as a provider "https://accounts.google.com/o/saml2?idpid=XXXXXXXXX"
SOCIAL_LOGIN_SAML_SP_ID = "example"  # The SP ID used at the IDP
SOCIAL_LOGIN_SAML_IDP_SSO_URL = "https://idp_sso_url"  # The url for the IDP SSO, for google: "https://accounts.google.com/o/saml2/idp?idpid=XXXXXXXXX"
SOCIAL_LOGIN_SAML_IDP_X509CERT = "-----BEGIN CERTIFICATE-----.....-----END CERTIFICATE-----"  # the X509 IDP CERT
SOCIAL_LOGIN_SAML_ATTRIBUTE_MAPPING={
  "uid": "uid",
  "email": "email",
  "email_verified": "email_verified",
  "first_name": "first_name",
  "last_name": "last_name"
}
SOCIAL_LOGIN_SAML_ALLOW_SINGLE_LABEL_DOMAINS = False  # important for Unit testing

APP_HOST = "example.com" the hostname of this backend

```

## Contributing
Contributions to this project are welcomed! The Contributing Guide is still under construction.

When creating a pull request make sure to use the following template:

```
Change Summary
 - item one
 - item two
Related issue number
 - issue a
 - issue b
Checklist
  [ ] code is ready
  [ ] add tests
  [ ] all tests passing
  [ ] test coverage did not drop
  [ ] PR is ready for review
```

## License
dj-rest-auth-saml is licensed under the MIT License - see the LICENSE file for details.
