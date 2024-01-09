import hashlib
from urllib.parse import parse_qsl
from urllib.parse import urlparse
from django.conf import settings


def decode_relay_state(relay_state):
    """According to the spec, RelayState need not be a URL, yet,
    ``onelogin.saml2` exposes it as ``return_to -- The target URL the user
    should be redirected to after login``. Also, for an IdP initiated login
    sometimes a URL is used.
    """
    ret = {}
    if relay_state:
        parts = urlparse(relay_state)
        if parts.scheme or parts.netloc or (parts.path and parts.path.startswith("/")):
            ret["next"] = relay_state
        else:
            ret = dict(parse_qsl(relay_state))
    return ret


def string_to_int_hash(s):
    # Create an md5 hash object
    hasher = hashlib.md5()
    # Update the hasher with the byte representation of the string
    hasher.update(s.encode())
    # Get the hexadecimal digest and convert it to an integer
    return int(hasher.hexdigest(), 16)


def add_default_saml_application(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    site = Site.objects.get(domain=settings.APP_HOST)

    if not settings.SOCIAL_LOGIN_SAML_ENABLED:
        return

    SocialApp = apps.get_model("socialaccount", "SocialApp")
    (social_app, created) = SocialApp.objects.get_or_create(
        provider="saml",
        name="SAML Integration",
        provider_id=settings.SOCIAL_LOGIN_SAML_IDP_PROVIDER_ID,
        client_id=settings.SOCIAL_LOGIN_SAML_SP_ID,
        settings={
            "attribute_mapping": {
                "uid": "uid",
                "email": "email",
                "email_verified": "email_verified",
                "first_name": "first_name",
                "last_name": "last_name",
            },
            "idp": {
                "entity_id": settings.SOCIAL_LOGIN_SAML_IDP_PROVIDER_ID,
                "sso_url": settings.SOCIAL_LOGIN_SAML_IDP_SSO_URL,
                "x509cert": settings.SOCIAL_LOGIN_SAML_IDP_X509CERT,
            },
        },
    )
    social_app.sites.add(site)