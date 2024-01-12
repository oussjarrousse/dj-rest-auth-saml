from importlib import import_module

import pytest
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
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
    def test_validate(self, unauthenticated_api_client, mocker):
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

        view = object()
        context = {"request": request, "view": view}
        serializer = SAMLSocialLoginSerializer(context=context)
        with pytest.raises(ValidationError):
            serializer.validate(None)

        view = CustomFinishACSView()
        context = {"request": request, "view": view}
        serializer = SAMLSocialLoginSerializer(context=context)
        with pytest.raises(ValidationError):
            serializer.validate(None)

        view.organization_slug = "example"
        serializer = SAMLSocialLoginSerializer(context=context)
        with pytest.raises(ValidationError):
            serializer.validate(None)

        engine = import_module(settings.SESSION_ENGINE)

        user = User(
            is_superuser=False,
            username="user",
            email="user@idp.com",
            is_active=False,
            first_name="user",
        )
        # user.save()

        store = engine.SessionStore("saml-acs-session")
        store["login"] = {
            "account": {},
            "user": {"username": user.username, "email": user.email},
            "email_addresses": [{"email": "user@idp.com"}],
            "state": {
                "process": "",
            },
        }

        setattr(request, "user", user)
        setattr(request, "saml_acs_session", store)
        context = {"request": request, "view": view}
        serializer = SAMLSocialLoginSerializer(context=context)
        with pytest.raises(ValidationError):
            serializer.validate(None)

        setattr(request, "session", store)

        mocker.patch(
            "dj_rest_auth_saml.serializers.complete_social_login", return_value=True
        )
        attr = {}
        context = {"request": request, "view": view}
        serializer = SAMLSocialLoginSerializer(context=context)
        r = serializer.validate(attr)
        assert "user" in attr
        assert attr["user"].username == user.username
