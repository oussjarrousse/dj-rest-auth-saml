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


def change_site_domain(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    domain = settings.APP_HOST
    name = settings.APP_NAME

    site, created = Site.objects.get_or_create(
        domain="example.com", defaults={"name": name, "domain": domain}
    )

    # if not created:
    site.domain = domain
    site.name = name
    site.save()


def add_default_saml_application(apps, schema_editor):
    if not settings.SOCIAL_LOGIN_SAML_ENABLED:
        return
    Site = apps.get_model("sites", "Site")
    site = Site.objects.get(domain=settings.APP_HOST)

    SocialApp = apps.get_model("socialaccount", "SocialApp")
    (social_app, created) = SocialApp.objects.get_or_create(
        provider="saml",
        name="SAML Integration",
        provider_id=settings.SOCIAL_LOGIN_SAML_IDP_PROVIDER_ID,
        client_id=settings.SOCIAL_LOGIN_SAML_SP_ID,
        settings={
            "attribute_mapping": settings.SOCIAL_LOGIN_SAML_ATTRIBUTE_MAPPING,
            "advanced": {
                "allow_single_label_domains": settings.SOCIAL_LOGIN_SAML_ALLOW_SINGLE_LABEL_DOMAINS,
                "authn_request_signed": settings.SOCIAL_LOGIN_SAML_AUTHN_REQUEST_SIGNED,
                "digest_algorithm": settings.SOCIAL_LOGIN_SAML_DIGEST_ALGORITHM,
                "logout_request_signed": settings.SOCIAL_LOGIN_SAML_LOGOUT_REQUEST_SINGED,
                "logout_response_signed": settings.OCIAL_LOGIN_SAML_LOGOUT_RESPONSE_SIGNED,
                "signature_algorithm": settings.SOCIAL_LOGIN_SAML_SIGNATURE_ALGORITHM,
                "metadata_signed": settings.SOCIAL_LOGIN_SAML_METADATA_SIGNED,  #
                "want_assertion_encrypted": settings.SOCIAL_LOGIN_SAML_WANT_ASSERTION_ENCRYPTED,
                "want_assertion_signed": settings.SOCIAL_LOGIN_SAML_WANT_ASSERTION_SIGNED,
                "want_message_signed": settings.SOCIAL_LOGIN_SAML_WANT_MESSAGE_SIGNED,
                "name_id_encrypted": settings.SOCIAL_LOGIN_SAML_NAME_ID_ENCRYPTED,
                "want_name_id_encrypted": settings.SOCIAL_LOGIN_SAML_WANT_NAME_ID_ENCRYPTED,
                "reject_deprecated_algorithm": settings.SOCIAL_LOGIN_SAML_REJECT_DEPRECATED_ALGORITHM,
                "want_name_id": settings.SOCIAL_LOGIN_SAML_WANT_NAME_ID,
                "want_attribute_statement": settings.SOCIAL_LOGIN_SAML_WANT_ATTRIBUTE_STATEMENT,
                "allow_repeat_attribute_name": settings.SOCIAL_LOGIN_SAML_ALLOW_REPEAT_ATTRIBUTE_NAME,
            },
            "idp": {
                "entity_id": settings.SOCIAL_LOGIN_SAML_IDP_PROVIDER_ID,
                "sso_url": settings.SOCIAL_LOGIN_SAML_IDP_SSO_URL,
                "x509cert": settings.SOCIAL_LOGIN_SAML_IDP_X509CERT,
            },
        },
    )
    social_app.sites.add(site)


def remove_default_saml_application(apps, schema_editor):
    SocialApp = apps.get_model("socialaccount", "SocialApp")
    SocialApp.objects.filter(name="SAML Integration").delete()
