from django.utils.translation import gettext_lazy as _
from oidc_provider.lib.claims import ScopeClaims


def userinfo(claims, user):
    """
    Adjust standard claims.

    Note: DO NOT add extra keys or delete existing ones in the claims dict.
    To do that, define OIDC_EXTRA_SCOPE_CLAIMS:
    (docs: https://django-oidc-provider.readthedocs.io/en/master/sections/settings.html#oidc-extra-scope-claims).
    """
    claims['preferred_username'] = user.username
    # Don't pass an email address, spiff says the account already exists
    # for any address.
    # claims['email'] = None

    return claims

def sub_generator(user):
    # django-oidc-provider returns user.id as 'sub' by default...
    return str(user.username)

class CustomScopeClaims(ScopeClaims):
    "Define non-standard Scopes & Claims."
    
    # If you want to change the description of the profile scope, you can redefine it.
    info_profile = (
        _(u'Profile'),
        _(u'Profile scope.'),
    )

    def scope_profile(self):
        return self.userinfo
