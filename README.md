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

```pytest
INSTALLED_APPS = [
    # ...
    "django.contrib.sites",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "mfa",  # this is django-mfa2
    "allauth",  # this is django-allauth
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.saml",  # saml support from django-allauth
    "dj_rest_auth", # this is dj-rest-auth
    "dj_rest_auth_saml"  # this package
]

## Configurations:

SOCIALACCOUNT_PROVIDERS = {
    "saml": {"Apps": [

    ]}
}

and follow the detailed in the following link to add your SAML provider(s) in the SOCIALACCOUNT_PROVIDERS["saml"]["Apps"] list:

https://docs.allauth.org/en/latest/socialaccount/providers/saml.html

alternatively you can add a migration that adds your SAML provider to the database:



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