import binascii
import logging

from allauth.socialaccount.providers.base import AuthError

try:
    from allauth.socialaccount.providers.saml.utils import decode_relay_state
except ImportError:
    from .utils import decode_relay_state

from .utils import string_to_int_hash

from .serializers import SAMLSocialLoginSerializer

from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.saml.utils import get_app_or_404
from allauth.socialaccount.providers.saml.views import SAMLViewMixin, FinishACSView
from allauth.socialaccount.sessions import LoginSession
from dj_rest_auth.models import get_token_model
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.utils import jwt_encode
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_300_MULTIPLE_CHOICES
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from rest_framework.views import APIView

logger = logging.getLogger(__name__)


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        # TODO:
        "SAMLResponse"
        # list all sensitive post parameters in the post requests
    )
)


class SAMLException(Exception):
    pass


class SAMLAuthenticationException(SAMLException):
    pass


class SAMLAuthenticationFailed(SAMLException):
    pass


class SAML2Adapter(SAMLViewMixin):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.organization_slug = kwargs.get("organization_slug")
        self.provider = self.get_provider(self.organization_slug)

    def authenticate(self):
        auth = self.build_auth(self.provider, self.organization_slug)
        try:
            auth.process_response()
        except binascii.Error:
            errors = ["invalid_response"]
        else:
            errors = auth.get_errors()
        if errors:
            # e.g. ['invalid_response']
            logger.error(
                "Error processing SAML response: %s: %s"
                % (", ".join(errors), auth.get_last_error_reason())
            )
            raise SAMLAuthenticationException(
                {
                    "is_error": True,
                    "provider_id": self.provider.id,
                    "saml_errors": errors,
                    "saml_last_error_reason": auth.get_last_error_reason(),
                }
            )

        if not auth.is_authenticated():
            raise SAMLAuthenticationFailed(
                {
                    "is_error": True,
                    "provider_id": self.provider.id,
                    "error": AuthError.CANCELLED,
                }
            )

        # manipulate uid to fake social uid
        if not auth.get_attribute("uid"):
            email = auth.get_attribute("email")
            if isinstance(email, list) and len(email) > 0:
                email = email[0]
            auth._attributes["uid"] = [str(string_to_int_hash(email))]

        if not auth.get_attribute("email_verified"):
            email = auth.get_attribute("email")
            if isinstance(email, list) and len(email) > 0:
                auth._attributes["email_verified"] = ["true"]

        if not auth.get_attribute("username"):
            firstname = auth.get_attribute("first_name")
            if isinstance(firstname, list) and len(firstname) > 0:
                firstname = firstname[0]
            if firstname:
                auth._attributes["username"] = [firstname.lower()]
        # else:
        #     username = auth.get_attribute("username")
        #     if isinstance(username, list) and len(username) > 0:
        #         username = username[0]
        #     if username:
        #         auth._attributes["username"] = [username.lower()]
        return auth


class CustomACSView(SocialLoginView):
    """
    the parent SocialLoginView defines:
        serializer_class = SocialLoginSerializer
        def process_login(self):
            get_adapter(self.request).login(self.request, self.user)

    """

    adapter_class = SAML2Adapter

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.organization_slug = kwargs.get("organization_slug")
        self.request = request

        adapter = self.adapter_class(request, *args, **kwargs)
        auth = adapter.authenticate()

        relay_state = decode_relay_state(request.POST.get("RelayState"))
        provider = adapter.get_provider(self.organization_slug)
        login = provider.sociallogin_from_response(request, auth)

        for key in ["process", "next"]:
            value = relay_state.get(key)
            if value:
                login.state[key] = value

        acs_session = LoginSession(request, "saml_acs_session", "saml-acs-session")
        acs_session.store["login"] = login.serialize()
        url = reverse(
            "saml_finish_acs",
            kwargs={"organization_slug": self.organization_slug},
        )
        response = HttpResponseRedirect(url)  # will redirect to the acs_finish
        acs_session.save(response)
        return response


class CustomFinishACSView(SocialLoginView):

    adapter_class = SAML2Adapter
    serializer_class = SAMLSocialLoginSerializer

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.organization_slug = kwargs.get("organization_slug")
        self.request = request

        self.serializer = self.get_serializer(
            data={}, context=self.get_serializer_context()
        )
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()
