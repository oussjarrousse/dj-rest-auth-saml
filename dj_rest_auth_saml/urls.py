from allauth.socialaccount.providers.saml.views import ACSView
from allauth.socialaccount.providers.saml.views import FinishACSView
from allauth.socialaccount.providers.saml.views import LoginView
from allauth.socialaccount.providers.saml.views import MetadataView
from allauth.socialaccount.providers.saml.views import SLSView
from django.conf import settings
from django.urls import include
from django.urls import path

from .views import CustomACSView
from .views import CustomFinishACSView

if settings.SOCIAL_LOGIN_SAML_ENABLED:
    urlpatterns = [
        path(
            # "auth/social-login/saml/<organization_slug>/",
            "<organization_slug>/",
            include(
                [
                    # login/ will initiate the login flow. It will send a get request to the IdP provider
                    # It will return a Redirect to the IdP login page for authentication.
                    # Once authentication is complete a post request is sent to the /acs
                    path(
                        "login/", LoginView.as_view(), name="saml_login"
                    ),  # also accepts "/login/?process=connect"
                    # acs/ accepts a POST requests containing POST.SAMLResponse that contains among other things
                    # The values for mapped attributes. the function will "store the session" and redirect to acs/finish/
                    path(
                        "acs/",
                        # ACSView.as_view(),
                        CustomACSView.as_view(),
                        name="saml_acs",
                    ),
                    # acs/finish/ receives a GET request
                    path(
                        "acs/finish/",
                        CustomFinishACSView.as_view(),
                        name="saml_finish_acs",
                    ),
                    path(
                        "sls/",
                        SLSView.as_view(),
                        name="saml_sls",
                    ),
                    path("metadata/", MetadataView.as_view(), name="saml_metadata"),
                    # I must provide something like "socialaccount_connections" for the case "/login/?process=connect" is passed
                ]
            ),
        )
    ]
