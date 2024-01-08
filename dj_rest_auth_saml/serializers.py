import logging

from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.sessions import LoginSession
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


class SAMLSocialLoginSerializer(SocialLoginSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        view = self.context.get("view")
        request = self._get_request()

        if not view:
            raise ValidationError(
                "View is not defined, pass it as a context variable",
            )
        adapter_class = getattr(view, "adapter_class", None)
        if not adapter_class:
            raise ValidationError("Define adapter_class in view")

        organization_slug = getattr(view, "organization_slug", None)
        if not organization_slug:
            raise ValidationError("Define organization_slug in view")

        adapter = adapter_class(request)
        provider = adapter.get_provider(
            organization_slug
        )  # with or without organization_slug ?
        app = provider.app

        # load session
        acs_session = LoginSession(request, "saml_acs_session", "saml-acs-session")
        serialized_login = acs_session.store.get("login")

        if not serialized_login:
            logger.error("Unable to finish login, SAML ACS session missing")
            raise ValidationError("SAML ACS session missing")

        acs_session.delete()

        try:
            login = SocialLogin.deserialize(serialized_login)
            ret = complete_social_login(request, login)
        except Exception as e:
            raise ValidationError(str(e))

        if not login.is_existing:
            login.lookup()
            login.save(request, connect=True)
        attrs["user"] = login.account.user

        return attrs

    def post_signup(self, login, attrs):
        """
        Inject behavior when the user signs up with a social account.

        :param login: The social login instance being registered.
        :type login: allauth.socialaccount.models.SocialLogin
        :param attrs: The attributes of the serializer.
        :type attrs: dict
        """
        pass
