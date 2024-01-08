import hashlib
from urllib.parse import parse_qsl
from urllib.parse import urlparse


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
