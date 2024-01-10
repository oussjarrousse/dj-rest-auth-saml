import pytest

from rest_framework.test import APIRequestFactory
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from dj_rest_auth_saml.utils import add_default_saml_application
from dj_rest_auth_saml.serializers import SAMLSocialLoginSerializer
from dj_rest_auth_saml.views import CustomFinishACSView
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from importlib import import_module


class Tests_SAMLSocialLoginSerializer:
    pass
    # @pytest.mark.django_db
    # def test_validate(self, unauthenticated_api_client):
    #     client = unauthenticated_api_client
    #     settings.APP_HOST = "example.com"
    #     add_default_saml_application(apps, None)

    #     factory = APIRequestFactory()
    #     request = factory.get("/api/v1/core/info/")
    #     request.user = AnonymousUser()

    #     setattr(request, "session", client.session)

    #     engine = import_module(settings.SESSION_ENGINE)
    #     SessionStore = engine.SessionStore

    #     # session_key = request.COOKIES.get("saml-acs-session")
    #     store = SessionStore("saml_acs_session")
    #     store["login"] = {
    #         "account": {},
    #         "user": {
    #             "username": "saml_user",
    #             "email": "user@example.com"
    #         },
    #         "state": {
    #             # "process": "xxx"
    #         },
    #         "email_addresses": [
    #             # "1":"saml_user@username.com"
    #         ]
    #     }

    #     setattr(request, "saml_acs_session", store)

    #     view = CustomFinishACSView()
    #     view.organization_slug = "example"
    #     serializer = SAMLSocialLoginSerializer(context={"request": request, "view": view})
    #     assert isinstance(serializer, SAMLSocialLoginSerializer)
    #     assert isinstance(serializer, SocialLoginSerializer)

    #     attrs = {
    #     }
    #     r = serializer.validate(attrs)
    #     assert isinstance(dict, attrs)
