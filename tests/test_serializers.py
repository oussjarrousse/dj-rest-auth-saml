from importlib import import_module

import pytest
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from dj_rest_auth_saml.serializers import SAMLSocialLoginSerializer
from dj_rest_auth_saml.utils import add_default_saml_application
from dj_rest_auth_saml.utils import change_site_domain
from dj_rest_auth_saml.views import CustomFinishACSView


class Tests_SAMLSocialLoginSerializer:
    def test_post_signup(self):
        # client = unauthenticated_api_client
        # settings.APP_HOST = "example.com"
        # add_default_saml_application(apps, None)
        serializer = SAMLSocialLoginSerializer()
        serializer.post_signup(None, None)

    @pytest.mark.django_db
    def test_validate(self, unauthenticated_api_client):
        client = unauthenticated_api_client
        settings.APP_HOST = "example.com"
        add_default_saml_application(apps, None)

        serializer = SAMLSocialLoginSerializer()
        assert serializer
        assert isinstance(serializer, SAMLSocialLoginSerializer)
        assert isinstance(serializer, SocialLoginSerializer)

        with pytest.raises(AttributeError):
            serializer.validate(None)

        factory = APIRequestFactory()
        request = factory.post("/")

        context = {"request": request, "view": None}
        serializer = SAMLSocialLoginSerializer(context=context)
        with pytest.raises(ValidationError):
            serializer.validate(None)

        view = CustomFinishACSView()

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

    #     view.organization_slug = "example"
    #     serializer = SAMLSocialLoginSerializer(context={"request": request, "view": view})

    #     attrs = {
    #     }
    #     r = serializer.validate(attrs)
    #     assert isinstance(dict, attrs)
