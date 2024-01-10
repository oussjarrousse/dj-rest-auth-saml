import pytest
from allauth.socialaccount.providers.saml.provider import SAMLProvider
from dj_rest_auth_saml.views import SAMLException
from dj_rest_auth_saml.views import SAMLAuthenticationException
from dj_rest_auth_saml.views import SAMLAuthenticationFailed
from dj_rest_auth_saml.views import SAML2Adapter
from dj_rest_auth_saml.views import CustomACSView
from dj_rest_auth_saml.views import CustomFinishACSView
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth_saml.utils import add_default_saml_application
from django.apps import apps

class Tests_SAML2Adapter():

    @pytest.mark.django_db
    @pytest.mark.FOCUS
    @pytest.mark.UNIT
    def test_init(self):
        add_default_saml_application(apps, None)
        request = {"secret": "some_secret"}
        adapter = SAML2Adapter(request, organization_slug="example")
        assert adapter.request == request
        assert adapter.organization_slug == "example"
        assert isinstance(adapter.provider, SAMLProvider)
        



class Tests_CustomACSView():

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

    def test_post(self):
        pass    