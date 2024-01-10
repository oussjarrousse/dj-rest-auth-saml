import json

import pytest
from allauth.socialaccount.providers.saml.provider import SAMLProvider
from dj_rest_auth.registration.views import SocialLoginView
from django.apps import apps
from django.conf import settings
from django.urls import reverse

from dj_rest_auth_saml.utils import add_default_saml_application
from dj_rest_auth_saml.utils import change_site_domain
from dj_rest_auth_saml.views import CustomACSView
from dj_rest_auth_saml.views import CustomFinishACSView
from dj_rest_auth_saml.views import SAML2Adapter
from dj_rest_auth_saml.views import SAMLAuthenticationException
from dj_rest_auth_saml.views import SAMLAuthenticationFailed
from dj_rest_auth_saml.views import SAMLException


class Tests_SAML2Adapter:
    @pytest.mark.django_db
    @pytest.mark.FOCUS
    @pytest.mark.UNIT
    def test_init(self):
        change_site_domain(apps, None)
        add_default_saml_application(apps, None)
        request = {"secret": "some_secret"}
        adapter = SAML2Adapter(request, organization_slug="example")
        assert adapter.request == request
        assert adapter.organization_slug == "example"
        assert isinstance(adapter.provider, SAMLProvider)

    @pytest.mark.django_db
    @pytest.mark.FOCUS
    @pytest.mark.UNIT
    def test_authenticate(self):
        pass


class Tests_CustomACSView:
    @pytest.mark.UNIT
    @pytest.mark.FOCUS
    def test_init(self):
        view = CustomACSView()
        assert view.adapter_class == SAML2Adapter
        assert isinstance(view, SocialLoginView)

    def test_dispatch(self):
        pass

    def test_get(self):
        pass

    def test_list(self):
        pass

    @pytest.mark.django_db
    @pytest.mark.FOCUS
    @pytest.mark.API
    def test_post(self, unauthenticated_api_client):
        settings.SOCIAL_LOGIN_SAML_ALLOW_SINGLE_LABEL_DOMAINS = True

        change_site_domain(apps, None)
        add_default_saml_application(apps, None)
        client = unauthenticated_api_client
        url = reverse("saml_acs", kwargs={"organization_slug": "example"})
        POST = {"title": "new idea"}
        headers = {"HTTP_HOST": "testserver"}
        r = client.post(
            url, json.dumps(POST), content_type="application/json", **headers
        )
        assert r.status_code == 200
