import pytest
from dj_rest_auth_saml.views import SAMLException
from dj_rest_auth_saml.views import SAMLAuthenticationException
from dj_rest_auth_saml.views import SAMLAuthenticationFailed
from dj_rest_auth_saml.views import SAML2Adapter
from dj_rest_auth_saml.views import CustomACSView
from dj_rest_auth_saml.views import CustomFinishACSView
from dj_rest_auth.registration.views import SocialLoginView

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