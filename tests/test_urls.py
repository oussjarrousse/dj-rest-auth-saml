from django.conf import settings

def test_urlpatters_saml_disabled():
    settings.SOCIAL_LOGIN_SAML_ENABLED = False
    from dj_rest_auth_saml.urls import urlpatterns
    assert isinstance(urlpatterns, list)
    assert len(urlpatterns) == 0

def test_urlpatters_saml_enabled():
    settings.SOCIAL_LOGIN_SAML_ENABLED = True
    from dj_rest_auth_saml.urls import urlpatterns
    assert isinstance(urlpatterns, list)
    assert len(urlpatterns) == 0
