from django.conf import settings

import importlib



def test_urlpatters_saml():
    settings.SOCIAL_LOGIN_SAML_ENABLED = False
    import dj_rest_auth_saml.urls
    assert isinstance(dj_rest_auth_saml.urls.urlpatterns, list)
    assert len(dj_rest_auth_saml.urls.urlpatterns) == 0
    settings.SOCIAL_LOGIN_SAML_ENABLED = True
    importlib.reload(dj_rest_auth_saml.urls)
    assert isinstance(dj_rest_auth_saml.urls.urlpatterns, list)
    assert len(dj_rest_auth_saml.urls.urlpatterns) == 1
