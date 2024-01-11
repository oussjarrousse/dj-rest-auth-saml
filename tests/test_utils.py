import pytest
from django.apps import apps
from django.conf import settings

from dj_rest_auth_saml.utils import add_default_saml_application
from dj_rest_auth_saml.utils import change_site_domain
from dj_rest_auth_saml.utils import decode_relay_state
from dj_rest_auth_saml.utils import remove_default_saml_application
from dj_rest_auth_saml.utils import string_to_int_hash


@pytest.mark.UTILS
def test_decode_relay_state():
    ret = decode_relay_state(None)
    assert isinstance(ret, dict)
    assert not ret

    ret = decode_relay_state("")
    assert isinstance(ret, dict)
    assert not ret

    url = "http://testserver?param1=value1&param2=value2"
    expected = {"next": url}
    ret = decode_relay_state(url)
    assert isinstance(ret, dict)
    assert ret == expected

    relative_path = "/relative/path?param1=value1&param2=value2"
    ret = decode_relay_state(relative_path)
    expected = {"next": relative_path}
    assert isinstance(ret, dict)
    assert ret == expected

    params = "param1=value1&param2=value2"
    expected = {"param1": "value1", "param2": "value2"}
    ret = decode_relay_state(params)
    assert isinstance(ret, dict)
    assert ret == expected


@pytest.mark.UTILS
def test_string_to_int_hash():
    s = ""
    result = string_to_int_hash(s)
    assert isinstance(result, int)
    assert result == 281949768489412648962353822266799178366


@pytest.mark.django_db
@pytest.mark.UTILS
def test_add_default_saml_application_and_remove():
    settings.SOCIAL_LOGIN_SAML_ENABLED = False
    # change_site_domain(apps, None)
    assert add_default_saml_application(None, None) is None
    settings.SOCIAL_LOGIN_SAML_ENABLED = True
    # assert change_site_domain(apps)
    settings.APP_HOST = "testserver"

    change_site_domain(apps, None)
    assert add_default_saml_application(apps, None) is None
    SocialApp = apps.get_model("socialaccount", "SocialApp")
    social_app = SocialApp.objects.get(provider="saml")
    assert social_app.client_id == settings.SOCIAL_LOGIN_SAML_SP_ID
    assert social_app.provider_id == settings.SOCIAL_LOGIN_SAML_IDP_PROVIDER_ID
    assert (
        social_app.settings["attribute_mapping"]
        == settings.SOCIAL_LOGIN_SAML_ATTRIBUTE_MAPPING
    )
    assert (
        social_app.settings["idp"]["entity_id"]
        == settings.SOCIAL_LOGIN_SAML_IDP_PROVIDER_ID
    )
    assert (
        social_app.settings["idp"]["sso_url"] == settings.SOCIAL_LOGIN_SAML_IDP_SSO_URL
    )
    assert (
        social_app.settings["idp"]["x509cert"]
        == settings.SOCIAL_LOGIN_SAML_IDP_X509CERT
    )

    remove_default_saml_application(apps, None)
    assert SocialApp.objects.all().count() == 0
